STEP F289 R1 — CLAIM F289, REPAIR R-1073, AND LAND T002: `doctor core`'s report as an importable function returning structured warnings, the command printing from it unchanged, and the self-use generator's Tier 3

GOAL
Pull request 283 is merged; `main` is at `d0239fa3` and F289 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F027's round 14 verdict, register R-1073,
record DECISION F289 D1, repair R-1073 in `tests/orchestration/test_diff_parser.py`, and land
T002: `doctor_core_report()` in `apps/cli/commands/worker_facade_cmd.py` with its structured
warnings, `_cmd_doctor_core` printing from it byte-unchanged, and `_doctor_warning_tier` in
`packages/orchestration/self_use_generator.py` rendering one actionable warning as a one-task job.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against the specification S1 to S7 below. Only the
`.agent/` records and the STATUS line travel as payloads.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f289-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f289-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f289-r1-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f289-r1-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f289-r1-drafts/`    The reviewer's drafts; do not touch them.
  `.remedy-wt/f289-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f289-r1-worker/`    YOURS for logs and scripts; create it if absent. All seven are
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
   `git log --oneline -1` must read `d0239fa3`. Report all three. Then
   `git checkout -b feature/f289-self-use-sources` and report the branch. Do NOT pull: the Open
   PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f289-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f289-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 146 | 19624 | c3825c100157897a46ffc99489eb5718a258868eb7ab348eaab45293fefdb8e8 |
| context.md | 38 | 1627 | 764044aa73bcb904fce2ddb75ecd1466bc1d588642b75999487a647efc457f85 |
| plan.md | 32 | 1222 | 52838685baed54c3a2672f8593942a42e0fb329e286b3d272405f0102c931dfb |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`d0239fa3` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F027's round 14 gate entry and
R-1073's registration appended), `docs/roadmap/STATUS.md` (F289's line `[ ]` to `[~]`) and
`.agent/decisions.md` (DECISION F289 D1 appended). Read D1 and R-1073 before you write code: they
are the design and the repair this specification implements.

THE SPECIFICATION
S1 R-1073. In `tests/orchestration/test_diff_parser.py`, `HUGE_DIFF_PARSE_CEILING_SECONDS` goes
   and three constants take its place, each with a comment: `SMALL_DIFF_BODY_LINE_COUNT = 1_000`,
   `PARSE_TIMING_SAMPLES = 5` and `HUGE_DIFF_MAX_SCALING = 20`. The test keeps its name. It builds
   both fixtures with `_generated_huge_single_file_diff`, times each as the MINIMUM of
   `PARSE_TIMING_SAMPLES` parses with `time.perf_counter()`, pins the parsed body-line count of
   BOTH views first, and asserts `huge / small < HUGE_DIFF_MAX_SCALING` with a message naming both
   times and the ratio. Its docstring keeps the 2026-08-28 measurement, adds the reviewer's
   reading at `d0239fa3` (the minimum of five parses, taken three times: 0.0103 to 0.0105 s for
   1,000 body lines, 0.1036 to 0.1049 s for 10,000, a ratio of 9.9 to 10.2), states that a linear
   parser reads about 10 and a quadratic one about 100 so the ceiling sits between them as
   DECISION F256 D4's ratio does, names R-1073 and the two hosted-CI overruns on Python 3.10, and
   says why the minimum is taken: noise only ever adds time. Nothing else in the file changes.
   In the same commit append ONE line to the end of `.agent/live_review.md`, starting with its own
   blank line: `Landed: R-1073 — the diff parser's timing test asserts the ratio of the minimum of
   five parses of the 10,000-line fixture to that of a 1,000-line fixture below 20, and the
   absolute ceiling is gone, at this round's C3.` — one physical line, exactly that text.
S2 THE WARNING. In `apps/cli/commands/worker_facade_cmd.py`, a frozen dataclass `DoctorWarning`
   of `warning`, `summary`, `detail`, `subject: str = ""` and `repair_path: str = ""`, a property
   `actionable` answering `bool(self.repair_path)`, and `as_json()` answering
   `{"warning": ..., "summary": ..., "detail": ...}`, those three keys in that order and no other.
   A module constant `MODEL_ALIAS_TABLE_PATH = "packages/orchestration/model_aliases.py"`.
S3 THE REPORT. A frozen dataclass `DoctorCoreReport` of `ready`, `checks`, `blockers`,
   `warnings` (a tuple of `DoctorWarning`), `dead_commands` and `disk`; `as_json()` answering
   `{"ready", "checks", "blockers", "warnings", "dead_commands", "disk"}` in exactly that key order,
   `warnings` as the list of each warning's `as_json()`; and `actionable_warnings()` answering the
   actionable ones as a tuple, in report order. `doctor_core_report() -> DoctorCoreReport` holds
   today's handler body from its first line through the computation of `ready`, moved, not
   rewritten: every probe keeps going through `importlib.import_module`, `remedy_scripts_dir()`
   and the lazy imports exactly where it does today, because the tests patch them there, and every
   `# noqa: BLE001 — ...` comment moves with its line unchanged, because
   `tests/test_ble001_ratchet.py` pins their number at 290. Its docstring names T5_F289.md T002 and
   DECISION F289 D1.
S4 THE KINDS. `_warn` builds a `DoctorWarning` and gains keyword arguments `subject` and
   `repair_path`. `dead_builtin_model` carries the dead model id as `subject` and
   `MODEL_ALIAS_TABLE_PATH` as `repair_path`; `dead_configured_model` carries the configured value
   as `subject` and no repair path; `unknown_env_variable` and `unparsable_env_variable` carry the
   variable's name as `subject` and no repair path; `dead_model_comparison` carries neither. No
   `summary` or `detail` text changes by one byte, and no warning kind is added.
S5 THE COMMAND. `_cmd_doctor_core(ns)` calls `doctor_core_report()`, takes `as_json()`, and
   renders the JSON and the text exactly as today from that dict. Its stdout, for `--json` and for
   text, is byte-identical to the base's under the same inputs, which G3's parity tool proves.
   `worker_facade_cmd.py` must not come to contain the string `live_review.md`
   (`tests/orchestration/test_development_artifact_boundary.py`).
S6 TIER 3. In `packages/orchestration/self_use_generator.py`:
   `_DOCTOR_PROVENANCE = "generated (self-use-generator tier 3, doctor core, {key})"` and a
   `_DOCTOR_PROVENANCE_RE` reading the key back; `_targeted_doctor_keys(queue_path)` answering
   every key an entry, consumed or not, targets; and `_doctor_warning_tier(queue_path)`, which
   imports `worker_facade_cmd` from `apps.cli.commands` INSIDE the function, calls
   `worker_facade_cmd.doctor_core_report()` through the module, catches nothing, and takes the
   first of `actionable_warnings()` whose key `f"{warning}:{subject}"` is not targeted. It refuses
   a `detail` holding a line shaped like `^## ` or `^Acceptance\s*:` (case-insensitive) with
   `SelfUseGenerationError`, as `_ledger_tier` refuses a paragraph. Otherwise it answers an entry
   with the next `SU-NNN` id, title `Clear doctor warning <warning> for <subject>`, `why` the
   detail, empty `consumed_by`, the provenance with the key, and the job text below, whose lines
   are shown indented by six spaces that are NOT part of it, in which WARNING, SUBJECT and
   REPAIR_PATH stand for the warning's three fields and every other character, backticks
   included, is literal; the text ends with one newline after its last line:
      # Job: Clear doctor warning WARNING for SUBJECT

      ## Task 1
      <the detail, verbatim, as one or more lines>

      Make the repair this warning names, in `REPAIR_PATH` and the tests that cover it. Do not edit any file under `.agent/`.

      Acceptance:
      - `remedy doctor core --json` no longer lists warning `WARNING` for `SUBJECT`.
      - No file under `.agent/` is changed by this task.
   The module docstring's item 3 and the Public API lines are
   rewritten to describe the built tier; items 0 to 2 and every other paragraph stay. The tier
   order in `generate_self_use_item` is unchanged.
S7 THE ORPHAN AND REACHABILITY GUARDS need no entry: no new module is added.

THE TESTS
In `tests/orchestration/test_self_use_generator.py`: the autouse fixture `_no_standing_order`
also points Tier 3 at an empty report, by monkeypatching `doctor_core_report` on
`apps.cli.commands.worker_facade_cmd` to answer a `DoctorCoreReport` with no warnings, so no
existing test reads the machine's real configuration; and a new class covering at least: a stub
report holding one actionable warning on an empty ledger answers the Tier 3 item, its title, id,
provenance, `why`, and a job text holding the detail verbatim, the repair path, the `.agent/`
sentence and the two acceptance bullets, which parses as a single-task job (use
`isolate_data_root`, as `test_the_appended_jobmarkdown_parses_as_a_single_task_job` does); only
non-actionable warnings answer None; of two actionable warnings the first is offered, then after
it is appended the second, and a consumed entry targeting a key still withdraws it; an eligible
ledger finding wins over Tier 3; a detail holding a `## ` line and one holding an `Acceptance:`
line each raise `SelfUseGenerationError`; a report that raises propagates its own exception; and
the REAL chain, with no stub: the dead-model loaders of `packages.orchestration.dead_model_list`
monkeypatched to declare the model id `claude-flagship` resolves to dead (read from
`packages.orchestration.model_aliases.resolve_model_alias`, never spelled), answers a Tier 3 item
naming that id and `packages/orchestration/model_aliases.py`.
In `tests/cli/test_worker_facade_cmd.py`, a new class covering at least: `doctor_core_report()`
answers a `DoctorCoreReport` whose `as_json()` equals the report keys of the command's own
`--json` output in the same run (with `packages.orchestration.budget_guard.FREE_DISK_PROBE`
monkeypatched to a constant, as `tests/orchestration/test_disk_floor.py` does); `as_json()`'s key
order; every warning's `as_json()` key list is exactly `["warning", "summary", "detail"]`; a dead
built-in default is actionable with its id as subject and `MODEL_ALIAS_TABLE_PATH` as repair
path, and that path exists in the repository; a dead configured id, and an unknown `REMEDY_`
variable set with `monkeypatch.setenv`, are not actionable and carry the value and the name as
subject; and `actionable_warnings()` answers exactly the actionable ones in order. Reuse the
file's own helpers (`_patch_dead_list`, `_dead_entry`, `a_builtin_model_id`, `_FakeConfig`).

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f289-r1-block.md` := this block, and `.agent/authored/f289-r1-plan.md` and
  `.agent/authored/f289-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F289 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 70. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f289-r1-claim.diff` := claim.diff.
  Subject: `F289 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 146.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F289 R1 C2: claim F289, re-head the live review record, book F027 R14, register R-1073, record D1`
  Expected by `git show --numstat` (insertions and deletions): 16/15 context.md, 60/0 decisions.md, 28/22 live_review.md, 19/12 plan.md, 1/1 STATUS.md.

C3 — R-1073: S1, `tests/orchestration/test_diff_parser.py` and the `Landed:` line.
  Subject: `F289 R1 C3: guard the diff parser's complexity class by a scale ratio (R-1073)`

C4 — THE CODE: S2 to S6 — `apps/cli/commands/worker_facade_cmd.py` and
  `packages/orchestration/self_use_generator.py`.
  Subject: `F289 R1 C4: make doctor core's report importable and render its actionable warnings as Tier 3`

C5 — THE TESTS AND THE TOOLS: the two test files, your mutation tool (G5) saved as
  `.agent/authored/f289-r1-mutations.py`, and your parity tool (G3) saved as
  `.agent/authored/f289-r1-parity.py`.
  Subject: `F289 R1 C5: test the doctor report and Tier 3, and add the mutation and parity tools`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F289 R1 C6: rewrite handoff for round 1`
  Then `git push -u origin feature/f289-self-use-sources`. Do NOT create a pull request: the
  branch opens one at F289's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C4a and C4b, C5a and C5b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f289-r1-*` copies and tools,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `tests/orchestration/test_diff_parser.py`,
   `apps/cli/commands/worker_facade_cmd.py`, `packages/orchestration/self_use_generator.py`,
   `tests/cli/test_worker_facade_cmd.py`, `tests/orchestration/test_self_use_generator.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only d0239fa3` at the
   branch tip after C6. Do NOT touch `packages/orchestration/diff_parser.py` (G5 mutates it only
   inside its worktree), `packages/orchestration/self_use_queue.py`,
   `packages/orchestration/self_use_runner.py`, `packages/orchestration/dead_model_list.py`,
   `packages/orchestration/model_aliases.py`, `apps/cli/command_catalog.py`, anything under
   `apps/ui/`, `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `README.md` or `docs/roadmap/features/T5_F289.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C6, and the correction is declared.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktrees G3 and G5 add go under
   `.remedy-wt/`, are removed as that gate's last action, and `git worktree list` is reported
   afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F289's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f289-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f289-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | docs/roadmap/STATUS.md | 54111 | e4ec53b9440611ebbe6239a2af1105a629427499bab85869338449de5444e039 |
 | .agent/live_review.md | 317231 | 6df1c98d4e37381aa83b91326bafaabe90bd813f2f6dd775c6cb810bf8a02b72 |
 | .agent/decisions.md | 2211184 | ed4530356eeb7203c79182eb4db25d585be69ac850a16b6902c8ac4d018c4be2 |
 | .agent/plan.md | 1222 | 52838685baed54c3a2672f8593942a42e0fb329e286b3d272405f0102c931dfb |
 | .agent/context.md | 1627 | 764044aa73bcb904fce2ddb75ecd1466bc1d588642b75999487a647efc457f85 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `d0239fa3` and at C2 (the reviewer read
 it empty at the first and `R-1073` alone at the second); at C2 the ledger has exactly one line
 reading `## Findings` and exactly one reading `## Steps`, and its last line begins `- R-1073 — `;
 F289's STATUS line at C2 read back in full, which must begin `- [~] F289 — `; and
 `git diff --name-only <C1b> <C2>`, which must name exactly the paths of the table above.

G3 THE CODE AND THE PARITY — `python3 -m ruff check apps/cli/commands/worker_facade_cmd.py
 packages/orchestration/self_use_generator.py tests/cli/test_worker_facade_cmd.py
 tests/orchestration/test_self_use_generator.py tests/orchestration/test_diff_parser.py` at C5;
 `git diff -U0 <C2> <C3> -- .agent/live_review.md`, reported whole, which must add the blank line
 and the one `Landed:` line and nothing else. Then THE PARITY: your tool
 `.agent/authored/f289-r1-parity.py` takes two tree paths, and for each tree runs, in a fresh
 `python3 -B` subprocess whose working directory is that tree, five scenarios, each calling
 `_cmd_doctor_core` once with `json=True` and once with `json=False`, capturing stdout, with
 `packages.orchestration.budget_guard.FREE_DISK_PROBE` patched to a constant and every
 `REMEDY_` variable removed from the child's environment except those a scenario sets: (a) as
 shipped; (b) the dead-model loaders declaring `resolve_model_alias("claude-flagship")` and the id
 `dead-configured-id` dead, with `packages.orchestration.config.get_config` answering a config
 whose `orchestrator.model` is `dead-configured-id`; (c) `REMEDY_ZZ_NOT_A_SETTING=1` set, plus one
 registered variable of a non-string type set to a value that does not parse as that type; (d)
 the dead-model loaders raising; (e) `remedy_scripts_dir` patched to an empty temporary
 directory. It prints one line per scenario and mode with both trees' sha256 and whether they are
 equal, and a final line `PARITY: <bool>`. Run it: `git worktree add --detach
 .remedy-wt/f289-r1-base d0239fa3` and `git worktree add --detach .remedy-wt/f289-r1-par <C4>`,
 then `python3 -B .agent/authored/f289-r1-parity.py
 /home/decodeux/Repos/remedy/.remedy-wt/f289-r1-base /home/decodeux/Repos/remedy/.remedy-wt/f289-r1-par`,
 and report its whole output; `PARITY: True` is required. Remove both worktrees, prune, and report
 `git worktree list`.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_worker_facade_cmd.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_diff_parser.py tests/orchestration/test_env_registry.py tests/orchestration/test_disk_floor.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_toolchain.py tests/cli/test_mission_cmd.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_test_categories.py tests/test_ble001_ratchet.py tests/test_imports.py tests/test_command_catalog.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection before any code change, serially, inside its authoring tree
 carrying the claim's records, and read `983 passed, 1 skipped` at real exit code 0; the one skip
 is the D12 quarantine in `tests/test_agent_tooling.py` and stays skipped. Report every `SKIPPED`
 line the `-rs` summary prints, the number of nodes the round adds (`--collect-only -q` on the
 two edited test files at `d0239fa3` and at C5), and account for any other difference from the
 reviewer's count. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f289-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named module INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider` over the worktree's
 `tests/cli/test_worker_facade_cmd.py`, `tests/orchestration/test_self_use_generator.py` and
 `tests/orchestration/test_diff_parser.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and last
 and ends with `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations, each a real behaviour change:
  m1 `DoctorWarning.as_json()` also writes `subject`;
  m2 the `dead_builtin_model` warning carries no repair path;
  m3 the `dead_configured_model` warning carries `MODEL_ALIAS_TABLE_PATH` as its repair path;
  m4 an `unknown_env_variable` warning carries no subject;
  m5 `DoctorCoreReport.as_json()` writes `warnings` before `blockers`;
  m6 Tier 3 ignores the keys the queue already targets;
  m7 Tier 3 offers the last actionable warning instead of the first;
  m8 Tier 3 accepts a detail holding a `## ` line;
  m9 Tier 3 writes the warning's summary as the task body instead of its detail;
  m10 `generate_self_use_item` tries Tier 3 before the ledger tier;
  m11 Tier 3 offers a warning that is not actionable;
  m12 `parse_unified_diff_to_view` in `packages/orchestration/diff_parser.py` does work
      proportional to the lines already parsed for every body line, so its cost grows with the
      square of the body-line count.
 Run it: `git worktree add --detach .remedy-wt/f289-r1-mut <C5>`, then
 `python3 -B .agent/authored/f289-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f289-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C5 before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f289-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6, C5, C4, C3, C2, C1b, C1a and `d0239fa3` in that
 order (more lines if constraint 2 split a commit); `git worktree list`, which must show the
 primary checkout and the worktrees constraint 6 names, and nothing else; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this
block expected (none is expected for C3, C4 and C5 — report what you measure), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F289, round 1, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T001 — the documentation-staleness catalog of at least ten checks and the
generator's Tier 2. State the open-findings count, 1 (R-1073, landed and awaiting the reviewer's
`Done:`), and the operator-questions count, 0.
