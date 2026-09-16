── STEP T003/8 — F261 — ROUND 23 ──
Goal: Book round 22's PASS, register R-0927 to R-0930 for F273 and record DECISION F261 D22, then
delete the queue words of `job`, `worker run` and `mission ledger` by one table; run the suite once.

Base commit: `21ab5e24`, on `feature/f261-cli-vocabulary-v2`. SESSION 6 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D22 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r23w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job`, `run_worker_once`,
`run_worker_loop` or any runner yourself: a job run started from inside a checkout creates a
`remedy/job-*` branch in it. `git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.
While a deletion is staged but not committed, `test_every_enumerated_path_exists_in_this_repo`
fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r23.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN23; slice RECORD23 is appended to
    `.agent/live_review.md` and slice DEC22 to `.agent/decisions.md`; in
    `docs/roadmap/features/T2_F273.md` the bytes of slice P273C-FROM are replaced by those of
    slice P273C-TO
C2  the queue words, `worker run` and `mission ledger`: copy
    `.remedy-wt/f261-block/f261-r23-queue.jsonl` to `.agent/authored/f261-r23-queue.jsonl` and
    apply it per THE TABLE, in one commit
C3  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r23.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and `docs/roadmap/features/T2_F273.md`. C2: the
table's own carrier and the paths G3 names. C3: `.agent/handoff.md`. The gate carrier G4 names
and the mutation carrier G5 names are READ from `.remedy-wt/f261-block/` and are never committed
and never copied into `.agent/`.

## The appends and the pair

RECORD23 and DEC22 each begin with an empty line, and both targets end in a newline at
`21ab5e24`: an append is the file's bytes followed by the slice's bytes, and nothing else. The
first paragraph of RECORD23 is the verdict paragraph of `.agent/handoff.md` at `21ab5e24` that
begins `Gate: F261 R22 — `, byte for byte. The pair P273C: TO contains FROM: false, so it is a
REWRITE; P273C-FROM occurs once in `docs/roadmap/features/T2_F273.md` at `21ab5e24`, and
at C1 P273C-FROM occurs 0 times and P273C-TO once.

## THE TABLE

The carrier holds one JSON array per line. Its sha256, to verify before copying:
`f261-r23-queue.jsonl` `8bba3dcab8f2a759d2561e9294f56b23f83632e9ee0121bfe6db9263b2e9bc9c`.
Apply the rows strictly in the order they appear in the file, each against the tree as the
previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of the table, and hand back with the row and the reading.
Stage C2 with `git add -A` after the table and its carrier. The table is the reviewer's measured
dry run of DECISION F261 D22, applied on `21ab5e24` in the reviewer's own worktree.

## SPEC S — the suite, once, after G5 and before C3

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r23w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C3, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r23w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph: this round resolves no finding.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 268 lines TOTAL and 193 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice CONTENT — the
   `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C2; then SPEC S, whose result is G6; G7
   after C3 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r23.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; the committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN23, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `21ab5e24` blob
followed by RECORD23, and `.agent/decisions.md` its blob followed by DEC22. The first paragraph
of RECORD23 after its empty line equals the `Gate: F261 R22 — ` line of `.agent/handoff.md` at
`21ab5e24`, read with `git show`. `docs/roadmap/features/T2_F273.md` equals its `21ab5e24` blob
with the pair P273C applied, with the counts The appends and the pair give. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 131 at `21ab5e24` and 132 at C1, with
`Gate: F261 R22 — ` 0 times at `21ab5e24` and once at C1; distinct `^- R-\d+ — ` ids 129 and
133, C1 minus base exactly `R-0927` through `R-0930`; distinct `^Done: R-\d+ — ` ids 9 and 9;
the open set by distinct id 120 and 124. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLE, at C2. `git diff --no-renames --name-only` from C2's parent prints exactly C2's
carrier and these paths: `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`, `apps/cli/commands/mission_cmd.py`, `apps/cli/commands/worker.py`, `docs/README.md`, `docs/system/worker.md`, `packages/orchestration/ui_server.py`, `packages/orchestration/worker_queue.py`, `scripts/remedy_runtime_cli_smoke.py`, `tests/cli/test_job_stop.py`, `tests/cli/test_mission_cmd.py`, `tests/cli/test_worker_cli_runtime.py`, `tests/orchestration/test_worker_queue.py`, `tests/test_command_catalog.py`, `tests/ui_contracts/test_design_drift.py`.
`git rev-parse C2:<object>` equals the reviewer's dry run — which applied the table on
`21ab5e24` itself, the record touching none of these objects — for `apps`, `packages`, `scripts`,
`tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` in that order:
`f8e56236a1c7846783a65f393632c464d44c985e`, `206dacf8455a86d4a1c0ab104776a396b9653150`, `3e3c450e0dffcdd11abbc52b0a7b085359df38e4`, `881c267bed5cc06cb66d7fa9d5c1dbdf52e112e0`, `52e345b71419d519c98eba49cea68cc424c249ce`, `cc42698197076bc70d79a91b05ca633d7ebd2df8`, `c282d425ef909cf9257605294f23aba7d9457fac`, `60ca9975fc7ee622c78aaf9e61219ab89e210233`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`.
Report C2's insertions per constraint 5.

G4 THE SWEEP, at C2. `git ls-tree <C2> -- tests/cli/test_worker_cli_runtime.py` prints nothing,
and the same command for `packages/orchestration/worker_queue.py` prints its blob, because that
module survives. The two patterns are the `deleted` and `control` values of
`.remedy-wt/f261-block/f261-r23-gates.json`, sha256 `7016ff41de87b5723daac450e5e33f960cb34df3034588dc76576afac4697b2c`;
read them from that file in Python and pass each as one argv element to
`git grep -n -I -E <pattern> <rev> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap' ':!docs/archive'`,
never retyping them in a shell. THE DELETED WORDS: at `21ab5e24` exit 0 with 60 lines in 12
files; at C2 exit 0 with exactly 6 lines, all in `tests/test_command_catalog.py`, the ids this
round adds to `TestDeletedCommands`. THE CONTROL, which proves this round did not reach the
group DECISION F261 D22 keeps deferred: 67 lines in 11 files at `21ab5e24` AND 67 lines in 11
files at C2. Report all four counts. `python3 -m ruff check` over every `.py` path of C2 that
still exists at C2 exits 0; report how many paths that was.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r23w/wt <C2's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`,
`tests/orchestration/test_import_reachability.py` and `tests/docs/` with `-rf --tb=no`. The
mutations are the rows of `.remedy-wt/f261-block/f261-r23-mutations.jsonl`, whose sha256 must equal
`cb14d8a8895d94d8b6d999908ccd4c114620149f0227bc5f9f4ab05816557201`; each row is `[label, path, from, to, node]`, the
`from` bytes must occur EXACTLY ONCE in that path inside the worktree, and the file is restored
with `git -C .remedy-wt/f261r23w/wt checkout -- <path>` after each run. Read that carrier; never
retype its bytes. (a) CONTROL: must exit 0. Each mutation row must exit 1 with its row's node
AMONG the failed nodes. Report each exit code, summary line, number of failed nodes and each
FROM's occurrence count; then `git worktree remove --force .remedy-wt/f261r23w/wt` and read
`git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C2: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C3 and the push. `git status --porcelain` prints `''`; C0a to C3 are
single-parent commits in that order on `21ab5e24`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C3

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 6 of feature F261 · round 23 · rounds so far 23`, with one sentence of context
self-assessment. `## Commits` lists C0a to C2, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C3's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 124 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 23; and `job rerun`
with `job fulfill`, the inventory's round L.

── SLICE PLAN23 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN23 sha256=1cc5c178b4de4b26b51b7c1be2cd1ad50828b62403feefe827c87bf863e101cb
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 23 continues T003. It books round 22's PASS, registers R-0927 to R-0930 for F273 and
records DECISION F261 D22, then deletes the queue words of `job`, `worker run` and
`mission ledger` by one table. The `propose` group stays deferred, for the reasons D22 measures.

## Next Steps

1. `job rerun` and `job fulfill`, the inventory's round L.
2. The `propose` group, with the DECISION its deletion needs about the two surviving gates D22
   names, and the F011 `--status` discriminator `tests/cli/test_job_stop.py` loses with it.
3. The rest of T003 in the inventory's order, with R-0767 and R-0894.
4. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
5. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 120 findings are open by distinct id before this round's record and 124 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves two after this one, and the inventory proposes
  more than two; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput, placing the follow-up
  feature directly after F261 per amend0906.
- A deletion that would break a SURVIVING command is deferred to a round that can rule on it,
  never shipped with a finding: that is why `propose` is still not in this round.
END PLAN23

── SLICE RECORD23 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD23 sha256=7963cc8e14f84e83a1dcc54929b7f1440552d061aefcafa8f00b32e6430dcabe

Gate: F261 R22 — the F261 round 22 entry. VERDICT PASS. Written by the planner and reviewer of session 40 after reading the committed range `13128d25`..`97ba6a5b` and re-deriving every reading below; the worker's report was evidence for none of them. It is booked here by the first commit of round 23 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r22.md` at `4f68adbc` and `.agent/last_block.md` at `41ea00ea` are byte-identical to the reviewer's scratch original, sha256 `cf597cb1597c147f1746d5be14b157075fb0f29976f6b2695f125d7cc4020546`, and the table committed at `b2d4822f` is byte-identical to the reviewer's carrier, which is the research helper's with the reviewer's one amendment applied. THE STATE: at `8d417c8c` and again at `97ba6a5b`, `.agent/plan.md` equals PLAN22, `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` equal their `13128d25` blobs followed by RECORD22, DEC21 and SLIP21, and `docs/roadmap/features/T2_F273.md` equals its `13128d25` blob with the pair P273B applied; the `Gate:` count reads 130 then 131 with `Gate: F261 R21 — ` 0 then 1, the distinct registered ids 125 then 129 with the delta exactly R-0923 to R-0926, the distinct `Done:` ids 8 then 9 with the one added exactly R-0900, and the open set 117 then 120. THE TABLE COMMIT: at `b2d4822f` the `apps`, `packages`, `scripts`, `tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` objects equal the reviewer's dry-run commit object for object, all nine, so the worker reproduced exactly the tree the reviewer tested; the path set is the dry run's nineteen plus the carrier, and `git show --numstat` reads 125 insertions against 1030 deletions, under the 500 cap. THE SWEEP: the deleted-word pattern reads 78 lines in 15 files at `13128d25` and exits 1 with no output at `97ba6a5b`, `apps/cli/commands/repair_cmd.py` is absent from the tree while `packages/orchestration/repair_loop.py` is present at blob `05433190`, and THE CONTROL that proves this round did not reach the group DECISION F261 D21 defers reads 60 lines in 12 files at both revisions. THE RED-PROOFS ran in the reviewer's own worktree on the tree whose objects the table commit reproduces: a control of 357 passed at exit 0, and each of the four rows of the mutation carrier `04d1f2c3440c8442d1a4d979aeacd2086749e970517bcb215d625d1abcded96a` exiting 1 with its named node among the failures — re-inserting a `repair` catalog entry, restoring the allowlist line of the deleted handler, restoring the `remedy repair propose` hint in `packages/orchestration/mission_readiness.py`, and restoring the present-tense `repair start` invocation in `docs/system/repair-loop-v0.md`; every FROM occurred exactly once in the file its row names. THE REVIEWER'S RUN in the primary checkout at `97ba6a5b` of the round's own test files, the files nearest every production module it touched, `tests/cli/test_golden_path.py`, the whole of `tests/docs/`, `tests/cli/test_propose_cli.py` as a control on the deferred group, `tests/ui_server/test_dashboard_cockpit_truth.py` and `tests/orchestration/test_evidence_index.py` read 1193 passed, and `python3 -m ruff check` over the eight edited files that survive printed `All checks passed!`. The worker ran the full suite once in the primary checkout, as the block orders: exit 0, `17681 passed, 23 skipped, 1 warning in 1280.58s`, with no line-initial `FAILED ` or `ERROR ` in the transcript. The open set reads 120 by distinct id at `97ba6a5b`.

- R-0927 — Low, QUEUEING A JOB AND RUNNING THE LOCAL WORKER HAVE NO HEIR, AND THE QUEUE AND TASK-EXECUTION FUNCTIONS KEEP ONLY TEST CALLERS. Raised by the planner and reviewer of session 41 while preparing F261 round 23, from readings its research helper took at `21ab5e24` and the reviewer re-took on its own dry-run tree, after searching the open set for the queue, the worker and the lease under §3 item 30: no open finding describes it; R-0904 names the queued GOAL of the deleted `queue` group and F048 binding, and R-0857 names worker words that round 23 does not touch. THE DEFECT, read at `21ab5e24`: `job enqueue`, `job pause`, `job cancel`, `job resume-queue` and `worker run` were the only production route into `packages/orchestration/worker_queue.py`'s queue, and this round deletes them under DECISION amend0905-vocab D4. Measured by the helper against a scratch data root: `worker run --once --provider fixture` ran a job's materialized task through `execute_task` to `task_completed`; read in the code at `21ab5e24`, the same path leases the entry with `claim_job`, marks expired leases stale with `detect_stale`, and `get_next_job` passes over paused, cancelled and proposal-blocked entries. `remedy job run <id>` runs pending tasks through the ping-pong loop and reads no queue, and `remedy job stop <id>` writes a safe-point stop request against the job record and touches no queue entry, so neither is an heir. After the table, `run_worker_once` and `run_worker_loop` have no production caller, and `enqueue_job`, `pause_job`, `cancel_job`, `resume_queued`, `get_next_job`, `_has_unresolved_proposals`, `claim_job`, `update_heartbeat`, `transition_state`, `release_lease`, `detect_stale`, `validate_provider`, `export_worker_result_json` and `is_valid_transition` are named in production only inside `worker_queue.py` itself, while `execute_task`, `BudgetGate` and `TaskExecutionRequest` in `packages/orchestration/task_execution.py` and `run_autorun` in `packages/orchestration/autorun.py` are named in production only by `worker_queue.py`. The modules stay whole under DECISION F261 D17's rule, because `worker status` and the cockpit's worker section still import `get_worker_status`, `list_queued` and `export_worker_status_json`. WHY LOW: an opt-in local execution path leaves, and no surviving command prints anything false about it. WHY F273's: deciding whether the queue has a word again or leaves with its modules is paydown, and F261 renames and prunes. FIX: either record by DECISION that `job run` and `job stop` replace the queue and delete the queue functions, `task_execution.py` and `run_autorun` with their tests, or give the queue a surviving word with a test that runs one queued job. Owner: F273.

- R-0928 — Low, `remedy worker status` AND THE COCKPIT'S WORKER SECTION READ A STATUS FILE AND A QUEUE THAT NOTHING WRITES ANY MORE. Raised by the planner and reviewer of session 41 while preparing F261 round 23, after searching the open set for the worker status file and the cockpit worker section under §3 item 30: no open finding describes them; R-0926 records the same CLASS for the two repair sections and names neither of these. THE DEFECT, read at `21ab5e24`: `worker_status.json` is written only by `_save_worker_status`, which only `run_worker_once` calls, and the queue directory only by the queue functions R-0927 names; this round deletes their last production callers. `remedy worker status`, a word D4 keeps, and `_build_worker_section` in `packages/orchestration/ui_server.py` both read them. Measured by the helper on the applied tree against a fresh data root: the command prints `Worker: (none)` and `State: idle`, the defaults `get_worker_status` returns when the file is absent, and the section reads `worker_available` false and a queue count of 0. The table empties the section's `next_command`, which named the deleted `worker run`, rather than leaving a hint no catalog entry answers. WHY LOW: a surviving word reports an idle worker for ever, which is true of a tree with no worker, and nothing else is affected. WHY F273's: giving the command a real source or deleting the section with its client mapping changes a surviving surface. FIX: either make `worker status` and the section read the job runner's own live state with a test that sees a running job, or delete both by DECISION with the cockpit-truth fixtures that pin them. Owner: F273.

- R-0929 — Low, READING A MISSION'S WHOLE DECISION LEDGER HAS NO READ-ONLY HEIR. Raised by the planner and reviewer of session 41 while preparing F261 round 23, after searching the open set for the mission ledger under §3 item 30: no open finding describes it. THE DEFECT, read at `21ab5e24`: the deleted `mission ledger <id>` printed the mission's goal, the number of iterations recorded and every ledger entry across every run, read-only, and its `--json` view carried the entries. Inventory ruling 6 names the ledger `mission run` prints as its heir, and the reviewer read that against the code at `21ab5e24`: `_cmd_mission_run_loop` in `apps/cli/commands/mission_cmd.py` renders only `result.entries`, the iterations of the run it is executing, and it appends new entries while doing so, so it is neither complete nor read-only. The table replaces the run's `Full ledger:` hint, which named the deleted word, with the ledger file's path from `ledger_path`. WHY LOW: a read-only view leaves and the data it showed stays on disk at the path the run now prints. WHY F273's: adding a section to a surviving mission view changes what that view does. FIX: a ledger section on `remedy mission show`, with a test that renders entries from two earlier runs without appending one. Owner: F273.

- R-0930 — Low, `remedy mission run` PRINTS THE ITERATIONS OF ITS OWN RUN WITH AN EMPTY TIMESTAMP. Raised by the planner and reviewer of session 41 while preparing F261 round 23, from a reading its research helper offered and the reviewer confirmed in the code, after searching the open set for the ledger timestamp under §3 item 30: no open finding describes it. The defect predates this round. THE DEFECT, read at `21ab5e24`: `_record` inside the orchestrator loop of `packages/orchestration/orchestrator_loop.py` builds a frozen `LedgerEntry` whose `recorded_at` defaults to the empty string, passes it to `append_ledger_entry`, which stamps the time only on the body it writes to disk, and then appends the unstamped entry to `result.entries`; `render_ledger` prints `at ` followed by `recorded_at`, so every entry `mission run` prints ends in `at` and nothing. The deleted `mission ledger` read the stamped copy from disk, so until this round a reader had a route to the time. WHY LOW: a cosmetic gap in a printed audit line; the stored ledger is correct. WHY F273's: it is a behaviour fix in a surviving command, which F261's Do-not-touch section excludes. FIX: carry the stamped body back into `result.entries`, with a test that asserts a non-empty time in the printed ledger of a `mission run`. Owner: F273.
END RECORD23

── SLICE DEC22 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC22 sha256=ce0a95819423b60f59746a6fe8bc89c6130c129217b8531bedc635f13e6b6a7b

## DECISION F261 D22 (2026-09-16, F261 round 23) — the deletion paragraph of the queue words of `job`, of `worker run` and of `mission ledger`, and why `propose` is still not in this round

CONTEXT. DECISION amend0905-vocab D4 keeps `worker` as `list`, `show`, `resources`, `unload`, `status` and `doctor`, gives `job` no queue word and gives `mission` no `ledger`, and `.agent/f261_t003_inventory.md` puts all six words in its round K. This round takes round K ahead of the `propose` half of round I that DECISION F261 D21 deferred, on a measurement: at `21ab5e24` the only production caller of `get_next_job`, and so of the `_has_unresolved_proposals` skip D21 named, is `run_worker_once`, which only `worker run` reaches. Measured by the reviewer's research helper in its own detached worktree, running every word in process against a scratch data root, and re-applied by the reviewer on its own dry-run tree, whose nine tree objects equal the helper's.

CHOSEN, FIRST: `job enqueue`, `job pause`, `job cancel`, `job resume-queue` and `worker run` go — their catalog entries, their handlers in `apps/cli/commands/job.py` and `apps/cli/commands/worker.py`, `tests/cli/test_worker_cli_runtime.py`, the catalog tests that pinned them, the `worker` mode of `scripts/remedy_runtime_cli_smoke.py`, and the two hints inside `run_worker_once` and the cockpit worker section's `next_command` that named deleted words; `docs/system/worker.md` stays under a dated banner in the past tense. THE HEIR: none for the queue itself. `job run` runs a job and `job stop` stops a running one at its next safe point, and neither reads the queue; R-0927 records the loss and R-0928 the two surviving readers of the files nothing writes now.

CHOSEN, SECOND: `mission ledger` goes with its handler and its tests. Inventory ruling 6 named the ledger `mission run` prints as the heir, and the reviewer read that against the code and found it partial — the run prints only its own iterations and appends while it does — so the run's `Full ledger:` hint now prints the ledger file's path, R-0929 records the missing read-only view, and R-0930 records the empty timestamp the run's own print carries, a defect older than this round.

CHOSEN, THIRD: NO package module and NO package symbol is deleted, which is DECISION F261 D17's rule. `packages/orchestration/worker_queue.py` keeps `worker status` and the cockpit's worker section as production importers, so the queue functions that become test-only are named in R-0927 rather than cut from a surviving module.

CHOSEN, FOURTH: the `propose` group STAYS DEFERRED, and this is the ruling the next `propose` round inherits. With `worker run` gone the gate D21 named has no production caller, but the helper's reading of the applied tree, which the reviewer confirmed in the code, finds two further SURVIVING gates on the proposal store. `self execute` refuses any proposed task whose status is not approved-for-build, and only the `propose` group's evaluate and approve words write that status. And the cockpit's job phases call `can_finalize` from `packages/orchestration/proposed_tasks.py`, which holds Build and Finalized at pending while any proposal is unresolved, so a job for which `self propose` or `job fulfill` wrote a proposal would never read finalized. Deleting `propose` would therefore still break surviving surfaces, and the round that takes it owes a DECISION on both gates and the feature-file amendment §4 item 7 requires.

CONSEQUENCE. `remedy job enqueue`, `remedy job pause`, `remedy job cancel`, `remedy job resume-queue`, `remedy worker run` and `remedy mission ledger` are unknown words and their ids join `TestDeletedCommands`; the catalog reads 30 groups and 155 commands. Four losses are recorded as R-0927 to R-0930 rather than replaced by a stub. HOW TO REVERSE: revert the round's table commit and delete this section.
END DEC22

── SLICE P273C-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273C-FROM sha256=1bec7f277852dd25fc6b3f1417420caa47eaf59c559c192476de03fa226f4f51
  with their fixtures, or the ruling that gave their stores a writer again.

## Do not touch
END P273C-FROM

── SLICE P273C-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273C-TO sha256=47ddf51384e8f332d4391a65d7918032be09f6746f2cfa12c75c5dd7da99fe79
  with their fixtures, or the ruling that gave their stores a writer again.
- R-0927 carries a resolution line naming the DECISION and the commit that deleted the queue functions,
  `task_execution.py` and `run_autorun` with their tests, or the surviving queue word with its test.
- R-0928 carries a resolution line naming the commit that gave `worker status` and the cockpit worker
  section a live source with its test, or the commit that deleted both with their fixtures.
- R-0929 carries a resolution line naming the surviving view that renders a mission's whole ledger
  read-only, with its test.
- R-0930 carries a resolution line naming the commit that printed a timestamp for every iteration
  of a `mission run`, with its test.

## Do not touch
END P273C-TO
