# Handback — F282 Findings paydown v2 · Round 7 · Book round 6 and land T015 and T016: R-0622's UI lint gate and R-1029's bootstrap rule

## Session

SESSION 1 of feature F282 · round 7 · rounds so far 7

This round booked round 6's PASS and the resolutions of R-1004 and
R-1045 into the ledger, recorded DECISION F282 D7, and landed T015 and
T016: `apps/ui`'s eslint config gets `typescript-eslint` and its parser
so the TypeScript block actually type-aware-lints, its one real finding
(a `react-hooks/exhaustive-deps` warning in `RemedyShell.tsx` where the
digest port was rebuilt every render) is repaired by building the port
once with `useMemo`, and a pytest node gates the lint at zero problems
(T015, R-0622); and both session bootstraps — Phase 0 of
`docs/agents/self_drive_protocol.md` and §1 of
`docs/agents/planner_reviewer_prompt.md` — now read `.agent/decisions.md`
by part (the last five plus any the open feature file names) instead of
whole (T016, R-1029). Roughly half of the session's working-context
budget remained at handback.

## Range

Review of `2a8186c4`..`HEAD`.

## Commits

### 6748d9e1 F282 R7 C1a: copy round 7 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r7-block.md | +213/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r7-ledger.diff | +14/-0 | Payload copy |
| .agent/authored/f282-r7-decisions.diff | +36/-0 | Payload copy |
| .agent/authored/f282-r7-plan.md | +30/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 293
(213+80), matching the block's stated formula "this block's line count
plus 80" exactly. Under the 500 cap.

### 66ed8202 F282 R7 C1b: copy round 7 product payload into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r7-product.diff | +470/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 470,
matching the block's expected 470 exactly.

### 6c176c6e F282 R7 C1c: copy round 7 test payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r7-tests.diff | +122/-0 | Payload copy |
| .agent/authored/f282-r7-mutations.py | +68/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 190
(122+68), matching the block's expected 190 exactly.

### 2b0032a9 F282 R7 C2: book round 6, resolve R-1004 and R-1045 and record DECISION F282 D7

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | `ledger.diff` applied: `Gate: F282 R6` entry and the `Done:` lines of R-1004 and R-1045 |
| .agent/decisions.md | +28/-0 | `decisions.diff` applied: DECISION F282 D7 (the UI lint parses TypeScript and gates at zero problems; both bootstraps read decisions by part) |
| .agent/plan.md | +9/-9 | Rewritten to the round-7 `plan.md` payload (via `shutil.copyfile`) |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 28/0 decisions.md, 6/0 live_review.md, 9/9 plan.md — matching
the block's expected numbers exactly.

### e6b47f3e F282 R7 C3: let the UI lint parse TypeScript, repair its finding, read decisions by part

| Path | +/- | Reason |
|---|---|---|
| apps/ui/eslint.config.js | +12/-1 | `product.diff` applied: T015 — `typescript-eslint` parser wired into the TypeScript block, `no-undef` off there (the parser's own guidance, `tsc` covers it), `@typescript-eslint/no-explicit-any` registered and ON |
| apps/ui/package-lock.json | +333/-0 | `product.diff` applied: T015 — the reviewer's `npm install -D typescript-eslint@^8.70.1` lockfile update |
| apps/ui/package.json | +1/-0 | `product.diff` applied: T015 — `typescript-eslint` added as a devDependency |
| apps/ui/src/components/shell/RemedyShell.tsx | +6/-3 | `product.diff` applied: T015 — the digest port is built once with `useMemo` and listed as a dependency, repairing the `react-hooks/exhaustive-deps` warning |
| docs/agents/planner_reviewer_prompt.md | +3/-1 | `product.diff` applied: T016 — §1 bootstrap reads `.agent/decisions.md` by part (last 5 plus the open feature's named decisions), not whole |
| docs/agents/self_drive_protocol.md | +5/-0 | `product.diff` applied: T016 — Phase 0 bootstrap reads `.agent/decisions.md` by part, same rule |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 12/1 eslint.config.js, 333/0 package-lock.json, 1/0
package.json, 6/3 RemedyShell.tsx, 3/1 planner_reviewer_prompt.md, 5/0
self_drive_protocol.md — matching the block's expected numbers exactly.

After C3, `npm ci --prefix apps/ui --no-audit --no-fund` was run in the
primary checkout (ordered by the block, not part of the commit diff):
real exit 0, "added 299 packages in 3s". `node_modules` is gitignored
and was the only untracked write.

### bd919630 F282 R7 C4: gate the UI lint and the bootstrap rule, R-0622 and R-1029

| Path | +/- | Reason |
|---|---|---|
| tests/docs/test_bootstrap_reads_decisions_by_part.py | +32/-0 (new file) | `tests.diff` applied: pins Phase 0 and §1 reading `.agent/decisions.md` by part (R-1029) |
| tests/ui_contracts/test_digest_mount.py | +12/-2 | `tests.diff` applied: the guard now requires the `useMemo` that makes the new dependency list safe, replacing the old pinned `[dashboard.jobId]` list |
| tests/ui_contracts/test_ui_lint.py | +46/-0 (new file) | `tests.diff` applied: runs the app's own eslint at `--max-warnings 0` and proves the parser reaches the hook rules on a stdin-fed probe (R-0622) |

Measured insertions by `git diff --cached --numstat` before commit: 32/0
test_bootstrap_reads_decisions_by_part.py, 12/2 test_digest_mount.py,
46/0 test_ui_lint.py — matching the block's expected numbers exactly.

### (this commit) F282 R7 C5: rewrite handoff for round 7

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `npm ci --prefix apps/ui --no-audit --no-fund` after C3, in the
  primary checkout — real exit 0, "added 299 packages in 3s".
- `git worktree add --detach .remedy-wt/f282-r7-mut bd919630` for the
  G5 red proofs — succeeded, HEAD detached at `bd919630`.
- `npm ci --prefix .remedy-wt/f282-r7-mut/apps/ui --no-audit --no-fund` —
  real exit 0, "added 299 packages in 3s".
- `python3 -B .remedy-wt/f282-r7-payloads/mutations.py
  .remedy-wt/f282-r7-mut` — real exit 0.
- `git worktree remove --force .remedy-wt/f282-r7-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows only the primary checkout, `.remedy-wt/f282-r7-dry`,
  `.remedy-wt/f282-r7-sim` and the four `job-*` worktrees constraint 6
  names.
- `git push origin feature/f282-findings-paydown-v2` after C5 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form, no `npm install`
  beyond the ordered `npm ci`.

## Verification

**G1 — transport**: each of the six payloads' lines/bytes/sha256 measured
against the block's PAYLOADS table — all six rows matched exactly
(ledger.diff 14/5777, decisions.diff 36/2902, plan.md 30/1160,
product.diff 470/19327, tests.diff 122/5591, mutations.py 68/3267 — all
sha256 digests equal to the table). The block itself: 213 lines (newline
count), sha256
`2fbe9fb0903dc1cd3b2f49fd5621ac5704ec30a25205725c1cef2c45d00268a9`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r7-*` blob read with `git show
<commit>:<path>` (block + ledger.diff + decisions.diff + plan.md at
`6748d9e1`; product.diff at `66ed8202`; tests.diff + mutations.py at
`6c176c6e`) compared byte-for-byte against its `.remedy-wt/f282-r7-payloads/`
(or block) source: all seven pairs byte-identical = True.

**G2 — the bookkeeping and the product**: at C2 (`2b0032a9`),
`.agent/live_review.md` 416714 bytes, sha256
`f3c06e2b382f2a4b7b70ddf6e6988391b718db7f40745bdb9792086af9b9505b`;
`.agent/decisions.md` 1926652 bytes, sha256
`c3940d43605b9a1bea462d4098efa64986127ad1feaaa273cc80c3f632aaf0d3`;
`.agent/plan.md` 1160 bytes, sha256
`a6555da8391f79ebe0044a4424497ee353e729bf9dccfe09271f801a41beb98b` — at
C3 (`e6b47f3e`), `apps/ui/package.json` 917 bytes, sha256
`20dbc5b0133872799684a72122e5f851584cda4098f6b56d9eadb019d95d76f4`;
`apps/ui/package-lock.json` 195480 bytes, sha256
`cd879535da0e509e7a629ff1fb5527ae088a1bc9e98ccbdcd4db27890b427da7`;
`apps/ui/eslint.config.js` 1136 bytes, sha256
`1046b9d03d48aa2f4c25671d9fded8032156ddf1238cafb20231431132849366`;
`apps/ui/src/components/shell/RemedyShell.tsx` 11668 bytes, sha256
`589f3a43ae2563e1a2a51c36ba7e653a116e794b040500e06f4651f17fb26615`;
`docs/agents/self_drive_protocol.md` 33367 bytes, sha256
`ec1a1de785e2dc83c8266a5d821055e66bf1be4fd54399727084f2d08cac0770`;
`docs/agents/planner_reviewer_prompt.md` 97059 bytes, sha256
`1243bb5b434293cb1776f5c479927aab65704f6a58e0cb036bce0dd6ad02b6eb` — at
C4 (`bd919630`), `tests/ui_contracts/test_ui_lint.py` 2004 bytes, sha256
`5fcbb12c0bf1939f4ffad94b21200b9f1a08c1056a6add0be9916cab419b5917`;
`tests/ui_contracts/test_digest_mount.py` 20073 bytes, sha256
`199df622fe67764ee7ac0cbe5f79785ab15fdc8f5b4495ef23471a36387c1af8`;
`tests/docs/test_bootstrap_reads_decisions_by_part.py` 1285 bytes, sha256
`543718b90e4819dda346da879490fb57a225fbad046735934cc00404bd1ac78f` — all
twelve equal to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 13 at
`2a8186c4`, 11 at C2; set difference: `R-1004` and `R-1045` the only ids
leaving, none arriving — matching the block's reading exactly. `git diff
--name-only 66ed8202 6c176c6e` names exactly
`.agent/authored/f282-r7-mutations.py`,
`.agent/authored/f282-r7-tests.diff` — C1c's list. `git diff --name-only
6c176c6e 2b0032a9` names exactly `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` — C2's list. `git diff
--name-only 2b0032a9 e6b47f3e` names exactly `apps/ui/eslint.config.js`,
`apps/ui/package-lock.json`, `apps/ui/package.json`,
`apps/ui/src/components/shell/RemedyShell.tsx`,
`docs/agents/planner_reviewer_prompt.md`,
`docs/agents/self_drive_protocol.md` — C3's list. `git diff --name-only
e6b47f3e bd919630` names exactly
`tests/docs/test_bootstrap_reads_decisions_by_part.py`,
`tests/ui_contracts/test_digest_mount.py`,
`tests/ui_contracts/test_ui_lint.py` — C4's list.

**G3 — the linter on this block**: at C4, in the primary checkout,
`python3 -m apps.cli.main integrity block .remedy-wt/f282-r7-block.md`,
real exit 0:
```
  [OK] item 1 (size): 213 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): states 11; .agent/live_review.md holds 11 open by distinct id, and the block registers 0 and resolves 0, leaving 11
  [OK] item 24 (gate paths resolve): 12 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G5 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```

**G4 — the tests and the lint**: in the primary checkout at C4, after the
`npm ci`, the ordered pytest selection (12 paths, including
`tests/cli/test_golden_path.py`), run SERIALLY, real exit 0: `1429
passed, 5 skipped in 83.59s (0:01:23)`. The reviewer's disposable-worktree
run without the golden path read `1386 passed, 6 skipped` at exit 0; this
run includes the golden path per the block's own command, so the higher
pass count and the one fewer skip are expected, not a deviation. `npm run
--silent lint --prefix apps/ui`: real exit 0, no output. `npm run
--silent typecheck --prefix apps/ui`: real exit 0. `python3 -m ruff
check tests/ui_contracts/test_ui_lint.py
tests/docs/test_bootstrap_reads_decisions_by_part.py
tests/ui_contracts/test_digest_mount.py`: real exit 0, "All checks
passed!". `python3 -m apps.cli.main integrity check --json`: real exit 0,
`check_count: 6`, all six checks (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`) `pass`, `fail_count: 0`, `ok: true`, `passed: true`.

**G5 — the red proofs**: `git worktree add --detach .remedy-wt/f282-r7-mut
bd919630` succeeded. `npm ci --prefix .remedy-wt/f282-r7-mut/apps/ui
--no-audit --no-fund`: real exit 0, "added 299 packages in 3s". `python3
-B .remedy-wt/f282-r7-payloads/mutations.py .remedy-wt/f282-r7-mut` (real
exit 0), whole output:
```
control_before REAL_EXIT=0
30 passed in 2.08s
m1_no_typescript_parser FROM count in apps/ui/eslint.config.js: 1
m1_no_typescript_parser REAL_EXIT=1
FAILED tests/ui_contracts/test_ui_lint.py::test_the_ui_lint_passes_with_no_problem
FAILED tests/ui_contracts/test_ui_lint.py::test_the_lint_parses_typescript_and_reaches_the_hook_rules
2 failed, 28 passed in 1.06s
m1_no_typescript_parser restored byte-identical: True
m2_no_undef_back_on FROM count in apps/ui/eslint.config.js: 1
m2_no_undef_back_on REAL_EXIT=1
FAILED tests/ui_contracts/test_ui_lint.py::test_the_ui_lint_passes_with_no_problem
1 failed, 29 passed in 1.81s
m2_no_undef_back_on restored byte-identical: True
m3_the_effect_misses_its_port FROM count in apps/ui/src/components/shell/RemedyShell.tsx: 1
m3_the_effect_misses_its_port REAL_EXIT=1
FAILED tests/ui_contracts/test_ui_lint.py::test_the_ui_lint_passes_with_no_problem
FAILED tests/ui_contracts/test_digest_mount.py::TestLastSeenIsReadBeforeItIsWritten::test_the_write_effect_body_is_only_the_one_call
2 failed, 28 passed in 1.83s
m3_the_effect_misses_its_port restored byte-identical: True
m5_the_port_rebuilt_every_render FROM count in apps/ui/src/components/shell/RemedyShell.tsx: 1
m5_the_port_rebuilt_every_render REAL_EXIT=1
FAILED tests/ui_contracts/test_digest_mount.py::TestLastSeenIsReadBeforeItIsWritten::test_the_write_effect_body_is_only_the_one_call
1 failed, 29 passed in 1.79s
m5_the_port_rebuilt_every_render restored byte-identical: True
m4_phase_0_reads_decisions_whole FROM count in docs/agents/self_drive_protocol.md: 1
m4_phase_0_reads_decisions_whole REAL_EXIT=1
FAILED tests/docs/test_bootstrap_reads_decisions_by_part.py::test_phase_0_reads_decisions_by_part
1 failed, 29 passed in 1.83s
m4_phase_0_reads_decisions_whole restored byte-identical: True
r1_eslint_config_before_this_round REAL_EXIT=1
FAILED tests/ui_contracts/test_ui_lint.py::test_the_ui_lint_passes_with_no_problem
FAILED tests/ui_contracts/test_ui_lint.py::test_the_lint_parses_typescript_and_reaches_the_hook_rules
2 failed, 28 passed in 0.60s
r1_eslint_config_before_this_round restored byte-identical: True
control_after REAL_EXIT=0
30 passed in 1.79s
REAL_EXIT=0
```
Matches the reviewer's reading exactly: control_before `30 passed` exit
0; m1 2 failed exit 1; m2 1 failed exit 1; m3 2 failed exit 1; m5 1
failed exit 1; m4 1 failed exit 1; r1 2 failed exit 1; control_after `30
passed` exit 0; every `restored byte-identical` line True. `git worktree
remove --force .remedy-wt/f282-r7-mut` and `git worktree prune`: both
real exit 0. `git worktree list` afterward: primary checkout plus
`.remedy-wt/f282-r7-dry`, `.remedy-wt/f282-r7-sim` and the four `job-*`
worktrees constraint 6 names — nothing else.

## Authored-text proofs

- `.agent/authored/f282-r7-block.md` (C1a) == `.remedy-wt/f282-r7-block.md`:
  byte-identical True (sha256
  `2fbe9fb0903dc1cd3b2f49fd5621ac5704ec30a25205725c1cef2c45d00268a9`, 213
  lines).
- `.agent/authored/f282-r7-ledger.diff`, `-decisions.diff`, `-plan.md`
  (C1a) == their `.remedy-wt/f282-r7-payloads/` sources: byte-identical
  True, all three.
- `.agent/authored/f282-r7-product.diff` (C1b) == its
  `.remedy-wt/f282-r7-payloads/` source: byte-identical True.
- `.agent/authored/f282-r7-tests.diff`, `-mutations.py` (C1c) == their
  `.remedy-wt/f282-r7-payloads/` sources: byte-identical True, both.
- `ledger.diff`, `decisions.diff`, `product.diff`, `tests.diff` were
  applied at C2/C3/C4 with `git apply --check` then `git apply` directly
  from the payload's own bytes under `.remedy-wt/f282-r7-payloads/` —
  never retyped, every `--check` and every real apply at real exit 0.
- `.agent/plan.md` at C2 == `plan.md` payload verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  table above).
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and every diff was applied by `git apply` reading the
  payload file directly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 293 insertions, matches block formula (213+80) exactly |
| C1b | done | 470 insertions, matches block exactly |
| C1c | done | 190 insertions, matches block exactly |
| C2 | done | 28/6/9 insertions by `git diff --cached --numstat`, matches block exactly |
| C3 | done | 12/1, 333/0, 1/0, 6/3, 3/1, 5/0, matches block exactly |
| C4 | done | 32/0, 12/2, 46/0, matches block exactly |
| C5 | done | this handback |
| Round 6 booking | done | `Gate: F282 R6` entry appended to `.agent/live_review.md` via `ledger.diff` |
| R-1004 | done | resolved — booked as one of the two ids leaving the open set at C2 |
| R-1045 | done | resolved — booked as one of the two ids leaving the open set at C2 |
| DECISION F282 D7 | done | recorded at C2 via `decisions.diff` |
| T015 | done | `typescript-eslint` and its parser added to `apps/ui`'s eslint config, the `RemedyShell.tsx` `exhaustive-deps` finding repaired with `useMemo`, gated by `tests/ui_contracts/test_ui_lint.py` (R-0622), landed at C3 with tests at C4 |
| T016 | done | both session bootstraps read `.agent/decisions.md` by part instead of whole, gated by `tests/docs/test_bootstrap_reads_decisions_by_part.py` (R-1029), landed at C3 with tests at C4 |
| G1 | done | all readings match; all seven authored copies byte-identical |
| G2 | done | all twelve sha256/byte readings match; open-set 13 to 11, R-1004/R-1045 leaving exactly as named; all four name-only diffs match exactly |
| G3 | done | integrity block linter, real exit 0, all 7 checkable items `[OK]` |
| G4 | done | 1429 passed, 5 skipped, exit 0 (reviewer's worktree run without golden path: 1386 passed/6 skipped); lint exit 0 no output; typecheck exit 0; ruff exit 0; integrity check all-pass exit 0 |
| G5 | done | mutation script output matches the reviewer's reading exactly across all seven sub-checks; worktree cleaned up |
| G6 | done | readings reported in the final reply only, per the block |
| Push | done | reported in the final reply only, per the block |

## Deviations & assumptions

None. Every reading this round matched the block's stated expectation
exactly. No payload was edited or retyped; every copy used
`shutil.copyfile` and every diff was applied via `git apply` reading the
payload file directly. The commit sequence landed in the block's exact
order C1a-C1b-C1c-C2-C3-C4-C5. This round is SESSION 1 of F282, its
seventh round.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
7, then T014 and T017 — R-0892 and R-0866. Open findings count: 11.
Operator-questions count: 0.
