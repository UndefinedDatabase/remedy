STEP F026 R3 — T003, FIRST HALF: the dashboard's `task_specs` section, the version chip on the node and in the popover, and the popover's Versions list

GOAL
Round 2 passed. Book it, resolve R-1059, record DECISION F026 D3, reword `job.edit-task`'s help
text, and land the first half of T003: the dashboard carries each plan task's spec, version chain and
runtime editability; an edited task shows a `v<n>` chip beside its graph node and in the detail
popover; and the popover lists the versions, each opening the fields that changed.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code and its tests against S1 to S8. Only the `.agent/` records travel as payloads. Read DECISION
F026 D3 (it arrives with C1b) before code, and `docs/ui/design_reference/` is binding on visuals.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f026-r3-payloads/` and `.remedy-wt/f026-r3/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f026-r3-dry/`, `.remedy-wt/f026-r3-sim/`, `.remedy-wt/f026-r3-drafts/`,
  `.remedy-wt/f026-r3-render/`   The reviewer's; do not touch them.
  `.remedy-wt/f026-r3-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
`for` loops, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture
real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>`, never `cd` your shell into a worktree. Use `python3 - <<'PY'` for
counting, hashing and copying (`shutil.copyfile`); a heredoc containing a dollar-brace or a
brace-quote shape is refused, so write such a script to a file under your own directory and run it.
NEVER run npm or npx; the vitest route for G5 is below.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell is in `/home/decodeux/Repos/remedy`; report `pwd`. `git status --porcelain` must be
   empty, `git branch --show-current` must read `feature/f026-task-edit-runtime`, and
   `git log --oneline -1` must read `10ec2512`. Report all three.
3. Measure the line count and sha256 of `.remedy-wt/f026-r3/block.md` and compare both with the two
   readings your delegation message states (R-0954); stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f026-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1150 | 2b82375cb0f32a7cc0fac17b1077716442f88d1b1c6e30344e28f1787d674709 |
| records.diff | 63 | 9689 | a0e6484f1ad7ee8173a9364e722b6a83109df434601ad3293f800ace1abbddf7 |

`plan.md` REWRITES `.agent/plan.md`. `records.diff`, generated with `git diff HEAD` from a tree at
`10ec2512`, appends round 2's gate entry and R-1059's `Done:` paragraph to `.agent/live_review.md`
and DECISION F026 D3 to `.agent/decisions.md`.

THE SPECIFICATION
S1 HELP TEXT. `job.edit-task`'s description in `apps/cli/command_catalog.py` becomes EXACTLY
   "Change one task of an approved job plan at runtime — its title, goal, acceptance criteria, size
   band or file hints — while its job is not running." Nothing else in that file changes.
S2 THE SECTION. `packages/orchestration/ui_server.py` gains `_build_task_spec_section(job)`, and
   `_build_dashboard`'s result gains `"task_specs": _build_task_spec_section(job)` directly after
   its `"pause"` entry. It returns `{"tasks": {}, "error": ""}` for a job with no stored plan with
   tasks; otherwise `{"tasks": {...}, "error": ""}` keyed by `str(task_id)` of every task entry
   whose `inputs["plan"]["planned_id"]` names a task of the stored plan, each value holding
   `planned_id`, `spec_version` (the entry's), `edit_state` — `runtime_edit_state(job.state,
   body["_approval"], entry.status, task_paused=<the job is paused, or the entry's id is among
   pause_control.paused_tasks(job id)>)`, or `""` when it raises `PlanEditRefused` —,
   `not_editable_because` (`""`, or that refusal's `detail`), `current` (the plan task's `title`,
   `goal`, `acceptance`, `est_tokens_band` and `files_hint`), and `versions` (for each dict
   `task_spec_versions(job id, planned id)` returns, in its order: those five fields read from its
   `plan_task`, plus `spec_version`, `state` and `archived_at`). It NEVER raises: a
   `PauseControlError`, `StopControlError`, `OSError` or `ValueError` met while reading returns
   `{"tasks": {}, "error": str(exc)}`. It imports lazily inside the function, as
   `_build_pause_section` does, and writes nothing.
S3 THE CLIENT DATA. `apps/ui/src/api/types.ts` gains `RemedyTaskSpecFields` (`title`, `goal`,
   `acceptance: string[]`, `estTokensBand`, `filesHint: string[]`), `RemedyTaskSpecVersion` (those
   plus `specVersion`, `state`, `archivedAt`), `RemedyTaskSpec` (`plannedId`, `specVersion`,
   `editState: "" | "waiting" | "paused" | "failed"`, `notEditableBecause`, `current`, `versions`)
   and `RemedyTaskSpecs` (`tasks: Readonly<Record<string, RemedyTaskSpec>>`, `error`), each with a
   doc comment naming DECISION F026 D3, and `RemedyDashboard` gains a REQUIRED `taskSpecs:
   RemedyTaskSpecs` after `pause`. `apps/ui/src/api/remedyApi.ts` gains `normalizeTaskSpecs(raw)`,
   used by `normalizeDashboardPayload` on `dashboard.task_specs` and by `normalizeApiFailure` on
   `undefined`: a missing or non-object section is `{tasks: {}, error: ""}`; an `edit_state` outside
   the three names is `""`; a `spec_version` that is not a number of at least 1 is 1; lists are
   string lists; every other missing field is `""`.
S4 THE PURE VIEW, a NEW FILE at `apps/ui/src/api/taskSpecView.ts`: `taskSpecOf(dashboard, taskId)`;
   `taskSpecVersions(dashboard)` (task id to spec version); `versionChipLabel(spec)` — `v<n>` when
   the spec version is 2 or more, else `null`; and `specVersionRows(spec)` — `[]` unless the spec
   version is 2 or more, else one row per archived version in ascending order then one for the
   current spec, each `{specVersion, current, state, archivedAt, changes}`, where `changes` lists,
   in the order title, goal, acceptance, size band, files, every field whose shown value differs
   from the PREVIOUS row's, as `{field, label, before, after}` with list values joined by `"; "`.
S5 THE CANVAS CHIP. `BrainTaskSeed` in `apps/ui/src/components/graph/brainOntology.ts` gains
   optional `specVersion`; the reducer's seeding in `brainReducer.ts` copies it into the task node's
   `meta.specVersion` when present; `dashboardBrainSeeds` in `brainView.ts` gains a third parameter
   `specVersions` (default `{}`) and puts `specVersion` on a seed ONLY when the map has the task;
   `BrainLayoutNode` in `forceBrainTypes.ts` and `PaintableNode` in `renderers/paintNode.ts` gain
   optional `chip`; `buildBrainLayout` in `buildForceBrainModel.ts` sets a task node's `chip` to
   `v<n>` ONLY when its `meta.specVersion` is a number of at least 2 (the key is absent otherwise);
   and `paintBrainNode`, after the cluster count and before the marks, paints a task node's chip
   with `ctx.fillStyle` the state's line colour, `ctx.font` `600 ${radius * 0.6}px <the label font
   token's value>`, `textAlign` `left`, `textBaseline` `top`, at `(x + radius * 0.8, y + radius *
   0.8)`, where `radius` is the one the painter already computed. A named constant carries 0.6 and
   0.8 beside `CLUSTER_COUNT_SIZE`. `BrainGraphStage.tsx` passes `taskSpecVersions(dashboard)`.
S6 THE POPOVER. `DetailPopover.tsx` reads the task's spec with `taskSpecOf`; its status row ends with
   `<span className={styles.versionChip} title="Edited at runtime">v<n></span>` when
   `versionChipLabel` gives one; and directly after `<PromptTracePanel … />` it mounts
   `<TaskVersionList key={task?.id ?? ""} rows={specVersionRows(spec)} />`. A NEW FILE at
   `apps/ui/src/components/detail/TaskVersionList.tsx` renders nothing for no rows, else a section
   headed "Versions" with `aria-label="Spec versions"`: one `<li>` per row holding a
   `<button type="button">` with `aria-expanded`, disabled when the row has no changes, reading
   `v<n> · replaced while <state>` for an archived row and `v<n> · current` for the current one;
   clicking opens (one at a time) a `<dl>` of the row's changes, each `<dt>` the label and each
   `<dd>` `<del>` old value, an arrow, `<ins>` new value. `DetailPopover.module.css` gains
   `.versionChip`, `.versionList`, `.versionRow` and `.versionDiff` with its `dt`/`dd`, using ONLY
   custom properties `apps/ui/src/styles/tokens.css` defines (the drift guard
   `tests/ui_contracts/test_design_drift.py` refuses others) and plain pixel sizes as the file
   already writes them: the chip an outlined pill (`--remedy-line` border, `--remedy-radius-pill`,
   `--remedy-ink-soft`, 600 11px `--remedy-font-ui`, `margin-left: auto`, and
   `.timeLabel + .versionChip` with a 6px left margin instead), the rows ghost buttons at 12.5px, the diff's `dt` 11px uppercase muted like the
   popover's field keys, its `dd` with zero margin and 12px `--remedy-font-mono`. No animation.
S7 THE LOG. `docs/ui/design_reference/assumption_log.md` gains two rows in its table's format after
   F025's, dated 2026-09-25, feature F026, citing DECISION F026 D3: one for the chip (the reference
   designs no version chip; text in the state's line colour and the label font, as the cluster
   count), one for the Versions list (the reference designs no version list; a §14 per-task list in
   the L2 popover).
S8 SIZE. Every commit under 500 inserted lines; split one that would reach it and say so.

THE TESTS, each named after its source: a NEW FILE at `tests/ui_server/test_dashboard_task_specs.py`
(a never-edited planned task: version 1, no versions, `waiting`; after one `edit_task_at_runtime`:
version 2 and one archived version with the old fields; a blocked task reads `failed`; a running job
reads `""` with a detail naming `running`; a job without a plan reads no tasks; a corrupt task pause
file reads no tasks and a non-empty `error`, and does not raise; `_build_dashboard(job)` carries the
key). `apps/ui/src/api/remedyApi.test.ts` (the mapping, the empty default, a bad `edit_state`, a bad
`spec_version`, the failure shape). A NEW FILE at `apps/ui/src/api/taskSpecView.test.ts` (chip labels for 1, 2 and
undefined; rows' order, current flag, per-field changes against the previous row, list joining).
`brainView.test.ts`, `buildForceBrainModel.test.ts` and `renderers/paintNode.test.ts` (the seed key
only when given; the chip only at 2 or more; the painter's `fillText` of the chip at the specified
point for a task and never for another kind). A NEW FILE at `tests/ui_contracts/test_task_version_contract.py` (the
popover mounts `TaskVersionList` with `key={task?.id ?? ""}` after `PromptTracePanel`;
`TaskVersionList.tsx` and `taskSpecView.ts` contain no `fetch`; every button there is
`type="button"` with `aria-expanded`).

BUNDLE — in this order.
C1a — `.agent/authored/f026-r3-block.md` := this block, `.agent/authored/f026-r3-plan.md` :=
  plan.md, `.agent/authored/f026-r3-records.diff` := records.diff, all by `shutil.copyfile`.
  Subject: `F026 R3 C1a: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 94. Report the number you measure.
C1b — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F026 R3 C1b: book round 2, resolve R-1059, record D3`
  Expected by `git show --numstat`: 43/0 .agent/decisions.md, 4/0 .agent/live_review.md, 10/10 .agent/plan.md.
C2 — S1. Subject: `F026 R3 C2: word job.edit-task's help text for the operator`
C3 — S2 and its test file. Subject: `F026 R3 C3: the dashboard carries each task's spec and version chain`
C4 — S3 and S4 with their tests. Subject: `F026 R3 C4: the client reads task specs and derives the chip and the version rows`
C5 — S5 with its tests. Subject: `F026 R3 C5: an edited task's node carries its version chip`
C6 — S6 and S7 with the contract test. Subject: `F026 R3 C6: the detail popover shows the chip and the Versions list`
C7 — the mutation tool (G5) as `.agent/authored/f026-r3-mutations.py`. Subject: `F026 R3 C7: the round's red-proof mutation tool`
C8 — `.agent/handoff.md` per `docs/agents/handback_template.md`. Subject: `F026 R3 C8: rewrite handoff for round 3`
  Then `git push origin feature/f026-task-edit-runtime` and report its real outcome.

CONSTRAINTS
1. Never edit or retype a payload. `git apply --check` before `git apply`; report its exit code.
2. The round's whole tracked path set: the `.agent/authored/f026-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `apps/cli/command_catalog.py`,
   `packages/orchestration/ui_server.py`, `apps/ui/src/api/types.ts`, `apps/ui/src/api/remedyApi.ts`,
   `apps/ui/src/api/remedyApi.test.ts`, `apps/ui/src/api/taskSpecView.ts`,
   `apps/ui/src/api/taskSpecView.test.ts`, under `apps/ui/src/components/graph/` the files
   `brainOntology.ts`, `brainReducer.ts`, `brainView.ts`, `brainView.test.ts`, `forceBrainTypes.ts`,
   `buildForceBrainModel.ts`, `buildForceBrainModel.test.ts`, `BrainGraphStage.tsx`,
   `renderers/paintNode.ts` and `renderers/paintNode.test.ts`, under `apps/ui/src/components/detail/`
   the files `DetailPopover.tsx`, `DetailPopover.module.css` and `TaskVersionList.tsx`,
   `docs/ui/design_reference/assumption_log.md`, `tests/ui_server/test_dashboard_task_specs.py`,
   `tests/ui_contracts/test_task_version_contract.py`, and `.agent/handoff.md`. Report
   `git diff --name-only 10ec2512` after C8. If a guard outside this set goes red (a TypeScript
   fixture that builds a `RemedyDashboard` without `taskSpecs`, for instance), STOP and hand back
   rather than widen the set. Do NOT touch `packages/orchestration/task_edit_runtime.py`,
   `packages/orchestration/pingpong_job.py`, `apps/ui/src/api/pauseSend.ts`, `README.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or
   `docs/roadmap/features/T5_F026.md`.
3. A red gate: STOP, commit and push what is verified, hand back honestly under AGENTS.md "If
   Blocked". Do not repair the reviewer's payloads.
4. NOTHING IS MERGED. No `gh pr merge`, `gh pr create`, checkout of `main`, branch deletion,
   force-push or `git stash`.
5. Leave every existing worktree, branch and stash alone. The G5 worktree goes under `.remedy-wt/`,
   is removed as that step's last action, and `git worktree list` is reported afterwards.
6. DO NOT run the full suite: amend0917 rule 1 gives F026 exactly one, at its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C8 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table; each
 `.agent/authored/f026-r3-*` payload copy compared byte for byte with its source (the block copy
 against `.remedy-wt/f026-r3/block.md`), read back with `git show <C1a>:<path>`.

G2 THE RECORDS — `git show <C1b>:<path>` of each file below hashes to the reviewer's reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 321169 | 3d044b3cd18c6f316415ead6462635c27d5d725efec46a2701b17c98e80e8646 |
 | .agent/decisions.md | 2135451 | 58e8b195149417b1873607ad9740fc425f65bbc07a93ae65c86c8b6729ad337a |
 | .agent/plan.md | 1150 | 2b82375cb0f32a7cc0fac17b1077716442f88d1b1c6e30344e28f1787d674709 |
 and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text reads R-1008,
 R-1055, R-1057, R-1058 and R-1059 at `10ec2512` and R-1008, R-1055, R-1057 and R-1058 at C1b.

G3 THE CODE — `python3 -m ruff check` over every `.py` path of constraint 2 at C7.

G4 THE TESTS — in the primary checkout at C7, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_dashboard_task_specs.py tests/ui_contracts/test_task_version_contract.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_dashboard_pause.py tests/orchestration/test_test_runner.py tests/ui_contracts tests/test_command_catalog.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the two new test files and the golden path, serially,
 in a tree at `10ec2512` carrying this round's records, and read `1628 passed, 10 skipped` at exit 0. Of those
 skips, the TypeScript node of `tests/ui_server/test_dashboard_contract.py`, the vitest node of
 `tests/orchestration/test_test_runner.py` (which runs every `.test.ts`) and the two lint nodes of
 `tests/ui_contracts/test_ui_lint.py` are toolchain nodes the primary checkout runs, and each must
 PASS in your run; the four D3 quarantines and the D12 quarantine stay skipped; report what the
 responsive node of `tests/ui_contracts/test_responsive.py` reads. Report every `SKIPPED` line and
 account for every other difference. Then `python3 -m apps.cli.main integrity check --json`: all
 six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool takes a worktree path; for each mutation it edits the named file
 INSIDE that worktree (asserting its FROM text occurs exactly once), runs the tests that cover it,
 restores the bytes, and prints label, exit code, failed count and failing ids; unmutated controls
 run first and last; it ends with `restored byte-identical: True` per file and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Python mutations run
 `python3 -B -m pytest -q -p no:cacheprovider tests/ui_server/test_dashboard_task_specs.py` from the
 worktree after purging `__pycache__`. TypeScript mutations run vitest over the worktree's changed
 `.test.ts` files by the SAME route `.agent/authored/f025-r6-mutations.py` uses — read its
 `run_vitest` and copy that route: the PRIMARY's `apps/ui/node_modules/.bin/vitest`, run from the
 PRIMARY `apps/ui`, with a scratch config under `.remedy-wt/` whose `include` names the worktree's
 test files by absolute path. The mutations:
  m1 the section's `versions` is always `[]` (ui_server.py);
  m2 the section lets a `PauseControlError` escape instead of reporting it (ui_server.py);
  m3 a `PlanEditRefused` makes `edit_state` read `"waiting"` (ui_server.py);
  m4 `normalizeTaskSpecs` drops `spec_version`, so every task reads 1 (remedyApi.ts);
  m5 `versionChipLabel` gives `v1` for version 1 (taskSpecView.ts);
  m6 `specVersionRows` compares every row against the FIRST row instead of the previous one;
  m7 the painter paints a chip for a non-task kind (paintNode.ts);
  m8 `buildBrainLayout` ignores `meta.specVersion` (buildForceBrainModel.ts);
  m9 `dashboardBrainSeeds` drops `specVersion` (brainView.ts).
 Run: `git worktree add --detach .remedy-wt/f026-r3-mut <C7>`, then
 `python3 -B .agent/authored/f026-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f026-r3-mut`,
 report its whole output; EVERY mutation must be red; one that stays green is reported, you add the
 test that catches it before C8 and re-run. Then `git worktree remove --force
 .remedy-wt/f026-r3-mut` and report `git worktree list`.

G6 TREE AND PUSH — after C8: `git status --porcelain` empty; `git log --oneline -n 10`; `git
 worktree list`; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft` EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside any this block
expected, every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit, per gate and per S-item), the deviations, and the next
expected action. Your Session section reads SESSION 1 of feature F026, round 3, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
3, then T003's second half — the edit affordance on eligible nodes only, sent through the write
door, and the end-to-end. State the open-findings count, 4, and the operator-questions count, 4.
