── STEP T001/3 — F280 — ROUND 3 ──
Goal: Book round 2's PASS with the resolutions of R-0767 and R-0894, register R-0935 and R-0936,
record DECISIONs F280 D3 and D4, then build `job budget <id> set` by one table and delete
`job fulfill` by a second; run the suite once.

Base commit: `4806b03ca5ec87efdb7f779f362e87cad0f57693`, on
`feature/f280-cli-vocabulary-v2-part-two`. SESSION 1 of F280. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F280 D3 and D4 once C1 has landed them.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two
or more characters long is a run of a single repeated character, and every box-drawing rule inside
the STEP and SLICE header lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)`, `$?` and `$VAR` expansions in a command are refused by form, so write such
checks as Python scripts under `.remedy-wt/f280r3w/`, never named after a standard-library module,
and use absolute paths rather than `cd x && ...`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on `sys.path`
and in `PYTHONPATH`, and asserts `apps.cli.commands.job` loaded from inside it. Never call
`run_job`, `run_job_fulfill` or any runner yourself: a job run started from inside a checkout
creates a `remedy/job-*` branch in it. `git branch --list 'remedy/job-*'` reads 17 lines now; keep
it so. While a deletion is staged but not committed, `test_every_enumerated_path_exists_in_this_repo`
fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f280-r3.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN3; slice RECORD3 is appended to
    `.agent/live_review.md` and slice DEC3 to `.agent/decisions.md`; pairs P280 and P273 are
    applied
C2  THE BUDGET WRITE: copy `.remedy-wt/f280-block/f280-r3-budget.jsonl` to
    `.agent/authored/f280-r3-budget.jsonl` and apply it per THE TABLES, in one commit
C3  THE FULFILL DELETION: the same for `f280-r3-fulfill.jsonl`
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f280-cli-vocabulary-v2-part-two`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f280-r3.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/features/T2_F280.md` and
`docs/roadmap/features/T2_F273.md`. C2 and C3: each table's own carrier and the paths G3 names for
that commit. C4: `.agent/handoff.md`. The gate carrier G4 names and the mutation carriers G5 names
are READ from `.remedy-wt/f280-block/` and are never committed.

## The appends and the pairs

RECORD3 and DEC3 each begin with an empty line, and both targets end in a newline at the base: an
append is the file's bytes followed by the slice's bytes, and nothing else. Each FROM slice occurs
exactly once in its target at the base, and each containment test printed
`TO contains FROM: false`, so each pair is a REWRITE: at C1 its FROM occurs 0 times and its TO once.
P280 `docs/roadmap/features/T2_F280.md`: FROM slice P280-FROM, TO slice P280-TO.
P273 `docs/roadmap/features/T2_F273.md`: FROM slice P273-FROM, TO slice P273-TO.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256, to verify before copying:
`f280-r3-budget.jsonl` `9ec801c5d67f03f705cfbb650b71af67ed489f4e497db257909285cc10952494` and
`f280-r3-fulfill.jsonl` `c3675d0d10503c6456d17e07f2563fa9530ba2abd325383300fc96b14f69326c`.
Apply a table's rows strictly in the order they appear in its file, each against the tree as the
previous rows left it, from the repository root: `["edit", path, old, new, count]` opens the path
with `encoding="utf-8", newline=""`, requires the number of occurrences of `old` to equal `count`
exactly, and replaces every occurrence with `new`; `["delete", path]` removes the file;
`["move", src, dst]` renames the file, whose target must not exist; `["create", path, content]`
writes `content` to a path that must not exist, with the same encoding and newline setting. A
count that differs or a target that exists is a STOP: touch nothing further, commit nothing of
that table, and hand back with the row and the reading. Stage each commit with `git add -A` after
its table and its carrier. The tables are two research helpers' builds of DECISIONs F280 D3 and D4,
the second on the first's result, which the reviewer re-applied with its own applier and tested.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f280r3w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f280r3w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f280-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph of your own: RECORD3's are the reviewer's.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 315 lines TOTAL and 221 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice
   CONTENT — the `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3's half for each table commit after that commit; G4 and G5
   after C3; then SPEC S, whose result is G6; G7 after C4 and the push, reported in the
   completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f280-r3.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN3, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its base blob followed
by RECORD3, and `.agent/decisions.md` its base blob followed by DEC3. Each of the two feature files
equals its base blob with its pair applied, with the counts The appends and the pairs give. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 29 at the base and 30 at C1, with
`Gate: F280 R2 — ` 0 times at the base and once at C1; distinct `^- R-\d+ — ` ids 130 and 132, C1
minus base exactly `R-0935` and `R-0936`; distinct `^Done: R-\d+ — ` ids 2 and 4, C1 minus base
exactly `R-0767` and `R-0894`; the open set by distinct id 128 and 128. `python3 -B -m pytest -q
tests/docs/` exits 0 at C1.

G3 THE TABLES. For each table commit, `git diff --no-renames --name-only` from its parent prints
exactly its carrier and these paths. C2: `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
`docs/guides/token-economy-user-guide-v0.md`, `docs/system/job-budget-enforcement-v0.md`,
`docs/system/real-test-execution-v1.md`, `docs/system/run-contract-v1.md`,
`docs/system/token-economy-context-budget-optimizer-v0.md`,
`packages/orchestration/run_contract.py`, `packages/orchestration/test_execution_service.py`,
`tests/cli/test_job_budget_set.py`, `tests/orchestration/test_job_budgets.py`. C3:
`apps/cli/command_catalog.py`, `apps/cli/commands/job.py`, `apps/cli/grouped.py`, `docs/README.md`,
`docs/guides/simple-operator-quickstart-v0.md`, `docs/system/core-product-spine-v0.md`,
`docs/system/first-fulfilled-job-demo-v0.md`, `docs/system/first-perfect-job-demo-v0.md`,
`docs/system/real-test-execution-v1.md`, `docs/system/run-contract-v1.md`,
`tests/orchestration/test_job_fulfillment.py`, `tests/test_command_catalog.py`.
`git rev-parse <commit>:<object>` for `apps`, `packages`, `scripts`, `tests`, `docs/guides`,
`docs/system`, `docs/README.md`, `README.md` and `.claude`, in that order, equals the reviewer's dry
run, which applied the tables on the base, the record touching none of these objects. At C2:
`3bda6ea6604ba8a7edfd9d08aef39b98f5edc28e`, `e5d99f301efb1073ba547c67b710288a24165d06`,
`4bea3f9f084c3987c399f39746b5b2c57be6ffca`, `d49f307a94d90f981ad9947b40d2dbc289e8ab29`,
`b1a68d32381c50bbfaa902bee6d32e058f9dda93`, `d5b2ad1170857a5456e58d76e068872939f93a60`,
`c282d425ef909cf9257605294f23aba7d9457fac`, `3c6b8d40ec4f4d76e05dc352a4b0ce8ef8970be5`,
`e3cd5e0ac262f3f993506e95825e270e39c03ec0`. At C3:
`068608a3598c7550d2c5c9c103d875357be2646f`, `e5d99f301efb1073ba547c67b710288a24165d06`,
`4bea3f9f084c3987c399f39746b5b2c57be6ffca`, `1c14c8b814e509f6549a4d7bb074891316283139`,
`969f52e3e9e7a8c4ac1ccfa2f216b05968f6bf58`, `3d77ab791e1ce9884320b0cd533783ca255a1963`,
`0f1933b93649df9471145f57c5fbe9302f6a0d97`, `3c6b8d40ec4f4d76e05dc352a4b0ce8ef8970be5`,
`e3cd5e0ac262f3f993506e95825e270e39c03ec0`. Report the insertions of C2 and C3 per constraint 5.
From the primary checkout at C2, `python3 -B -m pytest -q tests/cli/test_golden_path.py` exits 0.

G4 THE SWEEP, at C3. The four patterns are the `newword`, `fulfill`, `control_create` and
`control_propose` values of `.remedy-wt/f280-block/f280-r3-gates.json`, sha256
`0315f9e2de517116ade59953056d22d66f74d3e6d7d41451155bedd8faeb797e`; read them from that file in
Python and pass each as one argv element to
`git grep -n -I -E <pattern> <rev> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap' ':!docs/archive'`,
never retyping them in a shell, at the base, at C2 and at C3. The expected readings, lines and
files: `newword` 0 and 0, 11 and 8, 12 and 9; `fulfill` 33 and 11, 33 and 11, 11 and 8;
`control_create` 107 and 41, 107 and 41, 106 and 41; `control_propose` 59 and 12 at all three.
Print every line `fulfill` matches at C3. `python3 -m ruff check` over every `.py` path C2 or C3
edits exits 0; report how many paths that was.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f280r3w/wt <C3's sha>`, each run through
the runner with `-p no:randomly -p no:cacheprovider -rf --tb=no`, under `python3 -B`. Two carriers:
`.remedy-wt/f280-block/f280-r3-budget-mutations.jsonl`, sha256
`783cebe347b45a0a423dae731724c5598a1af1b1d2f4bec9e81c06ac9374b1bc`, over
`tests/cli/test_job_budget_set.py`; and `.remedy-wt/f280-block/f280-r3-fulfill-mutations.jsonl`,
sha256 `0884ccaea3efd7e950b5d25faa411b9454a86ec7d8df2c8a46113e69ae985d80`, over
`tests/test_command_catalog.py` and `tests/cli/test_advertised_commands.py`. Each row is
`[label, path, from, to, node]`, the `from` bytes must occur EXACTLY ONCE in that path inside the
worktree, and the file is restored with `git -C .remedy-wt/f280r3w/wt checkout -- <path>` after each
run. Read the carriers; never retype their bytes. For each carrier its CONTROL first, unmutated:
must exit 0. Each row must exit 1 with its row's node AMONG the failed nodes. Report each exit code,
summary line, each FROM's occurrence count and every failed node id; then
`git worktree remove --force .remedy-wt/f280r3w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line. A bad node
whose lone re-run exits 0 is reported as such with both readings and is not a STOP; a bad node
whose lone re-run fails is.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on the base; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f280-cli-vocabulary-v2-part-two`; `git worktree list` prints one
row, and `git branch --list 'remedy/job-*'` prints 17 lines.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F280 · round 3 · rounds so far 3`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C4's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 128 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 1`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 3; and moving the
fixtures and smoke sections off `job create`, then deleting `job create`.

── SLICE PLAN3 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN3 sha256=4753a5aaf37165034bd099f9ff20fbe0ed42a27e59b9f3680041866b5339dc94
# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 3 books round 2's PASS with the resolutions of R-0767 and R-0894, registers R-0935 and
R-0936, and records DECISIONs F280 D3 and D4. Its first table builds `job budget <id> set` over
the run contract's budget fields and the token budget profile (R-0906, R-0909); its second deletes
`job fulfill`. D4 defers `job attach-repo` and `job permit`. The worker runs the suite once.

## Next Steps

1. The fixtures and smoke sections moved off `job create`, then `job create` with its hints; the
   next record books round 3's verdict with the resolutions of R-0906 and R-0909.
2. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
3. The `flight_plan` rename; `worker doctor` and `job run --tasks`.
4. `job attach-repo` and `job permit`, only once a DECISION gives the repository attach and the
   capability grants another writer, as DECISION F280 D4 requires.
5. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 128 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- `job attach-repo` and `job permit` are the only command-line writers of a job's repository
  and of its test and revert grants, so the Acceptance line naming them cannot hold until a
  later DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 token and wall-clock budgets, so what
  `job budget <id> set` writes into the contract is not overwritten by them either.
END PLAN3

── SLICE RECORD3 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD3 sha256=32812ed1295a149d882a898289523e12a935ebce84af8846434a4eae088eb36d

Gate: F280 R2 — the F280 round 2 entry. VERDICT PASS. Written by the planner and reviewer of session 43 after reading the committed range `4e93c22c`..`4806b03c` and re-deriving every reading below; the worker's report was evidence for none of them except where named. It is booked here by the first commit of round 3 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f280-r2.md` at `7af33af1` and `.agent/last_block.md` at `b3906ab4` are byte-identical to the reviewer's scratch original, sha256 `fa7f1ba70e4b7c4987b54f359d7ed350ac5cfe0ab8f9f3a5989e26049900c5a4`, and the carriers committed at `787f3b74`, `8bd055d9` and `298cd353` are byte-identical to the reviewer's, sha256 `df98e2a6577c99a3162e6f6d96c370d192f50936da32ce0f852ca50ecdd1cd16`, `1c99303db9b5b2d85b45c108fbee662cf8672e1ccb66faf4f5a36dfb561a8756` and `5f4f42bbfcde8d23e2eb54e70abc487357a4706ff4ed891256cb93c4a09a3560`, the research helper's tables unamended. THE STATE: at `f53f109e`, `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md` and the three edited feature files are byte-identical to the blobs of the reviewer's own dry-run commit on `4e93c22c`; the `Gate:` count reads 28 then 29, the distinct registered ids 127 then 130 with the delta exactly R-0932 to R-0934, the distinct `Done:` ids 2 then 2, the open set 125 then 128. THE TABLE COMMITS: at `787f3b74`, `8bd055d9` and `298cd353` all nine objects the block names equal the helper's dry-run commits and the reviewer's own re-application of the tables on `4e93c22c`, and `git show --numstat` reads 158 insertions against 813 deletions, 200 against 1285 and 32 against 0. THE SWEEP, with the patterns of the gate carrier read as argv, at `4e93c22c` and at `298cd353`: the deleted symbols read 181 lines in 8 files and 8 lines in 2, the eight survivors being the evidence manifest field R-0932 records and one comment; the deleted flags 48 in 8 and 23 in 5, which are guard data, test comments and docstrings, and one row of the concept table of `docs/system/vocabulary.md`; the old quick start 5 in 2 and 2 in 1, the surviving `run show $RUN_ID` flow of `pingpong_loop.py`; the control on `propose` and `job fulfill` 89 lines in 14 files at every commit. THE RED-PROOFS ran in the reviewer's own worktree on the identical tree: a control of 349 passed at exit 0, and each of the six rows of the mutation carrier `77d447624774c1b3086b97cbced3b1971d24f21cc6e3ecd3c6c0a831c9c0a4ab` exiting 1 with its named node among the failures — re-adding `--builder` to `do run` or to `job run`, restoring the old quick start step, restoring either old provider message, and re-enabling prefix matching on the command parsers, which reddened the abbreviation case of `do run --builder` alone. THE REVIEWER'S RUNS: in its worktree `tests/cli/`, the catalog, role-flag, docs, import-reachability, ping-pong, provider-retry, repair-loop, stream-evidence, execution-loop, task-runner and roadmap-index tests read 2246 passed; in the primary checkout at `4806b03c` the catalog tests, the canary, `tests/cli/test_cli_ux.py`, the advertised-commands guard and `tests/docs/` read 490 passed. The worker's full-suite transcript, which the reviewer read, ends `17634 passed, 23 skipped, 1 warning in 1238.56s` with no line-initial `FAILED ` or `ERROR `. The open set reads 128 by distinct id at `4806b03c`.

Done: R-0767 — RESOLVED by F280 rounds 1 and 2. At `290bd0ed` the `job.run` catalog entry declares neither `--builder` nor `--reviewer` and `_cmd_job_run` hands `--builder-provider` and `--reviewer-provider` to `run_job`, so `remedy job run <id> --builder-provider ollama --reviewer-provider ollama` reaches the runner with both names; at `787f3b74` no catalog entry declares either flag and `_VALID_PINGPONG_PROVIDERS` is gone; at `298cd353` prefix matching is off, so neither word survives as an abbreviation. Verified by the reviewer: in its worktree, handing `run_job` no builder name reddened `TestJobRunProviderWiring::test_provider_flags_reach_run_job_as_the_role_names` in `tests/test_role_override_flags.py` among twelve nodes against a green control of 243, and re-adding the `--builder` flag to either command reddened `TestDeletedFlags::test_no_deleted_flag_is_declared_by_its_command` in `tests/test_command_catalog.py` against a green control of 349.

Done: R-0894 — RESOLVED by F280 round 2, whose DECISION F280 D2 is the deletion paragraph the fix asked for and states that the idea has no heir. At `787f3b74` the `do.run` entry declares neither `--scope-file` nor `--approve-scope` and `_cmd_do` reads no scope plan; at `8bd055d9` `packages/orchestration/scope_plan.py` and `tests/cli/test_scope_plan.py` are absent, `run_pingpong` has no scope parameter, and the import-reachability allowlist has no scope plan line. Verified by the reviewer: the deleted-symbol sweep reads 181 lines at `4e93c22c` and 8 at `298cd353`, none of them a scope plan reader or writer but the evidence manifest field R-0932 records; `TestDeletedFlags` pins both flags as undeclared and refused, and re-adding a deleted `do.run` flag reddened it against a green control.

- R-0935 — Medium, THE RUN CONTRACT NEVER INHERITS A JOB'S F018 TOKEN AND WALL-CLOCK BUDGETS, BECAUSE `build_default_run_contract` AND `_reconcile_budget_fields` READ THOSE BUDGETS AS ATTRIBUTES OF A DICT. Raised by the planner and reviewer of session 43 while preparing F280 round 3, from a reading its research helper took and the reviewer re-took, after searching the open set for the reconciliation, the one budget authority and the contract's budget fields under §3 item 30: no open finding describes it. THE DEFECT, read at `4806b03c`: `JobPlan.budgets` in `packages/orchestration/pingpong_job.py` is declared `dict | None`, and both functions in `packages/orchestration/run_contract.py` test `getattr(budgets, "max_total_tokens", None)` and `getattr(budgets, "max_wall_clock_minutes", None)` on it, which is None for every dict, so the contract keeps its own `max_tokens` and `max_runtime_seconds` whatever the job's budgets say, the reconciliation never runs, and the docstring's promise that JobBudgets is canonical for the overlapping fields holds for no job; `evaluate_run_action` then judges runtime and token usage through `check_budget` against those contract values. WHY MEDIUM: a gate that decides whether a test run or an apply may proceed reads limits the operator's budget flags never reach; nothing crashes and nothing prints a false budget. WHY F273's: the repair changes what a surviving budget gate decides, which this feature's Do-not-touch section excludes. FIX: read the budgets as a dict or validate them into `JobBudgets` in both functions, with a test that a job carrying `max_total_tokens` and `max_wall_clock_minutes` yields a contract whose `max_tokens` and `max_runtime_seconds` equal them, and decide in the same commit whether a value `job budget <id> set` wrote is overwritten by a later reconciliation. Owner: F273.

- R-0936 — Low, DELETING `job fulfill` LEAVES THE FIXTURE FULFILLMENT SPINE WITH TEST CALLERS ONLY, AND `job show --full` READING FULFILLMENT RECORDS NOTHING WRITES. Raised by the planner and reviewer of session 43 while preparing F280 round 3, from readings its research helper took on the reviewer's dry-run tree of that round's budget table and the reviewer re-took on its own tree, whose `apps` object is `068608a3`, after searching the open set for the fulfillment spine and its records under §3 item 30: no open finding describes them. THE DEFECT, read on that tree: `run_job_fulfill`, `summarize_job_fulfillment`, `fixture_plan_tasks`, `fixture_worker_output`, `fixture_review`, `finding_to_repair_task`, `fixture_repair_output`, `JobFulfillmentContract` and `save_fulfillment_record` in `packages/orchestration/job_fulfillment.py`, and `find_staged_changes`, `apply_staged_changes_to_target` and `discard_staging` in `packages/orchestration/staging_workspace.py`, have no production caller outside their modules, because the deleted handler was their only one; `_report_section` and `_extract_job_truth` in `apps/cli/commands/job.py` still read fulfillment records through `list_fulfillment_records`, which only that spine wrote. The modules stay under DECISION F261 D17's rule. WHY LOW: a fixture demonstration leaves with no heir and two report sections read an empty store; nothing prints anything false. WHY F273's: none of it is a command word. FIX: delete the test-only functions with their tests and the fulfillment sections of `job show --full` with theirs, or register the heir that writes fulfillment records. Owner: F273.
END RECORD3

── SLICE DEC3 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC3 sha256=afd00b43b3848494f15fcdbad129d000bb32fb978bcbb3a16861aefbed50a600

## DECISION F280 D3 (2026-09-16, F280 round 3) — `job budget <id> set <field> <value>` writes one field of the run contract's budget or of the token budget profile

CONTEXT. The Do-not-touch section of `docs/roadmap/features/T2_F280.md` names the new `job budget <id> set` write as one of the three places this feature may change what a surviving command does, by a dated DECISION with a feature-file amendment. DECISION amend0905-vocab D4 gives `job` the word `budget <id> [set …]`; R-0906 records that since `contract set` was deleted nothing can raise `max_test_runs`, which `build_default_run_contract` sets to 0 and `execute_test_run` refuses at, and R-0909 that the token budget profile lost its only writer with `token budget-set`. Measured at `4806b03c` by the reviewer's research helper in its own worktree and re-applied by the reviewer on its own tree, whose nine objects equal the helper's.

CHOSEN, FIRST: `remedy job budget <id>` prints what it printed before, and `remedy job budget <id> set <field> <value>` writes ONE integer field under the store's own snake_case name: the run contract's `max_loops`, `max_test_runs`, `max_runtime_seconds`, `max_tokens` and `max_cost_cents`, at least 0, loaded from the job or started from `build_default_run_contract` and saved with `save_contract`; or the token budget profile's `max_context_tokens`, `max_generation_tokens`, `max_total_estimated_tokens`, `prefer_local_under_tokens` and `require_human_approval_over_tokens`, at least 1, saved with `save_token_budget_profile`. It prints the field's old and new value and the store, or an object with those keys under `--json`. An unknown field, a non-integer, a value below its floor, an action other than `set` or a missing value exits 2 and writes nothing; an unknown job exits 1 with the show form's error.

CHOSEN, SECOND: F018's JobBudgets are NOT settable here, because `job run`'s budget flags and the stopped-job Decision guard own them; naming one exits 2 and names the `job run` flag. The catalog entry becomes `write_metadata`, and no production code reads `action_class`.

CHOSEN, THIRD: the refusals a zero or exhausted test-run budget produces in `evaluate_run_action`, and the guidance `execute_test_run` prints for them, name `remedy job budget <job_id> set max_test_runs <n>`; no decision logic changes. The `do continue` blockers R-0906 also named no longer exist.

ALTERNATIVES. Restoring `contract set` with every contract field, rejected because D4 gives no such word and a budget write needs no policy fields. Options per field instead of positional words, rejected because D4 spells the form `set …` and the deleted `contract set` took a field and a value.

CONSEQUENCE. `tests/cli/test_job_budget_set.py` pins that raising `max_test_runs` takes `execute_test_run` past the contract gate and that a token field reads back through the token economy report, which are the Acceptance lines of R-0906 and R-0909. R-0935 records that the contract never inherits the job's F018 token and wall-clock budgets, so a value written here is not overwritten by them. HOW TO REVERSE: revert the round's budget table commit, and delete this section and the dated paragraph it adds to T001 of `docs/roadmap/features/T2_F280.md`.

## DECISION F280 D4 (2026-09-16, F280 round 3) — the deletion paragraph of `job fulfill`, and why `job attach-repo` and `job permit` wait for a writer

CONTEXT. DECISION F261 D23 deferred `job fulfill` because its fixture contract was the only production write of a non-zero test budget; DECISION F280 D3 builds that write. Inventory ruling 7 of `.agent/f261_t003_inventory.md` deletes `job create`, `job attach-repo` and `job permit` with findings. Measured at `4806b03c` by the reviewer's read-only research helper, and for `job fulfill` rebuilt on the budget table's result by a second helper whose table the reviewer re-applied and tested: at `4806b03c` the only production writers of a job's `target_repo` are `_cmd_attach_repo` and `run_job_fulfill`, apart from `continue_from_node` copying a parent's value, and the only production writers of the `repo_test_run` grant are `_cmd_set_permission` and `run_job_fulfill`; `execute_test_run` refuses a job without that grant or without a `target_repo`, and `test discover`, `patch apply`, `patch revert` and `self execute` gate on the same repository or grants.

CHOSEN, FIRST: `job fulfill` goes — its catalog entry, handler and dispatch entry, the `--fixture-demo` special case of `apps/cli/grouped.py`, its command and catalog tests, and its id into `TestDeletedCommands`; the demonstration pages say in the past tense under a dated banner what it did. `packages/orchestration/job_fulfillment.py` stays under DECISION F261 D17's rule, because `job show --full` still imports it. THE HEIR: none for the fixture demonstration; the test-run budget it used to supply is `job budget <id> set`. R-0936 records the functions left with test callers only and the report sections that read records nothing writes.

CHOSEN, SECOND: `job attach-repo` and `job permit` are DEFERRED, on the rule DECISION F261 D21 applied to `propose`: deleting them would leave `test run`, `test discover`, `patch apply`, `patch revert` and `self execute` refusing every new job, which is a surviving command breaking and not a capability leaving. They go only in a round whose DECISION first gives the repository attach and the grants another writer, for example `do <order> --repo`, which F268 owns. `job create` is not deferred by this ruling: its heir is `do run "<goal>"`, and its fixtures move first.

CONSEQUENCE. `remedy job fulfill` is an unknown word; the Acceptance line naming `job attach-repo` and `job permit` stays open. HOW TO REVERSE: revert the round's fulfill table commit and delete this section and the paragraph it adds to T001 of `docs/roadmap/features/T2_F280.md`.
END DEC3

── SLICE P280-FROM ── target `docs/roadmap/features/T2_F280.md` ── REWRITE FROM ──
BEGIN P280-FROM sha256=4396ea48358dfa6d3a1ce436de4d20a10764c21400ef5b763a5ec10605769e99
factory builds; `do run` keeps both flags until its ping-pong path goes with R-0894.

## T002 — Descriptions, role labels, help wrapping, tests (carried over from F261's T004, whole)
END P280-FROM

── SLICE P280-TO ── target `docs/roadmap/features/T2_F280.md` ── REWRITE TO ──
BEGIN P280-TO sha256=dd8b96671e4c48b2a34c4b5cb311774fafdf098716c3898a68d7f5467a9d536b
factory builds; `do run` keeps both flags until its ping-pong path goes with R-0894.

Amended 2026-09-16 by DECISIONs F280 D3 and D4, measured at `4806b03c`: `job budget <id> set
<field> <value>` writes one integer budget field of the run contract or of the token budget
profile, and F018's job budgets stay with `job run`'s flags; `job fulfill` is deleted; and
`job attach-repo` and `job permit` wait for a round whose DECISION first gives the repository
attach and the capability grants another writer, because five surviving commands gate on them.

## T002 — Descriptions, role labels, help wrapping, tests (carried over from F261's T004, whole)
END P280-TO

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=48b5564f91b2ec70febf706468ab571b520010fd7feaee214f6ada2feb0f6b48
  of the `do run` ping-pong path it lists, with the tests that changed.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=0dae73a14ef5c3ac9395e9bc7f627518edb5774f18bd123782e195e88222b94e
  of the `do run` ping-pong path it lists, with the tests that changed.
- R-0935 carries a resolution line naming the test in which a job's F018 token and wall-clock
  budgets reach its run contract.
- R-0936 carries a resolution line naming the commit that deleted or gave an heir to the fixture
  fulfillment spine and the fulfillment sections of `job show --full`, with the tests that changed.

## Do not touch
END P273-TO
