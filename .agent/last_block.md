── STEP T001/2 — F280 — ROUND 2 ──
Goal: Book round 1's PASS, register R-0932 to R-0934 and record DECISION F280 D2, then delete the
ping-pong path of `do run` with the flags only it reads, the scope plan module and prefix matching
of flags, by three tables; run the suite once.

Base commit: `4e93c22cda4634020b4b52abe6c6654c4d2b6c15`, on
`feature/f280-cli-vocabulary-v2-part-two`. SESSION 1 of F280. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISION F280 D2 once C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two
or more characters long is a run of a single repeated character, and every box-drawing rule inside
the STEP and SLICE header lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f280r2w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.commands.do_cmd` loaded from inside it. Never call `run_job` or any runner
yourself: a job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 17 lines now; keep it so. While a deletion is staged but
not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f280-r2.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN2; slice RECORD2 is appended to
    `.agent/live_review.md` and slice DEC2 to `.agent/decisions.md`; pairs P268, P273 and P280
    are applied
C2  THE PATH: copy `.remedy-wt/f280-block/f280-r2-path.jsonl` to
    `.agent/authored/f280-r2-path.jsonl` and apply it per THE TABLES, in one commit
C3  THE SCOPE PLAN: the same for `f280-r2-scope.jsonl`
C4  NO PREFIX MATCHING: the same for `f280-r2-abbrev.jsonl`
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f280-cli-vocabulary-v2-part-two`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f280-r2.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/features/T2_F268.md`,
`docs/roadmap/features/T2_F273.md` and `docs/roadmap/features/T2_F280.md`. C2 to C4: each table's
own carrier and the paths G3 names for that commit. C5: `.agent/handoff.md`. The gate carrier G4
names and the mutation carrier G5 names are READ from `.remedy-wt/f280-block/` and are never
committed.

## The appends and the pairs

RECORD2 and DEC2 each begin with an empty line, and both targets end in a newline at the base: an
append is the file's bytes followed by the slice's bytes, and nothing else. Each FROM slice occurs
exactly once in its target at the base, and each containment test printed
`TO contains FROM: false`, so each pair is a REWRITE: at C1 its FROM occurs 0 times and its TO once.
P268 `docs/roadmap/features/T2_F268.md`: FROM slice P268-FROM, TO slice P268-TO.
P273 `docs/roadmap/features/T2_F273.md`: FROM slice P273-FROM, TO slice P273-TO.
P280 `docs/roadmap/features/T2_F280.md`: FROM slice P280-FROM, TO slice P280-TO.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256, to verify before copying:
`f280-r2-path.jsonl` `df98e2a6577c99a3162e6f6d96c370d192f50936da32ce0f852ca50ecdd1cd16`,
`f280-r2-scope.jsonl` `1c99303db9b5b2d85b45c108fbee662cf8672e1ccb66faf4f5a36dfb561a8756` and
`f280-r2-abbrev.jsonl` `5f4f42bbfcde8d23e2eb54e70abc487357a4706ff4ed891256cb93c4a09a3560`.
Apply a table's rows strictly in the order they appear in its file, each against the tree as the
previous rows left it, from the repository root: `["edit", path, old, new, count]` opens the path
with `encoding="utf-8", newline=""`, requires the number of occurrences of `old` to equal `count`
exactly, and replaces every occurrence with `new`; `["delete", path]` removes the file;
`["move", src, dst]` renames the file, whose target must not exist; `["create", path, content]`
writes `content` to a path that must not exist, with the same encoding and newline setting. A
count that differs or a target that exists is a STOP: touch nothing further, commit nothing of
that table, and hand back with the row and the reading. Stage each commit with `git add -A` after
its table and its carrier. The tables are the research helper's build of DECISION F280 D2 on the
base, which the reviewer re-applied there with its own applier and tested.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f280r2w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f280r2w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f280-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph: this round's resolutions are the reviewer's, at the next gate.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 319 lines TOTAL and 235 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice
   CONTENT — the `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3's half for each table commit after that commit; G4 and G5
   after C4; then SPEC S, whose result is G6; G7 after C5 and the push, reported in the
   completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f280-r2.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN2, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its base blob followed
by RECORD2, and `.agent/decisions.md` its base blob followed by DEC2. Each of the three feature
files equals its base blob with its pair applied, with the counts The appends and the pairs give.
Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 28 at the base and 29 at C1, with
`Gate: F280 R1 — ` 0 times at the base and once at C1; distinct `^- R-\d+ — ` ids 127 and 130, C1
minus base exactly `R-0932`, `R-0933` and `R-0934`; distinct `^Done: R-\d+ — ` ids 2 and 2; the
open set by distinct id 125 and 128. `python3 -B -m pytest -q tests/docs/` exits 0 at C1.

G3 THE TABLES. For each table commit, `git diff --no-renames --name-only` from its parent prints
exactly its carrier and these paths. C2: `apps/cli/command_catalog.py`,
`apps/cli/commands/do_cmd.py`, `apps/cli/grouped.py`, `docs/system/vocabulary.md`,
`packages/orchestration/pingpong_provider.py`, `tests/cli/test_cli_ux.py`,
`tests/cli/test_do_cmd_pingpong_budget.py`, `tests/cli/test_product_spine.py`,
`tests/cli/test_scope_plan.py`, `tests/orchestration/test_pingpong.py`,
`tests/orchestration/test_pingpong_cli.py`, `tests/orchestration/test_provider_retry.py`,
`tests/orchestration/test_repair_loop.py`, `tests/orchestration/test_stream_evidence_integration.py`,
`tests/test_cli_execution_loop_closure.py`, `tests/test_command_catalog.py`. C3:
`packages/orchestration/pingpong_loop.py`, `packages/orchestration/scope_plan.py`,
`tests/cli/test_scope_plan.py`, `tests/cli/test_task_input.py`,
`tests/orchestration/import_reachability_allowlist.txt`. C4: `apps/cli/grouped.py`,
`tests/test_command_catalog.py`. `git rev-parse <commit>:<object>` equals the reviewer's dry run,
which applied the tables on the base, the record touching none of these objects. At C2: `apps`
`733555aa61f117495b867bb9c6c8b87ac962d5ef`, `packages` `6f7b4b38bcbfaf9f2e73dc5b568e61310cfea8d7`,
`tests` `7bcf67a94161d6e65fbd974209d9d3b2f5524aec`. At C3: `apps`
`733555aa61f117495b867bb9c6c8b87ac962d5ef`, `packages` `ed64c3a499eb6ad4352a06de527bc8c04dc267e1`,
`tests` `9b4de341549b93d7d056c12fe51b8898af67eeed`. At C4, for `apps`, `packages`, `scripts`,
`tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` in that order:
`725c9980aeb4a9b4bedfca043d31ca6ab1130136`, `ed64c3a499eb6ad4352a06de527bc8c04dc267e1`,
`4bea3f9f084c3987c399f39746b5b2c57be6ffca`, `9ff3aca064ebd7f537cdb61f275307737bbede1e`,
`52e345b71419d519c98eba49cea68cc424c249ce`, `e730766a135cae17d4a1c9db43b61b147d349303`,
`c282d425ef909cf9257605294f23aba7d9457fac`, `3c6b8d40ec4f4d76e05dc352a4b0ce8ef8970be5`,
`e3cd5e0ac262f3f993506e95825e270e39c03ec0`. Report the insertions of C2, C3 and C4 per
constraint 5. From the primary checkout at C2, `python3 -B -m pytest -q
tests/cli/test_golden_path.py` exits 0.

G4 THE SWEEP, at C4. `git ls-tree` at C4 prints nothing for
`packages/orchestration/scope_plan.py`, `tests/cli/test_scope_plan.py` and
`tests/cli/test_do_cmd_pingpong_budget.py`, and prints a blob for
`packages/orchestration/pingpong_loop.py`. The four patterns are the `deleted`, `deleted_flags`,
`quick_start_old` and `control` values of `.remedy-wt/f280-block/f280-r2-gates.json`, sha256
`e3ade0340ac37143d0f2621c0212c9a08f74edad393c635ddce1be7ab3c30ba2`; read them from that file in
Python and pass each as one argv element to
`git grep -n -I -E <pattern> <rev> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap' ':!docs/archive'`,
never retyping them in a shell, at the base, at C2, at C3 and at C4. The expected readings, lines
and files: `deleted` 181 and 8, 111 and 5, 8 and 2, 8 and 2; `deleted_flags` 48 and 8, 22 and 5,
22 and 5, 23 and 5; `quick_start_old` 5 and 2, 2 and 1, 2 and 1, 2 and 1; `control` 89 and 14 at
all four. Print every line `deleted` and `quick_start_old` match at C4. `python3 -m ruff check`
over every `.py` path C2, C3 or C4 edits that still exists at C4 exits 0; report how many paths
that was.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f280r2w/wt <C4's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`,
`tests/cli/test_cli_ux.py`, `tests/orchestration/test_pingpong.py` and
`tests/orchestration/test_pingpong_cli.py` with `-p no:randomly -p no:cacheprovider -rf --tb=no`,
under `python3 -B`. The mutations are the rows of `.remedy-wt/f280-block/f280-r2-mutations.jsonl`,
whose sha256 must equal `77d447624774c1b3086b97cbced3b1971d24f21cc6e3ecd3c6c0a831c9c0a4ab`; each
row is `[label, path, from, to, node]`, the `from` bytes must occur EXACTLY ONCE in that path
inside the worktree, and the file is restored with
`git -C .remedy-wt/f280r2w/wt checkout -- <path>` after each run. Read that carrier; never retype
its bytes. CONTROL first, unmutated: must exit 0. Each row must exit 1 with its row's node AMONG
the failed nodes. Report each exit code, summary line, each FROM's occurrence count and every
failed node id; then `git worktree remove --force .remedy-wt/f280r2w/wt` and read
`git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad node
whose lone re-run exits 0 is reported as such with both readings and is not a STOP; a bad node
whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on the base; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f280-cli-vocabulary-v2-part-two`; `git worktree list` prints one
row, and `git branch --list 'remedy/job-*'` prints 17 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F280 · round 2 · rounds so far 2`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 128 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 1`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 2 with the resolutions
of R-0767 and R-0894; and `job budget <id> set`, R-0906 and R-0909.

── SLICE PLAN2 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN2 sha256=5ecf5aab9a7a5a38105937cc8312219f31c21ba242f8d02d3428c15418422385
# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 2 books round 1's PASS, registers R-0932 to R-0934 and records DECISION F280 D2. Its three
table commits delete the ping-pong path of `do run` with the flags only it reads, delete the
scope plan module with `run_pingpong`'s scope branches, and turn argparse prefix matching off, so
no deleted flag survives as an abbreviation of a kept one. The worker runs the suite once.

## Next Steps

1. `job budget <id> set` over the run-contract budget fields and the token budget profile
   (R-0906, R-0909), then `job fulfill`; the next record books round 2's verdict with the
   resolutions of R-0767 and R-0894.
2. The fixtures and smoke sections moved off `job create`, then `job create`, `job attach-repo`
   and `job permit`.
3. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
4. The `flight_plan` rename; `worker doctor` and `job run --tasks`.
5. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 128 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- The quick start this round writes needs `remedy init` first and stops at the default autonomy
  level before any build, as DECISION F280 D2 records.
- Prefix matching is off for every command, so an operator's abbreviated flag now exits 2; the
  reviewer's scan found no abbreviated Remedy flag in the repository.
END PLAN2

── SLICE RECORD2 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD2 sha256=49e29786693fcdbd54194e861ea05f069f0afc47e71a7012b3c5dda153944e6d

Gate: F280 R1 — the F280 round 1 entry. VERDICT PASS. Written by the planner and reviewer of session 43 after reading the committed range `9f1b6d25`..`4e93c22c` and re-deriving every reading below; the worker's report was evidence for none of them except where named. It is booked here by the first commit of round 2 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f280-r1.md` at `11454c29` and `.agent/last_block.md` at `be2271d3` are byte-identical to the reviewer's scratch original, sha256 `e0160539e502a0c73d2de3eb4f32190b065d94fe8e7915ecc41d3afe0043c9da`, and the table committed at `290bd0ed` is byte-identical to the reviewer's carrier, sha256 `91c80c258f7edf0d1b334f87e6b631f043f446afab3d387ed85ba4a579e4b92f`, which is the research helper's table unamended. THE STATE: at `cadd1e81`, `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and `docs/roadmap/features/T2_F280.md` are byte-identical to the blobs of the reviewer's own dry-run commit, which applied the block's slices to `9f1b6d25`, and at `5716d3a7` so are `docs/roadmap/STATUS.md` and `.agent/context.md`; the `Gate:` count reads 27 then 28, the distinct registered ids 127 then 127, the distinct `Done:` ids 2 then 2, the open set 125 then 125, STATUS 78 `[x]` lines and one `[~]` line. THE TABLE COMMIT: at `290bd0ed` the `apps`, `packages`, `scripts`, `tests`, `docs`, `README.md` and `.claude` objects equal both the research helper's dry-run commit and the reviewer's own re-application of the table on `9f1b6d25`; `git show --numstat` reads 134 insertions against 47 deletions, the six edited files plus the 21-row carrier. THE RED-PROOFS ran in the reviewer's own worktree on the identical tree: a control of 243 passed at exit 0, and each of the four rows of the mutation carrier `56d2b30989440182c1a51a17790c6df2ca03c296d9be578a001bc1169dc864c6` exiting 1 with its named node among the failures — handing `run_job` no builder name and no reviewer name each reddened 12 nodes, re-adding the `--builder` flag to `job run` reddened the refusal test alone, and re-admitting `fixture` reddened its three parametrized cases; every FROM is whole lines occurring exactly once. THE REVIEWER'S RUNS: in its worktree the round's four test files with `tests/cli/test_golden_path.py`, `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py` and `tests/cli/test_cli_ux.py` read 427 passed; on its dry-run tree `tests/docs/`, `tests/orchestration/test_roadmap_index.py`, three state readers, `tests/orchestration/test_live_review_rotation.py` and `tests/ui_server/test_dashboard_contract.py` read 502 passed with one failure, `test_vitest_passes`, which needs `apps/ui/node_modules` and passed alone in the primary checkout at `9f1b6d25`; in the primary checkout at `4e93c22c` `tests/test_role_override_flags.py`, the canary, `tests/docs/`, the roadmap index and the catalog tests read 443 passed, and `python3 -m ruff check` over the six edited files printed `All checks passed!`. The worker's G6 transcript reports thirteen serial runs in the primary checkout at `290bd0ed`, each exit 0. The open set reads 125 by distinct id at `4e93c22c`.

- R-0932 — Low, DELETING THE PING-PONG PATH OF `do run` LEAVES THREE PACKAGE FUNCTIONS WITH TEST CALLERS ONLY, TWO PROMPT PARAMETERS THAT PRODUCTION ONLY EVER FILLS WITH NOTHING, AND AN EVIDENCE FIELD NO WRITER FEEDS. Raised by the planner and reviewer of session 43 while preparing F280 round 2, from readings its research helper took and the reviewer re-took on its own dry-run tree of that round's three tables, whose `apps` object is `725c9980` and `packages` object `ed64c3a4`, after searching the open set for each symbol under §3 item 30: no open finding names any of them. THE DEFECT, read on that tree: `summarize_pingpong`, `load_task_file` and `load_task_stdin` in `packages/orchestration/pingpong_loop.py` have no caller under `apps/`, `packages/` or `scripts/` other than their own definitions, because their only production caller was `_cmd_do_pingpong` and the `do run` prelude; the `scope_contract` parameters of `compose_builder_prompt` and `compose_reviewer_prompt` in the same module now receive only their empty default in production, because `run_pingpong` stopped passing scope text when the scope plan module was deleted, while golden tests still feed them real text; `_build_manifest` in `packages/orchestration/pingpong_evidence.py` reads a `scope_plan` key from the run record that no production code writes, so the manifest's `scope_plan` field is always None; and the docstrings of `tests/cli/test_task_input.py` still describe a CLI handler that refuses `--task-file` with `--task-stdin`. They stay under DECISION F261 D17's rule, because each module keeps other production importers. WHY LOW: dead weight and a field that can never be filled, and nothing prints anything false. WHY F273's: none of it is a command word, so it is paydown work. FIX: delete the three functions and their tests, or give `do <order>` a caller for the task loaders if F268 wants them; drop the `scope_contract` parameters with the golden tests re-cut; drop the manifest's `scope_plan` field or record why its schema keeps it; correct the stale docstrings. Owner: F273.

- R-0933 — Low, `do run` VALIDATES `--builder-provider` AND `--fixture-builder` AND THEN READS NEITHER, SO BOTH FLAGS ARE ADVERTISED, REFUSE BAD VALUES AND DO NOTHING WITH GOOD ONES. Raised by the planner and reviewer of session 43 while preparing F280 round 2, from readings its research helper took at `9f1b6d25` and the reviewer re-took on its dry-run tree whose `apps` object is `725c9980`, after searching the open set for both flags under §3 item 30: no open finding names them. THE DEFECT: the `do.run` dispatch entry in `apps/cli/commands/do_cmd.py` passes `_parse_builder_provider(...)` and `_parse_fixture_builder(...)` to `_cmd_do`, whose body names neither parameter after its signature, and `run_do` takes no provider argument; the catalog entry advertises `--builder-provider` as "none, fixture, ollama" and `--fixture-builder` as a builder mode. Before F280 round 2 prefix matching also let `do run --builder ollama` parse as `--builder-provider ollama`, which the same round turns off. WHY LOW: an invalid value still exits 2, and a valid one silently changes nothing; no wrong state is written. WHY F268's: DECISION amend0905-vocab D4 gives `do <order>` the `--*-provider` triplet with meanings of its own, and ruling 3 of the F261 inventory leaves the other `do run` flags to that feature. FIX: `do <order>` either wires `--builder-provider` into the run it starts, with a test that the named provider is the one recorded, or the two flags leave the catalog with a deletion paragraph. Owner: F268.

- R-0934 — Low, THE ADVERTISED-FLAG SCANNER STOPS READING A COMMAND LINE AT ITS FIRST QUOTE CHARACTER, SO NO FLAG AFTER A QUOTED ARGUMENT IS EVER CHECKED AGAINST THE CATALOG. Raised by the planner and reviewer of session 43 while preparing F280 round 2, after its research helper's mutation of the root help's quick start went unseen, and after searching the open set for the scanner under §3 item 30: R-0847, which removed the scanner's group pre-filter, is resolved and named a different blind spot. THE DEFECT, read at `4e93c22c`: `scan_advertised_command_flags` in `tests/cli/test_advertised_commands.py` cuts each match's tail at `_COMMAND_LINE_END_RE`, which ends at any of `"`, `'` or a backtick, so the reviewer's call on the line `remedy do run "<goal>" --bogus-flag x` returned the pair with an empty flag list; the old quick start step `remedy do run "<goal>" --repo . --builder claude-cli --reviewer claude-cli --json` therefore passed the guard with both deleted flags in it. WHY LOW: the round that exposed it added `test_quick_start_flags_are_declared_by_their_commands` for the one string it knew of, and nothing false is on disk now. WHY F280's: T002 already extends that guard to `README.md` under R-0895. FIX: skip a quoted argument rather than ending the line at its opening quote, while still ending at the quote that closes the enclosing Python string, with a test whose advertisement puts an undeclared flag after a quoted goal. Owner: F280.
END RECORD2

── SLICE DEC2 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC2 sha256=75a063abf3bc580316d56db71d4546594d242df3707c79da6048095edcd1f779

## DECISION F280 D2 (2026-09-16, F280 round 2) — the deletion paragraph of the ping-pong path of `do run`, its flags and the scope plan, and argparse prefix matching is turned off

CONTEXT. Ruling 3 of `.agent/f261_t003_inventory.md` gives `do run` to F268 except `--builder`, `--reviewer`, the flags only its ping-pong path reads and the scope flags, and R-0894 orders the scope flags deleted with the scope plan writer and loader and the contracts they feed, with a deletion paragraph. Measured at `9f1b6d25` by the reviewer's first research helper, read-only, and rebuilt at `4e93c22c` by a second, whose three tables the reviewer re-applied there with its own applier: the ping-pong branch of `_cmd_do` in `apps/cli/commands/do_cmd.py` runs `_cmd_do_pingpong` when `--builder` or `--reviewer` names a provider, and every other invocation runs `run_do`; sixteen flags of `do.run` are read only on the ping-pong path or only to validate it; `packages/orchestration/scope_plan.py` has no production importer but `_cmd_do` and `run_pingpong`'s scope branches, which only that path fed; `run show` and `run list` keep a writer, because `run_pingpong` persists each run and `run_job` calls it for every task; and once `--builder` leaves `do run`, argparse's prefix matching reads `do run "<goal>" --builder ollama` as `--builder-provider ollama` and exits 0.

CHOSEN, FIRST: `do run` loses `--builder`, `--reviewer`, `--scope-file`, `--approve-scope`, `--task-file`, `--task-stdin`, `--max-rounds`, `--mode`, `--test-command`, `--provider-timeout-sec`, `--timeout-profile`, `--max-output-chars`, `--keep-staging`, `--claude-cli-write-mode`, `--stream-evidence` and `--repair-rounds`, with the branch and the prelude that read them, `_cmd_do_pingpong`, `pingpong_effective_model`, `_print_scope_summary`, `_resolve_timeout_precedence`, `_VALID_PINGPONG_PROVIDERS`, the dead special-cases of those names in `apps/cli/grouped.py`, the scope block of the `run show` text report, and the tests that drove only that path. THE HEIRS: `job run` runs the builder and reviewer loop over a job's tasks with the provider flags DECISION F280 D1 wired; a goal or an order file started without a job is `do <order>`, which F268 builds and which DECISION F259 D2 names as the heir of the task file.

CHOSEN, SECOND: `packages/orchestration/scope_plan.py` is deleted whole with its tests and its import-reachability line, and `run_pingpong` loses its `scope_data` and `scope_validation` parameters and both scope-contract branches. THE HEIR: none. Approving a feature list before a run needed a writer DECISION F261 D3 already deleted, and no D4 word takes the idea back; R-0894 is resolved by this deletion. Package functions left with test callers only stay under DECISION F261 D17's rule and are named in R-0932.

CHOSEN, THIRD: the root help's quick start is rewritten onto surviving commands — `do run "<goal>" --repo . --json` teed to a file, the `job_id` read back, and `job show $JOB_ID --full` — under a heading that says `remedy init` comes first, because without a project the run exits 3; the default run stops at the default autonomy level before building, and T002 re-derives the quick start with the README quickstart of R-0895. `test_quick_start_flags_are_declared_by_their_commands` pins that every flag it names is declared, because the advertised-flag scanner cannot see flags after a quoted goal, which is R-0934. The two provider messages of `packages/orchestration/pingpong_provider.py` name `--builder-provider` and `--reviewer-provider`.

CHOSEN, FOURTH: `build_parser` in `apps/cli/grouped.py` creates its root, group and command parsers with `allow_abbrev=False`, so no deleted flag lives on as an abbreviation of a kept one, which DECISION D-B of `docs/roadmap/features/T2_F261.md` forbids as an alias under another name. `TestDeletedFlags` in `tests/test_command_catalog.py` pins every deleted flag of `do run` and `job run` as undeclared and refused by the parser. This supersedes the sentence of DECISION F280 D1 saying `job run` refuses `--builder` as an ambiguous prefix: it is now an unrecognized argument, still exit 2. ALTERNATIVE: keep prefix matching and pin only `do run --builder`, rejected because every later deletion of a flag sharing a prefix would reopen the same alias.

CONSEQUENCE. `remedy do run "<goal>" --builder claude-cli` exits 2 and `remedy do run "<goal>"` runs as before; an abbreviated flag anywhere exits 2, and the reviewer's research helper found no abbreviated Remedy flag in the repository's code, scripts, docs or tests. R-0767 is resolved, because no catalog entry declares `--builder` or `--reviewer`. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC2

── SLICE P268-FROM ── target `docs/roadmap/features/T2_F268.md` ── REWRITE FROM ──
BEGIN P268-FROM sha256=87061091b30bf4e3f306bbca293d66610a74a03ff46570dbec4ef4fcb53f17bb
  that `job apply` accepts, and a test applies a fake-provider run started from `remedy do`.

## Do not touch
END P268-FROM

── SLICE P268-TO ── target `docs/roadmap/features/T2_F268.md` ── REWRITE TO ──
BEGIN P268-TO sha256=92335b8ab4fcf43d4553604e5541c434910153aed12a8cde7a5c7029cc9a9bba
  that `job apply` accepts, and a test applies a fake-provider run started from `remedy do`.
- R-0933 carries a resolution line: `--builder-provider` reaches the run `remedy do` starts, with the
  test that reads the recorded provider, or the flag leaves the catalog with its deletion paragraph.

## Do not touch
END P268-TO

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=4c7eefa041da48486d89966ac7019b074e5d4286c6243e64273da2504d3b177e
  that edits the target, or the DECISION and the commit that deleted the manifest diff functions.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=4bba5961f081ea97918ba311048604ac211066b5afec73e0b443430d726ca72e
  that edits the target, or the DECISION and the commit that deleted the manifest diff functions.
- R-0932 carries a resolution line naming the commit that deleted or re-used each test-only remnant
  of the `do run` ping-pong path it lists, with the tests that changed.

## Do not touch
END P273-TO

── SLICE P280-FROM ── target `docs/roadmap/features/T2_F280.md` ── REWRITE FROM ──
BEGIN P280-FROM sha256=f800f1d552a8403299f18b6df33da20879aecb4130edcea4bf88fbc8720dffd1
  the catalog's groups and commands equal DECISION amend0905-vocab D4.

## Findings this feature owns
END P280-FROM

── SLICE P280-TO ── target `docs/roadmap/features/T2_F280.md` ── REWRITE TO ──
BEGIN P280-TO sha256=0c5de9f576452ebf77383b02ce2dd8a8419941c2d1c346bfa59b406a55cfa3cc
  the catalog's groups and commands equal DECISION amend0905-vocab D4.
- R-0934 carries a resolution line naming the test in which an undeclared flag after a quoted
  argument fails the advertised-flag scanner.

## Findings this feature owns
END P280-TO
