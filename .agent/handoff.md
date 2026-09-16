# Handback — F261 CLI vocabulary v2, round 21

## Session

SESSION 5 of feature F261 · round 21 · rounds so far 21

Context self-assessment: comfortable — the round read the block, AGENTS.md, the protocol, the
handback template and the two carriers once each, applied two tables, ran six gates including a
full serial suite, and never needed to re-read a file; a further round of this shape would fit
with room to spare.

## Range

Review of `ab748c47`..`HEAD`, where `HEAD` is C4 — the commit that writes this file, which it
cannot name from inside itself (R-0149 self-reference pattern).

## Result — ONE GATE IS RED

**G5 (5) is UNRUNNABLE AS ORDERED and is therefore reported RED.** Slice `MUT-5-FROM` reads
**0 occurrences** in `docs/system/architecture.md` at C3, where the block's G5 requires the count
to read 1. The slice was not edited and no expected value was changed. The production tree is
NOT in doubt: G3 proved every one of the nine subtree ids at C2 and at C3 equals the reviewer's
own dry run, `docs/system` included. Details and the supplementary probe are under G5 below.
Everything else this round ordered — C0a to C3, G1, G2, G3, G4, G5 (a), (1), (2), (3), (4), (6)
and G6 — ran and is green.

## Commits

### 55c8a3ff F261 R21 C0a: save the round 21 step block under the authored directory

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r21.md` | +365/-0 | the block file the delegating message names, copied by `shutil.copyfile` |
| **Commit total** | **+365/-0** | constraint 5 reading: 365 insertions |

### 3e419b6d F261 R21 C0b: mirror the round 21 step block into the last block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +197/-154 | the same bytes, byte-identical to C0a's file |
| **Commit total** | **+197/-154** | constraint 5 reading: 197 insertions |

### e9e6bc93 F261 R21 C1: book round 20's PASS, register R-0916 to R-0922 for F273 and record DECISION F261 D20

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +13/-12 | full replacement by slice PLAN21 |
| `.agent/live_review.md` | +16/-0 | slice RECORD21 appended: the round 20 PASS and R-0916 to R-0922 |
| `.agent/decisions.md` | +16/-0 | slice DEC20 appended: DECISION F261 D20 |
| `docs/roadmap/features/T2_F273.md` | +19/-0 | pair P273 applied: acceptance lines for R-0916 to R-0922 |
| **Commit total** | **+64/-12** | constraint 5 reading: 64 insertions |

### 58be13e3 F261 R21 C2: delete the do continue command with its module and the repair-reconcile block it was the only caller of, re-pointing the hints and pages at patch apply, by the continue table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r21-continue.jsonl` | +62/-0 | the table carrier |
| `README.md` | +1/-1 | the guide's row relabelled, the page kept |
| `apps/cli/command_catalog.py` | +0/-19 | the `do.continue` catalog entry |
| `apps/cli/commands/do_cmd.py` | +0/-39 | `_cmd_do_continue` and its dispatch row |
| `docs/README.md` | +2/-2 | the guide's two index rows relabelled |
| `docs/guides/do-continue-v1.md` | +25/-18 | KEPT under a dated status banner naming the three surviving commands; forms rewritten to the past tense |
| `docs/guides/do-run-v1.md` | +1/-1 | the next-step line re-pointed at `patch apply` |
| `docs/system/operator-cockpit-v1.md` | +3/-3 | the cockpit prose re-pointed |
| `docs/system/provider-patch-materialization-v0.md` | +3/-3 | the materialization flow re-pointed |
| `docs/system/real-test-execution-v1.md` | +1/-1 | the caller sentence re-pointed |
| `docs/system/repair-loop-v0.md` | +1/-1 | the legacy apply sentence re-pointed |
| `docs/system/repair-loop-v1.md` | +28/-32 | the reconciliation section rewritten to say what is gone |
| `docs/system/repair-request-builder-v0.md` | +2/-2 | the next-steps prose re-pointed |
| `docs/system/self-dogfood-execution-v0.md` | +3/-3 | the attempt-state hint re-pointed |
| `docs/system/self-dogfood-v0.md` | +3/-3 | the roadmap-rule prose re-pointed |
| `docs/system/snapshot-rollback-v1.md` | +1/-1 | the snapshot-truth consumer list re-pointed |
| `packages/orchestration/do_continue.py` | +0/-952 | the module, deleted with its only production caller |
| `packages/orchestration/mission_readiness.py` | +7/-6 | the four next-safe actions that named the deleted word |
| `packages/orchestration/provider_patch_material.py` | +1/-1 | the flow docstring |
| `packages/orchestration/repair_loop.py` | +1/-182 | the repair-reconcile block, whose only caller was `do_continue.py` |
| `packages/orchestration/repair_request_builder.py` | +1/-1 | the next-step string |
| `packages/orchestration/repository_snapshot.py` | +4/-4 | the two shared-source docstrings |
| `packages/orchestration/run_contract.py` | +1/-1 | the contract-action comment |
| `packages/orchestration/self_dogfood.py` | +3/-3 | the roadmap rule and the report footer |
| `packages/orchestration/self_dogfood_execution.py` | +1/-1 | the `INTENT_APPROVED` next action |
| `tests/cli/test_do_continue_cli.py` | +0/-83 | the deleted command's CLI tests |
| `tests/orchestration/import_reachability_allowlist.txt` | +0/-1 | the deleted module's allowlist row |
| `tests/orchestration/test_do_continue.py` | +0/-419 | the deleted module's own tests |
| `tests/orchestration/test_fence_e2e.py` | +0/-18 | the `ContinueStopReason` fence class |
| `tests/orchestration/test_fence_production_e2e.py` | +4/-91 | the `run_do_continue` fence E2E class |
| `tests/orchestration/test_mission_readiness.py` | +54/-9 | the durable-snapshot case re-driven through `apply_patch_intent`, with its fixture moved here |
| `tests/orchestration/test_repair_apply_cycle.py` | +0/-194 | reached the deleted block only through `run_do_continue` |
| `tests/orchestration/test_repair_request_builder.py` | +2/-2 | the surviving-command assertion re-pointed |
| `tests/test_command_catalog.py` | +1/-0 | `do.continue` joins `TestDeletedCommands` |
| **Commit total** | **+216/-2097** | constraint 5 reading: 216 insertions |

### 28520ab8 F261 R21 C3: resolve R-0900 by naming a command at every group-only advertisement and guarding the one-token form against the default-subcommand map, by the R-0900 table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r21-r0900.jsonl` | +14/-0 | the table carrier |
| `docs/system/architecture.md` | +11/-12 | six group-only sites named `brain graph`; the `remedy project <id>` alias line deleted and the sentence beside it corrected |
| `docs/system/vocabulary.md` | +1/-1 | `remedy do --task-file` becomes `remedy do run --task-file` |
| `packages/orchestration/brain_detail.py` | +2/-2 | two next actions named the `brain` group alone |
| `packages/orchestration/flight_plan.py` | +1/-1 | the caller docstring named `remedy do --yes` |
| `packages/orchestration/orchestrator_loop.py` | +1/-1 | the same helper reference |
| `tests/cli/test_advertised_commands.py` | +116/-0 | the new group-only guard, resolving one-token advertisements against `_DEFAULT_COMMAND`/`_ALWAYS_INJECT` imported from `apps/cli/grouped.py`, with two scanner tests |
| **Commit total** | **+146/-17** | constraint 5 reading: 146 insertions |

### Item status — the block's ordered bundle

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit; its own numbers appear nowhere, per item 31 of §3 |
| G1 | done | green |
| G2 | done | green |
| G3 | done | green |
| G4 | done | green |
| G5 | deviated | (a), (1), (2), (3), (4) and (6) ran and are green; (5) is UNRUNNABLE as ordered — `MUT-5-FROM` reads count 0, not 1 — and is reported RED, unrepaired |
| G6 | done | green, exit 0, no bad node |
| G7 | done | runs after this commit and the push; reported in the round's completion message only |

## External actions

- `git push origin feature/f261-cli-vocabulary-v2` — run after this commit; its result is in the
  round's completion message with G7.
- `git worktree add --detach .remedy-wt/f261r21w/wt 28520ab8` — created for G5, then
  `git worktree remove --force .remedy-wt/f261r21w/wt` — removed; `git worktree list` one row.
- No `gh` command, no pull request created or edited, no merge, no force-push, no branch deleted.
- No `remedy` command run, and no runner or `run_job` invoked: `git branch --list 'remedy/job-*'`
  reads 16 lines at the end of the round, as it did at `ab748c47`.

## Verification

**G1 TRANSPORT — exit 0.** `.agent/authored/f261-r21.md` at C0a has sha256
`8d967dc0902c9dffd6f08013e69214e69701176ac41deddb9daae0bcc9584654`, equal to the digest the
delegating message gives; `.agent/last_block.md` at C0b is byte-identical to it (same sha256,
same bytes compared in memory). **17 slices FOUND**, each matching its BEGIN-marker sha256:
PLAN21, RECORD21, DEC20, P273-FROM, P273-TO and MUT-1 to MUT-6 FROM/TO. Each committed carrier's
sha256 equals its block digest: continue
`92eb43232502a82646611512ea577442b55e291123feddc54a6bcdb416722f73`, R-0900
`09421a05caeca521dfe981a589ac6f7075dd1542c0c0863244b1fa1c0207073a`.

**G2 THE RECORD at C1 — exit 0**, every reading as the block states it.

| Reading | Base `ab748c47` | C1 `e9e6bc93` |
|---|---|---|
| `.agent/plan.md` byte-identical to PLAN21 | — | yes, 37 lines (cap 50) |
| `^## Goal$` / `^## Next Steps$` in plan.md | — | 1 / 1 |
| `.agent/live_review.md` == base blob + RECORD21 | 1072965 B | equal, 1091527 B, delta 18562 |
| `.agent/decisions.md` == base blob + DEC20 | 1407747 B | equal, 1412169 B, delta 4422 |
| `T2_F273.md` == base blob with pair P273 applied | — | equal |
| P273-FROM occurrences | 1 | 0 |
| P273-TO occurrences | 0 | 1 |
| `^Gate: F\d+ R\d+ — ` | 129 | 130 |
| `Gate: F261 R20 — ` | 0 | 1 |
| distinct `^- R-\d+ — ` ids | 118 | 125 |
| C1 minus base | — | exactly `R-0916`, `R-0917`, `R-0918`, `R-0919`, `R-0920`, `R-0921`, `R-0922` |
| distinct `^Done: R-\d+ — ` ids | 8 | 8 |
| open set by distinct id | 110 | 117 |

`python3 -m pytest tests/docs/ -q` at C1: **exit 0**, `310 passed in 1.05s`.

**G3 THE TABLES at C2 and C3 — exit 0.** `git diff --no-renames --name-only` from each parent
printed exactly that commit's carrier plus the paths the block names — C2 **34 paths** (33 + the
carrier), C3 **7 paths** (6 + the carrier) — each set equal to the block's list with no path over
and none missing. Every `git rev-parse <commit>:<object>` equalled the reviewer's dry run, for all
nine objects at both commits:

| Object | C2 `58be13e3` | C3 `28520ab8` |
|---|---|---|
| `apps` | `10f52eca…` | `10f52eca…` |
| `packages` | `47723c13…` | `973237d2…` |
| `scripts` | `208d836b…` | `208d836b…` |
| `tests` | `2628d401…` | `185416da…` |
| `docs/guides` | `f45f164a…` | `f45f164a…` |
| `docs/system` | `7feec242…` | `ea4ece63…` |
| `docs/README.md` | `5fb479b1…` | `5fb479b1…` |
| `README.md` | `60ca9975…` | `60ca9975…` |
| `.claude` | `e3cd5e0a…` | `e3cd5e0a…` |

All 18 subtree ids reproduced the dry run exactly. Insertions per constraint 5: **C2 216, C3 146**
— with C0a 365, C0b 197 and C1 64, every commit of the round is under 500.

Table application: the continue table's **62 rows** and the R-0900 table's **14 rows** each
applied strictly in file order, and **every `edit` row's occurrence count read exactly the count
the row states** — 1 in 69 rows, 2 in one row and 3 in two rows, all 72 exact, beside the four
`delete` rows whose targets all existed. No STOP was reached, and each table was simulated whole
over an in-memory overlay before a byte was written, so a mismatching row would have touched
nothing.

**G4 THE SWEEP at C3 — exit 0.**

- `git ls-tree 28520ab8 -- packages/orchestration/do_continue.py` → **exit 0, stdout `''`**.
- The block's sweep at C3 → **exit 0, exactly 3 lines in 3 files**, one each, verbatim:

<!-- -->

      28520ab8:docs/system/repair-loop-v1.md:98:> D4 deleted the command, and `reconcile_repair_after_continue` in
      28520ab8:tests/cli/test_advertised_commands.py:28:subcommand, and ``remedy do --continue <id>`` exits 0 having printed group help
      28520ab8:tests/orchestration/test_self_dogfood_execution.py:200:        assert "run_do_continue" not in self.SRC

- The same command at `ab748c47` → **exit 0, 117 lines in 21 files**, so the pattern had real
  reach before this round and the block's expected counts reproduced exactly.
- `python3 -m ruff check` over every `.py` path of C2 and C3 still existing at C3 — 23 `.py`
  paths touched, **19 surviving**, four deleted — → **exit 0, `All checks passed!`**.

**G5 THE RED-PROOF — RED: five of six mutations green, mutation (5) unrunnable as ordered.**

In `git worktree add --detach .remedy-wt/f261r21w/wt 28520ab8`, each run through the runner, which
purges every `__pycache__`, changes into the worktree, puts it first on `sys.path` and in
`PYTHONPATH` and asserts the provenance: every run printed
`grouped loaded from: /home/decodeux/Repos/remedy/.remedy-wt/f261r21w/wt/apps/cli/grouped.py`
before a single test ran, so the editable install's resolution to the primary checkout was ruled
out each time. Each runnable mutation's FROM slice read **count 1** in its file before replacement
and was restored with `git -C … checkout -- <file>`; `git status --porcelain` in the worktree read
empty after every restore.

| # | File and mutation | Exit | Summary | Bad nodes | Named node among them |
|---|---|---|---|---|---|
| (a) CONTROL | — | **0** | `401 passed in 23.22s` | 0 | — |
| (1) | `apps/cli/commands/do_cmd.py`, a `do.continue` dispatch row | **1** | `1 failed, 400 passed in 23.24s` | 1 | yes — `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| (2) | `apps/cli/command_catalog.py`, a `do.continue` catalog entry | **1** | `1 failed, 400 passed in 23.32s` | 1 | yes — `TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` |
| (3) | `packages/orchestration/self_dogfood_execution.py`, the `remedy do continue` hint restored | **1** | `1 failed, 400 passed in 23.18s` | 1 | yes — `test_every_advertised_command_exists_in_the_catalog` |
| (4) | `packages/orchestration/brain_detail.py`, the group-only `remedy brain` form restored | **1** | `1 failed, 400 passed in 23.29s` | 1 | yes — `test_every_group_only_advertisement_reaches_a_command` |
| (5) | `docs/system/architecture.md`, the group-only `remedy brain` form restored | **— NOT RUN —** | — | — | **UNRUNNABLE: `MUT-5-FROM` count reads 0, not 1** |
| (6) | `docs/guides/do-continue-v1.md`, the deleted module's path restored into the status banner | **1** | `1 failed, 400 passed in 23.24s` | 1 | yes — `test_every_source_path_an_operator_facing_page_names_exists` |

RAW OUTPUT OF THE RED READING, from the mutation driver:

    MUTATION 5 in docs/system/architecture.md: FROM count = 0
    Traceback (most recent call last):
      File "/home/decodeux/Repos/remedy/.remedy-wt/f261r21w/mutate.py", line 32, in <module>
        assert count == 1, "count is not 1"
    AssertionError: count is not 1

WHY. `MUT-5-FROM` is the 52 bytes
`remedy brain graph <job_id> --json    # JSON export` with its terminating newline. The line that really
stands at `docs/system/architecture.md:1369` at C3 is
`remedy brain graph <job_id> --json    # JSON export (future frontend data source)` — the slice
drops the trailing ` (future frontend data source)`. The same holds for `MUT-5-TO` against the
base: at `ab748c47` line 1369 reads
`remedy brain <job_id> --json    # JSON export (future frontend data source)`, so the slice's
replacement text does not occur there either. The slice is short of the file, in both directions.
The slice was NOT edited, and no expected value was changed to make anything green.

THE PRODUCTION TREE IS NOT IN DOUBT. G3 above shows `docs/system` at C3 is
`ea4ece6386208842c2860c698ea8f99dc31fe586`, byte-for-byte the reviewer's own dry-run tree, so the
edit the R-0900 table made to this page is exactly the edit the reviewer measured.

SUPPLEMENTARY PROBE, clearly labelled as NOT gate (5) and NOT a substitute for it. To tell a
truncated slice apart from a guard that cannot see this corpus, the same group-only form was
restored using the file's REAL line — the slice's text plus the suffix it drops — inside the same
disposable worktree, and restored afterwards:

    REAL-LINE FROM count: 1
    RETURNCODE: 1
        FAILED tests/cli/test_advertised_commands.py::test_every_group_only_advertisement_reaches_a_command
        1 failed, 400 passed in 23.23s
    restore exit: 0
    worktree porcelain after restore: ''

So the new guard does reach `docs/system/architecture.md` and does go red when the group-only
`remedy brain` form returns there — which is the property gate (5) exists to establish. The gate
is still reported RED, because the round may not rewrite a slice to make a gate runnable.

After G5: `git worktree remove --force .remedy-wt/f261r21w/wt` (the worktree was clean before
removal — every mutation and the probe restored), `git worktree list` one row,
`git branch --list 'remedy/job-*'` **16 lines**.

**G6 THE SUITE, SPEC S at C3 — exit 0.** From the primary checkout's root, serially,
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs` with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, transcript at
`.remedy-wt/f261r21w/suite.txt`.

- return code **0**
- last output line: `17728 passed, 23 skipped, 1 warning in 1298.35s (0:21:38)`
- distinct bad nodes: **0** — no line-initial `FAILED ` or `ERROR ` in the output, so no lone
  re-run was owed.

**G7 THE TREE** runs after this commit and the push and is reported in the round's completion
message only, per the block.

## Authored-text proofs

| Authored file | Proof |
|---|---|
| `.agent/authored/f261-r21.md` | sha256 at C0a equals the delegating message's digest, `8d967dc0902c9dffd6f08013e69214e69701176ac41deddb9daae0bcc9584654` |
| `.agent/last_block.md` | byte-identical to the committed C0a file (same sha256, compared byte for byte in memory) |
| `.agent/authored/f261-r21-continue.jsonl` | committed sha256 `92eb43232502a82646611512ea577442b55e291123feddc54a6bcdb416722f73`, equal to the block's digest; verified BEFORE the copy and again after |
| `.agent/authored/f261-r21-r0900.jsonl` | committed sha256 `09421a05caeca521dfe981a589ac6f7075dd1542c0c0863244b1fa1c0207073a`, equal to the block's digest; verified BEFORE the copy and again after |
| Slices PLAN21, RECORD21, DEC20, P273-FROM/TO, MUT-1…6-FROM/TO | all 17 extracted strictly between their BEGIN and END lines; each sha256 matched its BEGIN marker; none was edited, including `MUT-5-FROM`, which does not occur in its target |

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2, C3, C4 landed in
   that order, one commit each, single-parent, on `ab748c47`. No extra commit, none dropped, no
   reordering.
2. **G5 (5) IS RED AND WAS NOT REPAIRED.** `MUT-5-FROM` reads 0 occurrences in
   `docs/system/architecture.md` at C3 against the block's required 1. The slice was not edited,
   the target was not edited, and the gate's expected value was not changed. The evidence says the
   slice text is truncated by the 30 characters ` (future frontend data source)`, not that the
   product is wrong: G3 shows the `docs/system` tree at C3 equals the reviewer's dry-run tree
   exactly. This is a reading for the reviewer to take, not one this round may take for it.
3. **Two measurements were taken AFTER the red gate rather than stopping at it**: mutation (6),
   which is part of the same gate and cost one run, and SPEC S / G6, which the block orders before
   C4. Both are pure measurements over already-committed code; neither changed a file, a gate or
   an expected value, and both are reported above with their real readings. The block's STOP
   instruction — commit what is honestly finished, write the handoff with the raw output, push,
   hand back — is what this handback does. Declared here because continuing past a red gate at all
   is a departure.
4. **One probe was run that the block did not order**, the supplementary probe under G5. It ran
   only inside the disposable worktree, restored its file, and is reported as supplementary
   evidence rather than as any gate's reading. Its purpose was to distinguish a truncated slice
   from a blind guard, which is the question the reviewer will have to answer.
5. **The G5 runner removes `REMEDY_PROJECT` and `REMEDY_DATA_DIR` from the environment.** The
   block specifies that hygiene for SPEC S and not for G5; neither variable was set in this
   session, so the removal was a no-op in fact and is declared only because the runner does it
   unconditionally. It also sets `PYTHONDONTWRITEBYTECODE=1` and runs `python3 -B`. For the same
   reason SPEC S's own three removals were no-ops: `PYTHONPATH`, `REMEDY_PROJECT` and
   `REMEDY_DATA_DIR` all read unset in this session before the suite was launched.
6. **No exit code in this handback comes from a piped invocation.** SPEC S ran through a Python
   wrapper that redirects pytest's combined output to `.remedy-wt/f261r21w/suite.txt` and reads
   the return code from `subprocess.run`; the block's ENVIRONMENT warning about `tail` is
   respected everywhere.
7. **The block's own size reproduces exactly, and so does its frame rule.** Measured on the
   committed final bytes of `.agent/authored/f261-r21.md`: **365 lines TOTAL** against the cap of
   490 and **248 lines of PROSE** against the cap of 400, where PROSE is every line that is not a
   line of slice content and the 34 `BEGIN`/`END` marker lines count as prose — both exactly the
   numerals constraint 7 declares. The frame rule of item 37 also holds on those same bytes:
   **0** lines of two or more characters are a run of a single repeated character, and across the
   18 header lines carrying box-drawing rules there are **0** rules that are not exactly two
   characters long.
8. **Scratch discipline.** All scratch, the runners and the G5 worktree lived under
   `.remedy-wt/f261r21w/`, uncommitted; no `.py` file was written under `.agent/`; no script was
   named after a standard-library module; no symlink was created; only
   `.remedy-wt/f261-block/` and `.remedy-wt/f261r21w/` were opened under `.remedy-wt/`.
9. **No STOP was encountered.** `.agent/STOP` was read before C0a, before C2 and before C4; all
   three reads exited 2, "No such file or directory".
10. **No table reached a STOP**: all 76 rows across the two carriers applied, and every `edit`
    row's occurrence count matched the count it states.
11. **Four capabilities leave with no heir at all.** This is DECISION F261 D20 as written, not a
    scope decision taken here: the continuation lease, the durable phase checkpoints, the
    apply-to-test linkage and the repair reconciliation have no surviving word, and R-0916 to
    R-0919 carry each loss to F273 rather than a stub being left behind.
12. **No suite was run while a deletion was staged but uncommitted**, per the block's ENVIRONMENT
    paragraph: the four deletions of C2 were staged and committed before any pytest invocation.

## Next

Open findings: **117 by distinct id**, of which three are High — **R-0803**, **R-0804** and
**R-0807**. `Operator questions open: 0` (`.agent/operator_questions.md` reads
`EMPTY — nothing is waiting on the operator.`).

The single expected next action, in order:

1. **Phase 1 rule 1** of `docs/agents/self_drive_protocol.md` — read `.agent/STOP` from disk; if
   it exists, write the handoff and end the session before anything else.
2. **The reviewer's verdict on round 21**, over the committed range `ab748c47`..C4, which must
   first take a reading on the red G5 (5) above. The `Done:` paragraph **R-0900** is owed once
   that verdict is taken, since this round's C3 is the repair its fix clause asks for.
3. **Round I of `.agent/f261_t003_inventory.md`**: the `propose` and `repair` groups, each
   re-measured before it is authored.
