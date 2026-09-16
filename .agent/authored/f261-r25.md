── STEP T003/8 — F261 — ROUND 25 ──
Goal: Book round 24's PASS and record DECISIONs F261 D24 and D25 with operator question Q3, then
land the `settings` alias over `config` by one table and register F280 by a second; run the
suite once and hand back the scope report.

Base commit: `d5e0a7b5`, on `feature/f261-cli-vocabulary-v2`. SESSION 6 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D24 and D25 once C1 has landed them.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r25w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or any runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r25.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN25; slice RECORD25 is appended to
    `.agent/live_review.md`; slice DEC24 and then slice DEC25 are appended to
    `.agent/decisions.md`; in `.agent/operator_questions.md` the bytes of slice QOP-FROM are
    replaced by those of slice QOP-TO
C2  the alias: copy `.remedy-wt/f261-block/f261-r25-alias.jsonl` to
    `.agent/authored/f261-r25-alias.jsonl` and apply it per THE TABLES, in one commit
C3  the registration of F280: copy `.remedy-wt/f261-block/f261-r25-split.jsonl` to
    `.agent/authored/f261-r25-split.jsonl` and apply it per THE TABLES, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r25.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and `.agent/operator_questions.md`. C2 and C3:
each table's own carrier and the paths G3 names for that commit. C4: `.agent/handoff.md`. The
mutation carrier G5 names is READ from `.remedy-wt/f261-block/` and is never committed and never
copied into `.agent/`.

## The appends and the pair

RECORD25, DEC24 and DEC25 each begin with an empty line, and both targets end in a newline at
`d5e0a7b5`: an append is the file's bytes followed by the slice's bytes, and nothing else, and
`.agent/decisions.md` at C1 is its blob followed by DEC24 followed by DEC25. The pair QOP:
TO contains FROM: false, so it is a REWRITE; QOP-FROM occurs once in `.agent/operator_questions.md` at
`d5e0a7b5`, and at C1 QOP-FROM occurs 0 times and QOP-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256, to verify before copying:
`f261-r25-alias.jsonl` `58f810e31bffb2fb8c2fbce5251b776a2df29fb641cd1a400984719052f3423f` and
`f261-r25-split.jsonl` `0bb2f13086a36429f4d9e3ab62f4d4f8e688f339da1f3fdb6abd2ba2a9e81243`.
Apply a table's rows strictly in the order they appear in its file, each against the tree as the
previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The alias table is the
reviewer's measured dry run of DECISION F261 D24 on `d5e0a7b5`, and the registration table is
its generator's output on that dry run's commit, applied there by the reviewer.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r25w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r25w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph: this round resolves no finding.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 302 lines TOTAL and 203 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice CONTENT — the
   `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3 half C2 after C2; G3 half C3, G4 and G5 after C3; then
   SPEC S, whose result is G6; G7 after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r25.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN25, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `d5e0a7b5` blob
followed by RECORD25, and `.agent/decisions.md` its blob followed by DEC24 and DEC25.
`.agent/operator_questions.md` equals its `d5e0a7b5` blob with the pair QOP applied, with the
counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads
133 at `d5e0a7b5` and 134 at C1, with `Gate: F261 R24 — ` 0 times at `d5e0a7b5` and once at C1;
distinct `^- R-\d+ — ` ids 134 and 134; distinct `^Done: R-\d+ — ` ids 9 and 9; the open set
by distinct id 125 and 125. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES. HALF C2, at C2: `git diff --no-renames --name-only` from C2's parent prints
exactly C2's carrier and these paths: `apps/cli/command_catalog.py`, `apps/cli/grouped.py`, `apps/cli/help_renderer.py`, `tests/cli/test_cli_ux.py`.
`git rev-parse C2:<object>` for `apps`, `packages`, `scripts`, `tests`, `docs/guides`,
`docs/system`, `docs/roadmap`, `docs/README.md`, `README.md` and `.claude`, in that order, equals
the reviewer's dry run, which applied the table on `d5e0a7b5` itself, the record touching none of
these objects: `4b3561d9c973b739fdd9c19bf18c4ed2c1fea95e`, `ec2c3efd7541c8cc7d30b2b226b109e1b285da45`, `3e3c450e0dffcdd11abbc52b0a7b085359df38e4`, `69cc72df6f8a81d55c5d8d94de401c7b0c88153f`, `52e345b71419d519c98eba49cea68cc424c249ce`, `cc42698197076bc70d79a91b05ca633d7ebd2df8`, `76bf53fdf467ecbf6bd80b35905b6609f7ede105`, `c282d425ef909cf9257605294f23aba7d9457fac`, `9cef3616d99c9689b6b100ea7792e9d8c2b7e57d`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`.
From the primary checkout at C2, `python3 -B -m pytest -q tests/cli/test_golden_path.py tests/cli/test_cli_ux.py`
exits 0.
HALF C3, at C3: the same name list from C3's parent prints exactly C3's carrier and these paths:
`README.md`, `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F261.md`, `docs/roadmap/features/T2_F268.md`, `docs/roadmap/features/T2_F270.md`, `docs/roadmap/features/T2_F271.md`, `docs/roadmap/features/T2_F277.md`, `docs/roadmap/features/T2_F279.md`, `docs/roadmap/features/T2_F280.md`, `tests/docs/test_docs_consistency.py`.
The same objects at C3 equal: `4b3561d9c973b739fdd9c19bf18c4ed2c1fea95e`, `ec2c3efd7541c8cc7d30b2b226b109e1b285da45`, `3e3c450e0dffcdd11abbc52b0a7b085359df38e4`, `29f5fccda172e532390a092be69d42357bfedf09`, `52e345b71419d519c98eba49cea68cc424c249ce`, `cc42698197076bc70d79a91b05ca633d7ebd2df8`, `dd955d0ca9a2ede0eb9c6282b527bb738a0770b7`, `c282d425ef909cf9257605294f23aba7d9457fac`, `60ded8dcaca796e8d61856b67d51f75a59f9440e`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`.
Report the insertions of C2 and of C3 per constraint 5.

G4 THE BEHAVIOUR, at C3, from the primary checkout's root. Each of
`python3 -B -m apps.cli.grouped settings --help`, `python3 -B -m apps.cli.grouped config --help`
and `python3 -B -m apps.cli.grouped roadmap status` exits 0; the first prints the line
` Also reachable as: remedy config`, the second the line ` Also reachable as: remedy settings`,
and the third a line beginning `Next unchecked: F280 — `. Report each exit code and each such
line. `python3 -B -m pytest -q tests/docs/` exits 0. `python3 -m ruff check` over every `.py` path
C2 or C3 edits exits 0; report how many paths that was. `git status --porcelain` prints `''`
after these commands.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r25w/wt <C3's sha>`, each run
through the runner with `-q -p no:randomly -p no:cacheprovider` over `tests/cli/test_cli_ux.py`,
`tests/test_command_catalog.py`, `tests/test_help_renderer.py`,
`tests/cli/test_advertised_commands.py` and `tests/docs/` with `-rf --tb=no`. The mutations are
the rows of `.remedy-wt/f261-block/f261-r25-mutations.jsonl`, whose sha256 must equal
`8275e65a0ef5cdc752122c144d44b41e596ff6ab6cc418c4cf17170c70a8b491`; each row is
`[label, path, from, to, node]`, the `from` bytes must occur EXACTLY ONCE in that path inside the
worktree, read and written with `encoding="utf-8", newline=""`, and the file is restored with
`git -C .remedy-wt/f261r25w/wt checkout -- <path>` after each run. Read that carrier; never retype
its bytes. (a) CONTROL: must exit 0. Each mutation row must exit 1 with its row's node AMONG the
failed nodes; a row reds further nodes that pin the same property, and those are expected rather
than a STOP. Report each exit code, summary line, number of failed nodes and each FROM's
occurrence count; then `git worktree remove --force .remedy-wt/f261r25w/wt` and read
`git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `d5e0a7b5`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 6 of feature F261 · round 25 · rounds so far 25`, with one sentence of context
self-assessment. Directly after the Session section it carries slice SCOPE25 byte for byte.
`## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's reading of that commit
and its deletions column; C4's own numbers appear nowhere, per item 31 of §3. `## Verification`
gives G1 to G6 with real exit codes. It states the open findings at 125 by distinct id, with the
High ids R-0803, R-0804 and R-0807, and `Operator questions open: 1`. Its `## Next` names, in
order: Phase 1 rule 1; the reviewer's verdict on round 25; and the closure sequence of F261.

── SLICE PLAN25 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN25 sha256=d874f5c0bce1f13fb7c75a46604407ae1eab1151f61a59fbc65701f8da00c8eb
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md` — as far as this feature reaches it; DECISION F261 D25
moves the rest to F280.

## Current Step

ROUND 25, the feature's soft limit. It books round 24's PASS and records DECISIONs F261 D24
and D25 with operator question Q3, then lands the `settings` alias over `config` by one table
and registers F280 by a second, and hands back the scope report D25 executes.

## Next Steps

1. The closure sequence of F261 under `docs/roadmap/STATUS_closure_protocol.md`: the
   integration gate, the ledger rotation, the one consolidation pass of the §3 checklist, the
   evidence package, the STATUS flip and the pull request.
2. F280, which Rule A5 proposes once F261 is merged.

## Risks

- 125 findings are open by distinct id; three are High, R-0803, R-0804 and R-0807. Seven that
  F261 owned move to F280 by DECISION F261 D25.
- F261 closes with the Goal & Done sentence not met, and says so in its Built State; the
  operator may reverse the split through operator question Q3.
- `propose` and `job fulfill` stay in the catalog because deleting either breaks a surviving
  command; F280 owes the rulings.
END PLAN25

── SLICE RECORD25 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD25 sha256=20902ad0963b416f83696d10fbfeac76132556d65b027a6bb8721c7ee5df1c49

Gate: F261 R24 — the F261 round 24 entry. VERDICT PASS. Written by the planner and reviewer of session 41 after reading the committed range `fc13ba87`..`d5e0a7b5` and re-deriving every reading below; the worker's report was evidence for none of them. It is booked here by the first commit of round 25 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r24.md` at `021b3c33` and `.agent/last_block.md` at `1fb1d5e1` are byte-identical to the reviewer's scratch original, sha256 `7ef435c5d02c99cd680106e5fc576e1a14b3383aead836eded3dc3bf8e6de9a5`, and the tables committed at `27dcd9e4` and `6f506cea` are byte-identical to the reviewer's carriers, sha256 `a3ece98b795f51e1e7703c0f5cc07af38c5787296d31d38606064f5c678bdbc7` and `f9d47405806677c0bb788285a86135ce0f3af981bd860581d76caed517242a2b`; the first is the research helper's rerun-only rebuild, and the second is the other helper's generator output, which the reviewer regenerated on its own rerun dry-run commit and found byte-identical to the table that helper built on `fc13ba87`. THE STATE: at `a9ed91b4` and again at `d5e0a7b5`, `.agent/plan.md` equals PLAN24, `.agent/live_review.md` and `.agent/decisions.md` equal their `fc13ba87` blobs followed by RECORD24 and DEC23, and `docs/roadmap/features/T2_F273.md` equals its `fc13ba87` blob with the pair P273D applied; the `Gate:` count reads 132 then 133, the distinct registered ids 133 then 134 with the delta exactly R-0931, the distinct `Done:` ids 9 then 9, and the open set 124 then 125. THE TABLE COMMITS: at `27dcd9e4` and at `6f506cea` the `apps`, `packages`, `scripts`, `tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` objects equal the reviewer's two stacked dry-run commits object for object, all eighteen, and each `--no-renames` name list equals its dry run's; `git show --numstat` reads 46 insertions against 480 deletions and 101 against 69. THE SWEEP, with the patterns of the reviewer's gate carrier read as argv at `fc13ba87`, `27dcd9e4` and `6f506cea`: the deleted `job rerun` words read 31 lines in 12 files, then 2 in 2, then 2 in 2, the survivors being the new `TestDeletedCommands` id and the docs-consistency pin of accepted F012 history; the `teach` group word reads 77 in 17, 77 in 17, then 10 in 6, the survivors being the two `TestRenamedCommands` rows, four lines of `docs/system/vocabulary.md` that record the rename and four prose uses of the verb; and THE CONTROLS on the two words DECISIONs F261 D22 and D23 keep deferred, `propose` at 67 in 11 and `job fulfill` at 21 in 7, read the same at all three. `apps/cli/commands/job_rerun_cmd.py`, `apps/cli/commands/teach_cmd.py` and `tests/cli/test_teach_cmd.py` are absent at `6f506cea`, and `apps/cli/commands/teacher_cmd.py` and `packages/orchestration/run_manifest.py` are present. THE RED-PROOFS ran in the reviewer's own worktree on the tree whose objects `6f506cea` reproduces, over the exact selection the block ordered: a control of 480 passed at exit 0, and each of the eight rows of the mutation carrier `c611f931d1a411ac3412d6879191823d96e3a6506954c7ebe3994a0996adfa2b` exiting 1 with its named node among the failures — the catalog entry, the dispatch entry, a quickstart invocation and the allowlist line of `job rerun`, each the only failure, and the dispatch key, a catalog id, the group word and the `teacher_qa` hint of the rename, which red three, six, four and five nodes that pin the same names; every FROM is whole lines occurring exactly once. THE REVIEWER'S RUN in the primary checkout at `d5e0a7b5` of the round's own test files, the run-manifest, worktree and teacher tests nearest every production module it touched, `tests/cli/test_golden_path.py`, `tests/cli/test_config_cmd.py`, the whole of `tests/docs/` and `tests/ui_server/` read 1404 passed, and `python3 -m ruff check` over the nineteen edited files that survive printed `All checks passed!`. The canary of the rename commit is in that run, because every tree object of `d5e0a7b5` equals `6f506cea`'s. The worker ran the full suite once in the primary checkout at the rename commit, as the block orders: exit 0, `17642 passed, 23 skipped, 1 warning in 1268.90s`, with no line-initial `FAILED ` or `ERROR ` in its transcript, which the reviewer read. The worker declared one departure, adding `-q -p no:cacheprovider -p no:randomly` to the red-proof runs the block ordered with `-rf --tb=no`; it narrows nothing the gate measures, and the reviewer's own runs used the same flags. The open set reads 125 by distinct id at `d5e0a7b5`.
END RECORD25

── SLICE DEC24 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC24 sha256=06cbaa231a1ce1cdc1d88d9e8b020574dd37cba76bdf7dce09f80d5a9a988e1b

## DECISION F261 D24 (2026-09-16, F261 round 25) — `settings` is an alias surface over `config`, carried by an `aliases` field of `GroupDef` and one resolver

CONTEXT. DECISION D-D of `docs/roadmap/features/T2_F261.md` makes `settings` a pure alias surface over the existing `config` group — one implementation, two words, each help text naming the other, registered as an alias and never as a duplicated set of command definitions — and ruling 11 of `.agent/f261_t003_inventory.md` proposes an `aliases` field with one resolver for every group lookup. Measured at `d5e0a7b5` by the reviewer's research helper and re-read by the reviewer: no `settings` group, command id, handler or hint exists anywhere, so there is no conflict to resolve, and the group lookups live in `apps/cli/grouped.py` and in `get_group` and `get_commands_for_group` of `apps/cli/command_catalog.py`.

CHOSEN. `GroupDef` gains `aliases: tuple[str, ...] = ()` beside `hidden`, and the `config` entry carries `aliases=("settings",)`. `resolve_group(word)` returns the group id a word names, by its id or an alias, or None, and `get_group`, `get_commands_for_group`, the help pre-scan, the unknown-group error, the default-subcommand injection and group help all resolve through it; `build_parser` registers the aliases with argparse, so both words parse to the same `config.*` command id and dispatch the same handler. `render_group_help` takes `also`, and a group's help page prints `Also reachable as:` with the group's other words, so `remedy settings --help` names `remedy config` and `remedy config --help` names `remedy settings`. `TestSettingsAlias` in `tests/cli/test_cli_ux.py` pins one `GroupDef`, the resolver, collision-freedom, both help pages, identical parse, dispatch and output under both words, the unknown-subcommand error and injection through an alias. NOT DONE, on purpose: the root help lists groups and does not name aliases, and `tests/cli/test_advertised_commands.py` resolves an advertisement against group ids only, so a future hint that advertises `remedy settings` would read as unknown there until that guard learns the resolver.

CONSEQUENCE. `remedy settings <command>` is `remedy config <command>` in every respect, and the Acceptance line on the two help texts holds. HOW TO REVERSE: revert the round's alias table commit and delete this section.
END DEC24

── SLICE DEC25 ── target `.agent/decisions.md` ── APPEND, after DEC24 ──
BEGIN DEC25 sha256=95dec9aba24e1c9ec84f9d3e2217be89b28fb767096a3187524e819274b69a22

## DECISION F261 D25 (2026-09-16, F261 round 25) — split-and-close at the soft limit: the rest of T003 and all of T004 become F280

CONTEXT. Round 25 is F261's twenty-fifth delegated round, the standing soft limit of operator amendment amend0827-process-diet rule 6, and operator amendments amend0905-throughput and amend0906-split-placement make split-and-close the default the session executes on its own authority, as a dated DECISION the operator may reverse. Measured at `d5e0a7b5` by the reviewer and its research helper: T001 and T002 are complete; T003 is reached for every group and word DECISIONs F261 D12 to D23 record, and this round adds the `settings` alias of DECISION F261 D24; still owed are the `propose` group, which DECISIONs F261 D21 and D22 defer because `self execute` and the cockpit's `can_finalize` gate on its store, `job fulfill`, which DECISION F261 D23 defers until `job budget <id> set` exists, that write itself, `job create`, `job attach-repo` and `job permit` with their fixtures, the `--builder` and `--reviewer` flags with the `job run` provider wiring and the ping-pong path of `do run`, and the `flight_plan` rename; T004 is not started.

CHOSEN, FIRST: F280, CLI vocabulary v2 part two, is registered in one commit, generated by the reviewer's helper from the files at this round's alias commit and applied by the table this round orders: `docs/roadmap/features/T2_F280.md`, its STATUS line directly after F261's inside the same Tier 2 heading, `TOTAL_FEATURES` at 280 with its comment, the README counters, and F280 added to the Depends-on lines of F268, F270, F271, F277 and F279, the open features that name F261 there. F280's T001 is F261's T003 quoted verbatim followed by what is owed, and its T002 is F261's T004 quoted verbatim; its Acceptance carries verbatim every F261 Acceptance line not reached, and adds lines for the unreached parts of T003.

CHOSEN, SECOND: F261's own Acceptance section is left as registered, as F272 and F274 left theirs, and its new Built State section records which slices and which Acceptance lines moved, what is reached and why the close is self-consistent: every deferred word is whole in the catalog and still works, and every deleted word left with its deletion paragraph and its id in `TestDeletedCommands`. The Goal & Done sentence that the catalog equals DECISION amend0905-vocab D4 exactly is NOT met at this close and is F280's.

CHOSEN, THIRD, per operator amendment amend0911-feedback rule A: the open findings F261 owned and did not resolve — R-0767, R-0805, R-0809, R-0894, R-0895, R-0906 and R-0909 — are re-assigned to F280, whose feature file names them; their registrations in `.agent/live_review.md` stay as written, because that file is append-only, and this paragraph is the re-assignment. The move is also operator question Q3, because it changes the roadmap's order.

ALTERNATIVES. Continuing past the limit is forbidden by the two amendments above. Deleting `propose` and `job fulfill` now to reach D4 is rejected, because DECISIONs F261 D21 to D23 measured that either deletion breaks a surviving command.

CONSEQUENCE. F261's next rounds are its closure sequence under `docs/roadmap/STATUS_closure_protocol.md`, whose accepted STATUS line and evidence become F280's starting point; Rule A5 then proposes F280. HOW TO REVERSE (operator): revert the registration commit, delete this section and answer Q3; F261 then carries its full T003, T004 and Acceptance again, reopened past its limit.
END DEC25

── SLICE QOP-FROM ── target `.agent/operator_questions.md` ── REWRITE FROM ──
BEGIN QOP-FROM sha256=522daeaebb0b8415d664318457d8980f80f8a2e670a38a4dd3cbf337ce982661
EMPTY — nothing is waiting on the operator.
END QOP-FROM

── SLICE QOP-TO ── target `.agent/operator_questions.md` ── REWRITE TO ──
BEGIN QOP-TO sha256=7a5ca72e1897065820dd7f697dda3670d770d1add9995d6ea24b28417eae4833
### Q3 — Command-name cleanup split in two (2026-09-16, F261, round 25)

What needs deciding. The feature that renames and prunes Remedy's commands reached its limit of twenty-five rounds before it was finished. Under your standing default I split it: this feature now closes with what it reached, and the rest is registered as a new follow-up feature placed directly after it on the roadmap, so it is the next thing the loop picks up once this one is closed. What moved is the removal of three command families that other working commands still depend on, the changes to how the run command chooses its builder and reviewer, the rename of the plan module, and the whole final pass over help texts, role labels and the visible order of command groups. Seven open review findings go with it.

Why it matters. The command tree is not yet the one the vocabulary decision describes: some words it retires still exist, because deleting them today would break commands that stay. The roadmap now has one more feature, and it sits ahead of every other unfinished feature.

My recommendation. Keep the split. Everything the first feature did is complete and tested, nothing is half-done, and the follow-up starts from a clean state with each blocked deletion named together with the reason it waits.

What happens if you say nothing. The first feature goes through its normal closing steps, and the loop then starts the follow-up feature.
END QOP-TO

── SLICE SCOPE25 ── target `.agent/handoff.md` ── HANDBACK SECTION, byte for byte ──
BEGIN SCOPE25 sha256=22fd48d078081ad39789e412b5cfcf8861c1c65f6337070ea61220de16c9ce10
## Scope report — F261 at its soft limit

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F261 reached the standing soft limit of 25 delegated rounds with round 25, in the feature's
sixth session. Operator amendments amend0905-throughput and amend0906-split-placement make
split-and-close the default the session executes, and this round executed it under DECISION
F261 D25, which the operator may reverse through operator question Q3.

FINISHED. T001: `do job-evidence`, `do job-promote` and `do job-run` became `job evidence`,
`job apply` and `job run`, and `do job-flow`, `do job-plan` and `do plan` were deleted
(DECISIONs F261 D1 to D3). T002: `do promote` and the run-level apply library were deleted,
`job_promote.py` became `job_apply.py` with its words, `job show` gained `--json`, `--full`
and the findings of blocked tasks, and the eight read views became its sections (D4 to
D11). T003, reached part: the hidden `roadmap` group (D12); fifteen groups deleted, from
`orchestrator` to `repair` (D13 to D17, D21); `do report` became the `run` group and five
further `do` words left (D18 to D20); the queue words of `job`, `worker run`, `mission
ledger` and `job rerun` were deleted (D22, D23); `teach` became `teacher` (D23); and the
`settings` alias now reaches `config` (D24).

MISSING, and now F280's: the `propose` group and `job fulfill`, each deferred because
deleting it breaks a surviving command (D21 to D23); `job budget <id> set`; `job create`,
`job attach-repo` and `job permit` with their fixtures; the `--builder` and `--reviewer`
flags with the `job run` provider wiring and the ping-pong path of `do run`; the
`flight_plan` rename; and all of T004 — descriptions, role labels, help wrapping, the
catalog ownership test, the dead-command doctor check, the enforced F259 test, the visible
group order and the README quickstart. Findings R-0767, R-0805, R-0809, R-0894, R-0895,
R-0906 and R-0909 move with them.

PROPOSAL EXECUTED. F280 is registered directly after F261 with that scope, and F261 closes
at the scope it reached through the normal closure sequence, which is the next session's
work.
END SCOPE25
