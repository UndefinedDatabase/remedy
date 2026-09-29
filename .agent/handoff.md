# Handback — F042 round 1: claim F042, book F041 R9, register R-1107, record D1, land T001

## Session

SESSION 1 of feature F042 · round 1 · rounds so far 1. Context self-assessment: after writing this
handoff and before pushing, roughly one-third of the session's context budget remained.

## Range

Review of `4e643440f`..`<this C7 commit>`. C1a (`907615f2f`), C1b (`7861df5dd`), C1c (`df8085835`),
C2 (`502b44f53`), C3 (`6ad4545ce`), C4 (`a0c2f1afc`), C5 (`06376f356`) and C6 (`2b8e16a89`) are all
content commits; C7 (this handoff commit) is written and pushed last, per the write-once rule.

## Commits

### 907615f2f F042 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r1-block.md | +307/-0 | copy of this round's block, byte for byte |
| .agent/authored/f042-r1-plan.md | +29/-0 | copy of the plan.md payload, byte for byte |
| .agent/authored/f042-r1-context.md | +34/-0 | copy of the context.md payload, byte for byte |

Expected by the block: 307 + 63 = 370; measured: 370 (307+29+34). Match. Under the 500-line stop
threshold the block names.

### 7861df5dd F042 R1 C1b: copy round 1 claim, allowlist, walk and routes diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r1-claim.diff | +141/-0 | copy of the claim.diff payload, byte for byte |
| .agent/authored/f042-r1-allowlist.diff | +12/-0 | copy of the allowlist.diff payload, byte for byte |
| .agent/authored/f042-r1-walk.diff | +30/-0 | copy of the walk.diff payload, byte for byte |
| .agent/authored/f042-r1-routes.diff | +120/-0 | copy of the routes.diff payload, byte for byte |

Expected by the block: 303; measured: 303 (141+12+30+120). Match.

### df8085835 F042 R1 C1c: copy round 1 tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r1-tests.diff | +268/-0 | copy of the tests.diff payload, byte for byte |

Expected by the block: 268; measured: 268. Match.

### 502b44f53 F042 R1 C2: claim F042, re-head the live review record, book F041 R9, register R-1107, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +12/-11 | rewritten to the context.md payload (`shutil.copyfile`) |
| .agent/decisions.md | +55/-0 | `git apply` of claim.diff: DECISION F042 D1 appended |
| .agent/live_review.md | +29/-21 | `git apply` of claim.diff: re-head, F041 R9 gate entry, R-1107 |
| .agent/plan.md | +16/-12 | rewritten to the plan.md payload (`shutil.copyfile`) |
| docs/roadmap/STATUS.md | +1/-1 | `git apply` of claim.diff: F042's line `[ ]` to `[~]` |

Expected by the block: 12/11 context.md, 55/0 decisions.md, 29/21 live_review.md, 16/12 plan.md, 1/1
STATUS.md; measured: identical. Match.

### 6ad4545ce F042 R1 C3: list the registered projects and compose each project's card for the cockpit
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/project_cockpit.py | +209/-0 | NEW, S1-S4: projects_view, find_project, project_summary |
| packages/orchestration/ui_server.py | +27/-0 | S5: two builders after `_build_layers_json`, two routes after `/api/layers` |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `git apply` of allowlist.diff |
| tests/ui_server/test_command_channel.py | +3/-2 | `git apply` of walk.diff |

Expected by the block: ui_server.py 27/0, allowlist.txt 1/0, test_command_channel.py 3/2 — measured
identical, exact match. project_cockpit.py: the block states the REVIEWER's own version of S1-S5 read
185/0 for this file, informational only (not a per-file expectation for the worker's own
implementation); mine reads 209/0 — a different but equivalent composition of the same five spec
clauses S1-S5, written independently against the reviewer's tests. Total this commit: 240
insertions, well under the 500-line cap.

### a0c2f1afc F042 R1 C4: add the reviewer's tests for the project list and the project card
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_project_cockpit.py | +262/-0 | NEW FILE, `git apply` of tests.diff, unedited |

### 06376f356 F042 R1 C5: add the reviewer's route tests for the project list and summary
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_projects_route.py | +114/-0 | NEW FILE, `git apply` of routes.diff, unedited |

### 2b8e16a89 F042 R1 C6: add the round 1 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f042-r1-mutations.py | +187/-0 | the G4 red-proof tool: 10 mutations, control first/last |

### (this commit) F042 R1 C7: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per the write-once rule (a handoff cannot table the commit that writes it) |

## External actions

`git push -u origin feature/f042-multi-project-cockpit` after C7: real outcome reported in the
worker's final reply, since this file cannot record a push that follows it.

No pull request created this round: the block orders NOTHING IS MERGED and states the branch opens
its PR at F042's closure, not this round.

`git worktree add --detach .remedy-wt/f042-r1-mut 2b8e16a89` for G4, then `shutil.copytree` of
`apps/ui/dist` into it (`symlinks=True`), then `git worktree remove --force .remedy-wt/f042-r1-mut`
and `git worktree prune` as G4's last action. `git worktree list | wc -l` read 62 at BEFORE ANYTHING
ELSE step 4 and 62 again after the removal and prune — unchanged.

## Verification

BEFORE ANYTHING ELSE — `.agent/STOP`: `ls` reported "No such file or directory" (absent). `pwd`
`/home/decodeux/Repos/remedy`. `git status --porcelain` empty. `git branch --show-current` `main`.
`git log --oneline -1` `4e643440f` — all matching. `git checkout -b
feature/f042-multi-project-cockpit` switched cleanly. Block bytes: measured 307 lines / sha256
`e601675fd48ab0203af808ed2da8808e43e40e7e2046013ebd63b9fee540c208`, matching both readings given in
the delegation message exactly. `git worktree list | wc -l`: 62.

PAYLOADS — measured against the table, all seven matched exactly: `claim.diff` 141 lines / 19159
bytes / `41af2109aa06d656904b394051e1aad35d8034bdeeb07ff2fd28b96d4eb95809`; `allowlist.diff` 12 lines
/ 634 bytes / `edd46ac7342bdd256408b613c2764f4eca1d6899d77c1617780a61b330302492`; `walk.diff` 30
lines / 1452 bytes / `505bbdd9d960fa402c013bbbbb7949a73e1de917565a5ea7ebf4986a75b1761b`; `tests.diff`
268 lines / 14388 bytes / `68e1ae11bb62040c8ca11359dc8a475776c25d25a2d84a523b78c8d2ba4a3d4d`;
`routes.diff` 120 lines / 5227 bytes /
`ee674a626dffb6f848e8a5650fc666e26555a6567d81726325c959c4f9ff7787`; `plan.md` 29 lines / 1023 bytes
/ `2d6d679af164e19e1e2698bec37b5ebc6dbd146cc98445578ddf49e1ae3f9c84`; `context.md` 34 lines / 1460
bytes / `a0626374212ca8a775e4c2809643f53e091f6610f25e67353e4e03577977a562`.

G1 TRANSPORT — every payload's measured lines/bytes/sha256 matched the table (above). Each
`.agent/authored/f042-r1-*` copy, read back with `git show <commit>:<path>`, is byte-identical to
its source (block copy against `.remedy-wt/f042-r1/block.md`, each other payload against
`.remedy-wt/f042-r1-payloads/<name>`): all eight comparisons matched exactly (Python `==` over the
raw bytes), sha256 equal on both sides in every row.

G2 THE CLAIM AND THE TESTS — every sha256 in the block's G2 table, read with `git show
<commit>:<path>` at the commit named, equal the reviewer's reading exactly: `.agent/context.md` at
C2 1460 bytes; `.agent/decisions.md` at C2 2476722 bytes; `.agent/live_review.md` at C2 308125
bytes; `.agent/plan.md` at C2 1023 bytes; `docs/roadmap/STATUS.md` at C2 58294 bytes;
`tests/orchestration/import_reachability_allowlist.txt` at C3 11207 bytes;
`tests/ui_server/test_command_channel.py` at C3 103781 bytes;
`tests/orchestration/test_project_cockpit.py` at C4 13893 bytes;
`tests/ui_server/test_projects_route.py` at C5 4895 bytes — all nine sha256 values equal the
block's table exactly (full hashes in the round's transcript, omitted here for length; every one
matched byte for byte). `open_finding_ids` (from `scripts/rotate_live_review.py`) over
`.agent/live_review.md`: `[]` at `4e643440f`, `['R-1107']` at C2 — matching the reviewer's stated
readings exactly. At C2 the ledger has exactly one line reading `## Findings` and exactly one
reading `## Steps`; its last non-empty line begins `- R-1107 — Low`. F042's STATUS line at C2 reads
back in full as `- [~] F042 — Multi-project cockpit`. `git diff --name-only <C1c> <C2>` names
exactly `.agent/context.md`, `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md` — exactly the C2 paths of the table, in that order.

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/project_cockpit.py
packages/orchestration/ui_server.py tests/orchestration/test_project_cockpit.py
tests/ui_server/test_projects_route.py tests/ui_server/test_command_channel.py
.agent/authored/f042-r1-mutations.py` at C6: `All checks passed!`, real exit 0. `git show --numstat
6ad4545ce`: 209/0 project_cockpit.py, 27/0 ui_server.py, 1/0 allowlist.txt, 3/2
test_command_channel.py (see C3 table above); the whole `ui_server.py` diff at C3 is the two builder
functions after `_build_layers_json` and the two routes after `/api/layers`, reported verbatim in
the worker's final reply. The serial pytest run at C6, in the primary checkout:
`bash -c 'python3 -m pytest -q -p no:cacheprovider -rs <the round's 27-file selection> 2>&1 | tail
-6; echo "REAL_EXIT=${PIPESTATUS[0]}"'` read `1066 passed, 1 skipped in 133.15s (0:02:13)`,
`REAL_EXIT=0`. This differs from the reviewer's `1065 passed, 2 skipped` by exactly the variance the
block itself predicts: "Your count may differ from it by what the round's copies hold and by the
installed UI toolchain" — this checkout's `node_modules` already carries vitest (unlike the
reviewer's fresh worktree), so the `tests/orchestration/test_test_runner.py:414` vitest-absent skip
the reviewer saw did not fire here; only the D12 quarantine skip
(`tests/test_agent_tooling.py:43`) printed, and the `-rs` summary printed exactly that one
`SKIPPED` line. Node counts by `--collect-only -q`: `tests/orchestration/test_project_cockpit.py`
21, `tests/ui_server/test_projects_route.py` 8 — both equal to the reviewer's reading exactly.
`python3 -m apps.cli.main integrity check --json`: all six checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`) `"status": "pass"`, `fail_count` 0, real exit 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f042-r1-mut 2b8e16a89` (clean checkout at
C6), `apps/ui/dist` copied in with `shutil.copytree(..., symlinks=True)`, then `python3 -B
.agent/authored/f042-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f042-r1-mut`. Whole
output (reported again verbatim in the worker's final reply): control (first) exit=0 failed=0; m1
exit=1 failed=1; m2 exit=1 failed=6; m3 exit=1 failed=1; m4 exit=1 failed=1; m5 exit=1 failed=3; m6
exit=1 failed=1; m7 exit=1 failed=1; m8 exit=1 failed=1; m9 exit=1 failed=1; m10 exit=1 failed=2;
control (last) exit=0 failed=0; every mutation's restore reported `restored byte-identical: True`;
final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. Every one of the ten mutations exited
non-zero — none stayed green. `git worktree remove --force .remedy-wt/f042-r1-mut` then `git
worktree prune`, both real exit 0; `git worktree list | wc -l` read 62 afterward, matching the step
4 reading.

## Authored-text proofs

Every `.agent/authored/f042-r1-*` copy (block, plan.md, context.md, claim.diff, allowlist.diff,
walk.diff, routes.diff, tests.diff) is byte-identical, read back from the commit that added it
(`git show <commit>:<path>`), to its source under `.remedy-wt/f042-r1-payloads/` or
`.remedy-wt/f042-r1/block.md` — see G1 above, all eight comparisons matched by direct byte
comparison and equal sha256 on both sides. `claim.diff`, `allowlist.diff`, `walk.diff`,
`tests.diff` and `routes.diff` were each applied unedited with `git apply` (real exit 0 on both
`--check` and the real apply, reported per-file above); the resulting file hashes at their commits
matched the reviewer's G2 table exactly (see G2). `.agent/plan.md` and `.agent/context.md` were
rewritten from their payloads with `shutil.copyfile`, then verified byte-identical at C2 against
the table's hashes (see G2).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C1c | done | |
| C2 | done | |
| C3 | done | S1-S5 written against the reviewer's tests, not yet run at commit time; G3/G4 below prove them |
| C4 | done | tests.diff applied unedited |
| C5 | done | routes.diff applied unedited |
| C6 | done | mutation tool written and used by G4 before this commit closes |
| C7 | done | this handback |
| G1 | done | all 8 authored copies byte-identical to source |
| G2 | done | all 9 hashes, both `## Findings`/`## Steps` counts, the open-id sets, the STATUS line and the C1c..C2 diff all matched |
| G3 | done | ruff clean, 1066 passed / 1 skipped at exit 0 (variance from the reviewer's count explained and expected), both node counts matched, integrity clean |
| G4 | done | all 10 mutations caught, all 10 restores byte-identical, both controls green |
| G5 | pending | after C7 — reported in the worker's final reply, since C7 cannot contain it |

## Deviations & assumptions

None from the block's ordered commit sequence: C1a, C1b, C1c, C2, C3, C4, C5, C6, C7 executed in
that exact order, no commit was split, reordered or added, and every commit stayed well under the
500-line cap (largest: C3 at 240 insertions). No payload was retyped or edited; every `.diff` was
applied with `git apply` verbatim. No test was edited to pass and no gate result was papered over.

One explained (not block-violating) variance, flagged in G3 above: the round's own pytest selection
read `1066 passed, 1 skipped` where the reviewer's simulation read `1065 passed, 2 skipped`. The
block itself states this may happen ("Your count may differ from it by what the round's copies hold
and by the installed UI toolchain") and names the exact mechanism — a fresh worktree lacks vitest,
this checkout has it installed — which is exactly what the missing `SKIPPED` line shows. Not treated
as a red gate.

Assumption: DECISION F042 D1's "the round's whole tracked path set" (constraint 3) is read as fixed
by the block's own enumeration, and no path outside it was touched; the exact `git diff --name-only
4e643440f` list at the branch tip is reported in the worker's final reply, taken after C7 exists.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of this round (F042 round 1).
3. Round 2: T002, the client's project context, the loaders keyed by project and the header
   switcher, per DECISION F042 D1 clause 6.

Open findings: 1. Operator questions open: 1.
