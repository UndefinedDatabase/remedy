# Handback — F261 CLI vocabulary v2, round 20

## Session

SESSION 4 of feature F261 · round 20 · rounds so far 20

Context self-assessment: comfortable — the round read the block, AGENTS.md, the protocol, the
T003 inventory and the handback template once each, applied three tables and ran seven gates
including a full serial suite without re-reading anything, and a further round of the same shape
would fit with room to spare.

## Range

Review of `71cba20e`..`HEAD`, where `HEAD` is C5 — the commit that writes this file, which it
cannot name from inside itself (R-0149 self-reference pattern).

## Commits

### 6e3405ba F261 R20 C0a: save the round 20 step block as the authored original

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r20.md` | +322/-0 | the block file the delegating message names, copied by `shutil.copyfile` |
| **Commit total** | **+322/-0** | constraint 5 reading: 322 insertions |

### 00bef4fc F261 R20 C0b: mirror the round 20 step block into the last block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +143/-217 | the same bytes, byte-identical to C0a's file |
| **Commit total** | **+143/-217** | constraint 5 reading: 143 insertions |

### 893a9a95 F261 R20 C1: re-point the plan at round 20, book round 19's PASS, register R-0913, R-0914 and R-0915 for F273 and record DECISION F261 D19

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +11/-11 | full replacement by slice PLAN20 |
| `.agent/live_review.md` | +8/-0 | slice RECORD20 appended: the round 19 PASS, R-0913, R-0914, R-0915 |
| `.agent/decisions.md` | +12/-0 | slice DEC19 appended: DECISION F261 D19 |
| `docs/roadmap/features/T2_F273.md` | +9/-0 | pair P273 applied: acceptance lines for R-0913, R-0914 and R-0915 |
| **Commit total** | **+40/-11** | constraint 5 reading: 40 insertions |

### c26c3a1a F261 R20 C2: delete the do repair-attest command, its handler and collect_diff_stat with that function's tests, by the repair-attest table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r20-repair-attest.jsonl` | +6/-0 | the table carrier |
| `apps/cli/command_catalog.py` | +0/-23 | the `do.repair-attest` catalog entry |
| `apps/cli/commands/do_cmd.py` | +0/-67 | `_cmd_do_repair_attest` and its dispatch row |
| `packages/orchestration/repair_attest.py` | +0/-29 | `collect_diff_stat`, whose only production caller was that handler |
| `tests/orchestration/test_repair_attest.py` | +0/-75 | the CLI dispatch tests and `collect_diff_stat`'s own tests |
| `tests/test_command_catalog.py` | +1/-0 | `do.repair-attest` joins `TestDeletedCommands` |
| **Commit total** | **+7/-194** | constraint 5 reading: 7 insertions |

### f6c723b8 F261 R20 C3: delete the do job-resume command and its handler, re-pointing the invocation prose and the test sites that drove the CLI, by the job-resume table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r20-job-resume.jsonl` | +9/-0 | the table carrier |
| `apps/cli/command_catalog.py` | +0/-26 | the `do.job-resume` catalog entry |
| `apps/cli/commands/do_cmd.py` | +0/-66 | `_cmd_do_job_resume` and its dispatch row |
| `apps/cli/commands/run_invocation.py` | +2/-2 | the module docstring now names `job run` alone as the lifecycle caller |
| `tests/cli/test_job_run_invocation_truth.py` | +2/-14 | the deleted command's invocation cases |
| `tests/cli/test_stream_evidence_tristate.py` | +0/-1 | the deleted command's tristate case |
| `tests/orchestration/test_job_worktree_handoff.py` | +7/-10 | the handoff cases re-pointed off the CLI word |
| `tests/test_command_catalog.py` | +1/-0 | `do.job-resume` joins `TestDeletedCommands` |
| **Commit total** | **+21/-119** | constraint 5 reading: 21 insertions |

### bab42400 F261 R20 C4: delete the do replan command and its handler, rewriting the six rejections that named it to name no command, by the replan table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r20-replan.jsonl` | +12/-0 | the table carrier |
| `apps/cli/command_catalog.py` | +0/-15 | the `do.replan` catalog entry |
| `apps/cli/commands/decision.py` | +1/-3 | two of the six rejections rewritten to name no command |
| `apps/cli/commands/do_cmd.py` | +0/-110 | `_cmd_do_replan` and its dispatch row |
| `apps/cli/commands/job.py` | +4/-7 | the other four rejections rewritten to name no command |
| `tests/cli/test_plan_approval.py` | +1/-1 | the rejection text the approval path pins |
| `tests/orchestration/test_prompt_trace.py` | +0/-10 | the replan prompt-trace case |
| `tests/orchestration/test_stream_evidence_integration.py` | +1/-1 | the rejection text the integration path pins |
| `tests/test_command_catalog.py` | +1/-0 | `do.replan` joins `TestDeletedCommands` |
| **Commit total** | **+20/-147** | constraint 5 reading: 20 insertions |

### Item status — the block's ordered bundle

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit; its own numbers appear nowhere, per item 31 of §3 |

## External actions

- `git push origin feature/f261-cli-vocabulary-v2` — run after this commit; its result is in the
  round's completion message with G7.
- `git worktree add --detach .remedy-wt/f261r20w/wt bab42400` — created for G5, then
  `git worktree remove --force .remedy-wt/f261r20w/wt` — removed, `git worktree list` one row.
- No `gh` command, no pull request created or edited, no merge, no force-push, no branch deleted.
- No `remedy` command run, and no runner or `run_job` invoked: `git branch --list 'remedy/job-*'`
  reads 16 lines at the end of the round, as it did at `71cba20e`.

## Verification

**G1 TRANSPORT — exit 0.** `.agent/authored/f261-r20.md` at C0a has sha256
`713761a2d0a064666e021dd54249fec39e325d8b352760977530016ee5bb9085`, equal to the digest the
delegating message gives; `.agent/last_block.md` at C0b is byte-identical to it (same sha256,
33873 bytes). 15 slices FOUND, each matching its BEGIN-marker sha256. Each committed carrier's
sha256 equals its block digest: repair-attest `6595ebb1…fe73`, job-resume `1de11fee…4eb4`,
replan `8982ac33…9d33`.

**G2 THE RECORD at C1 — exit 0**, every reading as the block states it.

| Reading | Base `71cba20e` | C1 `893a9a95` |
|---|---|---|
| `.agent/plan.md` byte-identical to PLAN20 | — | yes, 36 lines (cap 50) |
| `^## Goal$` / `^## Next Steps$` in plan.md | — | 1 / 1 |
| `.agent/live_review.md` == base blob + RECORD20 | 1062069 B | equal |
| `.agent/decisions.md` == base blob + DEC19 | 1404174 B | equal |
| `T2_F273.md` == base blob with pair P273 applied | — | equal |
| P273-FROM occurrences | 1 | 0 |
| P273-TO occurrences | 0 | 1 |
| `^Gate: F\d+ R\d+ — ` | 128 | 129 |
| `Gate: F261 R19 — ` | — | 1 |
| distinct `^- R-\d+ — ` ids | 115 | 118 |
| C1 minus base | — | exactly `R-0913`, `R-0914`, `R-0915` |
| distinct `^Done: R-\d+ — ` ids | 8 | 8 |
| open set by distinct id | 107 | 110 |

`python3 -m pytest tests/docs/ -q` at C1: **exit 0**, `310 passed in 1.03s`.

**G3 THE TABLES at C2, C3 and C4 — exit 0.** `git diff --no-renames --name-only` from each
parent printed exactly that commit's carrier plus the paths the block names — C2 6 paths, C3 8,
C4 9 — each set equal to the block's list with no path over and none missing. Every
`git rev-parse <commit>:<object>` equalled the reviewer's dry run:

| Object | C2 `c26c3a1a` | C3 `f6c723b8` | C4 `bab42400` |
|---|---|---|---|
| `apps` | `7524164c…` | `00706e15…` | `6616756a…` |
| `tests` | `799e2d94…` | `bad1d8e1…` | `49127a5c…` |
| `docs` | `0122c102…` | `0122c102…` | `0122c102…` |
| `scripts` | `208d836b…` | `208d836b…` | `208d836b…` |
| `packages` | `c6d3df57…` | `c6d3df57…` | `c6d3df57…` |
| `README.md` | `666769d2…` | `666769d2…` | `666769d2…` |

All 18 subtree ids reproduced the dry run exactly. Insertions per constraint 5: C2 7, C3 21,
C4 20 — every commit of the round under 500.

Table application: the repair-attest table's 6 rows, the job-resume table's 9 and the replan
table's 12 each applied strictly in file order, and **every `edit` row's occurrence count read
exactly the count the row states** — 1 in 26 rows and 3 in one row, all 27 exact. No STOP was
reached.

**G4 THE SWEEP at C4 — exit 0 overall.**

- `git grep -n -I -E '(^|[^.])repair-attest|(^|[^.])job-resume|do replan|_cmd_do_repair_attest|_cmd_do_job_resume|_cmd_do_replan|collect_diff_stat' bab42400 -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` → **exit 1, printed nothing** (stdout `''`). Control at `71cba20e`: the same command **exit 0, 30 matching lines in 11 files** — `apps/cli/command_catalog.py`, `apps/cli/commands/decision.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/commands/job.py`, `apps/cli/commands/run_invocation.py`, `packages/orchestration/repair_attest.py`, `tests/cli/test_job_run_invocation_truth.py`, `tests/cli/test_plan_approval.py`, `tests/cli/test_stream_evidence_tristate.py`, `tests/orchestration/test_job_worktree_handoff.py`, `tests/orchestration/test_repair_attest.py` — so the pattern had real reach before this round, and the block's expected file count of 11 reproduced exactly.
- `python3 -m ruff check` over every `.py` path of C2 to C4 still existing at C4, except
  `tests/orchestration/test_prompt_trace.py` — 13 files, none deleted this round → **exit 0,
  `All checks passed!`**.
- The exception, reported with both readings rather than repaired: `python3 -m ruff check
  tests/orchestration/test_prompt_trace.py` → **exit 1, `Found 2 errors.`**, two `I001` "Import
  block is un-sorted or un-formatted" at the two in-function import blocks. The SAME file at
  `71cba20e`, checked out into the G5 worktree and linted there, reads **exit 1, `Found 2
  errors.`**, the same two `I001` at the same two import blocks — at lines 360 and 445 rather than
  350 and 435, the shift being exactly the 10 lines this round's table deleted above them. The
  findings are pre-existing and this round neither introduced nor moved them.

**G5 THE RED-PROOF — exit 0.** In `git worktree add --detach .remedy-wt/f261r20w/wt bab42400`,
each run through the runner, which purges every `__pycache__`, changes into the worktree, puts it
first on `sys.path` and in `PYTHONPATH` and asserts the provenance: every run printed
`apps.cli.grouped loaded from /home/decodeux/Repos/remedy/.remedy-wt/f261r20w/wt/apps/cli/grouped.py`
before a single test ran, so the editable install's resolution to the primary checkout was ruled
out each time. Each mutation's FROM slice read **count 1** in its file before replacement and was
restored with `git -C … checkout -- <file>`; `git status --porcelain` in the worktree read empty
after every restore.

| # | File and mutation | Exit | Summary | Bad nodes | Named node among them |
|---|---|---|---|---|---|
| (a) CONTROL | — | **0** | `395 passed in 23.13s` | 0 | — |
| (1) | `apps/cli/commands/do_cmd.py`, a `do.repair-attest` handler row | **1** | `1 failed, 394 passed in 23.21s` | 1 | yes — `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| (2) | the same file, a `do.job-resume` handler row | **1** | `1 failed, 394 passed in 23.14s` | 1 | yes — `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| (3) | the same file, a `do.replan` handler row | **1** | `1 failed, 394 passed in 23.17s` | 1 | yes — `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| (4) | `apps/cli/command_catalog.py`, a `related=` naming `do.job-resume` | **1** | `1 failed, 394 passed in 23.15s` | 1 | yes — `TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command` |
| (5) | `apps/cli/commands/decision.py`, the `do replan` line restored after the rejection | **1** | `1 failed, 394 passed in 23.09s` | 1 | yes — `test_every_advertised_command_exists_in_the_catalog` |

Every one of (1) to (5) exited 1 with the named node among the failed nodes, and the CONTROL
exited 0, so each of the three guards is reachable and discriminating. (1) to (3) show the
dispatch-table guard discriminates per deleted id rather than firing on any one of them; (4)
shows a `related=` chain pointing at a deleted word is caught; (5) shows an advertised hint
naming a deleted word is caught — the three failure modes these three deletions could leave.

After G5: `git worktree remove --force .remedy-wt/f261r20w/wt` (the worktree was clean before
removal — every mutation restored), `git worktree list` one row, `git branch --list 'remedy/job-*'`
**16 lines**.

**G6 THE SUITE, SPEC S at C4 — exit 0.** From the primary checkout's root, serially,
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs` with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, transcript at
`.remedy-wt/f261r20w/suite_out.txt`.

- return code **0**
- last output line: `17772 passed, 23 skipped, 1 warning in 1300.41s (0:21:40)`
- distinct bad nodes: **0** — no line-initial `FAILED ` or `ERROR ` in the output, so no lone
  re-run was owed.

**G7 THE TREE** runs after this commit and the push and is reported in the round's completion
message only, per the block.

## Authored-text proofs

| Authored file | Proof |
|---|---|
| `.agent/authored/f261-r20.md` | sha256 at C0a equals the delegating message's digest, `713761a2d0a064666e021dd54249fec39e325d8b352760977530016ee5bb9085` |
| `.agent/last_block.md` | byte-identical to the committed C0a file (same sha256) |
| `.agent/authored/f261-r20-repair-attest.jsonl` | committed sha256 `6595ebb1ffade5df75f5872466dfda79c786965e933459ef91f6284f0d81fe73`, equal to the block's digest |
| `.agent/authored/f261-r20-job-resume.jsonl` | committed sha256 `1de11feedd5dde3b2b4978df2e1da56ffb88205fa6efb0ceb4e05381a7de4eb4`, equal to the block's digest |
| `.agent/authored/f261-r20-replan.jsonl` | committed sha256 `8982ac33ac039403f315d213258d8e0b0e37a2d296f98e8e7504b574a41b9d33`, equal to the block's digest |
| Slices PLAN20, RECORD20, DEC19, P273-FROM/TO, MUT-1…5-FROM/TO | all 15 extracted strictly between their BEGIN and END lines; each sha256 matched its BEGIN marker; none was edited |

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5 landed
   in that order, one commit each, single-parent, on `71cba20e`. No extra commit, none dropped, no
   reordering.
2. **The G5 runner removes `REMEDY_PROJECT` and `REMEDY_DATA_DIR` from the environment.** The
   block specifies that hygiene for SPEC S and not for G5; neither variable was set in this
   session, so the removal was a no-op in fact and is declared only because the runner does it
   unconditionally. It also sets `PYTHONDONTWRITEBYTECODE=1` and runs `python3 -B`. For the same
   reason SPEC S's own three removals were no-ops: `PYTHONPATH`, `REMEDY_PROJECT` and
   `REMEDY_DATA_DIR` all read unset in this session before the suite was launched.
3. **SPEC S ran detached and was polled, not piped.** The suite was started with
   `subprocess.Popen(start_new_session=True)` writing to `.remedy-wt/f261r20w/suite_out.txt`, and
   its return code was written to a file by the wrapper and read from there. The block's
   ENVIRONMENT paragraph warns that a pipe into `tail` hides pytest's exit code; no exit code in
   this handback comes from a piped invocation. The command, its flags, its working directory and
   its environment are exactly as SPEC S states them.
4. **The block's own size reproduces exactly, and so does its frame rule.** Measured on the
   committed final bytes of `.agent/authored/f261-r20.md`: **322 lines TOTAL** against the cap of
   490 and **233 lines of PROSE** against the cap of 400, where PROSE is every line that is not a
   line of slice content and the 30 `BEGIN`/`END` marker lines count as prose — both exactly the
   numerals constraint 7 declares. The frame rule of item 37 also holds on those same bytes:
   **0** lines of two or more characters are a run of a single repeated character, and across the
   16 header lines carrying box-drawing rules there are **0** rules that are not exactly two
   characters long.
5. **Scratch discipline.** All scratch, the runner and the G5 worktree lived under
   `.remedy-wt/f261r20w/`, uncommitted; no `.py` file was written under `.agent/`; no script was
   named after a standard-library module; no symlink was created; only
   `.remedy-wt/f261-block/` and `.remedy-wt/f261r20w/` were opened under `.remedy-wt/`.
6. **No STOP was encountered.** `.agent/STOP` was read before C0a, before C2 and before C5; all
   three reads exited 1, "No such file or directory".
7. **No table reached a STOP**: all 27 rows across the three carriers applied, and every `edit`
   row's occurrence count matched the count it states.
8. **Three capabilities leave with no heir at all.** This is DECISION F261 D19 as written, not a
   scope decision taken here: the operator attestation, the resume refusals and the flight-plan
   replan have no surviving word, and R-0914, R-0913 and R-0915 carry each loss to F273 rather
   than a stub being left behind.
9. **`tests/orchestration/test_prompt_trace.py` is left lint-dirty on purpose.** Its two `I001`
   findings pre-date this round and reproduce identically at `71cba20e`; G4 orders them reported
   with both readings rather than repaired, and repairing them would be an unrelated edit under
   AGENTS.md scope control.

## Next

Open findings: **110 by distinct id**, of which three are High — **R-0803**, **R-0804** and
**R-0807**. `Operator questions open: 0` (`.agent/operator_questions.md` reads
`EMPTY — nothing is waiting on the operator.`).

The single expected next action, in order:

1. **Phase 1 rule 1** of `docs/agents/self_drive_protocol.md` — read `.agent/STOP` from disk; if
   it exists, write the handoff and end the session before anything else.
2. **The reviewer's verdict on round 20**, over the committed range `71cba20e`..C5, booked into
   `.agent/live_review.md` by the first commit of round 21.
3. **Round 21's work**: the `do continue` hints, then the command and
   `packages/orchestration/do_continue.py`, with **R-0900**, as `.agent/f261_t003_inventory.md`
   proposes in its round H.
