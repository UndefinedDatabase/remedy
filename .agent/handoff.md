# Handback — F261 CLI vocabulary v2, round 18

## Session

SESSION 4 of feature F261 · round 18 · rounds so far 18

Context self-assessment: comfortable — the round read the block, AGENTS.md, the protocol, the
T003 inventory and the handback template, applied three tables and ran eight gates without
re-reading anything twice, and a further round of the same shape would fit.

## Range

Review of `43694261`..`HEAD`, where `HEAD` is C5 — the commit that writes this file, which it
cannot name from inside itself (R-0149 self-reference pattern).

## Commits

### 46a0857c F261 R18 C0a: save the round 18 step block under the authored directory

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r18.md` | +370/-0 | the block file the delegating message names, copied by `shutil.copyfile` |
| **Commit total** | **+370/-0** | constraint 5 reading: 370 insertions |

### f83cb299 F261 R18 C0b: mirror the round 18 step block into the last block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +140/-122 | the same bytes, byte-identical to C0a's file |
| **Commit total** | **+140/-122** | constraint 5 reading: 140 insertions |

### 9d28c213 F261 R18 C1: re-point the plan at round 18, book round 17's PASS and its prose slip, register R-0908 and R-0910 for F273 and R-0909 for this feature and record DECISION F261 D17

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +11/-10 | full replacement by slice PLAN18 |
| `.agent/live_review.md` | +8/-0 | slice RECORD18 appended: round 17 PASS, R-0908, R-0909, R-0910 |
| `.agent/decisions.md` | +14/-0 | slice DEC17 appended: DECISION F261 D17 |
| `.agent/prose_slips.md` | +2/-0 | slice SLIP18 appended: the round 17 scratch-directory wording slip |
| `docs/roadmap/features/T2_F273.md` | +5/-0 | pair P273 applied: acceptance lines for R-0908 and R-0910 |
| **Commit total** | **+40/-10** | constraint 5 reading: 40 insertions |

### 0a3f4dcf F261 R18 C2: delete the context group, its handler and its tests, re-pointing every hint that named the command, by the context table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r18-context.jsonl` | +28/-0 | the table carrier |
| `apps/cli/command_catalog.py` | +1/-17 | the `context` group and `context.inspect` go; `do.run` `related=` drops it |
| `apps/cli/commands/__init__.py` | +1/-2 | the handler module leaves the import and the dispatch tuple |
| `apps/cli/commands/context.py` | +0/-70 | the deleted handler |
| `packages/orchestration/brain_detail.py` | +1/-1 | hint re-pointed at `remedy brain context` |
| `packages/orchestration/do_run.py` | +1/-1 | hint re-pointed at `remedy job context <id> --task <t> --json` |
| `packages/orchestration/token_economy.py` | +4/-4 | two hints re-pointed at `remedy job show --full --json` |
| `scripts/remedy_smoke.sh` | +2/-2 | `context` out of the section 0 loop and its printed line |
| `docs/system/context-inspector.md` | +9/-8 | the heir paragraph replaces the command |
| `docs/system/architecture.md` | +2/-2 | two references re-pointed |
| `docs/guides/do-run-v1.md` | +2/-2 | two references re-pointed |
| `tests/cli/test_context_inspect_cli.py` | +0/-225 | tests of the deleted handler |
| `tests/cli/test_context_inspect_runtime.py` | +0/-276 | tests of the deleted handler |
| `tests/orchestration/import_reachability_allowlist.txt` | +0/-1 | the handler leaves the allowlist |
| `tests/orchestration/test_do_run.py` | +6/-5 | the re-pointed hint |
| `tests/orchestration/test_token_economy.py` | +2/-2 | the re-pointed hints |
| `tests/test_command_catalog.py` | +1/-0 | `context.inspect` joins `TestDeletedCommands` |
| `tests/test_context_coverage.py` | +1/-1 | the re-pointed hint |
| `tests/test_project_context_coverage.py` | +2/-2 | the re-pointed hint |
| **Commit total** | **+63/-621** | constraint 5 reading: 63 insertions |

### 4ea59820 F261 R18 C3: delete the token group with context-pack, their shared handler and its tests, replacing the two documented command fences with the cockpit heir, by the token table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r18-token.jsonl` | +17/-0 | the table carrier |
| `apps/cli/command_catalog.py` | +0/-77 | both groups and their five commands go |
| `apps/cli/commands/__init__.py` | +1/-2 | the shared handler module leaves import and dispatch tuple |
| `apps/cli/commands/token_cmd.py` | +0/-144 | the deleted handler, which served both groups |
| `packages/orchestration/token_economy.py` | +5/-7 | three hints re-pointed at `remedy job show --full --json` |
| `docs/guides/token-economy-user-guide-v0.md` | +9/-15 | three command fences replaced by dated heir paragraphs |
| `docs/system/token-economy-context-budget-optimizer-v0.md` | +10/-14 | the CLI fence replaced by a "No CLI surface" paragraph |
| `tests/cli/test_cli_ux.py` | +0/-1 | `token` and `context-pack` leave `_INTERNAL_GROUPS` |
| `tests/cli/test_token_cli.py` | +0/-80 | tests of the deleted handler |
| `tests/orchestration/import_reachability_allowlist.txt` | +0/-1 | the handler leaves the allowlist |
| `tests/test_command_catalog.py` | +5/-0 | the five deleted ids join `TestDeletedCommands` |
| **Commit total** | **+47/-341** | constraint 5 reading: 47 insertions |

### 72a57e38 F261 R18 C4: delete the review group, its handler, its tests and its smoke sections, and take the groups rounds 16 and 17 deleted out of the smoke script's group list, by the review table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r18-review.jsonl` | +25/-0 | the table carrier |
| `apps/cli/command_catalog.py` | +0/-55 | the `review` group and its four commands go |
| `apps/cli/commands/__init__.py` | +1/-2 | the handler module leaves import and dispatch tuple |
| `apps/cli/commands/dev.py` | +0/-1 | the `remedy review run` line leaves `dev status` |
| `apps/cli/commands/review_cmd.py` | +0/-181 | the deleted handler |
| `packages/orchestration/ui_view_model.py` | +1/-1 | the next-action command re-pointed at `remedy job show --full --json` |
| `scripts/remedy_smoke.sh` | +2/-62 | section 12ap deleted; the section 0 loop loses `review` and the five stale words |
| `docs/system/orchestrator-loop.md` | +6/-2 | the heir paragraph replaces the command |
| `docs/system/core-product-spine-v0.md` | +2/-2 | two references re-pointed |
| `docs/guides/simple-operator-quickstart-v0.md` | +2/-2 | reference re-pointed |
| `tests/cli/test_job_commands.py` | +0/-25 | a test of the deleted command |
| `tests/cli/test_review_cmd.py` | +0/-78 | tests of the deleted handler |
| `tests/orchestration/import_reachability_allowlist.txt` | +0/-1 | the handler leaves the allowlist |
| `tests/test_cli_execution_loop_closure.py` | +3/-121 | the reviewer CLI closure class goes with its command |
| `tests/test_command_catalog.py` | +4/-0 | the four deleted ids join `TestDeletedCommands` |
| `tests/test_data_paths.py` | +0/-4 | the routed-handler row of the deleted module |
| **Commit total** | **+46/-537** | constraint 5 reading: 46 insertions |

C5 writes this file and is not tabled here (R-0149 self-reference pattern, item 31 of §3).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this handback, then the push |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r18w/wt 72a57e38` | created for G5; `git worktree list` read two rows while it existed |
| `git worktree remove --force .remedy-wt/f261r18w/wt` | removed; `git worktree list` back to one row |
| `git push origin feature/f261-cli-vocabulary-v2` | pushed at C5 |

No pull request was created, none merged, nothing force-pushed, no branch deleted, no `remedy`
command run, and no runner or `run_job` invoked: `git branch --list 'remedy/job-*'` reads 16 lines
at the end of the round, as it did at `43694261`.

## Verification

**G1 TRANSPORT — exit 0.** `.agent/authored/f261-r18.md` at C0a has sha256
`9258ed4be5ca4f83ecd64f6ff4f94bd4ba0460045c765dabda92ce85415554ad`, equal to the digest the
delegating message gives; `.agent/last_block.md` at C0b is byte-identical to it (same sha256).
22 slices FOUND, each matching its BEGIN-marker sha256. Each committed carrier's sha256 equals
its block digest: context `d8ed7b75…c6e0`, token `330f8563…c23e`, review `07403106…b377`.

**G2 THE RECORD at C1 — exit 0**, every reading as the block states it.

| Reading | Base `43694261` | C1 `9d28c213` |
|---|---|---|
| `.agent/plan.md` byte-identical to PLAN18 | — | yes, 37 lines (cap 50) |
| `^## Goal$` / `^## Next Steps$` in plan.md | — | 1 / 1 |
| `.agent/live_review.md` == base blob + RECORD18 | 1044634 B | 1054600 B, equal |
| `.agent/decisions.md` == base blob + DEC17 | 1397236 B | 1400955 B, equal |
| `.agent/prose_slips.md` == base blob + SLIP18 | 309225 B | 309760 B, equal |
| `T2_F273.md` == base blob with pair P273 applied | — | equal |
| P273-FROM occurrences | 1 | 0 |
| P273-TO occurrences | 0 | 1 |
| `^Gate: F\d+ R\d+ — ` | 126 | 127 |
| `Gate: F261 R17 — ` | — | 1 |
| distinct `^- R-\d+ — ` ids | 110 | 113 |
| C1 minus base | — | exactly `R-0908`, `R-0909`, `R-0910` |
| distinct `^Done: R-\d+ — ` ids | 8 | 8 |
| open set by distinct id | 102 | 105 |

`python3 -m pytest tests/docs/ -q` at C1: **exit 0**, `310 passed in 1.06s`.

**G3 THE TABLES at C2, C3, C4 — exit 0.** `git diff --no-renames --name-only` from each parent
printed exactly that commit's carrier plus the paths the block names — C2 19 paths, C3 11, C4 16,
each set equal to the block's list with no path over and none missing. Every
`git rev-parse <commit>:<object>` equalled the reviewer's dry run:

| Object | C2 | C3 | C4 |
|---|---|---|---|
| `apps` | `de7e75f6…` | `fcfb42a7…` | `fcec307e…` |
| `tests` | `7222a99c…` | `2d162d7a…` | `bbd5299e…` |
| `docs` | `31e2b724…` | `d244ee09…` | `e2bf8ac0…` |
| `scripts` | `6314b0d7…` | `6314b0d7…` | `208d836b…` |
| `packages` | `2365aad4…` | `0a778e16…` | `bdd606d3…` |
| `README.md` | `15b9e0e8…` | `15b9e0e8…` | `15b9e0e8…` |

All 18 subtree ids reproduced the dry run exactly. Insertions per constraint 5: C2 63, C3 47,
C4 46 — every commit of the round under 500.

Table application: the context table's 28 rows, the token table's 17 and the review table's 25
each applied strictly in file order, and **every `edit` row's occurrence count read exactly the
count the row states (1 in all 70 rows)**. No STOP was reached.

**G4 THE SWEEP at C4 — exit 0 overall.**

- `git grep -n -I -E '<the block's pattern>' 72a57e38 -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` → **exit 1, printed nothing.** Control at `43694261`: the same command **exit 0, 126 matching lines in 25 files**, so the pattern had real reach before this round.
- `python3 -m ruff check` over every `.py` path of C2 to C4 still existing at C4 — 16 files (23 touched, 7 deleted) → **exit 0, `All checks passed!`**.
- The `for grp in` list of section 0 of `scripts/remedy_smoke.sh` at C4 reads **15 words**: `job project patch test brain worker memory dev file change event blocker decision ui do`. Every one is a key of `GROUPS` in `apps/cli/command_catalog.py` at C4 (30 keys); **words that are not a key: 0**. At `43694261` the same reading over 22 words names **5 that are not**: `policy`, `readiness`, `repo`, `dashboard`, `guide` — the groups rounds 16 and 17 deleted. The `GROUPS` reading was cross-checked against the live import at C4 (equal, 30 keys).

**G5 THE RED-PROOF — exit 0.** In `git worktree add --detach .remedy-wt/f261r18w/wt 72a57e38`,
each run through the runner, which changes into the worktree, puts it first on `sys.path` and in
`PYTHONPATH` and asserts the provenance: every run printed
`LOADED_FROM /home/decodeux/Repos/remedy/.remedy-wt/f261r18w/wt/apps/cli/grouped.py` and
`PROVENANCE_OK`, with pytest `rootdir` the worktree. Each mutation's FROM slice read count 1 in
its file before replacement and was restored with `git -C … checkout -- <file>`.

| # | File | Exit | Summary | Failed nodes | Named node among them |
|---|---|---|---|---|---|
| (a) CONTROL | — | **0** | `537 passed in 22.98s` | 0 | — |
| (1) | `apps/cli/commands/dev.py` (`context` handler row) | **1** | `1 failed, 536 passed` | 1 | yes — `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| (2) | `apps/cli/commands/dev.py` (`token` handler row) | **1** | `1 failed, 536 passed` | 1 | yes — same node |
| (3) | `apps/cli/commands/dev.py` (`review` handler row) | **1** | `1 failed, 536 passed` | 1 | yes — same node |
| (4) | `apps/cli/command_catalog.py` (`token` group, no commands) | **1** | `1 failed, 544 passed` | 1 | yes — `TestCatalogIntegrity::test_every_group_has_at_least_one_command` |
| (5) | `apps/cli/command_catalog.py` (`related=` names `review.list`) | **1** | `1 failed, 536 passed` | 1 | yes — `TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command` |
| (6) | `packages/orchestration/ui_view_model.py` (`review list` in the view model) | **1** | `1 failed, 536 passed` | 1 | yes — `test_every_advertised_command_exists_in_the_catalog` |
| (7) | `tests/cli/test_cli_ux.py` (`token`, `context-pack` internal again) | **1** | `3 failed, 534 passed` | 3 | yes — `TestGroupDefIntegrity::test_internal_groups_marked`, beside `TestAdvancedHelp::test_all_commands_shows_internal` and `TestHiddenCallable::test_hidden_group_callable` |
| (8) PROBE | `scripts/remedy_smoke.sh` (`policy` back in the section 0 loop) | **0** | `537 passed in 23.02s` | 0 | — |

(8) is the probe, not a colour, and neither colour is a STOP. Its reading is **green**: putting
`policy`, a group this branch deleted, back into the section 0 loop leaves the whole six-file
selection at 537 passed, exit 0. That is direct evidence for **R-0910** — no guard reads that
list, so a stale group word in it cannot redden a test.

After G5: `git worktree remove --force .remedy-wt/f261r18w/wt` (the worktree was clean before
removal — every mutation restored), `git worktree list` one row, `git branch --list 'remedy/job-*'`
**16 lines**.

**G6 THE SUITE, SPEC S at C4 — exit 0.** From the primary checkout's root, serially,
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs` with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, transcript at
`.remedy-wt/f261r18w/spec_s_full.txt`.

- return code **0**
- last output line: `17773 passed, 23 skipped, 1 warning in 1296.87s (0:21:36)`
- distinct bad nodes: **0** — no line-initial `FAILED ` or `ERROR ` in the output, so no lone
  re-run was owed.

**G7 THE TREE** runs after this commit and the push and is reported in the round's completion
message only, per the block.

## Authored-text proofs

| Authored file | Proof |
|---|---|
| `.agent/authored/f261-r18.md` | sha256 at C0a equals the delegating message's digest, `9258ed4be5ca4f83ecd64f6ff4f94bd4ba0460045c765dabda92ce85415554ad` |
| `.agent/last_block.md` | byte-identical to the committed C0a file (same sha256) |
| `.agent/authored/f261-r18-context.jsonl` | committed sha256 `d8ed7b75a5b2288ffe882beedab6fbb7ab067990d6db406938cc5c4ec3b7c6e0`, equal to the block's digest |
| `.agent/authored/f261-r18-token.jsonl` | committed sha256 `330f85636d66cc569fe46dc51833b0bf0a73b3ab68fc365a1fbcb5eba78c23ee`, equal to the block's digest |
| `.agent/authored/f261-r18-review.jsonl` | committed sha256 `07403106a52d0239b43eca5da42163ba0e0e155df90cbc680b293d5dd13b377a`, equal to the block's digest |
| Slices PLAN18, RECORD18, DEC17, SLIP18, P273-FROM/TO, MUT-1…8-FROM/TO | all 22 extracted strictly between their BEGIN and END lines; each sha256 matched its BEGIN marker; none was edited |

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5 landed
   in that order, one commit each, single-parent, on `43694261`. No extra commit, none dropped,
   no reordering.
2. **Two gate readings were first taken through a pipe that hides the exit code, and both were
   re-run unpiped before being recorded.** The G2 docs run was first invoked as
   `… | tail -5` and the G4 sweep was first invoked with a trailing `; true`; the block's
   ENVIRONMENT paragraph warns of exactly the first of these. Every exit code reported above comes
   from the unpiped re-run (the docs suite through a file redirect, the sweep through
   `subprocess.run`), never from the piped invocation. No reading changed.
3. **The block's declared PROSE count reproduces only under the marker-inclusive reading, and
   this is not a defect.** Measured on the committed final bytes, the block is **370 lines TOTAL**,
   exactly as constraint 7 declares, against the cap of 490. Its declared **271 lines of PROSE**
   reproduces exactly when the 44 `BEGIN`/`END` marker lines count as prose (370 − 99 slice-body
   lines = 271); under the stricter reading that also excludes the markers it is 227. Both
   readings are under the cap of 400, so nothing is violated either way. Recorded here rather than
   as a finding, per amend0827-process-diet rule 2.
4. **The frame rule of item 37 holds on the final bytes**: no line of two or more characters is a
   run of a single repeated character (0 such lines), and every box-drawing rule inside the STEP
   and SLICE header lines is exactly two characters long (0 exceptions).
5. **Scratch discipline.** All scratch, the runner and the G5 worktree lived under
   `.remedy-wt/f261r18w/`, uncommitted; no `.py` file was written under `.agent/`; no script was
   named after a standard-library module; no symlink was created; only
   `.remedy-wt/f261-block/` and `.remedy-wt/f261r18w/` were opened under `.remedy-wt/`.
6. **No STOP was encountered.** `.agent/STOP` was read before C0a, before C2 and before C5; all
   three reads exited 2, "No such file or directory".
7. **No table reached a STOP**: all 70 rows across the three carriers applied, and every `edit`
   row's occurrence count matched the count it states.

## Next

Open findings: **105 by distinct id**, of which three are High — **R-0803**, **R-0804** and
**R-0807**. `Operator questions open: 0` (`.agent/operator_questions.md` reads
`EMPTY — nothing is waiting on the operator.`).

The single expected next action, in order:

1. **Phase 1 rule 1** of `docs/agents/self_drive_protocol.md` — read `.agent/STOP` from disk; if
   it exists, write the handoff and end the session before anything else.
2. **The reviewer's verdict on round 18**, over the committed range `43694261`..C5, booked into
   `.agent/live_review.md` by the first commit of round 19.
3. **Round 19's work**: `do report` becomes `run show` and `run list`, and `do evidence` goes, as
   `.agent/f261_t003_inventory.md` proposes in its round F.
