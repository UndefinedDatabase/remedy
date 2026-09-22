STEP F283 R3 — R-1020's FIRST REPAIR: the job-id argument answers a machine

GOAL
Book round 2's PASS, correct R-1020's registration on the record, and land the layer the
finding needs: `apps/cli/job_id_arg.py::resolve_job_id_or_fail`, which catches what
`lookup_job_id` raises and refuses through `fail()`. Move `job.py`'s six call sites onto
it and turn the strict xfail green, deleting its mark in the same commit.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY A NEW MODULE RATHER THAN A CHANGE TO THE RESOLVER
`packages/orchestration/data_paths.py::resolve_job_id` is the EXITING form of the lookup:
it prints a prose line and calls `sys.exit` itself, one call ABOVE the handler's own
failure path. That is why `job show --json` still answered in prose after round 2 threaded
the flag into its handler. The non-exiting form already exists — `lookup_job_id` raises —
and `resolve_job_id`'s own docstring names this as the intended shape. So the repair is a
LAYER: a new `apps/cli/job_id_arg.py` that guards the parse once for every CLI caller.
`resolve_job_id` is NOT changed and NOT deleted; callers with no failure path of their own
keep using it. Remedy deliberately does not put `fail()` inside `packages/`: the envelope
is a CLI contract, and pushing it down would make the storage layer depend on the shape of
a command's stdout.

THE TEXT BRANCH IS BYTE-IDENTICAL. `fail()` writes `Error: ` itself, and the ambiguous
message reproduces the old helper's header line plus its one indented line per match, so
an operator's terminal does not change. `tests/test_data_paths.py` asserts one of those
lines exactly and is in this round's gate for that reason.

R-1020 IS NOT RESOLVED BY THIS ROUND. Six of its twenty-three call sites move; seventeen
stay, in `change`, `contract_cmd`, `decision`, `job_context_cmd`, `job_stop_cmd`, `patch`,
`project` and `teacher_cmd`. `tests.diff` adds a second guard that counts those seventeen
and reds if the number rises. The finding stays OPEN and keeps its owner.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r3-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f283-r3-scratch/`   YOURS. Every log, exit-code capture and script goes
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
   `fc8dfd85`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f283-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all seven under `.remedy-wt/f283-r3-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| allowlist.diff | 12 | 502 | 3129f68524a2154e48abba6c4f73012dd221919efcf7b7e592cca7985c1f3ed9 |
| job.diff | 70 | 2660 | bc363edb8174fd7e3c3a1446a0fb9afe9eae17ca8140553b802ae8ecf87a94b3 |
| job_id_arg.py | 60 | 2941 | 026c6c0b5b0c3af0fbee685fadb19ddd7aedd7ad810e158d1cd754c80c0828e7 |
| ledger.md | 4 | 6963 | 6560e044072d49abe999f9498d53f4a6e80c9c766e179504decc89a5df460dc8 |
| plan.md | 49 | 2377 | 9ba2e7b13ef410ffed3c38d4c21793766c922ccba6b2fb44fae62d6af763f75e |
| slips.md | 1 | 1420 | 2e904658e4cbf1f978ed770cca921885f35a6a126355b5ddddc93248ba246bf2 |
| tests.diff | 73 | 3828 | 006ee0bce3200a8cc07504360bda52a6260532f1a8e8429c0977c3f8bbd156bd |

`ledger.md` is an APPEND of TWO PARAGRAPHS beginning with a single newline that is the
record separator: the round 2 `Gate:` entry and a `DECISION F283 D1` record. `slips.md` is
an APPEND of ONE line with no leading newline. `plan.md` is a REWRITE.
`job_id_arg.py` is a NEW FILE, copied whole to `apps/cli/job_id_arg.py`. The three `.diff`
files go on with `git apply`; every one was generated from the tree at `fc8dfd85` and
every one dry-ran with `git apply --check` at real exit code 0.

THE CORRECTION IS A `DECISION` RECORD AND NOT A SECOND `- R-1020 — ` BLOCK, and that is
load-bearing rather than stylistic: `scripts/rotate_live_review.py::select_movable` moves a
finding pair only when its id has EXACTLY ONE registration record and EXACTLY ONE `Done:`
record, so a second registration line would jam R-1020's pair in the live ledger for good.
The reviewer verified on the composed text that the append leaves exactly one `^- R-1020 — `
line and zero `^Done: R-1020 — ` lines, and that the open count is 24 before and 24 after.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are TWO
commits because the block and its 269 lines of payload together exceed the 500-line cap.

C1a — copy this block
  `.agent/authored/f283-r3-block.md` := this block, byte-for-byte.
  Subject: `F283 R3 C1a: copy round 3 block into .agent/authored/`
  Its insertions are this block's own line count. Report it and confirm it is under 500.

C1b — copy all seven payloads into `.agent/authored/`
  One `.agent/authored/f283-r3-<name>` per payload, keeping each payload's own file name.
  Subject: `F283 R3 C1b: copy round 3 payloads into .agent/authored/`
  Expected insertions: 269.

C2 — book round 2's PASS and correct R-1020
  `.agent/live_review.md`   += ledger.md (append, +4)
  `.agent/plan.md`          := plan.md   (rewrite, +22/-22)
  `.agent/prose_slips.md`   += slips.md  (append, +1)
  Subject: `F283 R3 C2: book round 2's PASS and correct R-1020 on the record`
  EXPECTED INSERTIONS: 27 by `git show --numstat` — 4 plus 22 plus 1, every summand
  printed by the script that measured it rather than typed beside it, which is the
  counter-measure the slip this round books asks for. If yours differs, report what you
  measured and say so.

C3 — THE REPAIR, product and tests in ONE commit because the tests are what verify it
  Copy `job_id_arg.py` to `apps/cli/job_id_arg.py` and `git add` it — an untracked file
  fails `integrity check`'s `relevant_untracked`. Then `git apply` job.diff, tests.diff
  and allowlist.diff.
  Subject: `F283 R3 C3: resolve a job id through the envelope, not the exiting helper`
  Expected insertions: 116 — 60 for the new module, 8 for `job.py`, 47 for the test file
  and 1 for the allowlist.
  THE ALLOWLIST ENTRY IS NOT OPTIONAL: `tests/orchestration/test_import_reachability.py`
  is a ratchet over the reachable closure, and a new module reachable from an entry point
  reds it until its name is listed. `allowlist.diff` adds `apps.cli.job_id_arg` in sorted
  position.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F283 R3 C4: rewrite handoff for round 3`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the eight `.agent/authored/f283-r3-*` copies, `.agent/live_review.md`, `.agent/plan.md`,
   `.agent/prose_slips.md`, `apps/cli/job_id_arg.py`, `apps/cli/commands/job.py`,
   `tests/cli/test_job_refusal_envelope.py`,
   `tests/orchestration/import_reachability_allowlist.txt` and `.agent/handoff.md`.
   Report the length you measure rather than checking it against a number this block
   states. In particular do NOT touch anything under `packages/` —
   `packages/orchestration/data_paths.py` keeps `resolve_job_id` exactly as it is — and do
   NOT touch `README.md`, `docs/roadmap/**`, `.agent/candidates.md`, `.agent/context.md`,
   `.agent/decisions.md` or `.agent/operator_questions.md`.
4. DO NOT MIGRATE A CALL SITE OUTSIDE `job.py`. The seventeen in the eight other modules
   are later rounds. If a gate seems to need one moved, STOP and hand back.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
7. Leave the three `remedy/job-*` worktrees alone. Any worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT — for each of the seven payloads report the line count, byte count and sha256
 you measured against the PAYLOADS table; twenty-one readings, all equal. Then for each
 `.agent/authored/f283-r3-*` copy — one per payload plus the block copy, eight in all —
 compare it byte-for-byte with its source under `.remedy-wt/f283-r3-payloads/` (the block
 copy against `.remedy-wt/f283-r3-block.md`). Report one reading per copy and how many you
 compared; all True.

G2 THE BOOKING AND THE CORRECTION — at C2:
 (a) The `.agent/live_review.md` append by strict byte CONCATENATION: the reviewer
     measured 446450 plus 6963 equals 453413. The `.agent/prose_slips.md` append the same
     way: 358529 plus 1420 equals 359949. Report all six of your numbers.
 (b) THE CORRECTION DID NOT BREAK R-1020's PAIRING, which is the one thing that could go
     wrong here. Count, on the committed file at C2 and by line-anchored search:
     `^- R-1020 — ` must be 1 and `^Done: R-1020 — ` must be 0. Then report the open set
     by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py` at
     `fc8dfd85` and at C2 — the reviewer measured 24 and 24, with BOTH set differences
     empty, because this round registers nothing and resolves nothing.
 (c) `.agent/plan.md` at C2 equals `plan.md` byte-for-byte; report both sha256s and the
     line count, which is 49 and must be under the AGENTS.md 50-line rule.
 (d) `git diff --name-only <C1b> <C2>` names exactly three paths. Report the list and its
     length.

G3 THE REPAIR IS THE REVIEWER'S BYTES — at C3, report each `git apply --check`'s real exit
 code before its real apply, then `git diff --name-only <C2> <C3>`, which must name
 exactly `apps/cli/job_id_arg.py`, `apps/cli/commands/job.py`,
 `tests/cli/test_job_refusal_envelope.py` and
 `tests/orchestration/import_reachability_allowlist.txt`. Then report, by COUNTS you take
 from the committed tree: how many `resolve_job_id(` call sites remain in
 `apps/cli/commands/job.py`, and how many remain across all of `apps/cli/`. The reviewer
 measured 0 and 17. Confirm by reading that `packages/orchestration/data_paths.py` is NOT
 in the round's path set at all.

G4 THE REPAIR WORKS AND THE OPERATOR SEES THE SAME BYTES — run and report with real exit
 codes, in the primary checkout:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_import_reachability.py tests/cli/test_job_refusal_envelope.py tests/cli/test_job_budget_set.py tests/cli/test_job_commands.py tests/cli/test_job_show.py tests/cli/test_job_stop.py tests/cli/test_job_report.py tests/cli/test_plan_approval.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/test_cli_main.py tests/test_data_paths.py tests/test_run_log_cli.py tests/orchestration/test_structured_planner_cli.py; echo "REAL_EXIT=$?"'
```
 The reviewer measured `708 passed` at real exit code 0 with the whole round staged, and
 ZERO xfailed — the mark is gone, which is the point. REPORT THE XFAIL COUNT AS A NUMBER;
 it must be 0. `tests/test_data_paths.py` is in the selection because it asserts the
 resolver's prose line byte-for-byte and is the identity proof for this repair. Then
 `python3 -m ruff check apps/cli/commands/job.py apps/cli/job_id_arg.py tests/cli/test_job_refusal_envelope.py`,
 real exit code 0, and `python3 -m apps.cli.main integrity check --json`, which must read
 all five checks `pass` at `fail_count` 0. DO NOT run the full suite.

G5 THE REPAIR IS REAL AND STILL GATED — in a disposable worktree under `.remedy-wt/` at
 your C3 tree, never committed:
 (a) PROVE IT by calling the handler both ways and printing what you got:
     `_cmd_show_job(job_id_str="zzzznotajob", json_output=True)` must exit 1 with an EMPTY
     stderr and a stdout envelope carrying `"error": "invalid_job_id"`, `"ok": false` and
     `"schema_version": 1`; the same call with `json_output=False` must exit 1 with an
     EMPTY stdout and the stderr line
     `Error: No job matches 'zzzznotajob'. Try: remedy job list.` — byte-for-byte what the
     exiting helper printed before this round. Report both.
 (b) MUTATION ONE: in `apps/cli/job_id_arg.py` change `"invalid_job_id"` to `"bad_id"` and
     show `tests/cli/test_job_refusal_envelope.py` goes RED. The reviewer read
     `1 failed, 8 passed` at exit 1.
 (c) MUTATION TWO: revert `_cmd_show_job`'s call back to `resolve_job_id(job_id_str)` —
     restoring the `resolve_job_id` import so the file still parses — and show the same
     file goes RED. The reviewer read `1 failed, 8 passed` at exit 1. Without (c) the test
     could be satisfied by a token alone rather than by the call site actually moving.
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
Session section reads SESSION 1 of feature F283, round 3, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 3, then round 4 — R-1020's remaining seventeen call sites, largest module first:
`patch` 7, `change` 3, `teacher_cmd` 2, then `contract_cmd`, `decision`,
`job_context_cmd`, `job_stop_cmd` and `project` at one each. State the open-findings
count, 24 and unchanged by this round, and the operator-questions count, 2.
