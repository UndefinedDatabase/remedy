── STEP T001/5 — F280 — ROUND 5 ──
Goal: Repair the red gate round 4 hit — update the three `tests/test_remedy_smoke_script.py`
assertions that check for the retired `--task-type`/`--task-description` CLI flag text in
`scripts/remedy_smoke.sh`, so they check the keyword-argument text round 4's table put there
instead — then run the suite once.

Base commit: `8a4e3ed6286ad2c2d086d5243c9d5d502a0b2353`, on
`feature/f280-cli-vocabulary-v2-part-two`. SESSION 2 of F280. Read AGENTS.md and
docs/agents/self_drive_protocol.md before C0a.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two
or more characters long is a run of a single repeated character, and every box-drawing rule inside
the STEP header line is exactly two characters long.

WHY THIS ROUND EXISTS: round 4's own worker ran SPEC S and found it red —
`tests/test_remedy_smoke_script.py::TestSmokeScriptText::test_create_job_uses_write_readme_task_type`
and `test_create_job_uses_task_description_flag` failed, because those two assertions grep the
smoke script's TEXT for the literal substrings `"--task-type write_readme"` and
`"--task-description"`, and round 4's table replaced the CLI invocation those substrings lived in
with a direct call `_cmd_create_job(..., task_type='write_readme', task_description='Write/update
README.md for smoke target.')`. The worker stopped per its block's constraint 3 rather than
committing a false green, exactly as required, and pushed an honest handback. A third test in the
same class, `test_create_job_uses_task_type_flag`, still reads `"--task-type" in text` and still
passes, but only because the substring survives by accident in the unrelated error message on
line 315 of `scripts/remedy_smoke.sh` (`'ERROR: job state must be planned after job create
--task-type, got: '`), never in the job-creation call itself; this round corrects that assertion
too, in the same commit, since it is the same test class checking the same retired mechanism.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)`, `$?` and `$VAR` expansions in a command are refused by form, so write such
checks as Python scripts under `.remedy-wt/f280r5w/`, never named after a standard-library module,
and use absolute paths rather than `cd x && ...`; a pipe into `tail` hides pytest's exit code. Never
call `run_job`, `run_job_fulfill` or any runner yourself; `git branch --list 'remedy/job-*'` reads
17 lines now, keep it so.

WHY NO RED-PROOF THIS ROUND: the table edits only `tests/test_remedy_smoke_script.py`, itself a
test file, and no line under `apps/` or `packages/`. The proof that each assertion now measures
the right thing is the assertion passing against the current script and failing against round 3's
script (the reviewer's own dry run, below); no production code changes, so no mutation red-proof is
ordered.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f280-r5.md`, the block file the delegating message names, by
    `shutil.copyfile`, in its OWN commit
C0b `.agent/last_block.md`, the same bytes, in its OWN commit — do not combine C0a and C0b into one
    commit; they are two separate items of the bundle above and each gets its own commit
C1  THE FIX: copy `.remedy-wt/f280-block/f280-r5-fix.jsonl` to
    `.agent/authored/f280-r5-fix.jsonl` and apply it per THE TABLE, in one commit
C2  `.agent/handoff.md`, the handback; then `git push origin feature/f280-cli-vocabulary-v2-part-two`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created. This round
carries no `.agent/plan.md` or `.agent/live_review.md` change: round 4 has not yet reached a
verdict, so there is nothing yet to book, and the reviewer books rounds 4 and 5 together in the
first commit of round 6, per operator amendment amend0827-process-diet rule 1.

## Change — exactly these paths and no others

C0a: `.agent/authored/f280-r5.md`. C0b: `.agent/last_block.md`. C1: the table's own carrier and
`tests/test_remedy_smoke_script.py`. C2: `.agent/handoff.md`.

## THE TABLE

The carrier holds one JSON array per line. Its sha256, to verify before copying:
`f280-r5-fix.jsonl` `d253d15ab506e715a85e39a17be67163c89bff477d17f1d3d77f464f8dec0a7e`. Apply its
rows strictly in the order they appear, each against the tree as the previous rows left it, from
the repository root: `["edit", path, old, new, count]` opens the path with `encoding="utf-8",
newline=""`, requires the number of occurrences of `old` to equal `count` exactly, and replaces
every occurrence with `new`. A count that differs is a STOP: touch nothing further, commit nothing
of the table, and hand back with the row and the reading. Stage the commit with `git add -A` after
the table and its carrier. The table is the reviewer's own build, applied and tested by the
reviewer on its own tree before delegation, whose objects the worker's dry run must equal.

## SPEC S — the suite, once, after C1 and before C2

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f280r5w/`. Report pytest's return code, the run's last output line, and every distinct
bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `. Re-run each bad
node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C1 and before C2, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f280r5w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f280-block/` and your own
   directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Gate:`, `Done:` or plan paragraph of your own this round: there is nothing to book yet.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: TOTAL and PROSE lines against the caps of 490
   and 400, where PROSE is every line that is not a line of slice CONTENT — the `BEGIN` and `END`
   marker lines count as prose. This block carries no BEGIN/END slice, so CONTENT is 0 and PROSE
   equals TOTAL.
8. GATE ORDER. G1 after C0a/C0b; G2 after C1; then SPEC S, whose result is G3; G4 after C2 and the
   push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and no
   subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f280-r5.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the committed carrier's
sha256 equals `d253d15ab506e715a85e39a17be67163c89bff477d17f1d3d77f464f8dec0a7e`.

G2 THE TABLE. `git diff --no-renames --name-only` from C1's parent prints exactly the carrier and
`tests/test_remedy_smoke_script.py`. `git rev-parse <commit>:tests` at C1 equals the reviewer's dry
run, which applied the table on the base: `e5a6ea325f3c644968741f757e8b2690ab48b0e2`; every other
top-level object (`apps`, `packages`, `scripts`, `docs/guides`, `docs/system`, `docs/README.md`,
`README.md`, `.claude`) is untouched, unchanged from round 4's own base:
`068608a3598c7550d2c5c9c103d875357be2646f`, `e5d99f301efb1073ba547c67b710288a24165d06`,
`bde7eae195226e4567a0cdde74c54e51e735b137`, `969f52e3e9e7a8c4ac1ccfa2f216b05968f6bf58`,
`3d77ab791e1ce9884320b0cd533783ca255a1963`, `0f1933b93649df9471145f57c5fbe9302f6a0d97`,
`3c6b8d40ec4f4d76e05dc352a4b0ce8ef8970be5`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`. Report the
insertions and deletions of C1 per constraint 5; the reviewer's own dry-run commit reads 3
insertions against 3 deletions. `python3 -m ruff check tests/test_remedy_smoke_script.py` exits 0.
`python3 -B -m pytest -q tests/test_remedy_smoke_script.py` exits 0 with all nodes passed (157 in
the reviewer's own dry run); report the actual count. `git grep -n -I -E '"--task-type|--task-desc'
<rev> -- tests/test_remedy_smoke_script.py` reads 0 lines at C1 (3 at the base).

G3 THE SUITE, SPEC S at C1: must exit 0 with no bad node; report the last output line. A bad node
whose lone re-run exits 0 is reported as such with both readings and is not a STOP; a bad node
whose lone re-run fails is.

G4 THE TREE, after C2 and the push. `git status --porcelain` prints `''`; C0a to C2 are
single-parent commits in that order on the base, C0a and C0b each their own commit; `git rev-parse
HEAD` equals `git rev-parse origin/feature/f280-cli-vocabulary-v2-part-two`; `git worktree list`
prints one row, and `git branch --list 'remedy/job-*'` prints 17 lines.

## The handback, C2

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 2 of feature F280 · round 5 · rounds so far 2`, with one sentence of context
self-assessment. `## Commits` lists C0a, C0b and C1, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C2's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G3 with real exit codes. It states the open findings at 126 by
distinct id (unchanged: this round registers and resolves nothing), with the High ids R-0803,
R-0804 and R-0807, and `Operator questions open: 1`. Its `## Next` names, in order: Phase 1 rule 1;
the reviewer's combined verdict on rounds 4 and 5; and deleting `job create` with its hints.
