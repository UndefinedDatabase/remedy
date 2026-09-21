# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 9 · the `project` group and the three `do` refusals

## Session

SESSION 2 of feature F283 · round 9 · rounds so far 9

This round booked round 8's PASS and the `Done:` lines of R-1019 and R-1025, recorded
DECISION F283 D4 (an uppercase `ERROR: ` refusal migrates like `Error: ` and gains the
case), moved all 23 of the `project` group's mechanical refusal pairs reachable by the
migration rule onto `fail()` (2 stay — both `print(str(exc), file=sys.stderr)` with no
prefix at all), and migrated the three `do` refusals round 8 correctly declined —
`_cmd_do`'s contract-template lookup, `_cmd_run_show`'s run lookup and `_cmd_run_list`'s
list-option refusal — repairing the three tests that pinned their old `--json` shape.
Context self-assessment: roughly 98% of the working budget remained at the point this
handoff was written (about 14.7M of 15M tokens).

## Range

Review of `432c2eb4`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 191 | 191 | True |
| sha256 | `df592ea882bdbf169268619bcdabd1f436d41f9d65dd9c8673501d5f93520eaa` | `df592ea882bdbf169268619bcdabd1f436d41f9d65dd9c8673501d5f93520eaa` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `432c2eb4`, matching the delegation message.

## Commits

### d6eda8ea F283 R9 C1: copy round 9 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r9-block.md | +191/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r9-decisions.md | +28/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r9-ledger.md | +6/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r9-plan.md | +35/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **260** (191+28+6+35).

### 40654b27 F283 R9 C2: book round 8's PASS, resolve R-1019 and R-1025
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +28/-0 | append decisions.md: DECISION F283 D4 |
| .agent/live_review.md | +6/-0 | append ledger.md by strict byte concatenation: round-8 `Gate:` entry, `Done: R-1019`, `Done: R-1025` |
| .agent/plan.md | +10/-13 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed, not the whole file |

Measured insertions (`git show --numstat`): **44** (28+6+10); 13 deletions from the plan.md rewrite.

### fd2abcdc F283 R9 C3: project refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/project.py | +30/-54 | `fail` imported; 23 of the module's 25 mechanical print-then-exit pairs move onto `fail()` — `invalid_list_option` (reused), `invalid_project_id` (new, ×6), `project_not_found` (new, ×6), `not_a_git_repo` (new, ×2), `repo_ownership_conflict` (new, ×2), `invalid_job_id` (reused, ×2), `ambiguous_project` (new, ×2), `no_project` (reused), `job_already_in_project` (new). 6 of the 23 carried the uppercase `ERROR: ` prefix DECISION F283 D4 migrates the same way. 2 sites stay: `_cmd_project_current`'s and `_cmd_project_attach_repo`'s identical `(ProjectNotFoundError, InvalidProjectSelectorError)` branches, each a bare `print(str(exc), file=sys.stderr)` with no prefix at all |
| tests/cli/test_job_refusal_envelope.py | +38/-0 | `TestProjectRefusalsAreAllMigrated`: exactly one flagged and one unflagged site remain (the two no-prefix sites above); the module imports `fail` |
| tests/cli/test_project_current.py | +59/-0 | `_make_and_save_raw` helper (bypasses `save_project`'s slug-uniqueness check to build a duplicate-slug fixture); `TestProjectCurrentAmbiguousRefusal` — the `--json` envelope test (`ambiguous_project`, `schema_version` 1, `ok` false) and the text-mode test asserting the D4 case change (`Error: `, not `ERROR: `) — this is C3's required `project`-file envelope test and D4 text-mode assertion |

Measured insertions: **127** (30+38+59).

### a1cfd45b F283 R9 C4: the last three do refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/do_cmd.py | +7/-8 | `_cmd_do`'s contract-template lookup → `fail("unsupported_contract_template", ..., exit_code=2)` (new token); `_cmd_run_show`'s run lookup → `fail("run_not_found", ...)` (new token); `_cmd_run_list`'s list-option refusal → `fail("invalid_list_option", ...)` (reused) |
| tests/cli/test_cli_ux.py | +22/-1 | `TestRunShow::test_missing_run_exits_one` repaired to assert the envelope (`error` `run_not_found`) instead of stderr prose under `--json`; added `test_missing_run_text_mode_keeps_the_error_prefix` to keep the byte-identical text-mode coverage the repair displaced; `TestRunList::test_unknown_sort_field_exits_without_a_traceback` repaired to assert the envelope (`error` `invalid_list_option`) instead of stderr prose under `--json` |
| tests/cli/test_do_sequence_cli.py | +9/-3 | `test_contract_naming_no_template_exits_2_naming_the_templates_and_writes_nothing` repaired to assert the envelope (`error` `unsupported_contract_template`, exact `message`) instead of stderr prose and empty stdout under `--json` |
| tests/cli/test_job_refusal_envelope.py | +18/-24 | `TestDoRefusalsAreAllMigrated` docstring and assertion updated: one flagged site remains (`_cmd_do_order`'s `ctx.failed`, the double-envelope hazard), not four |

Measured insertions: **56** (7+22+9+18); 36 deletions.

### C5 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r9-redproof a1cfd45b` for G5 — used for the
  unmutated control and all four mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r9-redproof --force` — a plain remove
  sufficed because every mutation was reverted by hand back to the original text
  (verified clean with `git status --porcelain` after each revert) before removal.
- `git push origin feature/f283-machine-contracts-part-two` after C5 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed.
  The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| decisions.md | 28/28 | 1992/1992 | True |
| ledger.md | 6/6 | 5051/5051 | True |
| plan.md | 35/35 | 1502/1502 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r9-*` copies (the block copy plus three payloads), each
read back from the committed tree with `git show d6eda8ea:<path>` and compared
byte-for-byte with its source:

| copy | bytes | identical to source |
|---|---|---|
| f283-r9-block.md | 12043 | True |
| f283-r9-decisions.md | 1992 | True |
| f283-r9-ledger.md | 5051 | True |
| f283-r9-plan.md | 1502 | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`432c2eb4`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 487106 | 5051 | 492157 | True |
| .agent/decisions.md | 1797316 | 1992 | 1799308 | True |

Matches the reviewer's stated `487106 + ledger.md = 492157` and
`1797316 + decisions.md = 1799308` exactly.

**(b) Line-anchored on the committed ledger**: `^Done: R-1019 — ` = **1**;
`^Done: R-1025 — ` = **1**. Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `432c2eb4` | **24** |
| C2 (`40654b27`) | **22** |

Added: `[]`. Removed: `['R-1019', 'R-1025']`. Matches the reviewer's stated
24 → 22, ADDED empty, REMOVED `R-1019`/`R-1025`, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256 of the
committed blob (`6586cb3fe82c081328df99f71c6cea7fc5fa7a58303a606adeade8d10f52d5eb`)
equals the payload's sha256 from the PAYLOADS table.

Line count: **35**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `40654b27`→`fd2abcdc` | apps/cli/commands/project.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_project_current.py | 127 |
| C4 `fd2abcdc`→`a1cfd45b` | apps/cli/commands/do_cmd.py, tests/cli/test_cli_ux.py, tests/cli/test_do_sequence_cli.py, tests/cli/test_job_refusal_envelope.py | 56 |

At C4, `python3 .remedy-wt/f283-r6-scratch/pairs.py project.py do_cmd.py`:

```
project.py exits 2 mechanical 2 flagged 1 unflagged 1
   345 _cmd_project_current True json_output
   387 _cmd_project_attach_repo True None
do_cmd.py exits 2 mechanical 1 flagged 1 unflagged 0
   142 _refuse_before_any_step False None
   390 _cmd_do_order True json_output
```

The reviewer read at `432c2eb4` `project.py exits 25 mechanical 25 flagged 11
unflagged 14` and `do_cmd.py exits 5 mechanical 4 flagged 4 unflagged 0` — both
confirmed by this worker's own pre-edit run before C3. `project.py` fell to
`exits 2 mechanical 2 flagged 1 unflagged 1`: 23 of 25 mechanical pairs migrated,
the 2 remaining being the no-prefix `(ProjectNotFoundError,
InvalidProjectSelectorError)` sites the migration rule never reaches. `do_cmd.py`
fell to `exits 2 mechanical 1 flagged 1 unflagged 0`: the three round-8 deviations
migrated, `_refuse_before_any_step` (never mechanical, multi-print) and
`_cmd_do_order`'s `ctx.failed` (the double-envelope hazard) unchanged.

`git diff --name-only 432c2eb4 a1cfd45b -- packages/` prints **nothing** (real
exit code implicit 0, empty stdout) — confirmed `packages/` untouched across the
whole round.

### Token list — every `fail()` token C3 and C4 use, its line, new or reused

| commit | line | token | new/reused | search behind a `new` one |
|---|---|---|---|---|
| C3 | 56 | invalid_list_option | reused (blocker.py, change.py, decision.py, event.py, memory.py, mission_cmd.py, patch.py, worker.py all use it for the same `ListOptionError` condition) | — |
| C3 | 87 | invalid_project_id | new | `grep -rn "invalid_project" apps/cli/ tests/` before this commit: 0 `fail()` tokens matched (only test method NAMES like `test_invalid_project_id_exits`, not a token) |
| C3 | 94 | project_not_found | new | `grep -rn "project_not_found" apps/cli/ tests/` before this commit: 0 hits anywhere |
| C3 | 115 | invalid_project_id | reused (same commit, L87) | — |
| C3 | 119 | project_not_found | reused (same commit, L94) | — |
| C3 | 123 | not_a_git_repo | new | `grep -rn "not_a_git_repo" apps/cli/ tests/` before this commit: 0 hits (the exception class is `NotAGitRepoError`; no existing `fail()` token for it) |
| C3 | 125 | repo_ownership_conflict | new | `grep -rn "repo_ownership_conflict" apps/cli/ tests/` before this commit: 0 hits |
| C3 | 143 | invalid_project_id | reused (same commit) | — |
| C3 | 147 | project_not_found | reused (same commit) | — |
| C3 | 152 | invalid_job_id | reused (`job_context_cmd.py:276` raises the identical message pattern, `f"No job matches {job_id_str!r}. Try: remedy job list."`, from the same `JobNotFoundError`, under this exact token — the existing spelling for THIS message shape, distinct from the `job_not_found`/`str(exc)` shape used elsewhere) | — |
| C3 | 179 | invalid_project_id | reused (same commit) | — |
| C3 | 186 | project_not_found | reused (same commit) | — |
| C3 | 218 | invalid_project_id | reused (same commit) | — |
| C3 | 225 | project_not_found | reused (same commit) | — |
| C3 | 272 | invalid_project_id | reused (same commit) | — |
| C3 | 279 | project_not_found | reused (same commit) | — |
| C3 | 342 | ambiguous_project | new | `grep -rn "ambiguous_project" apps/cli/ tests/` before this commit: 0 `fail()` tokens (only unrelated test names in `test_runtime_config.py`) |
| C3 | 384 | ambiguous_project | reused (same commit, L342) | — |
| C3 | 393 | not_a_git_repo | reused (same commit, L123) | — |
| C3 | 395 | repo_ownership_conflict | reused (same commit, L125) | — |
| C3 | 421 | no_project | reused (`mission_cmd.py:51` raises the identical message, `"no project found. Run: remedy init\n  or pass --project <slug-or-id>"`, from the same `select_project`/`ProjectNotFoundError` path, under this exact token) | — |
| C3 | 433 | invalid_job_id | reused (same commit, L152) | — |
| C3 | 437 | job_already_in_project | new | `grep -rn "job_already_in_project\|already_in_project" apps/cli/ tests/` before this commit: 0 hits |
| C4 | 452 | unsupported_contract_template | new | `grep -rn "unsupported_contract_template\|contract_template_not_found\|invalid_contract_template" apps/cli/ tests/` before this commit: 0 hits; `contract_cmd.py`'s existing `invalid_contract` token names a DIFFERENT condition (a contract BODY breaking a D2 rule, not an unrecognized `--contract` flag value), so it is not the same condition and is not reused; named to match `do_cmd.py:441`'s `unsupported_provider`, the identical grammatical shape ("--x is not a Y; the Ys are") nine lines above in the same module |
| C4 | 483 | run_not_found | new | `grep -rn "run_not_found\|invalid_run_id\|No run matches" apps/cli/ tests/` before this commit: the only hit was the `print` statement itself (and its text-mode pin in `test_cli_ux.py`); no existing `fail()` token |
| C4 | 522 | invalid_list_option | reused (same as C3 L56; the repo-wide spelling for `ListOptionError`) | — |

New tokens this round: `invalid_project_id`, `project_not_found`, `not_a_git_repo`,
`repo_ownership_conflict`, `ambiguous_project`, `job_already_in_project`,
`unsupported_contract_template`, `run_not_found` — eight, each confirmed absent
from a `fail("<token>"` search over `apps/cli/` before its introducing commit.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r9-scratch/selection.txt`: **79** space-separated paths (round
8's widened selection plus the `project` test files); `tests/cli/test_project_current.py`
(C3's named `project` test file) is already in the list — no addition needed.

| when | exit code | summary |
|---|---|---|
| after C3 | 0 | 3395 passed |
| after C4 | 0 | 3396 passed |

Zero failed, zero errors, zero xfailed at each; the reviewer read `3390 passed`
at `432c2eb4` — the count rose both times, never fell. `python3 -m ruff check`
over every `.py` path the round touched (`apps/cli/commands/project.py`,
`apps/cli/commands/do_cmd.py`, `tests/cli/test_job_refusal_envelope.py`,
`tests/cli/test_do_sequence_cli.py`, `tests/cli/test_cli_ux.py`,
`tests/cli/test_project_current.py`): **All checks passed!**
`python3 -m apps.cli.main integrity check --json`: `"passed": true, "fail_count": 0`,
all five checks (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) read `"status": "pass"`.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r9-redproof` at `a1cfd45b`, never committed.

| step | exit code | result |
|---|---|---|
| unmutated control (`test_job_refusal_envelope.py`, `test_project_current.py`, `test_do_sequence_cli.py`, `test_cli_ux.py`) | 0 | 202 passed |
| (a) one migrated `fail()` in `project.py` (`_cmd_show_project`'s invalid-UUID site, L87) reverted to its old `print`+`sys.exit(1)` | 1 | `1 failed, 60 passed` — `TestProjectRefusalsAreAllMigrated::test_exactly_one_flagged_site_remains` (found 2 sites, not 1) |
| (b) the `project` refusal C3's envelope test reaches (`_cmd_project_current`'s `ambiguous_project` site) forced to `fail(..., json_output=False)` | 1 | `1 failed, 19 passed` — `TestProjectCurrentAmbiguousRefusal::test_json_output_is_an_envelope` |
| (c) that same site reverted to its old `print(f"ERROR: {exc}", file=sys.stderr)` + `sys.exit(1)` | 1 | `2 failed, 18 passed` — `TestProjectCurrentAmbiguousRefusal::test_text_mode_uses_error_prefix` (the target) and `::test_json_output_is_an_envelope` (collateral: the whole `fail()` call at that site is gone, so the `--json` envelope disappears too, not only the text-mode prefix) |
| (d) `_cmd_run_list`'s migrated refusal forced to `fail(..., json_output=False)` | 1 | `1 failed, 120 passed` — `TestRunList::test_unknown_sort_field_exits_without_a_traceback` |

Each mutation was reverted by hand and confirmed clean with `git status --porcelain`
before the next. `git worktree remove .remedy-wt/f283-r9-redproof --force` afterward.
`git worktree list` (post-removal): the primary checkout at `a1cfd45b` plus the three
`remedy/job-*` worktrees — `.remedy-wt/job-468c8e62a2cc4fac`, `.remedy-wt/job-86f628f5e4fb4e0c`,
`.remedy-wt/job-c1dba9c3d7874968` — untouched throughout.

## Deviations & assumptions

1. **The bundle ran C1 through C4 — four commits, exactly as ordered — before
   this handback commit C5.** Nothing was added, dropped or reordered.
2. **No expected insertion figure is given for C2's rewrite or for C3/C4, per
   the block's own convention**: only measured figures are reported above, and
   none of them was forced to match a prediction.
3. **`tests/cli/test_project_current.py` was chosen as "the `project` test file
   C3 names"**, over `tests/cli/test_project_summary_cli.py`, because it already
   houses `_cmd_project_current`'s and `_cmd_project_attach_repo`'s tests and is
   the natural home for the `ambiguous_project` refusal both those handlers share
   — the one refusal in the group that is BOTH reachable under `--json` (an
   envelope test) and was formerly `ERROR: `-prefixed (a D4 text-mode test), so
   one fixture (`_make_and_save_raw`, a duplicate-slug pair bypassing
   `save_project`'s uniqueness check) serves both required tests in the same
   commit.
4. **Mutation (c) reddened two tests, not one.** The block's G5 (c) names the
   text-mode test as the one that "must fail"; reverting the `ambiguous_project`
   site to its pre-migration form removes the ONLY `fail()` call there, so the
   `--json` envelope test built on the same call site fails too. Reported exactly
   as measured, not trimmed to the named test alone.
5. **Constraints 1, 3, 4 and 7 held throughout.** No payload was edited or
   retyped; the round's tracked path set is exactly the 14 paths constraint 3
   enumerates (verified by set-equality below, C5 included); `packages/` was
   never touched; every commit left the targeted G4 selection at zero failed
   (3395 passed after C3, 3396 after C4, both real full-selection runs, no
   partial substitute); the one G5 worktree was removed as G5's last action and
   the three `remedy/job-*` worktrees were left alone.

### The round's whole tracked path set (before this commit)

`git diff --name-only 432c2eb4 a1cfd45b` — **13** distinct paths
(`tests/cli/test_job_refusal_envelope.py` touched by both C3 and C4, counted
once); plus `.agent/handoff.md` from this commit makes **14** — set-equal to
constraint 3's enumeration (4 authored copies + live_review.md + decisions.md +
plan.md + handoff.md + project.py + do_cmd.py + test_job_refusal_envelope.py +
test_do_sequence_cli.py + test_cli_ux.py + test_project_current.py, the ONE
`project` test file C3 names):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r9-block.md | C1 `d6eda8ea` |
| 2 | .agent/authored/f283-r9-decisions.md | C1 `d6eda8ea` |
| 3 | .agent/authored/f283-r9-ledger.md | C1 `d6eda8ea` |
| 4 | .agent/authored/f283-r9-plan.md | C1 `d6eda8ea` |
| 5 | .agent/decisions.md | C2 `40654b27` |
| 6 | .agent/live_review.md | C2 `40654b27` |
| 7 | .agent/plan.md | C2 `40654b27` |
| 8 | apps/cli/commands/project.py | C3 `fd2abcdc` |
| 9 | tests/cli/test_job_refusal_envelope.py | C3 `fd2abcdc`, touched again by C4 `a1cfd45b` |
| 10 | tests/cli/test_project_current.py | C3 `fd2abcdc` |
| 11 | apps/cli/commands/do_cmd.py | C4 `a1cfd45b` |
| 12 | tests/cli/test_cli_ux.py | C4 `a1cfd45b` |
| 13 | tests/cli/test_do_sequence_cli.py | C4 `a1cfd45b` |
| 14 | .agent/handoff.md | C5 (this commit) |

No path outside the enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`,
`README.md`, `docs/roadmap/**`, and `apps/cli/json_envelope.py` appear **0**
times. `packages/` appears **0** times (confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r9-payloads/` and `.remedy-wt/f283-r9-block.md`: **four
  readings, all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/decisions.md` (decisions.md), byte numbers equal to the reviewer's
  (G2a).
- No payload was edited or retyped. All four `.agent/authored/` copies and the
  one product-file rewrite were made with `shutil.copyfile`; the two appends by
  reading each payload's bytes and writing base+payload back to disk.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the
  block's SPEC — there is no reviewer-authored diff to compare against for those
  files; the block's SPEC prose is the standard they were written to, and
  G3/G4/G5 above are the proof they meet it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `432c2eb4`; block 191 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 260 insertions |
| C2 book round 8 PASS, resolve R-1019/R-1025, record D4 | done | 44 insertions (28+6+10, 13 deletions from plan rewrite); open set 24→22, removed R-1019/R-1025 |
| C3 project refusals answer through fail() | done | 127 insertions; 23/25 mechanical pairs migrated, 2 no-prefix sites stay |
| C4 the last three do refusals answer through fail() | done | 56 insertions; 3 sites migrated, 3 tests repaired, ratchet updated |
| C5 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + decisions.md append | done | 487106+5051=492157; 1797316+1992=1799308 |
| G2(b) R-1019/R-1025 Done pairing + open set by distinct id | done | 1 Done R-1019 / 1 Done R-1025; 24→22, added none, removed R-1019/R-1025 |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 35 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; `pairs.py` matches at C4; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 3395/3396 passed, 0 failed/errors/xfailed (up from 3390); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d) | done | all four go RED at exactly the predicted test(s), (c) with one honestly-reported collateral failure; unmutated control 202 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 260, 44, 127, 56; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 14 paths after this commit, set-equal to the enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 3395 passed after C3, 3396 after C4, both real full-selection runs |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r9-redproof`, removed as G5's last action, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 9 — C1 through C5, with all six gates re-derived.
3. Then round 10 — `_cmd_do_order`'s result document takes the envelope (the
   `ctx.failed` double-envelope hazard resolved by restructuring the success
   path's JSON emission, not by wrapping the trailing print+exit), then the
   `grouped` and `test_cmds` groups.

Open findings count: **22**. Operator-questions count: **2**.
