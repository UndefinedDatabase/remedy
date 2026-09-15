── STEP T002/5 — F261 — ROUND 9 ──
Goal: Book round 8's PASS and the resolutions of R-0896 and R-0806, record DECISION F261 D8, and
fold `job assumptions`, `job fences` and `job dod` into `job show --full` in three commits by
applying three tables; run the suite once.

Base commit: `aff2b676`, on `feature/f261-cli-vocabulary-v2`. SESSION 2 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D7 and D8 once C1 has landed D8.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r9w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.commands.job` loaded from inside it. Never call `run_job` or a runner yourself:
a job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r9.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN9; slice RECORD9 is appended to
    `.agent/live_review.md` and slice DEC8 to `.agent/decisions.md`
C2  THE ASSUMPTIONS FOLD: copy `.remedy-wt/f261-block/f261-r9-fold-1.jsonl` to
    `.agent/authored/f261-r9-fold-1.jsonl` and apply it per THE TABLES, in one commit
C3  THE FENCES FOLD: the same with `f261-r9-fold-2.jsonl`, in one commit
C4  THE DOD FOLD: the same with `f261-r9-fold-3.jsonl`, in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r9.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/decisions.md`. C2 to C4: each table's own carrier and the
paths G3 names. C5: `.agent/handoff.md`.

## The appends

RECORD9 and DEC8 each begin with an empty line, and both targets end in a newline at `aff2b676`:
an append is the file's bytes followed by the slice's bytes, and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r9-fold-1.jsonl` `a1a7ae9b68ba24d067b58ca05998e396571be911cec0592f86256d131a0f9fa1`,
`f261-r9-fold-2.jsonl` `b5dbef9a488431e85ef88dcd3ff95087ca8feb66ee57925041332cd24028fc03`,
`f261-r9-fold-3.jsonl` `683e6c0595e342975b74272131c7892ee12be9c8ca72dae88a8e04e607165491`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D8: fold-1 its CHOSEN SECOND, fold-2 its CHOSEN
FIRST and THIRD, and fold-3 its CHOSEN FOURTH.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r9w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r9w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph beyond the two RECORD9 carries.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 286 lines TOTAL and 220 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r9.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN9, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `aff2b676` blob
followed by RECORD9, and `.agent/decisions.md` its `aff2b676` blob followed by DEC8. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 117 at `aff2b676` and 118 at C1, with
`Gate: F261 R8 — ` once at C1; distinct `^- R-\d+ — ` ids 103 and 103; distinct
`^Done: R-\d+ — ` ids 4 and 6, C1 minus base exactly `R-0806` and `R-0896`; the open set by
distinct id 99 and 97.

G3 THE FOLDS, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`,
`apps/cli/commands/job.py`, `tests/cli/test_decision_answers.py`, `tests/cli/test_job_show.py` and
`tests/test_command_catalog.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
`apps/cli/commands/job_context_cmd.py`, `docs/guides/job-context-view-user-guide-v0.md`,
`tests/cli/test_job_show.py`, `tests/orchestration/test_fence_e2e.py`,
`tests/orchestration/test_fence_production_e2e.py` and `tests/test_command_catalog.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/job.py`, `tests/cli/test_job_show.py`,
`tests/orchestration/test_dod_gate.py` and `tests/test_command_catalog.py`. `git rev-parse
<commit>:<dir>` equals the dry run: C2 `apps` `fd8eab43e8389f8b8ee15c1cbe2514b71815a787`, `tests`
`2b5ab527538225353c7ece866f80bd41309c653b`; C3 `apps` `d14bb7f2a5433e2e9e228ddcc090d5143e5c19bc`, `tests`
`fdbb77e587d38bcd66874fc2d7a2d8910414fa68`, `docs` `d74ed73f2a078c66e6c60f11370bfb581892e704`; C4 `apps`
`d8be0bc2889f21334572707612fb0ff623e4c1ac`, `tests` `7979b693ff9c8c975ec10b733fedc3bbf3023e01`, `docs` the same as C3. At
each of those commits `packages`, `scripts` and `README.md` equal their objects at `aff2b676`,
and at C2 `docs` does too. Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -F -e '"job.assumptions"' -e '"job.fences"' -e '"job.dod"'
-e _cmd_job_assumptions -e _cmd_job_fences -e _cmd_job_dod <C4> -- apps packages scripts tests
docs README.md ':!docs/roadmap'` prints exactly three lines, the `DELETED` entries of those three
ids in `tests/test_command_catalog.py`. `git grep -n -I -E 'remedy job (assumptions|fences|dod)\b'
<C4> -- apps packages scripts tests docs README.md ':!docs/roadmap'` exits 1 and prints nothing.
`python3 -m ruff check` over every `.py` path of C2, C3 and C4 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r9w/wt <C4's sha>`, each run
through the runner over `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`,
`tests/cli/test_decision_answers.py`, `tests/orchestration/test_fence_e2e.py`,
`tests/orchestration/test_fence_production_e2e.py` and `tests/orchestration/test_dod_gate.py`
with `-rf --tb=no`. Every mutation is in `apps/cli/commands/job.py`, replaces the bytes of slice
MUT-<n>-FROM, whose count there must read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r9w/wt checkout -- apps/cli/commands/job.py`. (a) CONTROL: must exit 0.
Each of (1) to (5) must exit 1 with the named node among the failed nodes:
(1) a `job.fences` handler row: `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`;
(2) a plain `RuntimeError` for a missing target repo:
`TestCLIJobFences::test_missing_target_repo_is_a_no_target_repo_error`;
(3) two registry entries swapped: `TestSections::test_full_prints_the_registered_sections_in_the_d4_order`;
(4) the dod `check_count` key dropped: `TestJobDodCommand::test_json_output_carries_the_gate_record`;
(5) empty assumptions markdown: `TestAssumptionsCommand::test_the_section_holds_the_log`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r9w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `aff2b676`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 2 of feature F261 · round 9 · rounds so far 9`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 97 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 9; the folds of
`job summary`, `job digest`, `job status` and `job report`.

── SLICE PLAN9 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN9 sha256=f0f9b6c004095f37bf13cee577e1918cb738d5b47042e5ce58e947a9608aae2a
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 9 continues T002. It books round 8's PASS and the resolutions of R-0896 and R-0806,
records DECISION F261 D8, then folds `job assumptions`, `job fences` and `job dod` into
sections of `job show --full`, one command per commit, each applying a table the round saves
under `.agent/authored/` and adding the command's id to the deleted-command guard.

## Next Steps

1. The folds of `job summary`, `job digest`, `job status` and `job report`, one per commit.
2. The fold of `do job-report`, with its hints and `related=` tuples.
3. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
4. T003, the prune to D4, with R-0900; then T004.

## Risks

- 99 findings are open by distinct id before this round's record and 97 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job status` and `job report` carry most of the read tests and printed hints left to fold.
END PLAN9

── SLICE RECORD9 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD9 sha256=8d867688ff198f78b7277b319f7e95233ae22c55015b9870da5cbd0c4143caf6

Gate: F261 R8 — the F261 round 8 entry. VERDICT PASS. Written by the planner and reviewer of session 37 after reading the committed range `22173331`..`aff2b676` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 9 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r8.md` at `505deb15` and `.agent/last_block.md` at `83dff65a` are byte-identical to the reviewer's scratch original, sha256 `2da5521352b55cac563eadaa828144af0435198ab6609057f822824147439e7a`, and the three tables committed at `9d8d57f6`, `068ee126` and `720874b8` are byte-identical to the reviewer's. THE STATE: at `1c3bf3e3` and again at `720874b8`, `.agent/plan.md` equals PLAN8, `.agent/live_review.md` and `.agent/decisions.md` equal their `22173331` blobs followed by RECORD8 and DEC7, and `docs/roadmap/features/T2_F273.md` equals its `22173331` blob with pair P273 applied; at `178ae847` and again at `aff2b676` the record is that blob followed by RECORD8 and LANDED8. THE SHOW COMMITS: at `9d8d57f6`, `068ee126` and `720874b8` the `apps`, `packages`, `tests`, `scripts`, `README.md` and `docs/system` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly, and `docs/roadmap` equals its object at `1c3bf3e3`; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 199, 308 and 177 insertions. At `720874b8` the fixed-string grep of `job.permissions` and `_cmd_show_permissions` prints only the `DELETED` entry of `tests/test_command_catalog.py`, and ruff over the round's touched `.py` files exits 0. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17681 passed, `tests/ui_server/test_dashboard_contract.py` read 73 passed, and the record slices applied on top of the dry run passed `tests/docs/` and every test file that reads the edited state files, apart from `tests/ui_server` and `test_vitest_passes` failing for the worktree's missing UI build. Over `tests/cli/test_job_show.py`, `tests/cli/test_advertised_commands.py` and `tests/test_command_catalog.py`, which passed 52 unmutated, removing `--json` from `job show` failed 5 tests, raising the findings cap to eleven failed 1, reading the first round instead of the last failed 3, narrowing the section guard to `KeyError` failed 1, restoring a `job.permissions` handler row failed 1, and replacing the findings with an empty list failed 6, the fake-provider acceptance test among them. THE REVIEWER'S RUN in the primary checkout at `aff2b676` of `tests/cli/test_job_show.py`, `tests/cli/test_advertised_commands.py`, `tests/test_command_catalog.py`, `tests/test_cli_main.py`, `tests/test_brain_detail.py`, `tests/cli/test_plan_approval.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 603 passed, and `git branch --list 'remedy/job-*'` read 16 lines before and after the round. The open set reads 99 by distinct id at `aff2b676`.

Done: R-0896 — RESOLVED by F261 round 8. `9d8d57f6` declares `--json` on `job show`, whose output is the same with or without it, drops `--json` from the three `patch approve` hints that never had it, and adds `test_every_advertised_flag_is_declared_by_its_command` and `test_every_operator_facing_advertised_flag_is_declared_by_its_command` to `tests/cli/test_advertised_commands.py`, which hold every `--flag` after a `remedy <group> <sub>` hint against the arguments that command declares. Verified by the reviewer of session 37: the objects of `9d8d57f6` equal the reviewer's dry run, in which removing `--json` from `job show` failed both new tests among 5; `git grep -n "job show .*--json"` over `apps`, `packages`, `scripts`, `docs/system` and `docs/guides` printed 19 lines at `22173331`, and the flag tests pass over all of them in the reviewer's run at `aff2b676`. A hint that names only a group is not flag-checked; that form is R-0900.

Done: R-0806 — RESOLVED by F261 round 8. `068ee126` makes `job show` print `blocked_task_findings`: for every blocked task, the reviewer findings of its run's last round with `id`, `severity`, `file` and `summary`, where `summary` is the title, ten by default and every one with `--full`, and the same findings on stderr. The acceptance test is `tests/cli/test_job_show.py::TestABlockedFakeRunShowsItsFindingText::test_the_persisted_finding_summary_appears_in_job_show`, which blocks a job through the fake provider in a temporary git repository and finds the persisted finding summaries in the command's JSON and stderr; it was added at `068ee126` and passes in the reviewer's run at `aff2b676`. Verified by the reviewer of session 37: the objects of `068ee126` equal the reviewer's dry run, in which replacing the findings with an empty list failed that test, raising the cap to eleven failed the ten-finding test, and reading the first round instead of the last failed three tests.
END RECORD9

── SLICE DEC8 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC8 sha256=7b3c0f88db4699850d6213ad7bbd07f9d39ec66a128b53e89b5d649cc3a4f157

## DECISION F261 D8 (2026-09-15, F261 round 9) — the deletion paragraph of `job assumptions`, `job fences` and `job dod`, and the error a section names

CONTEXT. DECISION F261 D7 made the read views of a job sections of `job show --full` and folded `job permissions` first. This round folds three more, one per commit. Measured at `aff2b676` by the reviewer's research helper and re-read by the reviewer on the dry-run trees.

CHOSEN, FIRST: A SECTION MAY NAME ITS OWN ERROR. A builder that cannot describe its job raises `ShowSectionError(code, message)`, defined in `apps/cli/commands/job.py`; `_build_show_sections` turns it into `{"ok": false, "error": {"code": code, "message": message}}` and the stderr line `Error: <code>: <message>`. Any other exception stays `section_failed`, and `job show --full` still exits 0.

CHOSEN, SECOND: `job assumptions`. Deleted: the catalog entry `job.assumptions`, its handler-table row and `_cmd_job_assumptions`. THE HEIR is the `assumptions` section: `markdown` holds the assumption log `render_assumptions_md` renders from the job's flight plan, and `evidence_copy` the path of an existing `assumptions.md` evidence copy or null; its text is the former output. Like the command, the view only checks whether that file exists and writes nothing.

CHOSEN, THIRD: `job fences`. Deleted: the catalog entry `job.fences`, its handler-table row and `_cmd_job_fences`. `job context` now relates to `job show` alone, and the docstring of `apps/cli/commands/job_context_cmd.py` and `docs/guides/job-context-view-user-guide-v0.md` name the `fences` section instead. THE HEIR is the `fences` section. Its data is the former `--json` payload, with `job_id` the full job id where the command echoed the id as typed. The command's non-zero exits become error envelopes: `no_target_repo` for a job without `target_repo` in its metadata and `target_repo_missing` for a missing directory (each exit 2), `fence_config_error` (exit 3), and `builtin_resolution_failed` when the builtin denies cannot be resolved (exit 4).

CHOSEN, FOURTH: `job dod`. Deleted: the catalog entry `job.dod`, its handler-table row and `_cmd_job_dod`. THE HEIR is the `dod` section: its data holds the five keys of the former `--json` payload, `job_id`, `compiled`, `origin`, `check_count` and `gate`, in that order rather than sorted; its text is the former matrix, under the heading `--- Dod ---`.

CONSEQUENCE. `remedy job assumptions`, `remedy job fences` and `remedy job dod` exit with an argument error, and their ids join `TestDeletedCommands`. The registry holds `permissions`, `fences`, `assumptions` and `dod`, in D4's order. For a job whose fences cannot be resolved, `job show --full` exits 0 and says why inside the section. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC8

── SLICE MUT-1-FROM ── G5 (1) only, never a file ──
BEGIN MUT-1-FROM sha256=22233892605d17303cd9a816b9b5c2bdf5437a8af11309548ed1fe992b6e55cf
    "job.digest": lambda args: _cmd_job_digest(args.job_id,
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only, never a file ──
BEGIN MUT-1-TO sha256=aca2ba87b604e2d44c85100c89e431d936dccb8bee6e723ad245e1f2ed88a89d
    "job.fences": lambda args: None,
    "job.digest": lambda args: _cmd_job_digest(args.job_id,
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only, never a file ──
BEGIN MUT-2-FROM sha256=db637940426523d45e725a7d6dc2a4e94c79a4d0d27fd1cae9e63590bab80d6f
        raise ShowSectionError("no_target_repo", f"Job {short_id} has no target_repo attached")
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only, never a file ──
BEGIN MUT-2-TO sha256=6f48df5de2f51b3e6a8b0c5a1bd9f107357053093a6e9fb2f9236013f1b56dab
        raise RuntimeError("no_target_repo", f"Job {short_id} has no target_repo attached")
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only, never a file ──
BEGIN MUT-3-FROM sha256=14bb0ed20c5461f62ffb93cde6a3cfb969c694af086c55706b42865eaff7df07
    ("fences", _fences_section),
    ("assumptions", _assumptions_section),
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only, never a file ──
BEGIN MUT-3-TO sha256=e5507fb0a91c31d7c06c432474797a20cf1681474da514be637cbd003534aaa3
    ("assumptions", _assumptions_section),
    ("fences", _fences_section),
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only, never a file ──
BEGIN MUT-4-FROM sha256=aa1c0178fbb3fd6414db1e345fbd74b1908f539297138f8784015fee19031203
        "check_count": 0 if dod is None else len(dod.checks),
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only, never a file ──
BEGIN MUT-4-TO sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only, never a file ──
BEGIN MUT-5-FROM sha256=9c1a75f5f1f3c999eaced49e5cede7480b085b64c52cce345d63894e7b64b4ef
    return {"markdown": markdown, "evidence_copy": evidence_copy}, lines
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only, never a file ──
BEGIN MUT-5-TO sha256=97da22c2b58c73510e70f4162951ae20a640bc8dcdea4e6c0d6b58caec2bc056
    return {"markdown": "", "evidence_copy": evidence_copy}, lines
END MUT-5-TO
