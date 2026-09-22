STEP F283 R2 — T001 SLICE B PART ONE: thread the flag where a command declares it, and register R-1020

GOAL
Book round 1's PASS, register R-1020, and migrate the ELEVEN refusal sites of
`apps/cli/commands/job.py` that sit outside `_cmd_run_next_task_local`. Two of the four
handlers serve commands declaring `supports_json: True`, so the flag is THREADED into them;
the other two can never receive one, so their sites take `json_output=False` and the reason
is on the record.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THIS ROUND MIGRATES, AND WHY THOSE ELEVEN
  `_cmd_show_job`       1 site  — `job.show` declares `supports_json: True` and answers a
                                  failure in prose today. THREADED: the signature gains
                                  `json_output: bool = False` and the `job.show` dispatch
                                  lambda passes `getattr(args, "json", False)`.
  `_refuse_budget_set`  1 site  — serves `job budget set`, also `supports_json: True`. It
                                  becomes `_refuse_budget_set(error, message, *,
                                  json_output) -> NoReturn` calling `fail()`, and its SIX
                                  callers each pass a token and the flag they already hold.
  `_cmd_create_job`     5 sites — has NO catalog entry and NO dispatch lambda; it is
                                  reachable only by direct import, so no `--json` can
                                  reach it. `json_output=False`.
  `_cmd_plan_job_local` 5 sites — `job.plan` declares `supports_json: False`.
                                  `json_output=False`.
NOT IN THIS ROUND: `_cmd_run_next_task_local`'s eight sites. Ten tests monkeypatch it with
a single-positional lambda, so threading it moves those tests in the same commit and that
is its own round. Landed 11, deferred 8 — a round never defers more than it lands
(amend0917 rule 3).

THE ONE TRANSFORMATION TO UNDERSTAND, unchanged from round 1: `fail()` writes the
`Error: ` prefix itself, so a migrated site passes its message WITHOUT it. `job.diff`
carries every site already transformed, and the identity proof is that
`tests/test_cli_main.py`, `tests/test_run_log_cli.py` and the job suites assert several of
these lines byte-for-byte.

R-1020 — WHAT THE AUTHORING DRY RUN FOUND, and why this round registers it rather than
fixing it. With the flag threaded, `_cmd_show_job(job_id_str="zzzznotajob",
json_output=True)` STILL writes prose to stderr and leaves stdout empty, because
`resolve_job_id` in `packages/orchestration/data_paths.py` prints and exits one line above
the handler's own failure path. 52 of the catalog's 111 `supports_json` commands reach one
of three such shared EXITING helpers. The repair needs a shape decision for the multi-line
ambiguous-prefix message and is round 3's, so this round PINS the gap executable:
`tests.diff` adds a test asserting the envelope `job show --json` owes, marked
`@pytest.mark.xfail(strict=True, ...)`. It reports XFAIL today. Do not try to make it pass.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r2-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f283-r2-scratch/`   YOURS. Every log, exit-code capture and script goes
      here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `python3 -c` or `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`); a `python3 -c` script with a newline followed by `#` is rejected.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f283-machine-contracts-part-two`, and `git log --oneline -1` must read
   `2aa0a6f8`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f283-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all five under `.remedy-wt/f283-r2-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| f283.diff | 25 | 1428 | 736d793e4529729ee1269b55475f0845c22c00ea0ff039b6e72bfd7bab509ef3 |
| job.diff | 229 | 10824 | e17f2c4b0be012278e22ec94e10b5d1ac0edc8fd8e41b05057f13c303a947817 |
| ledger.md | 4 | 7749 | 98ef4d9c8bbdd1abe060033824a951edeefe384357a80428a2bff95f9493d458 |
| plan.md | 49 | 2586 | a0c9d01a8ebf2140d845cddd4ac207580bb607ace8a53f8cde86fec40cbef405 |
| tests.diff | 52 | 2841 | e6d881b669759c29e4e680813b70a0658abf85dedfdb0c0d3e9e2625562e5150 |

`ledger.md` is an APPEND of TWO PARAGRAPHS beginning with a single newline that is the
record separator: the round 1 `Gate:` entry and the `- R-1020` registration, in that
order. `plan.md` is a REWRITE. The three `.diff` files go on with `git apply`; every one
was generated from the tree at `2aa0a6f8` and every one dry-ran with `git apply --check`
at real exit code 0.

THE ELEVEN SITES AND THEIR TOKENS, printed by the run that measured them, at the line
numbers they hold at `2aa0a6f8`. Each token is named for the CONDITION (DECISION F277 D8);
a catch-all handler gets a token named for the layer that refused (DECISION F277 D9). You
do not apply this table by hand — `job.diff` already carries it — you use it to READ the
diff and confirm the diff does what this says.

| exit line | code | function | token | json_output |
|---|---|---|---|---|
| 68 | 1 | _cmd_create_job | missing_argument | False |
| 74 | 1 | _cmd_create_job | invalid_task_type | False |
| 81 | 1 | _cmd_create_job | invalid_task_type | False |
| 95 | 3 | _cmd_create_job | no_project | False |
| 122 | 2 | _cmd_create_job | invalid_budget | False |
| 223 | 1 | _cmd_show_job | job_store_error | threaded |
| 733 | 1 | _cmd_plan_job_local | job_not_found | False |
| 796 | 1 | _cmd_plan_job_local | planner_capability_missing | False |
| 825 | 1 | _cmd_plan_job_local | planner_output_invalid | False |
| 831 | 1 | _cmd_plan_job_local | missing_dependency | False |
| 837 | 1 | _cmd_plan_job_local | planner_failed | False |

`_cmd_show_job` keeps its COMBINED `except (JobNotFoundError, JobStoreError)` handler and
gets ONE token, `job_store_error`, named for the layer. Finding R-0902 put those two
conditions in one handler on purpose — "a record that exists and cannot be read is named,
like a missing one, never a traceback" — and splitting it to win a second token would
undo a decision this feature does not own. The six `_refuse_budget_set` callers take
`invalid_argument`, `budget_field_wrong_store` twice, `unknown_budget_field` and
`invalid_budget_value` twice. EVERY MIGRATED SITE KEEPS THE EXIT CODE IT ALREADY USED.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are TWO
commits because the block and its payloads together exceed the 500-line cap; each stands
on its own arithmetic.

C1a — copy this block
  `.agent/authored/f283-r2-block.md` := this block, byte-for-byte.
  Subject: `F283 R2 C1a: copy round 2 block into .agent/authored/`
  Its insertions are this block's own line count. Report that count and confirm it is
  under 500; STOP rather than commit if it is not.

C1b — copy all five payloads into `.agent/authored/`
  One `.agent/authored/f283-r2-<name>` per payload, keeping each payload's own file name.
  Subject: `F283 R2 C1b: copy round 2 payloads into .agent/authored/`
  Expected insertions: 359.

C2 — book round 1's PASS and register R-1020
  `.agent/live_review.md`            += ledger.md (append, +4)
  `.agent/plan.md`                   := plan.md   (rewrite, +31/-31)
  `docs/roadmap/features/T2_F283.md` := `git apply` of f283.diff (+10/-0)
  All three in ONE commit: amend0917 rule 4 puts the plan slice and the verdict booking
  together, and amend0911-feedback rule A requires the owning feature's Acceptance line to
  ride in the SAME commit as the registration that assigns it.
  Subject: `F283 R2 C2: book round 1's PASS and register R-1020`
  EXPECTED INSERTIONS: 45 by `git show --numstat`. If yours differs, report what you
  measured and say so.

C3 — THE SLICE, product and tests in ONE commit because the tests are what verify it
  `git apply` job.diff then tests.diff.
  Subject: `F283 R2 C3: thread the json flag into job show and budget set, migrate eleven refusals`
  Expected insertions: 88 — 58 for `job.py` and 30 for the test file.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F283 R2 C4: rewrite handoff for round 2`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the six `.agent/authored/f283-r2-*` copies (the block plus the five payloads), `.agent/live_review.md`, `.agent/plan.md`,
   `docs/roadmap/features/T2_F283.md`, `apps/cli/commands/job.py`,
   `tests/cli/test_job_refusal_envelope.py` and `.agent/handoff.md`. Report the length you
   measure rather than checking it against a number this block states. In particular do
   NOT touch `README.md`, `docs/roadmap/STATUS.md`, `.agent/candidates.md`,
   `.agent/context.md`, `.agent/decisions.md`, `.agent/operator_questions.md`, anything
   under `packages/`, or any CLI module other than `job.py`.
4. DO NOT MIGRATE A SITE THIS BLOCK DOES NOT NAME, and DO NOT REPAIR R-1020. The eight
   `_cmd_run_next_task_local` sites, the four non-mechanical sites and the three shared
   exiting helpers stay exactly as they are. The xfail must still report XFAIL at the end
   of this round; an XPASS is a FAILED round, not a bonus.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. Any worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT — for each of the five payloads report the line count, byte count and sha256
 you measured against the PAYLOADS table; fifteen readings, all equal. Then for each
 `.agent/authored/f283-r2-*` copy — one per payload plus the block copy, six in all —
 compare it byte-for-byte with its source under `.remedy-wt/f283-r2-payloads/` (the block
 copy against `.remedy-wt/f283-r2-block.md`). Report one reading per copy and how many you
 compared; all True.

G2 THE BOOKING — at C2:
 (a) The `.agent/live_review.md` append by strict byte CONCATENATION. The reviewer
     measured 438701 plus 7749 equals 446450. Report your three beside those.
 (b) The open set by distinct id, with the repository's OWN `open_finding_ids` from
     `scripts/rotate_live_review.py`, which takes the file's TEXT, at `2aa0a6f8` and at
     C2. The reviewer measured 23 then 24. Report both counts AND the set difference in
     both directions: added exactly `{R-1020}`, removed empty.
 (c) `.agent/plan.md` at C2 equals `plan.md` byte-for-byte; report both sha256s and the
     line count, which is 49 and must be under the AGENTS.md 50-line rule.
 (d) `git diff --name-only <C1b> <C2>` names exactly three paths. Report the list and its
     length.

G3 THE SLICE IS THE REVIEWER'S BYTES — at C3, report each `git apply --check`'s real exit
 code before its real apply, then `git diff --name-only <C2> <C3>`, which must name
 exactly `apps/cli/commands/job.py` and `tests/cli/test_job_refusal_envelope.py`. Then
 report, by COUNTS you take from the committed tree and not from this block: how many
 `fail(` call sites `apps/cli/commands/job.py` now has, how many print-then-exit pairs
 remain in a handler WITHOUT `json_output`, and in which function they sit. The reviewer
 measured 32 `fail(` sites — round 1's 20, plus this round's 11, plus the one inside
 `_refuse_budget_set` itself — and 8 pairs remaining, all in `_cmd_run_next_task_local`.

G4 THE SLICE WORKS AND THE OPERATOR SEES THE SAME BYTES — run and report with real exit
 codes, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_job_refusal_envelope.py tests/cli/test_job_budget_set.py tests/cli/test_job_commands.py tests/cli/test_job_show.py tests/cli/test_job_stop.py tests/cli/test_job_report.py tests/cli/test_plan_approval.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/test_cli_main.py tests/test_data_paths.py tests/test_run_log_cli.py tests/orchestration/test_structured_planner_cli.py; echo "REAL_EXIT=$?"'
```
 The reviewer measured `703 passed, 1 xfailed` at real exit code 0 with the whole round
 staged. `tests/docs/` is in it because `docs/roadmap/**` changed; `tests/test_cli_main.py`
 and `tests/test_run_log_cli.py` are the identity proof for `_cmd_create_job` and
 `_cmd_plan_job_local`, whose sites no other suite reaches. REPORT THE XFAIL COUNT AS A
 NUMBER: it must be 1, and it must not be an XPASS. Then
 `python3 -m ruff check apps/cli/commands/job.py tests/cli/test_job_refusal_envelope.py`,
 real exit code 0, and `python3 -m apps.cli.main integrity check --json`, which must read
 all five checks `pass` at `fail_count` 0. DO NOT run the full suite: amend0917 rule 1
 gives a feature exactly one full-suite run and F283's belongs to its closure.

G5 THE NEW BEHAVIOUR IS REAL AND THE GUARD STILL GATES — in a disposable worktree under
 `.remedy-wt/` at your C3 tree, never committed:
 (a) PROVE THE THREADING, by calling the handler both ways and printing what you got:
     `_cmd_job_budget_set(job_id="zzzznotajob", field_name="not_a_field", raw_value="5",
     json_output=True)` must exit 2 with an EMPTY stderr and a stdout envelope carrying
     `"error": "unknown_budget_field"`, `"ok": false` and `"schema_version": 1`; the same
     call with `json_output=False` must exit 2 with an EMPTY stdout and the stderr line
     `Error: unknown budget field 'not_a_field'. Settable: ...`. Report both.
 (b) MUTATE AND SHOW RED: change `fail("unknown_budget_field"` to
     `fail("bad_field"` and show `tests/cli/test_job_refusal_envelope.py` still passes —
     it does, because no test names that token yet — and then change the ratchet's
     expected 8 to 9 and show the STRUCTURAL guard goes RED at
     `test_the_unflagged_sites_are_counted_not_forgotten`. Report both readings honestly,
     including the first one that does NOT go red: that is the reviewer's own gap and the
     handback is where it gets said, not hidden.
 Then REMOVE the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 5`, which must show C4, C3, C2, C1b, C1a in that order;
 `git worktree list`, which must show the primary checkout and the three `remedy/job-*`
 worktrees and nothing else; `git push origin feature/f283-machine-contracts-part-two`
 with its real outcome; then
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 1 of feature F283, round 2, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 2, then round 3 — R-1020's repair, which the reviewer rules comes BEFORE any
further group migration, because T001's catalog half is worth nothing while 52 of the 111
`supports_json` commands answer a bad argument in prose. Name that round 3 must delete the
`xfail` mark in the same commit that turns it green. State the open-findings count, 24
after C2, and the operator-questions count, 2.
