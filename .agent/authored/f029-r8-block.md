STEP F029 R8 — BOOK R7, RECORD D7, AND NOTE A RERUN IN ITS MISSION'S DOSSIER: the feature file's last edge case, a rerun of a mission's job read into the dossier's DECISIONS at the loop's next refresh

GOAL
Round 7 passed. Book its gate entry, record DECISION F029 D7, and land the edge case the feature
file names and no round has built yet: under a mission, the dossier notes the rerun. Every subtree
rerun of one of the mission's jobs becomes one DECISIONS item, read from that job's own `reruns`
record whenever `refresh_mission_dossier` advances the dossier. A mission without a rerun keeps a
byte-identical dossier. The closure sequence follows this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code and tests against S1 and S2. Read DECISION F029 D7 (it arrives with C2) and, whole:
`packages/orchestration/mission_dossier.py` from `PLAN_RISK_ID_TEMPLATE` down to the end of
`refresh_mission_dossier`, together with `DossierItem`, `IterationFacts`, `_merge_by_id` and
`dossier_sections`; `tests/orchestration/test_mission_dossier.py`; and in
`packages/orchestration/subtree_rerun.py` the record `fold_subtree_rerun` appends to `job.reruns`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f029-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f029-r8/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f029-r8-sim/`, `.remedy-wt/f029-r8-dry/`, `.remedy-wt/f029-r7-sim/`,
  `.remedy-wt/f029-r7-dry/` and `.remedy-wt/f029-review/`: the reviewer's; do not touch or read them.
  `.remedy-wt/f029-r8-worker/`    YOURS for logs and scripts; create it if absent. Gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f029-subtree-rerun`, and `git log --oneline -1` must read `a5933b73`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f029-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f029-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 52 | 12822 | 2aac7defedfab8ff85ed0625483484a29d82968abe859a4aa97f1cad6b6759ae |
| plan.md | 31 | 1086 | 1243204d604ff092bfe26b0357bb03141ab9d502887d6a7b9aa1e343a756710f |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer generated
it with `git diff HEAD` from a tree at `a5933b73`. It appends round 7's gate entry to
`.agent/live_review.md` and DECISION F029 D7 to `.agent/decisions.md`.

THE SPECIFICATION — all of it in `packages/orchestration/mission_dossier.py`, placed beside the
code it extends, each new name with the one-line WHY comment or docstring AGENTS.md asks for.
S1 THE ITEMS. (a) `RERUN_ID_TEMPLATE = "RR-{job}-{rerun}"` directly after `ITERATION_ID_TEMPLATE`.
   (b) `rerun_decision_items(job_reruns)` takes `(job_id, record)` pairs and answers one
   `DossierItem` per pair, in order, reading every field defensively: a record that is not a
   dict, or whose `rerun_id` or `root_task_id` is missing or empty, is skipped; with `n` = the
   length of the record's `subtree` list minus one (0 when it is not a list or tuple, never below
   0), `root` its `root_task_id`, `job8` = `job_id[:8]`, `reset12` = the first twelve characters
   of its `reset_commit` ("" when missing) and `override` = `record["model"]["override"]` when
   `model` is a dict and that value a non-empty string: id `RERUN_ID_TEMPLATE.format(job=job8,
   rerun=<the rerun_id>)`; text `f"rerun of task {root} and {n} task{'' if n == 1 else 's'} after
   it on job {job8}"`; `resolved=True`; outcome `f"reset to {reset12}, run on {override}"` when
   there is an override, else `f"reset to {reset12}, the job's own model"`.
S2 THE SOURCE. `mission_job_reruns(mission, root=None)` answers, for each id of
   `mission.job_ids()` in order, `(job_id, record)` for every dict in that job's `reruns`, in
   order, loading the job with `load_job_plan(job_id, root)` imported INSIDE the function, as the
   module already imports `orchestrator_loop` inside its functions; a job that loads as None is
   skipped.
S3 THE WIRING. `mission_iteration_facts` gains the keyword `reruns: Sequence[tuple[str, dict]] =
   ()`, and its decisions become the ledger's items followed by `rerun_decision_items(reruns)`; its
   docstring names the job's `reruns` record as the third source. `refresh_mission_dossier` passes
   `reruns=mission_job_reruns(mission, root)`. Nothing else in the module changes.

THE TESTS — appended to `tests/orchestration/test_mission_dossier.py` as new classes that reuse its
existing fixtures and constants; no existing test is edited. `rerun_decision_items`: an override
and no override, a blank override read as none, the singular with one task after the root and the
plural with none and with two, a non-dict record and records missing `rerun_id` or `root_task_id`
skipped, missing optional fields read as "" and 0, and several records kept in order.
`mission_iteration_facts`: reruns follow the ledger's items, and `reruns=()` equals the facts
built without the keyword. `mission_job_reruns`: two reruns of one job in order, and an unknown job
id skipped without raising. End to end: a real mission with one linked job whose saved record
(`save_job_plan`) carries a `reruns` entry; `refresh_mission_dossier`, then `render_dossier_body`
of the answered dossier holds the item's id and its text.

BUNDLE — the commits are C1 to C5, in this order.
C1 — `.agent/authored/f029-r8-block.md` := this block, `.agent/authored/f029-r8-booking.diff` and
  `.agent/authored/f029-r8-plan.md` := the payloads, by `shutil.copyfile`.
  Subject: `F029 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 83. Report the number you measure.
C2 — `git apply` booking.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F029 R8 C2: book round 7 and record D7`
  Expected by `git show --numstat`: 34/0 decisions.md, 2/0 live_review.md, 5/9 plan.md.
C3 — S1 to S3 with THE TESTS. Subject: `F029 R8 C3: note a rerun in its mission's dossier`
C4 — `.agent/authored/f029-r8-mutations.py` (G5). Subject: `F029 R8 C4: add the round 8 mutation tool`
C5 — `.agent/handoff.md` per `docs/agents/handback_template.md`. Subject: `F029 R8 C5: rewrite handoff for round 8`
  Then `git push origin feature/f029-subtree-rerun` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C3 before you commit
   it; if it would reach 500, the tests become their own commit after the code, each leaving G4's
   selection green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f029-r8-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/mission_dossier.py`, `tests/orchestration/test_mission_dossier.py` and
   `.agent/handoff.md`. Report `git diff --name-only a5933b73` after C5. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test THIS round wrote that is wrong may be corrected
   before C5, and the correction is declared. An existing test that goes red is reported, and you
   stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F029 one full-suite run, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; then
 each `.agent/authored/f029-r8-*` copy read back with `git show <C1>:<path>` compared byte for byte
 with its source (the block copy against `.remedy-wt/f029-r8/block.md`). One reading per copy.
G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2305437 | 3b5d7d9a94aaa3c50bee1f3380c79d2183a8fe419aa956440aae0d0ec1c90eea |
 | .agent/live_review.md | 332588 | da9d083a9deddd4f9b8ae2607fa92289e1d138ddb0ad4c82fbacd5b2952d4953 |
 | .agent/plan.md | 1086 | 1243204d604ff092bfe26b0357bb03141ab9d502887d6a7b9aa1e343a756710f |
 Also `open_finding_ids` over the ledger's text at `a5933b73` and at C2 (the reviewer read `[]` at
 both), and `git diff --name-only <C1> <C2>`, which must name exactly the paths of the table.
G3 THE CODE — `python3 -m ruff check packages/orchestration/mission_dossier.py
 tests/orchestration/test_mission_dossier.py` at C4 with its real exit code; then quote from the
 diff `rerun_decision_items`, `mission_job_reruns`, and the changed lines of
 `mission_iteration_facts` and `refresh_mission_dossier`.
G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_mission_dossier.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_handoff.py tests/orchestration/test_subtree_rerun_prepare.py tests/orchestration/test_subtree_rerun.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `a5933b73` and read
 `933 passed, 7 skipped` at real exit code 0; the seven skips are F252 quarantines. Report every
 `SKIPPED` line and account for any difference from 933 beyond the nodes this round adds: the
 reviewer read `104 tests collected` from `python3 -m pytest --collect-only -q -p no:cacheprovider
 tests/orchestration/test_mission_dossier.py` at `a5933b73`; report the same command at C4. Then
 `python3 -m apps.cli.main integrity check --json`: every check's status and `fail_count`.
G5 THE RED PROOFS — your tool `.agent/authored/f029-r8-mutations.py` takes a worktree path. It runs
 `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_dossier.py` with the
 worktree as working directory and an environment of the tool's own plus `PYTHONPATH` = the
 worktree and `PYTHONDONTWRITEBYTECODE` = "1", after purging every `__pycache__` directory under
 the worktree, and first prints `__file__` of `packages.orchestration.mission_dossier` under that
 environment, which must lie inside the worktree. Each mutation edits `mission_dossier.py` INSIDE
 the worktree (its FROM text asserted to occur exactly once) and is restored. Unmutated controls
 run first and last. It counts failures from the distinct `FAILED ` lines, prints one line per
 mutation (label, exit code, failed count, the failing tests' names) and ends with `restored
 byte-identical: True`, the PRIMARY checkout's `git status --porcelain` (which must be empty) and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `rerun_decision_items` answers an empty list whatever it is given;
  m2 the outcome always reads "the job's own model";
  m3 `refresh_mission_dossier` no longer passes `reruns`;
  m4 the text's plural suffix is always "s".
 Run it: `git worktree add --detach .remedy-wt/f029-r8-mut <C4>`, then
 `python3 -B .agent/authored/f029-r8-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f029-r8-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, then you add the test that catches it before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f029-r8-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.
G6 TREE AND PUSH — after C5: `git status --porcelain`, empty; `git log --oneline -n 6`;
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected, every gate's real output and exit code, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per S-item), the deviations, and the next expected action. Your Session section reads SESSION 2
of feature F029, round 8, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 8, then the closure sequence. State the open-findings count, 0, and the operator-questions
count, 0.
