STEP F283 R4 — R-1020's LAST REPAIR: no module under apps/cli/ calls the exiting resolver

GOAL
Book round 3's PASS, correct the call-site count on the record and register R-1021, then
move EVERY remaining call of `packages.orchestration.data_paths.resolve_job_id` under
`apps/cli/` onto `apps/cli/job_id_arg.py`, one module per commit, under a guard that reads
import BINDINGS rather than one spelling.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THIS ROUND YOU WRITE THE CODE. Rounds 1 to 3 applied reviewer-authored diffs. This round
the reviewer authors only the three RECORD payloads below; every change under `apps/` and
`tests/` is yours, written to the SPEC in each commit. The reviewer reads your committed
diff and re-runs your gates before any verdict.

WHY THE COUNT CHANGED
Round 3's guard `TestTheExitingResolverIsStillReachable` counts calls whose callee is the
bare NAME `resolve_job_id`. `apps/cli/commands/decision.py` also binds it as `_rji`,
inside `_cmd_decision_resolve`, and calls it three times. Measured at `3b4acafd` with an
alias-aware reading, twenty call sites remain, in these modules:
  patch.py 7 · decision.py 4 · change.py 3 · teacher_cmd.py 2 · contract_cmd.py 1 ·
  job_context_cmd.py 1 · job_stop_cmd.py 1 · project.py 1
`packages/orchestration/decision_inbox.py` also calls it; it is under `packages/`, not a
CLI refusal, and is NOT in scope.

THE ONE RULE FOR EVERY MIGRATED SITE
  job_id = resolve_job_id_or_fail(<the raw id>, json_output=<flag>)
where <flag> is the handler's own `json_output` when the handler has that parameter, and
the literal `False` when it does not. With `False` the stderr bytes are identical to the
exiting helper's, so a command that declares no `supports_json` changes nothing an
operator sees. Import `resolve_job_id_or_fail` from `apps.cli.job_id_arg` at MODULE level
and delete each `resolve_job_id` / `_rji` import the migration leaves unused. Do not touch
`packages/` at all: `resolve_job_id` and `_exit_ambiguous` stay exactly as they are.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r4-payloads/`  READ-ONLY. The reviewer's originals; the transport proof
      compares against them. Never write here.
  `.remedy-wt/f283-r4-scratch/`   YOURS for logs, exit-code captures and scripts. The
      reviewer's own scripts already there (`sites.py`, `lookup_sites.py`, `measure.py`)
      are READ-ONLY to you. Both directories are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `$?` or `${...}` outside a `bash -c`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `python3 - <<'PY'` scripts (or
a file under your scratch directory) for counting, hashing and copying (`shutil.copyfile`).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f283-machine-contracts-part-two`, and `git log --oneline -1` must read
   `3b4acafd`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f283-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all three under `.remedy-wt/f283-r4-payloads/`, printed by the reviewer's
`measure.py` (lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 6332 | 557699ac708f25bb2fe507dc5da067f7e01a781ea4c40ca54a6a1d2034f1dfa6 |
| plan.md | 47 | 2283 | 3e2aaf77adceed0c2cd21f6d3d88749dfee7d1496f50d5295799c6716a6f798f |
| slips.md | 2 | 995 | b28250b9e47ca33d58029055c9be43305165e8f84e90a8448c372423363a3bc6 |

`ledger.md` is an APPEND beginning with the single newline that separates records: the
round 3 `Gate:` entry and the `- R-1021 — ` registration. `slips.md` is an APPEND of two
lines with no leading newline. `plan.md` is a REWRITE. Never retype or edit a payload.

BUNDLE — commits C1 to C9, in this order.

C1 — copy this block and the three payloads
  `.agent/authored/f283-r4-block.md` := this block; `.agent/authored/f283-r4-<name>` for
  each payload, keeping its file name. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R4 C1: copy round 4 block and payloads into .agent/authored/`

C2 — book round 3's PASS, correct the count, register R-1021
  `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md ·
  `.agent/prose_slips.md` += slips.md
  Subject: `F283 R4 C2: book round 3's PASS and register R-1021`

C3 — the layer, `job stop`, and a guard that reads bindings
  SPEC, `apps/cli/job_id_arg.py`:
  - Add `refuse_ambiguous_job_id(raw: str, matches: list[str], *, json_output: bool)
    -> NoReturn`, holding the body of the current `except JobIdAmbiguous` branch
    unchanged — same message, `exit_code=2`, `matches=` the sorted full ids. That branch
    now calls it. Update the module docstring only where it describes this.
  SPEC, `apps/cli/commands/job_stop_cmd.py`, the `if _load_job(job_id) is None:` block:
  - Replace the `try: resolve_job_id(...) except SystemExit` construction with
    `lookup_job_id`: on `JobIdAmbiguous` call `refuse_ambiguous_job_id(job_id,
    exc.matches, json_output=json_output)`; on any other `JobIdError` call
    `fail("job_not_found", f"No job matches {job_id!r}. Try: remedy job list.",
    json_output=json_output, exit_code=EXIT_UNKNOWN_JOB, job_id=job_id)`.
    The text branch keeps its bytes and exit 3 (`tests/cli/test_job_stop.py` asserts
    both); the JSON branch becomes the envelope with `job_id` kept and stderr empty.
  SPEC, `tests/cli/test_job_refusal_envelope.py`:
  - A module-level `_exiting_resolver_calls(source: str) -> int` that collects every
    name bound by `from packages.orchestration.data_paths import resolve_job_id` or
    `... import resolve_job_id as <alias>` ANYWHERE in the tree (module or function
    level), and counts `ast.Call` nodes whose callee is one of those names or is an
    attribute `<anything>.resolve_job_id`.
  - `TestTheExitingResolverIsStillReachable` compares a per-file dict built with it
    against a module constant `_EXITING_RESOLVER_REMAINING`, which at C3 reads
    {"change.py": 3, "contract_cmd.py": 1, "decision.py": 4, "job_context_cmd.py": 1,
     "patch.py": 7, "project.py": 1, "teacher_cmd.py": 2}
    and must EQUAL the measured dict. `apps/cli/job_id_arg.py` never appears in it.
  - A non-vacuity test: `_exiting_resolver_calls` returns 1 for a source string that
    binds the resolver `as _x` inside a function and calls `_x("a")`, and 1 for one
    that calls `data_paths.resolve_job_id("a")`.
  - The ambiguous branch's first tests. Fixture: `monkeypatch.setenv("REMEDY_DATA_DIR",
    str(tmp_path))` and two `jobs/<id>/job.json` files for
    `aaaa1111-0000-0000-0000-000000000001` and `...0002` (the shape
    `tests/test_data_paths.py` already builds). (i) `resolve_job_id_or_fail("aaaa1111",
    json_output=True)` exits 2, stderr empty, envelope `error` `ambiguous_job_id`,
    `ok` false, `schema_version` 1, `matches` equal to both ids sorted. (ii) With
    `json_output=False` it exits 2 with empty stdout and stderr EQUAL to what
    `packages.orchestration.data_paths.resolve_job_id("aaaa1111")` writes to stderr,
    captured in the same test — the identity proof, computed, not typed.
  - `tests/cli/test_job_stop.py::test_an_unknown_job_exits_3_in_json_mode_too`
    additionally asserts stderr is empty and `schema_version` is 1.
  Subject: `F283 R4 C3: the ambiguous refusal gets a name, job stop answers in the envelope`

C4 — `apps/cli/commands/patch.py`, all seven sites; delete `"patch.py"` from
  `_EXITING_RESOLVER_REMAINING` in the same commit.
  Subject: `F283 R4 C4: patch resolves a job id through the envelope`

C5 — `apps/cli/commands/change.py`, all three sites; delete `"change.py"` from the
  constant. `tests/cli/test_change_proof_cli.py` patches
  `apps.cli.commands.change.resolve_job_id` with `side_effect=lambda raw: raw` at every
  one of its uses: move each to `apps.cli.commands.change.resolve_job_id_or_fail` with
  `side_effect=lambda raw, **_: raw`, and change nothing else in that file.
  Subject: `F283 R4 C5: change resolves a job id through the envelope`

C6 — `apps/cli/commands/decision.py`, all four sites; delete `"decision.py"` from the
  constant.
  SPEC: `_load_job_events(job_id_str: str, *, json_output: bool = False)`; its
  `JobNotFoundError` branch becomes `fail("job_not_found", str(exc),
  json_output=json_output)` (same text bytes); `_cmd_decision_list` and
  `_cmd_decision_show` pass their own `json_output` to it and `_cmd_decision_explain`
  passes nothing. The three `_rji` sites in `_cmd_decision_resolve` use `False`, because
  `decision.resolve` declares no `supports_json`.
  Subject: `F283 R4 C6: decision resolves a job id through the envelope`

C7 — the tail: `teacher_cmd.py` 2, `contract_cmd.py` 1, `job_context_cmd.py` 1,
  `project.py` 1. The constant becomes `{}` and the test asserts the measured dict is
  EMPTY. In `teacher_cmd.py` the module docstring's exit-code bullet that begins
  `* 1 or 2 — raised by ``resolve_job_id`` itself:` names
  ``apps.cli.job_id_arg.resolve_job_id_or_fail`` instead and adds that under `--json`
  the refusal is the envelope; nothing else in that docstring changes. In
  `tests/cli/test_job_context_cmd.py`, `TestJobContextRefusesInTheCallersShape._run`
  patches `data_paths.resolve_job_id`; point that patch at the name the handler now
  calls, keep the comment above it true, and change nothing else in that file.
  In `apps/cli/commands/job.py`, `_digest_section`'s docstring says `job show` resolves
  the job with `resolve_job_id`, which round 3 made false: name
  `resolve_job_id_or_fail` there. Nothing else in `job.py` changes.
  Subject: `F283 R4 C7: the last four modules resolve a job id through the envelope`

C8 — THE ENVELOPE, PROVED THROUGH THE REAL PARSER
  SPEC, a new class in `tests/cli/test_job_refusal_envelope.py`, one parametrized case
  per catalog command id among: `change.list`, `change.show`, `change.proof`,
  `decision.list`, `decision.show`, `job.contract`, `job.context`, `job.stop`,
  `patch.list`, `patch.apply`, `patch.revert`, `patch.approve-hunks`,
  `teacher.narrate`, `teacher.ask`. Each runs `apps.cli.grouped.main(argv)` in-process
  with the job id `zzzznotajob`, placeholders for any other required positional you
  read off the catalog entry, and `--json`, under a `REMEDY_DATA_DIR` set to
  `tmp_path`. It asserts: stderr empty; stdout is ONE JSON object with `ok` false and
  `schema_version` 1; `error` is `invalid_job_id` at exit 1 — except `job.stop`, which
  is `job_not_found` at exit 3.
  A command whose refusal fires BEFORE its id reaches the resolver is NOT forced: leave
  it out of the list, never mark it xfail or skip, and name it in the handback with the
  refusal you measured — that is evidence for a later round, not a defect of this one.
  Subject: `F283 R4 C8: every migrated JSON command answers a bad id in the envelope`

C9 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`.
  Subject: `F283 R4 C9: rewrite handoff for round 4`
  Then `git push origin feature/f283-machine-contracts-part-two`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is: the four `.agent/authored/f283-r4-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
   `.agent/handoff.md`, `apps/cli/job_id_arg.py`, and under `apps/cli/commands/`
   `job_stop_cmd.py`, `patch.py`, `change.py`, `decision.py`, `teacher_cmd.py`,
   `contract_cmd.py`, `job_context_cmd.py`, `project.py`, `job.py`, and
   `tests/cli/test_job_refusal_envelope.py`, `tests/cli/test_job_stop.py`,
   `tests/cli/test_change_proof_cli.py`, `tests/cli/test_job_context_cmd.py`. Report the
   set you measure. Nothing under `packages/`, `docs/`, `README.md`, and none of
   `.agent/candidates.md`, `.agent/context.md`, `.agent/decisions.md`,
   `.agent/operator_questions.md`, `apps/cli/json_envelope.py`.
4. MIGRATE ONLY THE TWENTY. The nineteen `lookup_job_id` sites of R-1021 (`brain`,
   `snapshot_cmds`, `test_cmds`, `event`, `file`, `memory`, `project.py`'s line near
   157) are the NEXT round. Refusal pairs other than the ones the SPEC names stay.
5. Every commit leaves the targeted selection of G4 green; a test a migration breaks is
   repaired in that SAME commit, inside constraint 3's paths, or you STOP.
6. If a gate goes red and the fix is outside constraint 3, STOP: commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
7. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`.
8. Leave the three `remedy/job-*` worktrees alone. A worktree you add for G5 goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is
   reported afterwards (finding R-0940).

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). Gates G1 to G5 run BEFORE C9 and the
handback quotes them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then
 each committed `.agent/authored/f283-r4-*` blob, read with `git show <C1>:<path>`,
 compared byte-for-byte with its source (the block copy against
 `.remedy-wt/f283-r4-block.md`). One reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION: `.agent/live_review.md` at `3b4acafd` (453413 bytes)
     plus ledger.md equals the committed file; the reviewer composed 459745.
     `.agent/prose_slips.md` (359949) plus slips.md; the reviewer composed 360944.
 (b) Line-anchored on the committed ledger: `^- R-1020 — ` 1, `^Done: R-1020 — ` 0,
     `^- R-1021 — ` 1. Open set by distinct id via `open_finding_ids` from
     `scripts/rotate_live_review.py` at `3b4acafd` and at C2: the reviewer measured 24
     and 25, ADDED exactly `R-1021`, REMOVED empty. Report both sets' differences.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE MIGRATION, COUNTED FROM THE TREE — for every commit C3 to C8 report
 `git diff --name-only <parent> <commit>` and `git show --numstat` insertions (commits
 before C9 only). Then at C8 report, from the reviewer's
 `python3 .remedy-wt/f283-r4-scratch/sites.py`: `TOTAL 0`. And report
 `git diff --name-only 3b4acafd <C8> -- packages/` — it must print nothing.

G4 THE TARGETED SELECTION, in the primary checkout at C8:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -n auto tests/cli/test_job_refusal_envelope.py tests/cli/test_job_stop.py tests/cli/test_patch_cmd.py tests/cli/test_change_proof_cli.py tests/cli/test_decision_answers.py tests/cli/test_decision_cmd.py tests/cli/test_do_sequence_cli.py tests/cli/test_job_context_cmd.py tests/cli/test_plan_approval.py tests/cli/test_project_current.py tests/cli/test_scoped_listings.py tests/cli/test_study_teacher_e2e.py tests/cli/test_teacher_cmd.py tests/orchestration/test_import_reachability.py tests/orchestration/test_escalation.py tests/orchestration/test_project_resolution.py tests/orchestration/test_proposal_decision.py tests/test_cli_main.py tests/test_data_paths.py tests/test_grouped_cli.py tests/test_patch_intent_approval.py tests/test_project_context_coverage.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/orchestration/test_job_stop_integration.py; echo "REAL_EXIT=$?"'
```
 The reviewer read `1084 passed` at `3b4acafd`. Report your summary
 line and exit code; zero failed, zero xfailed, and the passed count may only rise. Then
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/; echo "REAL_EXIT=$?"'`,
 `python3 -m ruff check` over every `.py` path in constraint 3, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass`. DO NOT run
 the full suite.

G5 RED-PROOFS — in ONE disposable worktree under `.remedy-wt/` at C8, never committed.
 Run `tests/cli/test_job_refusal_envelope.py` UNMUTATED first and report it (exit 0).
 Then each mutation alone, reverted before the next, reporting the summary line, the
 exit code and the names of the failing tests:
 (a) `refuse_ambiguous_job_id`'s `exit_code=2` becomes `exit_code=1` — the JSON
     ambiguous test must fail.
 (b) its message loses the indented match lines (the `\n{listed}` part) — the text
     identity test must fail.
 (c) `_cmd_decision_list` passes `json_output=False` to `_load_job_events` — the
     `decision.list` case of C8 must fail.
 (d) in `patch.py`, one migrated site becomes `_r(job_id_str)` with
     `from packages.orchestration.data_paths import resolve_job_id as _r` inside that
     function — the binding guard must fail. This is the alias round 3's guard missed.
 Then remove the worktree and report `git worktree list`.

G6 TREE AND PUSH — after C9: `git status --porcelain` empty; `git log --oneline -n 10`;
 `git worktree list` (primary plus the three `remedy/job-*`); the push's real outcome;
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.
 These go in your final reply, not the handback — the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit
changed-files table with the insertions git MEASURED (no expected figure is given for
code commits on purpose), every gate's real output and exit code, the item-status table,
the deviations, any C8 command left out and why, and the next action. Your Session
section reads SESSION 2 of feature F283, round 4, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the
review of round 4, then round 5 — R-1020's `Done:` booked in its first commit, and
R-1021's nineteen `lookup_job_id` sites moved onto `resolve_job_id_or_fail`. State the
open-findings count, 25 after this round, and the operator-questions count, 2.
