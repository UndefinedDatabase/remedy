STEP F026 R1 — CLAIM F026 AND LAND T001: the runtime task edit's state gate, versioned in-place apply, spec archive, approval seal and failed-to-pending reset

GOAL
Pull request 280 is merged; `main` is at `90555849` and F026 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F025's round 11 verdict, record DECISION
F026 D1, and land T001: `TaskEntry` gains a persisted `spec_version`, and a new module
`packages/orchestration/task_edit_runtime.py` edits one task of an approved plan at runtime — the
state gate, the plan editor's own edit applied in place, the prior spec archived, the approval seal
following the edit, and a failed task reset to pending — with its unit tests in
`tests/orchestration/test_task_edit_runtime.py` and a mutation tool proving the tests bite.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against the specification S1 to S10 below. Only the
`.agent/` records and the STATUS line travel as payloads.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f026-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f026-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f026-r1-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f026-r1-drafts/`    The reviewer's drafts; do not touch them.
  `.remedy-wt/f026-r1-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `90555849`. Report all three. Then
   `git checkout -b feature/f026-task-edit-runtime` and report the branch. Do NOT pull: the Open
   PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f026-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f026-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 162 | 19066 | 6743772dbd62984b4b0c8f600ce5695436e1dbfb5e7522b4d15af56ebc985def |
| context.md | 39 | 1729 | 89abf24a2c7df9523ce0e5b65df41dc75c2e09cfb5773df3857465acba026006 |
| plan.md | 36 | 1367 | 120e6b858a7a736cd6b2f5d8c780ebc5f59763b7986cbb288d82929b78e8726c |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`90555849` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F025's round 11 gate entry
appended), `docs/roadmap/STATUS.md` (F026's line `[ ]` to `[~]`) and `.agent/decisions.md`
(DECISION F026 D1 appended). Read D1 before you write code: it is the design this specification
implements, and it records what was measured at `4cb6b970`.

THE SPECIFICATION
S1 THE FIELD. `TaskEntry` in `packages/orchestration/pingpong_job.py` gains
   `spec_version: int = 1`, with a one-line comment above it naming DECISION F026 D1. `_export_job`
   writes it on every task as `"spec_version"`, and `_import_job` reads it back as an `int`,
   defaulting to 1 when the key is absent, so a record written before F026 loads at version 1.
   Nothing else in that file changes.
S2 THE MODULE. A NEW FILE at `packages/orchestration/task_edit_runtime.py`, with a docstring naming
   DECISION F026 D1 and stating, in a sentence each, why the edit is the plan editor's own
   `plan_edit_task` and why it is refused while the job runs. It imports `apply_edit`,
   `plan_edit_lock`, `plan_version`, `PlanEditRefused`, `EDIT_LOG_KEY`, `EDIT_LOG_EVIDENCE` and
   `EDIT_LOG_SCHEMA_V` from `packages/orchestration/plan_editing.py`, and edits that file only as S9
   says. No import of `subprocess`, `signal` or `threading`.
S3 THE STATE GATE, pure — no I/O:
   `RUNTIME_EDITABLE_STATES = ("waiting", "paused", "failed")`.
   `runtime_edit_state(job_state, approval, task_status, *, task_paused) -> str` returns one of
   those three names or raises `PlanEditRefused`, reading states by their string value (a
   `RunState` or a plain string). In this order: a job state of `running` raises
   `job_not_editable`, and so does a terminal one, `completed`, `failed` or `cancelled`; an
   approval of `pending` or `rejected` raises `plan_not_editable`; then a task status of `pending`
   is `paused` when `task_paused` is true and `waiting` otherwise, a status of `failed` or
   `blocked` is `failed`, and EVERY other status raises `task_not_editable`. Every refusal's
   `detail` names the state or status it refused.
S4 THE EDIT, `edit_task_at_runtime(job_id, task_id, fields, *, expected_spec_version, actor,
   root=None) -> TaskEditResult`, where `task_id` is the `TaskEntry`'s own id, the one a task pause
   file is keyed by. Under `plan_edit_lock(job_id, root)`, as ONE transaction:
   load the record with `require_job_plan(job_id, root)`; refuse `no_task_plan` when it has no
   stored plan with tasks; take `task_paused` as true when the job's state is `paused` or when
   `pause_control.paused_tasks(job_id, control_root_path=safe_points.control_root(root))` holds an
   entry for `task_id` (read it only for a `pending` task); find the entry by `task_id`, refusing
   `unknown_task` when none matches and `not_a_plan_task` when its `inputs["plan"]` carries no
   `planned_id`, and `unknown_task` when the stored plan has no task with that planned id; apply
   S3; refuse `version_conflict`, with `current_version` the entry's spec version, when
   `expected_spec_version` differs from it; then `apply_edit(plan, "plan_edit_task",
   {"task_id": <planned id>, "fields": fields})`, any refusal of which is re-raised with
   `current_version` set to the entry's spec version. A refusal of ANY kind writes nothing: the
   record's bytes, the evidence export directory and the archive are untouched.
S5 THE ARCHIVE, written after the edit has validated and BEFORE the record is written: create-only,
   under `task_specs/` in `job_evidence_export_dir(job_id, root)`, named `<planned id>.v<n>.json`
   when the planned id matches `[A-Za-z0-9][A-Za-z0-9_-]{0,63}` and
   `<first 32 hex chars of sha256(planned id)>.v<n>.json` otherwise, where `<n>` is the entry's
   spec version BEFORE the edit. It holds the plan task as it stood (`model_dump()`), the entry's
   `title` and `acceptance`, `task_id`, `planned_id`, `spec_version` n, the editable `state`, and
   `archived_at`. An existing file of that name whose JSON equals the new payload apart from
   `archived_at` is kept as it is (a crash between the archive and the record write); any other
   existing file refuses `spec_archive_conflict` and writes nothing. An archived spec is never
   rewritten.
S6 THE WRITE, one `save_job_plan(job, root)`: the stored plan becomes the edited plan's
   `model_dump()` plus every `_`-prefixed key of the old body; `_version` is raised by one; ONE
   entry is appended to `_edits` — `version`, `ts`, `actor`, `command` `"plan_edit_task"`, `args`
   exactly as passed to `apply_edit`, `before` and `after` as whole task lists as `edit_plan` logs
   them, and a `runtime` object holding `task_id`, `planned_id`, `state`, `spec_version` (the new
   one), `status_before`, `status_after`, `restored` (the ids S7 returned to `pending`, in plan
   order), `approved_plan_sha256_before`, `approved_plan_sha256_after` and `archive` (the archive's
   path relative to the export directory). When the approval is `approved` and records
   `_approved_plan_sha256`, that key becomes `plan_content_hash` of the new body. THE ENTRY IS
   UPDATED IN PLACE: from the edited plan's tasks mapped by `map_task_plan_to_tasks` and
   `record_llm_task_deliverables`, the one whose planned id matches gives the entry its `title`,
   its `acceptance` and the `inputs` keys that mapping wrote (`plan`, and `deliverable` when set);
   every other field and every other `inputs` key of the entry is kept, and its `spec_version` is
   raised by one. No other `TaskEntry` changes except as S7 says.
S7 THE RESET, in that same write, for the `failed` state only: the entry's status becomes
   `pending` and its `error` becomes `""`; and every entry AFTER it in the job's task order whose
   status is `skipped` becomes `pending`. A `waiting` or `paused` task keeps its status.
S8 AFTER THE WRITE, outside the lock, as `edit_plan` does: `write_plan_md` for the new plan version
   with the edit log, and the edit log's export `EDIT_LOG_EVIDENCE`. Then return
   `TaskEditResult`, a frozen dataclass of `job_id`, `task_id`, `planned_id`, `state`,
   `spec_version`, `plan_version`, `entry` (the log entry), `archive_path` and `restored`.
   Also add `task_spec_versions(job_id, planned_id, *, root=None) -> tuple[dict, ...]`: every
   archived spec of that planned id, parsed, in ascending version order; empty when none exists.
S9 `PlanEditRefused`'s docstring in `plan_editing.py` gains one sentence naming the codes
   `task_edit_runtime` raises that it does not list — `job_not_editable`, `task_not_editable`,
   `not_a_plan_task` and `spec_archive_conflict`. No other line of `plan_editing.py` changes.
S10 THE ORPHAN GUARD. Nothing imports the new module until T002 wires it into the door and the CLI,
   so `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py` gains its entry, with the reason
   "F026 T001: the runtime task edit backend; T002 wires it into the write door and the CLI".
   T002 removes it.

THE TESTS — a NEW FILE at `tests/orchestration/test_task_edit_runtime.py`, against a data root under
`tmp_path` (monkeypatch `REMEDY_DATA_DIR` as `tests/orchestration/test_plan_editing.py` does, and
build the job the way its `_save_job` does, with the approval `approved` and the hash
`consume_plan_approval` would record). It must cover at least: S3 as a parametrized matrix over
every task status constant in `pingpong_job` (`TASK_*`) plus the pending-and-paused row, and every
job state of `RunState`, each refusal's code and that its detail names the state; S4 through the
module for a waiting, a paused (by a task pause file, and by a paused job) and a failed task, and
for a `blocked` one; a refused running, passed and applied task leaving the record's bytes, the
export directory and `task_specs/` unchanged; a revalidation refusal (an empty acceptance list)
and an unknown field changing nothing; `version_conflict` with the current version; an unknown
task and a task without a planned id; S5's archive path and content, a second edit writing
`.v2.json` and leaving `.v1.json` byte-identical, the equal-archive crash case accepted, the
conflicting archive refused with nothing written, and a planned id with `/` stored under its
digest name; S6's in-place update keeping `task_id`, `run_id`, `repair_rounds_used` and a foreign
`inputs` key, the prompt fields `title` and `acceptance` carrying the new goal and criteria,
`spec_version` 2 then 3, `_version` raised, the `runtime` object's every key, `replay_edits` over
the stored `_edits` reconstructing the stored plan, and `approved_plan_mismatch` reading None after
the edit; S7's reset of a failed and of a blocked task with `error` cleared and the skipped tasks
after it restored while a skipped task BEFORE it stays skipped; S8's `plan_v<n>.md` and export
written; and S1's round trip of `spec_version` through `save_job_plan` and `load_job_plan`, and a
record with no `spec_version` key loading at 1.

BUNDLE — the commits are C1a, C1b, C2, C3a, C3b, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f026-r1-block.md` := this block, and `.agent/authored/f026-r1-plan.md` and
  `.agent/authored/f026-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F026 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 75. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f026-r1-claim.diff` := claim.diff.
  Subject: `F026 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 162.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F026 R1 C2: claim F026, re-head the live review record, book F025 R11, record D1`
  Expected by `git show --numstat` (insertions and deletions): 16/12 context.md, 77/0 decisions.md, 24/25 live_review.md, 23/14 plan.md, 1/1 STATUS.md.

C3a — THE FIELD: S1, in `packages/orchestration/pingpong_job.py` only.
  Subject: `F026 R1 C3a: persist a per-task spec version on the task entry`

C3b — THE MODULE: S2 to S10 — `packages/orchestration/task_edit_runtime.py`, `git add`ed (an
  untracked module fails `integrity check`'s `relevant_untracked`), the docstring sentence in
  `packages/orchestration/plan_editing.py`, and the `ALLOWED_UNWIRED` entry.
  Subject: `F026 R1 C3b: add the runtime task edit with its state gate, archive and reset`

C4 — THE TESTS AND THE MUTATION TOOL: `tests/orchestration/test_task_edit_runtime.py`, and your
  mutation tool (G5) saved as `.agent/authored/f026-r1-mutations.py`.
  Subject: `F026 R1 C4: test the runtime task edit and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F026 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f026-task-edit-runtime`. Do NOT create a pull request: the
  branch opens one at F026's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f026-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/task_edit_runtime.py`, `packages/orchestration/plan_editing.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/test_task_edit_runtime.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 90555849` and the
   branch tip after C5. Do NOT touch `packages/orchestration/pause_control.py`,
   `packages/orchestration/job_plan.py`, `packages/orchestration/ui_server.py`,
   `apps/cli/command_catalog.py`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md` or `docs/roadmap/features/T5_F026.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4 (`.remedy-wt/f026-r1-dry` and the older `f015-*`, `f020-*`, `f023-*`,
   `f024-*`, `f025-*` and `f284-*` ones), and every existing stash alone. The worktree G5 adds goes
   under `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F026's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f026-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f026-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its authoring tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 313268 | f52e411c6c7b92b7a8fc9559e15cb6c1cbc39e31ab95ed02a07b1273314647d8 |
 | docs/roadmap/STATUS.md | 52501 | 2efac767f5287a635edf2c67508d539a7f7fc52b3978d7bccfe1017e4f876980 |
 | .agent/decisions.md | 2127334 | 11c5bc0880af1bb26f2d5af82d2217b8a539f7566462ad35be3fa41cdac76d4b |
 | .agent/plan.md | 1367 | 120e6b858a7a736cd6b2f5d8c780ebc5f59763b7986cbb288d82929b78e8726c |
 | .agent/context.md | 1729 | 89abf24a2c7df9523ce0e5b65df41dc75c2e09cfb5773df3857465acba026006 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `90555849` and at C2 (the reviewer read
 R-1008, R-1055, R-1057 and R-1058 at both); at C2 the ledger has exactly one line reading
 `## Findings` and exactly one reading `## Steps`, and its last line begins `Gate: F025 R11 — `;
 F026's STATUS line at C2 read back in full, which must read
 `- [~] F026 — Task edit at runtime`; and `git diff --name-only <C1b> <C2>`, which must name
 exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/pingpong_job.py
 packages/orchestration/task_edit_runtime.py packages/orchestration/plan_editing.py
 tests/test_no_orphan_modules.py tests/orchestration/test_task_edit_runtime.py` at C4;
 `git diff --numstat <C2> <C3a>`, which must name `packages/orchestration/pingpong_job.py` alone;
 `git diff -U0 <C3a> <C3b> -- packages/orchestration/plan_editing.py`, reported whole, which must
 touch only `PlanEditRefused`'s docstring; and a python `ast` reading at C4 of every module the new
 module imports (each `Import` and `ImportFrom` node), which must name none of `subprocess`,
 `threading` or `signal`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_plan_editing.py tests/orchestration/test_plan_edit_execution.py tests/orchestration/test_job_plan.py tests/orchestration/test_pause_control.py tests/orchestration/test_pause_resume.py tests/orchestration/test_job_administrative_fields.py tests/orchestration/test_unified_store_parity.py tests/orchestration/test_job_state_field.py tests/orchestration/test_run_contract.py tests/test_no_orphan_modules.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/orchestration/test_import_reachability.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the new test file and the golden path, serially,
 inside its authoring tree carrying the claim's records, and read `841 passed, 3 skipped` at real exit code
 0. TWO of those skips are toolchain nodes a worktree cannot run and the primary checkout can, and
 each must PASS in your run, not skip: the typescript node in
 `tests/ui_server/test_dashboard_contract.py` (`tsc --noEmit`) and the vitest node in
 `tests/orchestration/test_test_runner.py`. The third, the D12 quarantine in
 `tests/test_agent_tooling.py`, stays skipped. Report every `SKIPPED` line the `-rs` summary
 prints, the number of nodes your new file contributes (`--collect-only -q` on it), and account
 for any other difference from the reviewer's count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f026-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/orchestration/test_task_edit_runtime.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and last
 and ends with `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations, each a real behaviour change:
  m1 the gate admits a `running` job;
  m2 the gate admits a `completed` job;
  m3 the gate admits a `pending` approval;
  m4 the gate admits a `running` task;
  m5 the gate admits an `applied_to_job_workspace` task;
  m6 the gate refuses a `blocked` task;
  m7 a pending task with a task pause file reads `waiting`;
  m8 a stale `expected_spec_version` is accepted;
  m9 the entry is replaced by the freshly mapped one instead of updated in place;
  m10 `spec_version` is not raised;
  m11 the archive is written before the edit validates, so a refused edit leaves one;
  m12 an existing archive with other content is overwritten;
  m13 the approval hash is not re-stamped;
  m14 a failed task keeps its status;
  m15 the skipped tasks after the reset task stay skipped;
  m16 every skipped task is restored, including one before the reset task;
  m17 the log entry's `command` is not `plan_edit_task`;
  m18 `_export_job` drops `spec_version` (in `pingpong_job.py`);
  m19 `_import_job` ignores a stored `spec_version` and reads 1 (in `pingpong_job.py`).
 Run it: `git worktree add --detach .remedy-wt/f026-r1-mut <C4>`, then
 `python3 -B .agent/authored/f026-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f026-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f026-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C5, C4, C3b, C3a, C2, C1b, C1a and `90555849` in that
 order; `git worktree list`, which must show the primary checkout and the worktrees constraint 6
 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected (none is expected for C3a, C3b and C4 — report what you measure), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F026, round 1, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — `job.edit-task` in the catalog, the CLI and the write door with its audit,
and the prompt-trace proof on a fake run. State the open-findings count, 4, and the
operator-questions count, 4.
