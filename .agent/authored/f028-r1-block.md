STEP F028 R1 — CLAIM F028 AND LAND T001: the draft pass of a task injection — the planner's one structured call, the placement, the budget check with its shortfall seed, the fence flags, and the draft as a create-only control file with a time to live

GOAL
Pull request 286 is merged; `main` is at `ceb90b8a` and F028 is the next unchecked line. Cut its
branch, claim it, re-head the live review record, book F288's round 10 verdict, record DECISION
F028 D1, and land T001: a new module `packages/orchestration/task_injection.py` that turns an
operator's task text into a DRAFT — a planned task, its placement, its budget check and its fence
flags — and stores that draft as a create-only control file that expires, plus its tests. Nothing
in this round applies a draft to a job; that is T002.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against the specification S1 to S8 below. Only the
`.agent/` records and the STATUS line travel as payloads. Read DECISION F028 D1 in the claim diff
before you write code: it is the design this specification implements. Read
`packages/orchestration/task_veto.py` whole before you write S8: its control-file helpers are the
pattern S8 copies.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f028-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f028-r1-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored.

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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `ceb90b8a`. Report all three. Then
   `git checkout -b feature/f028-task-injection` and report the branch. Do NOT pull: the Open PR
   Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 162 | 18447 | 6bbd385903e1ac6bcaf0bc7984ca7ff0499750482d6c07eb1d9576fd809f22d6 |
| context.md | 35 | 1462 | 72fac8a4bb22b544cd25f48eadccdd1a0d0a43a5b2f3f4a4b86b790d396f5683 |
| plan.md | 31 | 1178 | 9c5cdea09c3134af7505405261ba73f8ed58e9e32b6bb34db25532286031cb38 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`ceb90b8a` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F288's round 10 gate entry
appended), `docs/roadmap/STATUS.md` (F028's line `[ ]` to `[~]`) and `.agent/decisions.md`
(DECISION F028 D1 appended).

THE SPECIFICATION — all in the new module `packages/orchestration/task_injection.py`, whose
docstring names F028 T001 and DECISION F028 D1 and says in two sentences why a running job is
reached through control files and never through `job.json`. No `except Exception` anywhere in it.
S1 CONSTANTS. `INJECTION_DRAFT_SCHEMA_V = "task_injection_draft_v1"`,
   `INJECTION_DRAFTS_DIRNAME = "injection_drafts"`, `INJECTION_DRAFT_TTL_SECONDS = 900`,
   `MAX_INJECTION_TEXT_CHARS = 2000`, `INJECTED_TASK_ID_PREFIX = "INJ"`, `MAX_PLAN_TASKS` imported
   as `_MAX_TASK_PLAN_TASKS` from `packages/orchestration/schemas/models.py`, the placement bases
   `PLACEMENT_STATED = "stated"`, `PLACEMENT_CONTENT_OVERLAP = "content_overlap"` and
   `PLACEMENT_FRONTIER_DEFAULT = "frontier_default"`,
   `SHORTFALL_OPTIONS = ("extend_budget", "shrink_task", "drop")`, and
   `PLAN_BAND_TO_TOKEN_BAND` mapping `S`, `M`, `L`, `XL` to `TokenBand.LOW`, `TokenBand.MEDIUM`,
   `TokenBand.HIGH` and `TokenBand.UNKNOWN` of `token_economy`. Two exceptions:
   `TaskInjectionRefused(Exception)` carrying `code` and `detail`, and
   `TaskInjectionError(RuntimeError)` for a control area that cannot be used or an entry that
   cannot be trusted — loud, as `TaskVetoError` is.
S2 THE DRAFT MODEL. `InjectedTaskDraft(_Structured)` with `SCHEMA_V` the tag above,
   `schema_v: Literal["task_injection_draft_v1"]`, and `title: str`, `goal: str`,
   `acceptance: list[str]` (at least one), `est_tokens_band` (the plan `TokenBand` of
   `schemas/models.py`), `files_hint: list[str] = []` and `rationale: str`; a model validator
   refuses a blank acceptance entry, a blank title and a blank goal. It is NOT added to
   `SCHEMA_REGISTRY`.
S3 THE TEXT. `validate_injection_text(text) -> str` returns the text UNCHANGED or raises
   `TaskInjectionRefused`: not a `str` or blank after `.strip()` is `text_required`; longer than
   `MAX_INJECTION_TEXT_CHARS` is `text_too_long`; a character of `[\x00-\x08\x0b-\x1f\x7f]`, or a
   text `stream_evidence.redact_text` would change, is `text_invalid`. Newline and tab pass.
S4 THE GATE AND THE ID. `injection_refusal(job_state, plan_task_count) ->
   TaskInjectionRefused | None`, pure: a state `pingpong_job.job_is_terminal` calls terminal is
   `job_terminal` with the detail `f"the job is {state!r}; start a follow-up job for this work
   instead"` (state as its bare string value); `plan_task_count >= MAX_PLAN_TASKS` is `plan_full`,
   its detail naming the cap; otherwise None. `next_injected_task_id(existing_ids) -> str` answers
   the smallest `f"INJ{k}"`, `k` from 1, not in `existing_ids`.
S5 THE PLACEMENT. `place_injected_task(plan_tasks, files_hint, *, after=None) -> dict`, pure,
   over a list of `PlannedTask`, answering `{"depends_on", "basis", "position", "rationale"}` with
   `position` always `len(plan_tasks)`. Paths compare after surrounding whitespace and one leading
   `./` are dropped. In order: `after` not None and not an id of the plan raises
   `TaskInjectionRefused("unknown_task", ...)`, the detail
   `f"there is no task {after!r} in this job's plan; its tasks are: {listing}"` where `listing`
   joins the first ten ids with `", "` and, when there are more, adds `f" and {n} more"`;
   `after` given is `depends_on=[after]`, basis `stated`, rationale
   `f"placed after {after} because you named it"`; else the ids of every plan task sharing a path
   with `files_hint`, in plan order, basis `content_overlap`, rationale
   `f"placed after {', '.join(ids)} because they touch the same files: {', '.join(paths)}"` with
   `paths` the sorted shared paths; else `depends_on=[]`, basis `frontier_default`, rationale
   `"placed at the end of the plan with no dependency, because no planned task touches its files"`.
S6 THE BUDGET CHECK AND THE SEED. `injection_budget_check(budgets, counters, *, band, config) ->
   dict` calls `budget_guard.predict_next_task_cost(budgets, counters,
   band=PLAN_BAND_TO_TOKEN_BAND[band], config=config)` and answers the prediction's `to_json()`
   plus `"plan_band": band` and `"shortfall": prediction.would_breach`.
   `shortfall_decision_seed(check) -> dict` answers `question`, `options` (a list equal to
   `SHORTFALL_OPTIONS`), `option_labels` (one plain sentence per option; the `shrink_task` label
   says the task cannot shrink when `shrink_band` is None), `arithmetic` (the check's),
   `extend_to_usd` and `shrink_band`. `extend_to_usd` is
   `float(Decimal(repr(round(spent + expected, 6))).quantize(Decimal("0.01"), ROUND_CEILING))`
   over the check's `spent_cost_usd` and `expected_cost_usd`; `shrink_band` is the next smaller
   plan band (`XL`→`L`→`M`→`S`) and None for `S`.
S7 THE FENCES AND THE PROMPT. `fence_conflicts(files_hint, fences) -> list[dict]` reads a
   `JobFences` or None with `fnmatch.fnmatch`, in `files_hint` order: the first deny glob a path
   matches gives `{"path", "rule": "deny", "glob"}`; otherwise, when `fences.allow` is not empty
   and no allow glob matches, `{"path", "rule": "not_allowed", "glob": ""}`; a path meeting
   neither gives nothing. `compose_injection_prompt(text, plan_tasks, *, after=None) -> str` holds
   the operator's text verbatim, every plan task's id, title and `files_hint`, the stated `after`
   when given, and instructions to phrase acceptance criteria as checks a test can make, to choose
   `est_tokens_band` and to name the files the task will touch.
S8 THE DRAFT AND ITS FILE. `draft_task_injection(job, text, *, call_fn, budgets, counters, config,
   actor, after=None, now=None, control_root_path=None) -> dict` NEVER raises for a refusal: it
   answers `{"outcome": "refused", "code", "detail"}` from the first of, in order, S3, S4's
   terminal check, a `job.task_plan` that is None or fails `TaskPlan.model_validate` once its
   `_`-prefixed keys are dropped (`no_task_plan`), S4's cap check, S5's unknown `after` (checked
   BEFORE any call), `call_fn` None (`planner_unavailable`), a `run_structured_call` over
   `InjectedTaskDraft` with `compose_injection_prompt` that is not ok (`draft_unparseable`), and a
   `TaskPlan` of the plan's tasks plus the new `PlannedTask` that fails validation
   (`draft_invalid`). A refusal writes nothing. Otherwise the new `PlannedTask` takes S4's id, the
   draft's fields and S5's `depends_on`; the check is S6 over its band; and the answer is
   `outcome` (`"drafted"`, or `"shortfall"` when the check shows one), `job_id`, `draft_id` (from
   `safe_points.new_request_id()`), `confirm_token` (the draft id, or None on a shortfall),
   `task` (the `PlannedTask`'s `model_dump()`), `placement` (S5's dict), `task_rationale` (the
   draft's), `budget_check`, `decision_seed` (S6's seed on a shortfall, else None),
   `fence_conflicts` (S7 over `job.fences`), `drafted_at` and `expires_at` (`now`, default the
   current UTC time, and `now` plus `INJECTION_DRAFT_TTL_SECONDS`, both `isoformat()`),
   `planner_calls` (the call's `calls`) and `text`. Before answering it publishes the answer, plus
   `injection_draft_v: 1`, `status` (`"confirmable"` or `"needs_decision"`), `actor` (bounded as
   `task_veto._bounded_actor` bounds it) and `after`, as ONE create-only file in
   `INJECTION_DRAFTS_DIRNAME` under the job's control directory, named by the first 32 hex
   characters of the sha256 of the draft id plus `.json`, through `safe_points.open_job_control_fd`
   and `secure_fs.write_file_atomically(..., create_only=True)` exactly as `record_task_veto` does,
   with a named-directory helper of its own written as `task_veto._open_named_dir` is.
   `read_injection_draft(job_id, draft_id, *, now=None, control_root_path=None) -> dict` answers
   the stored record, or raises `TaskInjectionRefused`: `draft_unknown` when `draft_id` fails
   `safe_points.is_safe_id` or no file exists, `draft_expired` when `now` is at or past
   `expires_at`. It never deletes a file. A file that is not a JSON object, or whose `draft_id`
   differs from the one asked for, raises `TaskInjectionError`.

THE TESTS — NEW FILE at `tests/orchestration/test_task_injection.py`, every test using `tmp_path` as the
control root and a fake `call_fn(prompt, attempt) -> str` answering JSON, never a real provider.
At least: S3's four codes and a text holding a newline and a tab returned unchanged, the
secret-shaped sample BUILT AT RUN TIME by concatenation and never written whole in the file;
S4's `job_terminal` for `completed`, `failed` and `cancelled` with the follow-up words in the
detail, None for `paused`, `blocked`, `planned` and `running`, `plan_full` at 25 tasks, and the
ids `INJ1`, `INJ3` over `INJ1`, `INJ2`, and `INJ1` over `INJ2`; S5's three bases with their exact
rationale sentences, the plan order of the overlap ids, `./a.py` meeting `a.py`, and
`unknown_task` with more than ten ids naming the count left over; S6 with a limit of $1.00, spent
$0.90, a price basis of $0.01 per thousand tokens and class defaults 8000, 32000 and 120000 —
band `S` no shortfall, band `M` a shortfall whose seed reads `extend_to_usd` 1.22 and
`shrink_band` `S`, band `XL` read as `unknown` with basis `class_default_missing_band`, spent
$0.95 with band `S` a shortfall with `shrink_band` None, and no cost limit no shortfall; S7's
deny flag, allow miss, allowed path and None fences; and S8: a drafted answer whose file exists
and reads back through `read_injection_draft` equal to the answer plus the stored keys, the fake
call receiving the text verbatim, `planner_calls` 1, then 2 after one invalid reply,
`draft_unparseable` after two with no file written, `planner_unavailable` and `unknown_task` with
the fake never called and no file written, a shortfall answer with no token, status
`needs_decision` and its seed, `read_injection_draft` at 899 seconds reading and at 900 seconds
refusing `draft_expired` with the file still present, `draft_unknown` for an unknown id and for
`../x`, `TaskInjectionError` for a corrupt file, and `task_injection_draft_v1` absent from
`SCHEMA_REGISTRY`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f028-r1-block.md` := this block, and `.agent/authored/f028-r1-plan.md` and
  `.agent/authored/f028-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F028 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 66. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f028-r1-claim.diff` := claim.diff.
  Subject: `F028 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 162.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F028 R1 C2: claim F028, re-head the live review record, book F288 R10, record D1`
  Expected by `git show --numstat` (insertions and deletions): 13/13 context.md, 80/0 decisions.md, 23/20 live_review.md, 18/13 plan.md, 1/1 STATUS.md.

C3 — THE CODE: `packages/orchestration/task_injection.py`, and in the same commit one entry in
  `ALLOWED_UNWIRED` of `tests/test_no_orphan_modules.py`, in its alphabetical place,
  `("packages/orchestration/task_injection.py", "F028 T001's draft pass; T002's confirmation wires it into run_job (DECISION F028 D1)")`,
  because the module has no importer until T002 and the orphan guard would otherwise go red.
  Subject: `F028 R1 C3: draft a task injection with its placement, budget check, fence flags and expiring control file`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_task_injection.py` and your mutation tool
  (G5) saved as `.agent/authored/f028-r1-mutations.py`.
  Subject: `F028 R1 C4: test the injection draft pass and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F028 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f028-task-injection`. Do NOT create a pull request: the
  branch opens one at F028's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/task_injection.py`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/test_task_injection.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only ceb90b8a` at the
   branch tip after C5. Do NOT touch `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/plan_editing.py`, `packages/orchestration/task_veto.py`,
   `packages/orchestration/schemas/models.py`, `packages/orchestration/ui_server.py`, anything
   under `apps/`, `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `README.md` or `docs/roadmap/features/T5_F028.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F028's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f028-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | docs/roadmap/STATUS.md | 54827 | b04a95ce95ad188d7b71b81053613dc0338031914d8b2b05b4fc544f918f6c39 |
 | .agent/live_review.md | 309281 | cd3ff35d8c4c71ff1bef4dadf8251484b6ea85ab7450899cb019681608909860 |
 | .agent/decisions.md | 2250640 | 56a1d938b0db6bfb7ac41d6c52acb2a20b7356da40395a7fc913a1cf2437ba6f |
 | .agent/plan.md | 1178 | 9c5cdea09c3134af7505405261ba73f8ed58e9e32b6bb34db25532286031cb38 |
 | .agent/context.md | 1462 | 72fac8a4bb22b544cd25f48eadccdd1a0d0a43a5b2f3f4a4b86b790d396f5683 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `ceb90b8a` and at C2 (the reviewer read
 it empty at both); at C2 the ledger has exactly one line reading `## Findings` and exactly one
 reading `## Steps`, and its last line begins `Gate: F288 R10 — `; F028's STATUS line at C2 read
 back in full, which must begin `- [~] F028 — `; and `git diff --name-only <C1b> <C2>`, which
 must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/task_injection.py
 tests/orchestration/test_task_injection.py tests/test_no_orphan_modules.py` at C4, with its real
 exit code. Then report, quoted from `git show <C3>`, the whole of `place_injected_task`,
 `shortfall_decision_seed` and the refusal ladder at the top of `draft_task_injection`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_plan_editing.py tests/orchestration/test_task_veto.py tests/orchestration/test_budget_guard.py tests/orchestration/schemas/test_schemas.py tests/orchestration/test_structured_outputs.py tests/orchestration/test_import_reachability.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/orchestration/test_task_injection.py`, serially, in
 the primary checkout at `ceb90b8a` before any change, and read `1022 passed, 7 skipped` at real
 exit code 0. The seven skips are the F252 quarantines in `tests/regression/test_named_bugs.py`
 and `tests/test_agent_tooling.py` and stay skipped. Report every `SKIPPED` line the `-rs`
 summary prints, the node count of `tests/orchestration/test_task_injection.py` by
 `--collect-only -q`, and account for any difference from 1022 plus that count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r1-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/task_injection.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_task_injection.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and
 last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. The mutations, each a real behaviour change:
  m1 S3 admits the character `\x07`;
  m2 S4 answers None for a terminal job;
  m3 `next_injected_task_id` always answers `INJ1`;
  m4 S5 ignores `after`;
  m5 S5 never finds a content overlap;
  m6 `XL` reads as `TokenBand.HIGH`;
  m7 a shortfall answer carries the draft id as its confirm token;
  m8 `extend_to_usd` rounds down (`ROUND_FLOOR`);
  m9 `read_injection_draft` refuses only strictly after `expires_at`;
  m10 S7 never flags a deny glob;
  m11 the structured call runs with `allow_parse_retry=False`;
  m12 the unknown-`after` check runs after the call instead of before it.
 Run it: `git worktree add --detach .remedy-wt/f028-r1-mut <C4>`, then
 `python3 -B .agent/authored/f028-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r1-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C5 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r1-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `ceb90b8a` in that order
 (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your
 step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F028, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — the confirmation, the runner's fold, the edit log, the provenance, the event
and the shortfall seed's answers. State the open-findings count, 0, and the operator-questions
count, 0.
