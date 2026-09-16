── STEP T001/6 — F280 — ROUND 6 ──
Goal: Book rounds 4 and 5's combined PASS and register R-0937, then delete `job create`: its
catalog entry, its dispatch row, the two dangling `related=` references, its own tests, its four
production hint strings, and its docs advertisements; run the suite once.

Base commit: `e81c8e94d0cefeb5264c3fb44047556a26a4a05a`, on
`feature/f280-cli-vocabulary-v2-part-two`. SESSION 2 of F280. Read AGENTS.md and
docs/agents/self_drive_protocol.md before C0a.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two
or more characters long is a run of a single repeated character, and every box-drawing rule inside
the STEP header line is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)`, `$?` and `$VAR` expansions in a command are refused by form, so write such
checks as Python scripts under `.remedy-wt/f280r6w/`, never named after a standard-library module,
and use absolute paths rather than `cd x && ...`; a pipe into `tail` hides pytest's exit code. Never
call `run_job`, `run_job_fulfill` or any runner yourself; `git branch --list 'remedy/job-*'` reads
17 lines now, keep it so. `python3 -m ruff check` NEVER names a `.sh` path — an explicit path
bypasses its file-type discovery and parses the shell script as Python (finding R-0819's class);
check `scripts/remedy_smoke.sh` only with `bash -n`, and this round does not edit it anyway.

WHY A PATCH, NOT A TABLE, THIS ROUND: the change touches twelve files, several with multi-line
prose edits, so the carrier is a unified diff, `git apply --check` then `git apply`, in the manner
DECISION F272 D15 already established for an overlay carrier, rather than a JSONL edit table.

WHY NO RED-PROOF THIS ROUND: the deleted code (the catalog entry and the dispatch row) has no
test that exercises it directly any more once `TestDeletedCommands` and `TestRequiredCommands` are
updated — that update IS the proof, and `tests/cli/test_advertised_commands.py`'s own sweep is the
proof that nothing still advertises the deleted word. `_cmd_create_job` itself is UNEDITED by this
round, so there is no production behaviour left to mutate.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f280-r6.md`, the block file the delegating message names, by
    `shutil.copyfile`, in its OWN commit
C0b `.agent/last_block.md`, the same bytes, in its OWN commit — do not combine C0a and C0b into one
    commit, as round 4's worker mistakenly did
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN6; slice RECORD6 is appended to
    `.agent/live_review.md`
C2  THE PATCH: copy `.remedy-wt/f280-block/f280-r6-deletejobcreate.patch` to
    `.agent/authored/f280-r6-deletejobcreate.patch`, `git apply --check` it against the tree at
    C1, then `git apply` it, then `git add -A` and commit, in one commit
C3  `.agent/handoff.md`, the handback; then `git push origin feature/f280-cli-vocabulary-v2-part-two`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f280-r6.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`. C2: `.agent/authored/f280-r6-deletejobcreate.patch` and the twelve paths
G3 names. C3: `.agent/handoff.md`.

## The append

RECORD6 begins with an empty line, and the target ends in a newline at the base: an append is the
file's bytes followed by the slice's bytes, and nothing else.

## THE PATCH

Its sha256, to verify before copying: `f280-r6-deletejobcreate.patch`
`063e220ea405d9a5fa79a459fcd4c8aad696af91c32aa656497281f4533dbef3`. From the repository root, at
the C1 tree: `git apply --check .agent/authored/f280-r6-deletejobcreate.patch` must exit 0 before
`git apply` runs it for real; either exiting non-zero is a STOP — touch nothing further, commit
nothing of the patch, and hand back with the raw output. The patch is the reviewer's own diff,
built and dry-run applied and tested by the reviewer, twice independently, on its own trees before
delegation, whose objects the worker's own apply must equal.

## SPEC S — the suite, once, after C2 and before C3

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f280r6w/`. Report pytest's return code, the run's last output line, and every distinct
bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `. Re-run each bad
node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C3, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f280r6w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f280-block/` and your own
   directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Gate:`, `Done:` or finding paragraph of your own beyond RECORD6, which is the
   reviewer's, already written.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 222 lines TOTAL and 176 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice
   CONTENT — the `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3 and G4 after C2; then SPEC S, whose result is G5; G6 after
   C3 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and no
   subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f280-r6.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; the committed patch's sha256 equals
`063e220ea405d9a5fa79a459fcd4c8aad696af91c32aa656497281f4533dbef3`.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN6, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its base blob followed
by RECORD6. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 31 at the base and 32 at C1,
with `Gate: F280 R4 — ` 0 times at the base and once at C1; distinct `^- R-\d+ — ` ids 132 at the
base and 133 at C1, the delta exactly `R-0937`; distinct `^Done: R-\d+ — ` ids 6 at both; the open
set by distinct id 126 at the base and 127 at C1.

G3 THE PATCH. `git diff --no-renames --name-only` from C2's parent prints exactly the patch file
and: `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
`docs/guides/simple-operator-quickstart-v0.md`, `docs/system/architecture.md`,
`docs/system/first-fulfilled-job-demo-v0.md`, `docs/system/project-scoping-v0.md`,
`packages/orchestration/autonomy_readiness.py`, `packages/orchestration/cockpit.py`,
`packages/orchestration/timeline.py`, `packages/orchestration/trust_report.py`,
`tests/test_command_catalog.py`, `tests/test_grouped_cli.py` — twelve paths. `git rev-parse
<commit>:<object>` for `apps`, `packages`, `scripts`, `tests`, `docs/guides`, `docs/system`,
`docs/README.md`, `README.md` and `.claude`, in that order, equals the reviewer's own two
independent dry-run applications, which agreed with each other: `e236db2d080e1307f936446a2d1f24e8e0f5b8a8`,
`905f8acfa8e41b944133a841aa0c451620618c5b`, `bde7eae195226e4567a0cdde74c54e51e735b137`,
`f7d5bf6dbe99b6c85c1bb670826d12192b16cc8f`, `9c86d25d406764a55bdaf4cee06f01ee14e2b5ab`,
`4e35fafb4567ba17c51f1961deaec6607c709922`, `0f1933b93649df9471145f57c5fbe9302f6a0d97`,
`3c6b8d40ec4f4d76e05dc352a4b0ce8ef8970be5`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0` — `scripts`,
`docs/README.md`, `README.md` and `.claude` are untouched, unchanged from round 5's own base.
Report the insertions and deletions of C2 per constraint 5; the reviewer's own dry-run commit reads
35 insertions against 66 deletions over the twelve paths. `python3 -m ruff check` over the eight
edited `.py` paths exits 0.

G4 THE SWEEP, at C2. Two readings. First, `git grep -n -I -E '"-m", "apps\.cli\.main", "job",
"create"' <rev> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'
':!docs/archive'` (the CLI-dispatch pattern round 4 already swept): 0 lines at the base and at C2,
unchanged, since this round touches no dispatch call site. Second, over the WORKING TREE (not a
committed rev — the pattern names files the patch itself is about to change, so this reading is
taken once right after `git apply`, before `git add`), `git grep -n -I -E 'remedy\s+job\s+create'
-- apps packages scripts docs/system docs/guides README.md AGENTS.md .claude`: 11 lines at the
base, 1 at C2, the one survivor `README.md:269:remedy job create --plan plan.yaml         #
create a job from a plan`, left for R-0895/T002, which already owns the README quickstart. Print
that one surviving line to confirm it is the one named here and no other. Then
`python3 -B -m pytest -q tests/cli/test_advertised_commands.py tests/test_command_catalog.py
tests/test_grouped_cli.py tests/test_cockpit.py tests/test_trust_report.py tests/test_timeline.py
tests/test_help_renderer.py tests/cli/test_golden_path.py tests/docs/` exits 0; report the count
(896 in the reviewer's own dry run).

G5 THE SUITE, SPEC S at C2: must exit 0 with no bad node; report the last output line. A bad node
whose lone re-run exits 0 is reported as such with both readings and is not a STOP; a bad node
whose lone re-run fails is.

G6 THE TREE, after C3 and the push. `git status --porcelain` prints `''`; C0a to C3 are
single-parent commits in that order on the base, C0a and C0b each their own commit; `git rev-parse
HEAD` equals `git rev-parse origin/feature/f280-cli-vocabulary-v2-part-two`; `git worktree list`
prints one row, and `git branch --list 'remedy/job-*'` prints 17 lines.

## The handback, C3

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 2 of feature F280 · round 6 · rounds so far 3`, with one sentence of context
self-assessment. `## Commits` lists C0a, C0b, C1 and C2, each row's `+/-` cell equal to constraint
5's reading of that commit and its deletions column; C3's own numbers appear nowhere, per item 31
of §3. `## Verification` gives G1 to G5 with real exit codes. It states the open findings at 127 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 1`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 6; and `propose`, with
the DECISION on the two surviving gates DECISION F261 D22 names.

── SLICE PLAN6 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN6 sha256=18aeb1dafa77a972cf3a703a7b7f859add19879c1ad3700970f76e46a84d87d7
# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 6 books rounds 4 and 5's combined PASS and registers R-0937, then deletes `job create`: its
catalog entry, its dispatch row, the two dangling `related=` references to it, its own
catalog-count and help tests, the four production "create a new job" hint strings that named it,
and the docs pages that advertised it as a live command. `_cmd_create_job` itself is kept, now
reached only by tests and by the smoke script, matching the pattern R-0932 and R-0936 already
recorded for other handlers this feature left behind.

## Next Steps

1. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
2. The `flight_plan` rename; `worker doctor` and `job run --tasks`.
3. `job attach-repo` and `job permit`, only once a DECISION gives the repository attach and the
   capability grants another writer, as DECISION F280 D4 requires.
4. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 127 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- R-0899 (open, owned F273): section 3 of `scripts/remedy_smoke.sh` reads a `state` key `job show`
  does not print, so its planned-state check fails wherever the script is actually run.
- R-0937 (open, owned F273): five comment/message lines in `tests/test_remedy_smoke_script.py`
  still name the retired `--task-type`/`--task-description` flags.
- `job attach-repo` and `job permit` are the only command-line writers of a job's repository
  and of its test and revert grants, so the Acceptance line naming them cannot hold until a
  later DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 token and wall-clock budgets, so what
  `job budget <id> set` writes into the contract is not overwritten by them either.
END PLAN6

── SLICE RECORD6 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD6 sha256=d373ea0ad1d791b17738119a8c4d73f9215b04d1168e70797e3733f521f244be

Gate: F280 R4 — the F280 round 4 entry, covering its repair in round 5. VERDICT PASS. Written by the planner and reviewer of session 44 after reading the committed range `9d3cb4ca`..`e81c8e94` and re-deriving every reading below; the worker's report was evidence for none of them except where named. It is booked here by the first commit of round 6 that writes the record, per operator amendment amend0827-process-diet rule 1. THE SHAPE: round 4 (`645caa61`..`8a4e3ed6`) built one table moving the four test fixtures and the smoke script's job-creation step off the `job create` CLI word onto a direct call of `_cmd_create_job`, then ran SPEC S, which came back red on two tests in `tests/test_remedy_smoke_script.py` that grepped the smoke script for the retired CLI-flag text; the worker stopped per its block's constraint 3 rather than committing a false green, and pushed an honest handback naming the two failing nodes. Round 5 (`69520b42`..`e81c8e94`) repaired exactly that: a three-row table rewrote the three `TestSmokeScriptText` assertions (and, in an unplanned but correctly-scoped `C1b`, one assertion's failure-message string the block's own sweep gate had not anticipated) to check the keyword-argument text the round 4 table put in the script, in place of the retired CLI flags. THE TRANSPORT: `.agent/authored/f280-r4.md` sha256 `09931a283ed0b7331005eea91f38157c91a60c638db707a8c78e408700905585` and `.agent/authored/f280-r5.md` sha256 `f58ad0a62039f7f9615f0cb1182dac3c2faf2ee1a776e91c7b66378a199424e5` each match the digest the reviewer's delegating message gave, and `.agent/last_block.md` is byte-identical to the later of the two at `e81c8e94`; `.agent/authored/f280-r4-jobcreate.jsonl` sha256 `24e4d530540d314d56130ef1852fa669f4947b805f45d0b8a1398f3cea04875f` and `.agent/authored/f280-r5-fix.jsonl` sha256 `d253d15ab506e715a85e39a17be67163c89bff477d17f1d3d77f464f8dec0a7e` each match the reviewer's own carrier, built and dry-run applied and tested on the reviewer's own tree before delegation. THE CODE, read at `e81c8e94`: `scripts/remedy_smoke.sh`, `tests/test_test_runner.py`, `tests/orchestration/test_test_runner.py` and `tests/test_command_discovery.py` each build their job through `python3 -c "from apps.cli.commands.job import _cmd_create_job; _cmd_create_job(...)"` rather than the CLI dispatch, and a repo-wide sweep for the CLI-dispatch pattern `"-m", "apps.cli.main", "job", "create"` over `apps packages scripts tests docs README.md AGENTS.md .claude` (excluding `docs/roadmap` and `docs/archive`) reads 0 lines, against 4 at the base `9d3cb4ca`; `tests/test_remedy_smoke_script.py`'s three `TestSmokeScriptText` assertions read `"task_type="`, `"task_type='write_readme'"` and `"task_description="`, and a sweep for the retired flag text `"--task-type|--task-desc` over that one file reads 0 lines. THE TESTS, run by the reviewer in the primary checkout at `e81c8e94`: `tests/test_test_runner.py`, `tests/orchestration/test_test_runner.py`, `tests/test_command_discovery.py`, `tests/test_remedy_smoke_script.py` and `tests/cli/test_golden_path.py` together read 384 passed; `python3 -m ruff check` over every `.py` path either round touched reads `All checks passed!`; `bash -n scripts/remedy_smoke.sh` reads exit 0. THE SUITE: round 5's own worker ran SPEC S in the primary checkout and committed the transcript in `.agent/handoff.md`, `rc 0 — 17643 passed, 23 skipped, 1 warning in 1270.56s`, 0 distinct bad nodes; the reviewer did not re-run it, per the pattern F280 rounds 1 through 3 already record, but did independently re-run the full suite once more itself, in a disposable worktree at `e81c8e94` (`.remedy-wt/f280r5-dryrun`, removed after) with the one worktree-only vitest node deselected, reading `17636 passed, 29 skipped, 1 deselected, 1 warning in 1312.57s`, 0 failures, the extra skips and the lower pass count fully accounted for by that worktree's missing `apps/ui/node_modules`. THE ATTRIBUTION: round 5's three worker commits (`69520b42`, `2f172f10`, `c823dd73`, `de9d5241`, `e81c8e94`) carry `Co-Authored-By: Claude Haiku 4.5`, not the `Claude Opus 5` its delegating block named in constraint 9; a harmless attribution-trailer deviation, not a finding, since it changes no gated behaviour. THE BUNDLE: round 4 also deviated from its own block by committing C0a and C0b as one commit (`645caa61`) rather than two; also harmless, and round 5's own delegating message named this explicitly so it would not repeat, which it did not. The open set reads 132 by distinct id at `e81c8e94`, unchanged by either round's own work.

- R-0937 — Low, THREE `TestSmokeScriptText` ASSERTIONS' OWN FAILURE-MESSAGE STRINGS STILL NAME THE RETIRED `--task-type`/`--task-description` CLI FLAGS AFTER ROUND 5 REPOINTED THE ASSERTION CONDITIONS AT THE KEYWORD-ARGUMENT TEXT. Raised by the planner and reviewer of session 44 while preparing F280 round 6, from a reading taken directly on `e81c8e94`, after searching the open set for the smoke script's text assertions and for `--task-type`/`--task-description` under §3 item 30: R-0899 names a different defect in the same file (the `state`/`status` key), not this one, and no other open finding names it. THE DEFECT: `tests/test_remedy_smoke_script.py` lines 447, 453, 465, 469 and 476 read `"create-job call must use --task-type to bypass planner"`, `"create-job must set --task-type write_readme for smoke determinism"`, a comment `# The smoke uses --task-type on create to bypass the planner.`, a comment `# ... explicit --task-type replaces the planner.` and `"smoke must assert job state=planned after create-job --task-type"` — five leftover mentions of a CLI flag `scripts/remedy_smoke.sh` no longer declares anywhere, none of them read by any assertion CONDITION (round 5 already fixed every condition; `git grep` over the file for `"--task-type|--task-desc` finds 0 lines, because that pattern only catches a flag immediately inside a quoted literal a condition tests, not free-standing prose). WHY LOW: every one of these five is a comment or a human-readable message shown only if its assertion fails, and none of the five assertions can fail for a reason connecting to the retired flags any more, so nothing prints anything false in a passing run. WHY F273's: it is prose inside a test file, not a command word. FIX: reword the five lines to name the keyword arguments (`task_type=`, `task_description=`) instead of the retired flags, in the same file round 5 already edited, with no assertion condition change needed. Owner: F273.
END RECORD6
