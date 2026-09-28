STEP F038 R2 — BOOK ROUND 1 AND R-1091's RESOLUTION, THEN LAND T001's PROJECT SCOPE, THE NODE SCOPE's PROMPT TRACES AND THE SPEC's SET-LIST UPDATE

GOAL
Round 1 is reviewed PASS at `733d5db6` and R-1091's repair is reviewed. Book both, record
DECISION F038 D3, rewrite the spec's two scope paragraphs to the built set, and extend
`packages/orchestration/chat_evidence.py`: the node scope gains one item per entry of the task's
prompt trace (its metadata, never the prompt text), and a NEW project scope collects one registry
project's own records — its record, its repository's roadmap position, its linked jobs' open
decisions and patterns, its missions' dossiers, its token ledger's totals and one digest per
linked job, newest first — composed under the same cap. The module still writes no file, calls no
model, runs no subprocess, and nothing imports it yet.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S5 below. Only the `.agent/` records and the
spec's paragraphs travel as payloads. Read DECISION F038 D3 in the records diff before you write
code: it is the design this specification implements. Before you write anything, read whole:
`packages/orchestration/chat_evidence.py` and `tests/orchestration/test_chat_evidence.py` as they
stand at `733d5db6`; `RemyProject` in `packages/orchestration/project_registry.py`;
`list_job_plans_safe` in `packages/orchestration/pingpong_job.py`; `list_decisions` and
`open_decisions` in `packages/orchestration/decision_queue.py`; `detect_patterns` and
`ProjectPattern` in `packages/orchestration/project_summary.py`; `build_index`, `proposed_feature`
and `RoadmapGrammarError` in `packages/orchestration/roadmap_index.py`; `build_job_digest` in
`packages/orchestration/job_digest.py`; `list_missions_safe` and `create_mission` in
`packages/orchestration/mission_state.py`; `load_dossier_state`, `save_dossier_state`,
`MissionDossier` and `DossierItem` in `packages/orchestration/mission_dossier.py`; `query_cost`,
`CostRow`, `CallRecord` and `record_call` in `packages/orchestration/token_ledger.py`; `run_dir`
in `packages/orchestration/data_paths.py`; and `PromptTraceEntry` in
`packages/orchestration/prompt_trace.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f038-r1-*`, `.remedy-wt/f038-r2-dry/`, `.remedy-wt/f038-r2-sim/`,
  `.remedy-wt/f038-r2-src/`, `.remedy-wt/f038-review/`   The reviewer's; do not touch them.
  `.remedy-wt/f038-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set `REMEDY_DATA_DIR` inside tests with `monkeypatch.setenv`, never on a command line.
Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `733d5db69`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 105 | 13552 | f8c89e25ef3e44c9dee183e9ac0337478aada610d31c7b59f6c110eea6d072ea |
| plan.md | 30 | 992 | bcb8cca73a353e29155d1d7eebcf64dab77b0504e644a13f4ddb3052095c2219 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `733d5db6` into which it wrote the edits. It
appends round 1's gate entry and R-1091's `Done:` paragraph to `.agent/live_review.md`, appends
DECISION F038 D3 to `.agent/decisions.md`, and rewrites the two scope paragraphs of section 2 of
`docs/roadmap/design/grounded-chat-spec.md`.

THE SPECIFICATION, all of it in `packages/orchestration/chat_evidence.py`. No `except Exception`
anywhere and no `# noqa: BLE001`; every catch names its exception classes.
S1 THE CONSTANTS AND THE PROSE. `CHAT_SCOPE_PROJECT = "project"` joins, and
   `CHAT_SCOPES = (CHAT_SCOPE_NODE, CHAT_SCOPE_PROJECT)`. `CHAT_ANCHOR_KINDS` becomes exactly
   `("node", "round", "prompt", "diff", "event", "project", "roadmap", "decision", "pattern",
   "dossier", "ledger", "job")`. The module docstring, and the comments above `CHAT_SCOPES` and
   `CHAT_ANCHOR_KINDS`, say what the module now holds — both scopes — and name DECISION F038 D3
   beside D1; no sentence may still say the project scope joins later or count the kinds as four.
S2 THE PROMPT TRACE, in the node scope, directly AFTER the rounds and BEFORE the diff. When the
   task's `run_id` is not a string matching `^[0-9a-f]{8,32}$`, one `node` item
   `Prompt trace: not recorded (no_run_recorded)`. Otherwise read
   `run_dir(<run id>)/"prompt_trace.jsonl"` as UTF-8: a `FileNotFoundError` gives
   `Prompt trace: not recorded (trace_missing)`; any other `OSError` or a `UnicodeDecodeError`
   gives `Prompt trace: not recorded (trace_unreadable)`. Each line that parses as JSON into a dict
   is one item, in file order, kind `prompt`, ref `<task id>#<round>/<role>`, text
   `Prompt for round <round>, <role> (<prompt_kind>): <prompt_tokens_estimated> tokens estimated;
   provider <provider>; model <configured_model>`, where an empty or absent `role`, `prompt_kind`,
   `provider` or `configured_model` reads `not recorded`; `round` and `prompt_tokens_estimated`
   are written as found. A line that does not parse, or parses to something not a dict, is
   skipped. No item ever carries `prompt_text_redacted` or any other prompt text. When the file
   gave no item, one `node` item `Prompt trace: not recorded (trace_empty)`.
S3 THE PROJECT SCOPE. `collect_project_evidence(project) -> list[ChatEvidenceItem]`, where
   `project` is a `RemyProject` and `<pid>` is `str(project.id)`. The jobs are those of
   `list_job_plans_safe()` (in its order, newest first) whose `str(job_id)` is in
   `project.job_ids`; each job's events are `load_run_events(resolve_data_root(), <job id>)`. Every
   item is made with `make_chat_item`, in this order:
   (a) `project` `<pid>`: `Project <name>: <n> linked jobs; repository <canonical_repo_path or
       "not recorded">`.
   (b) the roadmap: no `canonical_repo_path` → `project` `<pid>`
       `Roadmap position: not recorded (no repository)`; `build_index(canonical_repo_path)`
       raising `RoadmapGrammarError`, `OSError` or `UnicodeDecodeError` → `project` `<pid>`
       `Roadmap position: not recorded (<the exception's class name>)`; `proposed_feature` giving
       no feature → `project` `<pid>` `Roadmap position: no open feature`; otherwise `roadmap`
       `<feature id>` `Roadmap: <feature id> — <title> is in progress` for the reason
       `in_progress`, else `... is the next open feature`.
   (c) for each job in order, each decision of `open_decisions(list_decisions(job, <its
       events>))` in that order: `decision` `<job id>/<decision id>`
       `Open <severity> decision on job <job id>: <safe_summary, or the type when empty>`.
   (d) each pattern of `detect_patterns(<the jobs>, <events by job id>)`: `pattern`
       `<pattern_id>` `Pattern <kind> (<severity>): <summary>`.
   (e) for each mission of `list_missions_safe(<pid>)` in its order whose
       `load_dossier_state(<pid>, <mission id>)` is not None: `dossier` `<mission id>`
       `Mission goal: <goal>`; then `Mission next step: <next_step>` when set; then
       `Mission risk: <text>` for each risk not `resolved`, in order. When no item came of it, one
       `project` `<pid>` `Mission dossier: not recorded`.
   (f) `query_cost(project_id=<pid>)`: `sqlite3.Error` → `project` `<pid>`
       `Token ledger: not readable (<the exception's class name>)`; `ledger_exists` false →
       `project` `<pid>` `Token ledger: not recorded`; otherwise `ledger` `<pid>`
       `Token ledger: calls <calls>; tokens in <tokens_in>; tokens out <tokens_out>; cost <cost>`
       from `report.total`, where a None figure reads `unmeasured` and the cost reads `$` plus two
       decimals.
   (g) for each job in order, from `build_job_digest(job, <its events>)`: `job` `<job id>`
       `Job <job id> (<state>): <headline> Open decisions: <decisions.open_count>. Next:
       <primary_action.label>`. When there is no job, one `project` `<pid>`
       `Jobs: not recorded for this project`.
S4 `project_evidence_set(project, *, token_cap=CHAT_EVIDENCE_TOKEN_CAP) -> ChatEvidenceSet` is
   `compose_chat_evidence(CHAT_SCOPE_PROJECT, str(project.id), collect_project_evidence(project),
   token_cap=token_cap)`.
S5 THE IMPORTS. At module level: the standard library, the seven modules round 1 imports, and
   only these further names — `run_dir` from `data_paths`; `list_decisions` and `open_decisions`
   from `decision_queue`; `build_job_digest` from `job_digest`; `load_dossier_state` from
   `mission_dossier`; `list_missions_safe` from `mission_state`; `list_job_plans_safe` from
   `pingpong_job`; `detect_patterns` from `project_summary`; `RoadmapGrammarError`, `build_index`
   and `proposed_feature` from `roadmap_index`; `query_cost` from `token_ledger`. Nothing from
   `ui_server`, `apps`, `project_brain` or `project_brain_aggregate`.
S6 THE GUARD. The reason of the `chat_evidence.py` line in `ALLOWED_UNWIRED` of
   `tests/test_no_orphan_modules.py` reads "F038's grounded chat evidence, the node and project
   scopes and the composer; the chat command wires it in a later round (DECISION F038 D1 (6)) and
   removes this line", split over lines as it is now. Nothing else in that file changes.

THE TESTS, in `tests/orchestration/test_chat_evidence.py`. FIVE EXISTING TESTS CHANGE, because
this round changes what they pin, and nothing else in them changes:
`test_a_fully_recorded_task_yields_exactly_the_eleven_items_in_order` is renamed with `twelve`
and gains `("node", task_id, "Prompt trace: not recorded (trace_missing)")` after its second round
item; `test_a_task_with_nothing_recorded_yields_exactly_the_eight_items` is renamed with `nine` and
gains `("node", task_id, "Prompt trace: not recorded (no_run_recorded)")` after its run-rounds
item; `test_node_evidence_set_composes_the_collected_items` expects 9 items;
`test_chat_item_problems_reads_each_of_its_lines` expects the twelve kinds of S1 in its two
messages; and `test_a_malformed_item_and_the_scope_project_are_refused` is renamed
`test_a_malformed_item_and_an_unknown_scope_are_refused` and refuses the scope `mission` with
`scope 'mission' is not one of node, project`. NEW TESTS, records written by the real writers
(`save_job_plan` with an explicit `created_at`, `create_mission` and `save_dossier_state`,
`record_call`, a `prompt_trace.jsonl` under `run_dir`, events under `run_log_dir`, a
`docs/roadmap/STATUS.md` under a repository in `tmp_path`), at least one each: a trace of a
builder entry carrying `prompt_text_redacted`, a line that is not JSON, a JSON list, a blank line
and a reviewer entry without a model gives exactly the two prompt items S2 states and no item
holds the prompt text; a trace holding only a blank line says `trace_empty`; a project with no
repository, job, mission or ledger gives exactly the five items S3 states for that case; the
roadmap reads `in progress` for a `[~]` line, `the next open feature` for a `[ ]` line after an
`[x]` one, `no open feature` when every line is `[x]`, and `not recorded (RoadmapGrammarError)`
for a feature id listed twice; two linked jobs and one unlinked give job items for the linked two
only, newest first, their decisions grouped by job newest first with refs `<job id>/...`, and —
each linked job carrying one `test_run_completed` event whose metadata `status` is `failed` —
exactly one pattern, `("pattern", "test_1", "Pattern repeated_test_failure (low): Tests failed 2
times across 2 job(s)")`; a mission's dossier with a next step, one open and one resolved risk
gives exactly three dossier items; the ledger reads `calls 1; tokens in 100; tokens out 50; cost
$0.25` for one measured call and `unmeasured` for all three figures of an unmeasured one; and
`project_evidence_set` is deterministic, names scope `project` and the project id, omits nothing,
and writes no file under `tmp_path`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f038-r2-block.md` := this block and `.agent/authored/f038-r2-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F038 R2 C1a: copy round 2 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 30. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the records diff
  `.agent/authored/f038-r2-records.diff` := records.diff.
  Subject: `F038 R2 C1b: copy round 2 records diff into .agent/authored/`
  Expected insertions: 105.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F038 R2 C2: book round 1 and R-1091's resolution, record D3, update the spec's sets`
  Expected by `git show --numstat` (insertions and deletions): 51/0 decisions.md, 4/0
  live_review.md, 8/11 plan.md, 15/8 grounded-chat-spec.md.

C3 — THE CODE: `packages/orchestration/chat_evidence.py` and S6's reason.
  Subject: `F038 R2 C3: collect the project scope and the node scope's prompt traces`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_chat_evidence.py` and your mutation tool
  (G5) saved as `.agent/authored/f038-r2-mutations.py`.
  Subject: `F038 R2 C4: test the project scope and the prompt items, add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R2 C5: rewrite handoff for round 2`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/roadmap/design/grounded-chat-spec.md`, `packages/orchestration/chat_evidence.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/test_chat_evidence.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 733d5db69` at the
   branch tip after C5. Do NOT touch anything under `apps/`, any other file under `packages/`,
   `tests/orchestration/import_reachability_allowlist.txt`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`
   or `docs/roadmap/features/T5_F038.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test other than the five named above that goes red is never edited to pass; report it
   and stop.
5. NOTHING IS MERGED OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no
   branch deletion, no force-push, no `git stash`, and no `git commit --amend` or any other
   rewrite of a commit, pushed or not: a wrong commit subject is declared, never amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r2-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2382330 | d4b172c0f51fe848cd385753ebb4044a40353e53ac1e1c0db015429ebc5c62e2 |
 | .agent/live_review.md | 312479 | 2092ebf2ecece86924a54d63527c96efd2aa62b2b8244eaa493a988352b9ec2b |
 | docs/roadmap/design/grounded-chat-spec.md | 5261 | d4075ecf42cbd4c32cc327c61ab65fccba37cee1928f1da7ef8b65b62acf6f9e |
 | .agent/plan.md | 992 | bcb8cca73a353e29155d1d7eebcf64dab77b0504e644a13f4ddb3052095c2219 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT read with `git show <commit>:<path>`, at
 `733d5db69` and at C2 (the reviewer read `['R-1091']` and `[]`); and
 `git diff --name-only <C1b> <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/chat_evidence.py
 tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py` at C4, with its real
 exit code. Then report, quoted from `git show <C3>`, the module docstring, the whole of the
 prompt-trace function of S2, and the whole of `collect_project_evidence`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_chat_evidence.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_env_registry.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -4; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `733d5db69` and read
 `756 passed, 6 skipped` at exit code 0, the six skips being the F252 quarantine in
 `tests/regression/test_named_bugs.py`; over its simulation tree, a fresh worktree carrying this
 round's records and its own version of the code and tests, it read `765 passed, 8 skipped` at
 exit code 0, where the two further skips are the vitest tests of
 `tests/orchestration/test_test_runner.py`, which run in the primary checkout. Report the node
 count of `tests/orchestration/test_chat_evidence.py` by `--collect-only -q` at `733d5db69` and at
 C4, every `SKIPPED` line and the summary, and account for any difference from 756 passed by
 those two counts. Then `python3 -m apps.cli.main integrity check --json`, which must read all
 six checks `pass` at `fail_count` 0, because R-1091 is resolved at C2.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r2-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/chat_evidence.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_chat_evidence.py` from the worktree's root after purging its
 `__pycache__` directories, with the worktree's root first on `PYTHONPATH`, restores the bytes,
 and prints one line per mutation: its label, the exit code, the failed count and the failing
 node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  n1 a prompt item's text carries the entry's `prompt_text_redacted`;
  n2 a trace line that parses to something not a dict is not skipped;
  n3 the project scope takes every job, linked or not;
  n4 the linked jobs come oldest first;
  n5 a decision's ref is its id alone, without its job;
  n6 the roadmap is read from Remedy's own repository instead of the project's;
  n7 an in-progress feature reads as the next open feature;
  n8 a resolved dossier risk is listed;
  n9 an unmeasured ledger figure reads 0;
  n10 the job items come before the decisions;
  n11 the prompt items come after the diff.
 Run it: `git worktree add --detach .remedy-wt/f038-r2-mut <C4>`, then
 `python3 -B .agent/authored/f038-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r2-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f038-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `733d5db69` in that
 order (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal
 your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F038, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T001's grounded answer: the citation check, the unsupported marker and the canary
suite. State the open-findings count, 0, and the operator-questions count, 1.
