STEP F283 R5 — R-1021: a prefix two jobs share is refused as AMBIGUOUS everywhere

GOAL
Book round 4's PASS, R-1020's `Done:` and R-1022's registration, then move the nineteen
hand-caught `lookup_job_id` sites under `apps/cli/` onto
`apps/cli/job_id_arg.py::resolve_job_id_or_fail`, one module per commit, and fix
R-1022's two sentences.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge. As in round 4, the reviewer
authors only the RECORD payloads; every change under `apps/` and `tests/` is yours,
written to the SPEC in each commit.

THE DEFECT (R-1021, registered at `901ba21d`)
`lookup_job_id` raises `JobIdAmbiguous` for a prefix that matches more than one job, and
`JobIdAmbiguous` is a `ValueError`. Nineteen sites catch it with `except ValueError` (or
wider) and answer "No job matches" at exit 1 — a false message, and under `--json` an
`invalid_job_id` with no `matches`. Measured at `6c199d4f` by the reviewer's
`.remedy-wt/f283-r5-scratch/lookup_ctx.py`:
  brain.py 11 · snapshot_cmds.py 2 · test_cmds.py 2 · event.py 1 · file.py 1 ·
  memory.py 1 · project.py 1 (`_cmd_attach_project_job`)
The two other `lookup_job_id` callers — `apps/cli/job_id_arg.py` and
`apps/cli/commands/job_stop_cmd.py` — already handle `JobIdAmbiguous` and do NOT move.

THE ONE RULE FOR EVERY MIGRATED SITE
Replace the whole `try: job_id = lookup_job_id(<raw>) / except ValueError: <refusal>`
construction with
  job_id = resolve_job_id_or_fail(<raw>, json_output=<flag>[, job_id=<raw>])
where <flag> is the handler's `json_output` or `as_json` when it has one and the literal
`False` when it does not. The `job_id=` payload is passed ONLY where the old JSON refusal
carried a `job_id` key (`snapshot_cmds.py` and `test_cmds.py::_cmd_test_status`, which
print `{"error": "invalid_job_id", "job_id": ...}` today). With `False` the stderr bytes
of the not-found case are identical to today's; the ambiguous case changes to what the
rest of the CLI already says, which is the repair. Import `resolve_job_id_or_fail` at
MODULE level and delete each `lookup_job_id` import the migration leaves unused.
`project.py`'s site catches `(ValueError, JobNotFoundError)` around TWO calls: split it
so the id resolves through `resolve_job_id_or_fail(..., json_output=False)` and the
`require_job_plan` call keeps a `try/except JobNotFoundError` that prints today's bytes.
Do not touch `packages/` at all.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r5-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r5-scratch/`   YOURS for logs, captures and scripts; the reviewer's
      scripts already there (`lookup_ctx.py`, `handler_ids.py`) are read-only to you.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `$?` or `${...}` outside a `bash -c`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts or a
file in your scratch directory for counting, hashing and copying (`shutil.copyfile`).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `6c199d4f`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r5-block.md` against the two readings your delegation message
   states. Report both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r5-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 6 | 7100 | 511d753dca96b9af83bba940c4e84f1051b2ec6177b57ae53a798092e9bbe3b0 |
| plan.md | 40 | 1870 | f06f1ab9cce24a1f40106403127b4193587efe595ab0e33d7d12085a981f02e3 |

`ledger.md` is an APPEND beginning with the single newline that separates records: the
round 4 `Gate:` entry, R-1020's `Done:` line and R-1022's registration. `plan.md` is a
REWRITE. There is no slips payload this round. Never retype or edit a payload.

BUNDLE — commits C1 to C9, in this order.

C1 — `.agent/authored/f283-r5-block.md` := this block; `.agent/authored/f283-r5-<name>`
  for each payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R5 C1: copy round 5 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md
  Subject: `F283 R5 C2: book round 4's PASS, resolve R-1020, register R-1022`

C3 — the pass-through, the guard, and R-1022
  SPEC, `apps/cli/job_id_arg.py`: `resolve_job_id_or_fail(raw, *, json_output,
  **payload: Any)` and `refuse_ambiguous_job_id(raw, matches, *, json_output,
  **payload: Any)` forward `payload` to every `fail()` they make; docstrings say so in
  one sentence each. Behaviour with no payload is unchanged.
  SPEC, `tests/cli/test_job_refusal_envelope.py`:
  - A module-level `_lookup_calls(source: str) -> int` counting `ast.Call` nodes whose
    callee is the name `lookup_job_id` or an attribute `<anything>.lookup_job_id`, and a
    test class asserting the per-file dict over `apps/cli/` EQUALS a module constant
    `_LOOKUP_CALLERS`, which at C3 reads
    {"brain.py": 11, "event.py": 1, "file.py": 1, "job_id_arg.py": 1,
     "job_stop_cmd.py": 1, "memory.py": 1, "project.py": 1, "snapshot_cmds.py": 2,
     "test_cmds.py": 2}
    and whose comment says it falls to `job_id_arg.py` and `job_stop_cmd.py` alone, the
    two callers that handle `JobIdAmbiguous` themselves. One non-vacuity test: an
    attribute call in a source string counts 1.
  - A test that `resolve_job_id_or_fail("zzzznotajob", json_output=True, job_id="x")`
    exits 1 with an envelope carrying `job_id` equal to `"x"`.
  - R-1022: the docstring of `TestEveryMigratedJsonCommandAnswersABadIdInTheEnvelope`
    no longer says the handback names a command left out; it says a command whose
    refusal fired before the resolver would be left out and named in its round's
    handback, and that in round 4 none was. The comment above
    `_EXITING_RESOLVER_REMAINING` names the `Gate: F283 R3` entry of
    `.agent/live_review.md` as where the alias correction is recorded. Nothing else in
    those two passages changes.
  Subject: `F283 R5 C3: the job-id layer carries a payload, and a guard pins its callers`

C4 — `brain.py`, all eleven; its key leaves `_LOOKUP_CALLERS` in the same commit.
  Subject: `F283 R5 C4: brain refuses an ambiguous job id as ambiguous`
C5 — `snapshot_cmds.py`, both, with `job_id=`; its key leaves the constant. Add one test
  (in the file you judge nearest; name it in the handback) that `snapshot inspect
  zzzznotajob <any> --json` through `apps.cli.grouped.main` exits 1 with an envelope
  whose `job_id` is `zzzznotajob`.
  Subject: `F283 R5 C5: snapshot refuses a job id through the envelope`
C6 — `test_cmds.py`, both (`job_id=` only where the old JSON carried it); its key leaves
  the constant.
  Subject: `F283 R5 C6: test refuses a job id through the envelope`
C7 — the tail: `event.py`, `file.py`, `memory.py`, `project.py`. `_LOOKUP_CALLERS`
  becomes {"job_id_arg.py": 1, "job_stop_cmd.py": 1}. `tests/cli/test_change_proof_cli.py`
  patches `apps.cli.commands.file.lookup_job_id` once
  (`test_file_why_proof_status_agrees_with_change_proof_path`): point it at
  `apps.cli.commands.file.resolve_job_id_or_fail` with `side_effect=lambda raw, **_: raw`
  and change nothing else in that file.
  Subject: `F283 R5 C7: the last four modules refuse an ambiguous job id as ambiguous`

C8 — THE DEFECT, PROVED THROUGH THE REAL PARSER
  SPEC, a new class in `tests/cli/test_job_refusal_envelope.py`. A fixture writes two
  `jobs/<id>/job.json` records, `aaaa1111-0000-0000-0000-000000000001` and `...0002`,
  under a `REMEDY_DATA_DIR` set to `tmp_path` (the shape round 4's ambiguous tests use).
  (i) One parametrized case per `supports_json` command id among `brain.graph`,
  `brain.node`, `brain.context`, `brain.continue`, `event.list`, `event.show`,
  `event.timeline`, `event.replay`, `file.why`, `memory.learn`, `snapshot.inspect`,
  `snapshot.list-applies`, `test.discover`, `test.status`: `apps.cli.grouped.main` with
  job id `aaaa1111`, placeholders for other required positionals read off the catalog,
  and `--json`; exit 2, stderr empty, one envelope with `error` `ambiguous_job_id` and
  `matches` equal to both ids sorted.
  (ii) One parametrized case per text-only command id among `brain.view`, `brain.trust`,
  `brain.timeline`, `brain.cockpit`, `brain.constitution`: exit 2, empty stdout, and
  stderr EQUAL to what `packages.orchestration.data_paths.resolve_job_id("aaaa1111")`
  writes, captured in the same test.
  A command that does not reach the resolver with that argv, or whose refusal fires
  first, is NOT forced: leave it out, never xfail or skip it, and name it in the handback
  with what you measured.
  Subject: `F283 R5 C8: an ambiguous job id is refused as ambiguous through the parser`

C9 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R5 C9: rewrite handoff for round 5`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the three `.agent/authored/f283-r5-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
   `apps/cli/job_id_arg.py`, and under `apps/cli/commands/` `brain.py`,
   `snapshot_cmds.py`, `test_cmds.py`, `event.py`, `file.py`, `memory.py`, `project.py`;
   `tests/cli/test_job_refusal_envelope.py`, `tests/cli/test_change_proof_cli.py`, and
   the ONE test file C5 names. A test a migration breaks is repaired in that same commit
   ONLY if it is one of those paths; any other breakage means STOP. Report the set you
   measure. Nothing under `packages/` or `docs/`, no `README.md`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/decisions.md`,
   `.agent/operator_questions.md`, `.agent/prose_slips.md`, `apps/cli/json_envelope.py`.
4. Migrate ONLY the nineteen. Refusal pairs that are not a `lookup_job_id` guard stay as
   they are, including every other `print(...); sys.exit()` in those modules.
5. Every commit leaves the G4 selection green.
6. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
7. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
8. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C9 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r5-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r5-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `6c199d4f` (459745 bytes)
     plus ledger.md equals the committed file; the reviewer composed 466845.
 (b) Line-anchored on the committed ledger: `^- R-1020 — ` 1, `^Done: R-1020 — ` 1,
     `^- R-1022 — ` 1, `^Done: R-1022 — ` 0. Open set by distinct id via
     `open_finding_ids` from `scripts/rotate_live_review.py` at `6c199d4f` and at C2: the
     reviewer measured 25 and 25, ADDED exactly `R-1022`, REMOVED exactly `R-1020`.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE MIGRATION, COUNTED FROM THE TREE — for every commit C3 to C8 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions. At C8
 run the reviewer's `python3 .remedy-wt/f283-r5-scratch/lookup_ctx.py` and report its
 output: exactly two rows, `job_id_arg.py` and `job_stop_cmd.py`. Report
 `git diff --name-only 6c199d4f <C8> -- packages/`, which must print nothing.

G4 THE TARGETED SELECTION, in the primary checkout at C8:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/cli/test_change_proof_cli.py tests/cli/test_event_list_cmd.py tests/cli/test_file_provenance_cli.py tests/cli/test_memory_cmd.py tests/cli/test_snapshot_cli_runtime.py tests/cli/test_real_test_execution_cli.py tests/cli/test_test_run_runtime.py tests/cli/test_project_current.py tests/test_brain_detail.py tests/test_brain_smoke.py tests/test_brain_viewer.py tests/test_agent_loop.py tests/test_cockpit.py tests/test_timeline.py tests/test_trust_report.py tests/test_project_constitution.py tests/test_project_brain.py tests/test_memory_learn.py tests/test_command_discovery.py tests/test_test_runner.py tests/test_context_coverage.py tests/test_project_context_coverage.py tests/orchestration/test_project_resolution.py tests/orchestration/test_import_reachability.py tests/test_cli_main.py tests/test_data_paths.py tests/test_grouped_cli.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py; echo "REAL_EXIT=$?"'
```
 The reviewer read `1658 passed` at real exit code 0 at `6c199d4f`. If C5's new test lives
 in a file outside that list, add that file to the command and say so. Report your summary
 line and exit code; zero failed, zero xfailed, and the passed count may only rise. Then
 `python3 -m ruff check` over every `.py` path in constraint 3 that the round touched,
 and `python3 -m apps.cli.main integrity check --json`, all five checks `pass`. DO NOT
 run the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C8, never committed.
 Run `tests/cli/test_job_refusal_envelope.py` and C5's test file UNMUTATED first and
 report it (exit 0). Then each mutation alone, reverted before the next, reporting the
 summary line, the exit code and the names of the failing tests:
 (a) in `brain.py`, `_cmd_brain`'s migrated call passes `json_output=False` — the
     `brain.graph` case of C8 (i) must fail.
 (b) in `snapshot_cmds.py`, `_cmd_snapshot_inspect` drops its `job_id=` payload — C5's
     test must fail.
 (c) in `memory.py`, the migrated call is put back as the old `try: lookup_job_id /
     except ValueError: fail("invalid_job_id", ...)` construction — the `_LOOKUP_CALLERS`
     guard AND the `memory.learn` case of C8 (i) must fail.
 (d) in `apps/cli/job_id_arg.py`, `refuse_ambiguous_job_id` stops forwarding `payload`
     — report what goes red; if nothing does, say so plainly (it is a probe, not a
     colour: no C8 case passes a payload on the ambiguous path).
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C9: `git status --porcelain` empty; `git log --oneline -n 10`;
 `git worktree list` (primary plus the three `remedy/job-*`); the push's real outcome;
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the item-status table, the deviations, every C8 command left out and why, and the
next action. Your Session section reads SESSION 2 of feature F283, round 5, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 5, then round 6 — R-1021's and R-1022's `Done:` lines booked in its first
commit, and `_cmd_run_next_task_local`'s eight print-then-exit pairs in `job.py`, whose
ten monkeypatching tests move in the same commit. State the open-findings count, 25
after this round, and the operator-questions count, 2.
