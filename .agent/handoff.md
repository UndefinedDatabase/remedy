# Handback — F261 CLI vocabulary v2, round 19

## Session

SESSION 4 of feature F261 · round 19 · rounds so far 19

Context self-assessment: comfortable — the round read the block, AGENTS.md, the protocol, the
T003 inventory and the handback template once each, applied two tables and ran seven gates
including a full serial suite without re-reading anything, and a further round of the same shape
would fit with room to spare.

## Range

Review of `ac87bcc4`..`HEAD`, where `HEAD` is C4 — the commit that writes this file, which it
cannot name from inside itself (R-0149 self-reference pattern).

## Commits

### 3d6f7bcf F261 R19 C0a: save the round 19 step block under the authored directory

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r19.md` | +396/-0 | the block file the delegating message names, copied by `shutil.copyfile` |
| **Commit total** | **+396/-0** | constraint 5 reading: 396 insertions |

### 690710d3 F261 R19 C0b: mirror the round 19 step block into the last block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +206/-180 | the same bytes, byte-identical to C0a's file |
| **Commit total** | **+206/-180** | constraint 5 reading: 206 insertions |

### 4ba46a24 F261 R19 C1: re-point the plan at round 19, book round 18's PASS and its prose slip, register R-0911 and R-0912 for F273 and record DECISION F261 D18

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +11/-12 | full replacement by slice PLAN19 |
| `.agent/live_review.md` | +6/-0 | slice RECORD19 appended: the round 18 PASS, R-0911, R-0912 |
| `.agent/decisions.md` | +10/-0 | slice DEC18 appended: DECISION F261 D18 |
| `.agent/prose_slips.md` | +2/-0 | slice SLIP19 appended: the round 18 PROSE-count wording slip |
| `docs/roadmap/features/T2_F273.md` | +4/-0 | pair P273 applied: acceptance lines for R-0911 and R-0912 |
| **Commit total** | **+33/-12** | constraint 5 reading: 33 insertions |

### 747d0a19 F261 R19 C2: rename the do report command into the new run group as `run show` and `run list`, re-pointing every hint that named the old word, by the run table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r19-run.jsonl` | +28/-0 | the table carrier |
| `README.md` | +1/-1 | the quickstart fence names `remedy run show` |
| `apps/cli/command_catalog.py` | +22/-5 | the `run` group after `job`; `do.report` becomes `run.show`; `run.list` added; `do.evidence` `related=` re-pointed |
| `apps/cli/commands/do_cmd.py` | +54/-18 | `_cmd_do_report` becomes `_cmd_run_show` and `_cmd_run_list`; two dispatch rows |
| `apps/cli/grouped.py` | +1/-1 | step 3 of the quick start re-pointed |
| `packages/orchestration/pingpong_loop.py` | +7/-7 | the next-commands keys and shell flow, the `do run --json` payload keys, the summary `Report:` line |
| `tests/cli/test_cli_ux.py` | +89/-11 | five `_cmd_run_show` call sites; `TestRunList` and `TestRunShow`; the two new group guards |
| `tests/cli/test_product_spine.py` | +2/-2 | the re-pointed hint |
| `tests/cli/test_task_input.py` | +4/-4 | the re-pointed hints |
| `tests/orchestration/test_pingpong_cli.py` | +6/-6 | the re-pointed hints |
| `tests/test_cli_execution_loop_closure.py` | +1/-1 | the re-pointed hint |
| `tests/test_command_catalog.py` | +2/-0 | `do.report` to `run.show` and `run.list` in `TestRenamedCommands` |
| **Commit total** | **+217/-56** | constraint 5 reading: 217 insertions |

### 146f97a9 F261 R19 C3: delete the do evidence command, its handler and its dispatch tests, re-pointing the redaction regression at the surviving exporter, by the evidence table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r19-evidence.jsonl` | +8/-0 | the table carrier |
| `apps/cli/command_catalog.py` | +0/-17 | the `do.evidence` catalog entry |
| `apps/cli/commands/do_cmd.py` | +0/-35 | `_cmd_do_evidence` and its dispatch row |
| `tests/orchestration/test_evidence_bundle.py` | +6/-33 | `TestCliDispatch` deleted; the stdout-worded redaction test renamed to what it reads |
| `tests/test_command_catalog.py` | +1/-0 | `do.evidence` joins `TestDeletedCommands` |
| **Commit total** | **+15/-85** | constraint 5 reading: 15 insertions |

### Item status — the block's ordered bundle

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit; its own numbers appear nowhere, per item 31 of §3 |

## External actions

- `git push origin feature/f261-cli-vocabulary-v2` — run after this commit; its result is in the
  round's completion message with G7.
- `git worktree add --detach .remedy-wt/f261r19w/wt 146f97a9` — created for G5, then
  `git worktree remove --force .remedy-wt/f261r19w/wt` — removed, `git worktree list` one row.
- No `gh` command, no pull request created or edited, no merge, no force-push, no branch deleted.
- No `remedy` command run, and no runner or `run_job` invoked: `git branch --list 'remedy/job-*'`
  reads 16 lines at the end of the round, as it did at `ac87bcc4`.

## Verification

**G1 TRANSPORT — exit 0.** `.agent/authored/f261-r19.md` at C0a has sha256
`05bbae28083528a53f95defd8aa4db6d68f519e20c1fc67c5449c01ef8641560`, equal to the digest the
delegating message gives; `.agent/last_block.md` at C0b is byte-identical to it (same sha256).
22 slices FOUND, each matching its BEGIN-marker sha256. Each committed carrier's sha256 equals
its block digest: run `0e6d26ec…8cd2`, evidence `af19a558…e68f`.

**G2 THE RECORD at C1 — exit 0**, every reading as the block states it.

| Reading | Base `ac87bcc4` | C1 `4ba46a24` |
|---|---|---|
| `.agent/plan.md` byte-identical to PLAN19 | — | yes, 36 lines (cap 50) |
| `^## Goal$` / `^## Next Steps$` in plan.md | — | 1 / 1 |
| `.agent/live_review.md` == base blob + RECORD19 | 1050615 B | 1058070 B, equal |
| `.agent/decisions.md` == base blob + DEC18 | 1395584 B | 1398797 B, equal |
| `.agent/prose_slips.md` == base blob + SLIP19 | 307900 B | 308405 B, equal |
| `T2_F273.md` == base blob with pair P273 applied | — | equal |
| P273-FROM occurrences | 1 | 0 |
| P273-TO occurrences | 0 | 1 |
| `^Gate: F\d+ R\d+ — ` | 127 | 128 |
| `Gate: F261 R18 — ` | — | 1 |
| distinct `^- R-\d+ — ` ids | 113 | 115 |
| C1 minus base | — | exactly `R-0911`, `R-0912` |
| distinct `^Done: R-\d+ — ` ids | 8 | 8 |
| open set by distinct id | 105 | 107 |

`python3 -m pytest tests/docs/ -q` at C1: **exit 0**, `310 passed in 1.06s`.

**G3 THE TABLES at C2 and C3 — exit 0.** `git diff --no-renames --name-only` from each parent
printed exactly that commit's carrier plus the paths the block names — C2 12 paths, C3 5 — each
set equal to the block's list with no path over and none missing. Every
`git rev-parse <commit>:<object>` equalled the reviewer's dry run:

| Object | C2 `747d0a19` | C3 `146f97a9` |
|---|---|---|
| `apps` | `5b305ea8…` | `e3cf5879…` |
| `tests` | `aec26723…` | `d51c09d1…` |
| `docs` | `07f12816…` | `07f12816…` |
| `scripts` | `208d836b…` | `208d836b…` |
| `packages` | `6bf22116…` | `6bf22116…` |
| `README.md` | `666769d2…` | `666769d2…` |

All 12 subtree ids reproduced the dry run exactly. Insertions per constraint 5: C2 217, C3 15 —
every commit of the round under 500.

Table application: the run table's 28 rows and the evidence table's 8 each applied strictly in
file order, and **every `edit` row's occurrence count read exactly the count the row states** —
1 in 34 rows, 5 in one row and 2 in one row, all 36 exact. No STOP was reached.

**G4 THE SWEEP at C3 — exit 0 overall.**

- `git grep -n -I -E 'remedy do report|_cmd_do_report|_cmd_do_evidence' 146f97a9 -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` → **exit 1, printed nothing** (stdout `''`). Control at `ac87bcc4`: the same command **exit 0, 28 matching lines in 7 files** — `README.md`, `apps/cli/commands/do_cmd.py`, `apps/cli/grouped.py`, `packages/orchestration/pingpong_loop.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_task_input.py`, `tests/orchestration/test_pingpong_cli.py` — so the pattern had real reach before this round, and the block's expected file count of 7 reproduced exactly.
- `python3 -m ruff check` over every `.py` path of C2 and C3 still existing at C3 — 11 files, none deleted this round → **exit 0, `All checks passed!`**.

**G5 THE RED-PROOF — exit 0.** In `git worktree add --detach .remedy-wt/f261r19w/wt 146f97a9`,
each run through the runner, which purges every `__pycache__`, changes into the worktree, puts it
first on `sys.path` and in `PYTHONPATH` and asserts the provenance: every run printed
`apps.cli.grouped -> /home/decodeux/Repos/remedy/.remedy-wt/f261r19w/wt/apps/cli/grouped.py`
before a single test ran, so the editable install's resolution to the primary checkout was ruled
out each time. Each mutation's FROM slice read **count 1** in its file before replacement and was
restored with `git -C … checkout -- <file>`; `git status --porcelain` in the worktree read empty
after every restore.

| # | File and mutation | Exit | Summary | Bad nodes | Named node among them |
|---|---|---|---|---|---|
| (a) CONTROL | — | **0** | `395 passed in 23.46s` | 0 | — |
| (1) | `apps/cli/command_catalog.py`, the `run` group removed | **1** | `4 failed, 383 passed in 22.57s` | 4 | yes — `TestGroupDefIntegrity::test_all_groups_still_in_catalog` |
| (2) | `apps/cli/command_catalog.py`, `run.show` removed, handler row kept | **1** | `3 failed, 392 passed in 23.38s` | 3 | yes — `TestGroupDefIntegrity::test_run_group_holds_exactly_show_and_list` |
| (3) | `apps/cli/commands/do_cmd.py`, `run.show`'s handler row removed, catalog entry kept | **1** | `2 failed, 393 passed in 23.41s` | 2 | yes — `TestGroupDefIntegrity::test_run_commands_have_handlers` |
| (4) | `packages/orchestration/pingpong_loop.py`, the old `do report` hint restored | **1** | `1 failed, 394 passed in 23.41s` | 1 | yes — `test_every_advertised_command_exists_in_the_catalog` |
| (5) | `apps/cli/command_catalog.py`, `do.report` put back | **1** | `1 failed, 394 passed in 23.29s` | 1 | yes — `TestRenamedCommands::test_no_old_id_is_left_in_the_catalog` |
| (6) | `apps/cli/command_catalog.py`, `do.evidence` put back | **1** | `1 failed, 394 passed in 23.42s` | 1 | yes — `TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` |
| (7) | `apps/cli/commands/do_cmd.py`, `run list --json` printing other bytes | **1** | `1 failed, 394 passed in 23.36s` | 1 | yes — `TestRunList::test_no_flag_prints_list_runs_verbatim` |
| (8) | `apps/cli/commands/do_cmd.py`, `run list` dropping the catalog's `--limit` | **1** | `1 failed, 394 passed in 23.40s` | 1 | yes — `TestRunList::test_limit_flag_is_honoured` |

Every one of (1) to (8) exited 1 with the named node among the failed nodes, and the CONTROL
exited 0, so each of the eight guards is reachable and discriminating. Mutations (7) and (8)
are the ones that matter for the ONE DECLARED DIFFERENCE of DECISION F261 D18: they show the
five list options are implemented rather than decorative — changing the no-flag payload reddens
the verbatim guard, and ignoring `--limit` reddens the limit guard.

After G5: `git worktree remove --force .remedy-wt/f261r19w/wt` (the worktree was clean before
removal — every mutation restored), `git worktree list` one row, `git branch --list 'remedy/job-*'`
**16 lines**.

**G6 THE SUITE, SPEC S at C3 — exit 0.** From the primary checkout's root, serially,
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs` with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, transcript at
`.remedy-wt/f261r19w/spec_s_full.txt`.

- return code **0**
- last output line: `17785 passed, 23 skipped, 1 warning in 1309.12s (0:21:49)`
- distinct bad nodes: **0** — no line-initial `FAILED ` or `ERROR ` in the output, so no lone
  re-run was owed.

**G7 THE TREE** runs after this commit and the push and is reported in the round's completion
message only, per the block.

## Authored-text proofs

| Authored file | Proof |
|---|---|
| `.agent/authored/f261-r19.md` | sha256 at C0a equals the delegating message's digest, `05bbae28083528a53f95defd8aa4db6d68f519e20c1fc67c5449c01ef8641560` |
| `.agent/last_block.md` | byte-identical to the committed C0a file (same sha256) |
| `.agent/authored/f261-r19-run.jsonl` | committed sha256 `0e6d26ecb22e8429982cacbf26409d1152be18f3437e08e2c5b9c53914368cd2`, equal to the block's digest |
| `.agent/authored/f261-r19-evidence.jsonl` | committed sha256 `af19a5585abbe883e6a683756967d76cd427db08475ab860fd5362477cc2e68f`, equal to the block's digest |
| Slices PLAN19, RECORD19, DEC18, SLIP19, P273-FROM/TO, MUT-1…8-FROM/TO | all 22 extracted strictly between their BEGIN and END lines; each sha256 matched its BEGIN marker; none was edited |

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3, C4 landed in
   that order, one commit each, single-parent, on `ac87bcc4`. No extra commit, none dropped, no
   reordering.
2. **Each table was applied through an in-memory overlay and flushed only after every row had
   succeeded.** The block's STOP clause requires that a count mismatch "touch nothing further";
   applying row by row directly to the tree would already have written the rows before the
   failing one. The overlay is seeded from the tree and each row reads the overlay, so the
   semantics of "each against the tree as the previous rows left it" are unchanged — only the
   moment of writing moves. No row failed in either table, so the two routes would have produced
   identical trees, and G3's twelve subtree ids confirm the result byte for byte.
3. **The G5 runner removes `REMEDY_PROJECT` and `REMEDY_DATA_DIR` from the environment.** The
   block specifies that hygiene for SPEC S and not for G5; neither variable was set in this
   session, so the removal was a no-op in fact and is declared only because the runner does it
   unconditionally. It also sets `PYTHONDONTWRITEBYTECODE=1` and runs `python3 -B`.
4. **The block's own size reproduces exactly, and so does its frame rule.** Measured on the
   committed final bytes of `.agent/authored/f261-r19.md`: **396 lines TOTAL** against the cap of
   490 and **262 lines of PROSE** against the cap of 400, where PROSE is every line that is not a
   line of slice content and the 44 `BEGIN`/`END` marker lines count as prose — both exactly the
   numerals constraint 7 declares. This is the reading SLIP19 makes binding, and it now
   reproduces without a declared difference. The frame rule of item 37 also holds: **0** lines of
   two or more characters are a run of a single repeated character, and across the 23 header
   lines carrying box-drawing rules there are **0** rules that are not exactly two characters long.
5. **Two readings were first taken through a pipe that hides the exit code, and both were re-run
   unpiped before being recorded.** The G2 docs run was first invoked as `… | tail -15`; the
   block's ENVIRONMENT paragraph warns of exactly that. Every exit code reported above comes from
   an unpiped `subprocess.run`, never from a piped invocation. No reading changed.
6. **Scratch discipline.** All scratch, the runner and the G5 worktree lived under
   `.remedy-wt/f261r19w/`, uncommitted; no `.py` file was written under `.agent/`; no script was
   named after a standard-library module; no symlink was created; only
   `.remedy-wt/f261-block/` and `.remedy-wt/f261r19w/` were opened under `.remedy-wt/`.
7. **No STOP was encountered.** `.agent/STOP` was read before C0a, before C2 and before C4; all
   three reads exited 2, "No such file or directory".
8. **No table reached a STOP**: all 36 rows across the two carriers applied, and every `edit`
   row's occurrence count matched the count it states.
9. **`export_evidence` survives the deletion of `do evidence`.** This is DECISION F261 D18's
   chosen second as written, not a scope decision taken here: eight test classes drive the
   surviving bundle builder and the redaction helper through it, and R-0911 carries both the lost
   export and that function's state to F273.

## Next

Open findings: **107 by distinct id**, of which three are High — **R-0803**, **R-0804** and
**R-0807**. `Operator questions open: 0` (`.agent/operator_questions.md` reads
`EMPTY — nothing is waiting on the operator.`).

The single expected next action, in order:

1. **Phase 1 rule 1** of `docs/agents/self_drive_protocol.md` — read `.agent/STOP` from disk; if
   it exists, write the handoff and end the session before anything else.
2. **The reviewer's verdict on round 19**, over the committed range `ac87bcc4`..C4, booked into
   `.agent/live_review.md` by the first commit of round 20.
3. **Round 20's work**: `do repair-attest`, `do job-resume` and `do replan`, as
   `.agent/f261_t003_inventory.md` proposes in its round G.
