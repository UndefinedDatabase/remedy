STEP T001/1 - F262 List commands v2, ROUND 2
FEATURE F262 - List commands v2 (Tier 2) - SESSION 1, ROUND 2

Goal
  Ship T001, the shared listing-option surface: `--sort`, `--desc`,
  `--since`, `--until` and `--limit` attached to every list-shaped
  catalog command BY CONSTRUCTION, plus a catalog-derived coverage test
  proving no list command is missing one. This round changes what
  argparse ACCEPTS, not what any store's output looks like - no
  handler's behavior changes (T002/T003 do that).

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r2.md
  C0b mirror it to .agent/last_block.md
  C1  append GATE1 to .agent/live_review.md - books round 1's PASS
      verdict (the reviewer's own, not a worker claim), per
      docs/agents/self_drive_protocol.md's rule that a verdict is
      booked into the FIRST commit of the next round that is happening
      anyway
  C2  ship T001: apps/cli/command_catalog.py (the shared surface) and
      tests/test_command_catalog.py (the coverage test), together, per
      the CODE SPEC below
  C3  apply PLAN3 to .agent/plan.md
  C4  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r2.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - apps/cli/command_catalog.py (C2) -
  tests/test_command_catalog.py (C2) - .agent/plan.md (C3) -
  .agent/handoff.md (C4)

CODE SPEC for C2 - read this fully before writing anything. This is a
description of the required change, not a byte-exact slice: write it as
idiomatic Python matching the surrounding file's style, but every name,
signature and behavior below is BINDING, not a suggestion.

  In apps/cli/command_catalog.py:

  1. Change the import line `from dataclasses import dataclass` to
     `from dataclasses import dataclass, replace`.

  2. Rename the existing catalog tuple's binding from `CATALOG` to
     `_BASE_CATALOG` (the line currently reading exactly
     `CATALOG: tuple[CommandEntry, ...] = (` becomes
     `_BASE_CATALOG: tuple[CommandEntry, ...] = (`). Do not touch any
     entry inside the tuple - only its own binding name changes.

  3. Immediately after that tuple's closing `)` (currently followed by
     two blank lines and then the "# The whole surface of the UI write
     door" comment before `UI_EXPOSED_COMMANDS`), insert a new section
     defining:
     - Five module-level ArgDef constants, named exactly
       `_LIST_SORT_ARG`, `_LIST_DESC_ARG`, `_LIST_SINCE_ARG`,
       `_LIST_UNTIL_ARG`, `_LIST_LIMIT_ARG`:
         `_LIST_SORT_ARG = ArgDef("--sort", "Sort field; this command's
         own columns are the valid set (see --help)", required=False,
         is_option=True)`
         `_LIST_DESC_ARG = ArgDef("--desc", "Reverse the sort order",
         required=False, is_option=True, is_flag=True)`
         `_LIST_SINCE_ARG = ArgDef("--since", "Only rows at or after
         this time: an ISO-8601 timestamp, or a relative form such as
         2d or 12h", required=False, is_option=True)`
         `_LIST_UNTIL_ARG = ArgDef("--until", "Only rows before this
         time: an ISO-8601 timestamp, or a relative form such as 2d or
         12h", required=False, is_option=True)`
         `_LIST_LIMIT_ARG = ArgDef("--limit", "Max rows to return",
         required=False, is_option=True)`
       Wrap long `ArgDef(...)` calls across lines however the file's
       existing style does (it already wraps long ArgDef calls widely).
     - `_LIST_OPTION_ARGS: tuple[ArgDef, ...]` holding those five, in
       the order sort, desc, since, until, limit.
     - `def _is_list_command(entry: CommandEntry) -> bool:` returning
       `entry.subcommand == "list" or entry.subcommand.endswith("-list")`.
       This is the ONLY place the list-command rule is defined; the
       test in C2 imports it rather than restating it.
     - `def _with_list_options(entry: CommandEntry) -> CommandEntry:`
       that returns `entry` unchanged when `_is_list_command(entry)` is
       false; otherwise computes `existing = {a.name for a in
       entry.args}`, `missing = tuple(a for a in _LIST_OPTION_ARGS if
       a.name not in existing)`, and returns `entry` unchanged if
       `missing` is empty, else `replace(entry, args=(*entry.args,
       *missing))`. THIS IS LOAD-BEARING: a command that already
       declares a flag of the same name (today only `event.list`, which
       already has `--since` and `--limit`) must keep its OWN existing
       ArgDef for that name untouched and only gain the flags it is
       missing - adding a second ArgDef of an already-present name
       crashes argparse at parser-build time with a conflicting-option
       error (verified by the reviewer before this round: see
       Constraint 6).
     - Finally, `CATALOG: tuple[CommandEntry, ...] = tuple(
       _with_list_options(c) for c in _BASE_CATALOG)` - this replaces
       the old plain-tuple `CATALOG` binding; it is still named
       `CATALOG` and every existing importer of `CATALOG` is unaffected
       in name, only in the content of list-shaped entries.

  In tests/test_command_catalog.py:

  1. Add `_is_list_command` to the existing
     `from apps.cli.command_catalog import (...)` import block.

  2. Add a new test class, placed after `TestCatalogExpensive` and
     before `TestCatalogSensitivity`, named `TestListCommandOptions`,
     with a short one-line docstring crediting F262 T001, holding
     exactly these three tests:
     - `test_every_list_command_carries_all_four_flags`: builds
       `list_commands = [c for c in CATALOG if _is_list_command(c)]`,
       asserts it is non-empty, then for each command asserts
       `{"--sort", "--since", "--until", "--limit"} - {a.name for a in
       cmd.args}` is empty, with an assertion message naming the
       command_id and the missing flags.
     - `test_every_list_command_has_exactly_one_desc_flag`: for each
       command in the same `list_commands`, asserts exactly one arg
       named `--desc` and that its `is_flag` is `True`.
     - `test_the_parser_builds_for_every_list_command`: imports
       `build_parser` from `apps.cli.grouped` and simply calls it with
       no arguments inside the test body (building the WHOLE parser
       tree once is the cheapest proof that no command anywhere in the
       catalog - list-shaped or not - has two ArgDefs sharing a flag
       name, which is exactly the collision class this round's own
       design avoids by construction; a short docstring says so).

Constraints
  1. C1's append to .agent/live_review.md is applied BYTE FOR BYTE:
     extract GATE1 from the COMMITTED .agent/authored/f262-r2.md by its
     BEGIN/END markers (excluded) and apply with a script, never by
     retyping. GATE1 carries ZERO internal newlines and NO trailing
     newline of its own. The base file (measured by the reviewer before
     this round) is 2414126 bytes with NO trailing newline; the applied
     file must equal base + one newline byte + GATE1's own bytes,
     exactly 2417095 bytes total. Report the arithmetic and a `cmp`
     against a script-extracted copy of GATE1, both directions.
  2. C2's Python is written by hand from the CODE SPEC above (not
     extracted from a marker slice) - normal careful engineering, not a
     byte-transport exercise. Self-review it against the spec before
     committing: every named symbol (`_LIST_SORT_ARG` through
     `_LIST_LIMIT_ARG`, `_LIST_OPTION_ARGS`, `_is_list_command`,
     `_with_list_options`, the renamed `_BASE_CATALOG`, the rebuilt
     `CATALOG`) must exist with the exact behavior described, and
     nothing in `_BASE_CATALOG`'s existing entries changes.
  3. `python3 -m py_compile apps/cli/command_catalog.py
     tests/test_command_catalog.py` must exit 0 for both (ruff is
     denied this session - attempt it anyway and report the exact
     refusal or the real result, never assume).
  4. C2 is ONE commit covering both files - the shared surface and its
     coverage test land together, since neither is meaningful alone.
  5. PLAN3 REPLACES .agent/plan.md whole-file, ending WITHOUT a trailing
     newline, same as every prior round.
  6. The reviewer independently verified before authoring this block,
     in a throwaway (uncommitted) local check: adding a second `--since`
     ArgDef to `event.list`'s existing args raises
     `ArgumentError: argument --since: conflicting option string:
     --since` when `grouped.build_parser()` runs. This is why
     `_with_list_options` (spec item above) is add-only-if-missing
     rather than a blind append, and why `test_the_parser_builds_for_
     every_list_command` exists as a whole-catalog regression net for
     exactly this failure mode.
  7. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  8. Read .agent/STOP from disk before the first commit and again
     before C4. If it exists, finish the commit in hand, write the
     handback, and stop.
  9. Self-review loop before every commit (git diff --stat, git diff).
     Push after C4 (git push origin feature/f262-list-commands-v2). No
     pull request, no merge.
  10. `git rev-parse HEAD` before C0a must read
      `9d15b7f2a23fb7234d7e2f33f043689363050eeb` (report the full SHA);
      `git branch --show-current` must read
      `feature/f262-list-commands-v2`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output. This round earns the mutation red-proof and the full suite (not
just the round-scoped tests) because C2 edits a catalog every list
command's parser is built from, and dozens of unrelated test files
import from apps.cli.command_catalog - the blast radius is the whole
CLI surface, not just the eight files this round's change set names.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f262-r2.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND, FULL FORENSICS (this is one of the two files
     that keep full byte forensics under the gate-budget rule). Extract
     GATE1 from the COMMITTED authored file to scratch. Report:
       base size immediately before C1 (bytes, trailing-newline byte)
       GATE1 own byte length and internal-newline count
       base + 1 + GATE1_length, compared against the post-C1 file's real
         byte length - state match True/False
       tail slice (last GATE1_length bytes of the post-C1 file) compared
         against GATE1 - state equal True/False
       negative control: flip the first byte of a COPY of GATE1, confirm
         the flipped copy does NOT match the real tail - state
         rejected True/False
  G3 THE CODE, READ NOT ONLY GATED. Report the full diff of
     apps/cli/command_catalog.py. Confirm by direct reading (not by
     count alone) that every named symbol in the CODE SPEC exists with
     the described behavior, that no existing `_BASE_CATALOG` entry's
     bytes changed (only the tuple's own binding name), and that the
     rest of the file - everything before the renamed binding and
     everything after `UI_EXPOSED_COMMANDS` - is byte-identical to the
     pre-round file (`git diff` naming zero changed lines outside the
     inserted/renamed region). Then, independently, run this exact
     check and report its output verbatim:
       python3 -c "from apps.cli.command_catalog import CATALOG,
       _is_list_command; lc = [c for c in CATALOG if
       _is_list_command(c)]; print(len(lc)); missing = {c.command_id:
       sorted({'--sort','--since','--until','--limit'} - {a.name for a
       in c.args}) for c in lc}; print({k: v for k, v in
       missing.items() if v})"
     The count must be 28 and the missing-flags dict must be empty.
     `python3 -m py_compile apps/cli/command_catalog.py
     tests/test_command_catalog.py` -> exit 0 for both, reported
     separately.
  G4 THE NEW TESTS, BEFORE AND AFTER. Report
     `python3 -m pytest tests/test_command_catalog.py -q` run once
     BEFORE C2 (base count) and once AFTER C2 (must be base + 3, all
     passing - a MOVED count is the goal of this gate, not a finding).
  G5 THE MUTATION RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY,
     NEVER IN THE PRIMARY CHECKOUT. Create a throwaway worktree at HEAD
     after C2 is committed. Inside it only: edit
     `apps/cli/command_catalog.py` to remove `_LIST_UNTIL_ARG` from the
     `_LIST_OPTION_ARGS` tuple (four entries instead of five), then run
     `python3 -m pytest
     tests/test_command_catalog.py::TestListCommandOptions -q` and
     report the failure - it must name `--until` as missing across
     every list command's assertion message, not merely fail silently.
     Then revert the edit inside the worktree and re-run the same
     command, reporting a clean pass again. Remove the worktree by its
     exact path (`git worktree remove <path>`) before C3, and report
     `git worktree list` afterward showing only the primary checkout.
  G6 THE FULL SUITE, THE REVIEWER'S BASELINE ALREADY TAKEN. Run
     `python3 -m pytest -n auto -q` once, after C2, in the primary
     checkout (worktree already removed). Report the final summary line
     verbatim. The reviewer's own pre-round baseline is 19601 passed,
     23 skipped, 1 warning - report this round's numbers beside it and
     name any difference explicitly; do not silently explain one away.
  G7 THE PLAN. Extract PLAN3 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G8 THE TREE, THE COMMITS AND THE SWEEP. `git status --porcelain`
     immediately before C4 is staged -> empty. `git ls-files
     .remedy-wt` -> no output. For C0a, C0b, C1, C2 and C3 (every commit
     before the handback), report each one's insertion count from
     `git show --numstat`, the '+' column only, compared cell by cell
     against the handback's Commits table. Then the staleness sweep,
     one line per file this round touched.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. SESSION
  1, ROUND 2 of F262. Item-status table with every ordered item (C0a
  through C4, G1 through G8) exactly once, Commits table, one line per
  gate followed by its real transcript, Deviations (apply anything that
  looks wrong exactly as specified and declare it - never silently
  correct the block), Next (round 3 is T002).

SLICES. Each slice lies between its own one-line BEGIN and END marker,
markers excluded. The slices carried here are GATE1 and PLAN3.

<<<BEGIN GATE1>>>
Gate: R1 — the F262 R1 entry. R1 CLAIMED THE FEATURE AND SHIPPED NO CODE — the reviewer cut the branch directly by git plumbing at `7c65d9ccfb512aef1c3eea0245030647332c26ea` (PR #235's merge commit) and delegated one round: C0a save the block, C0b mirror it, C1 the plan, C2 the STATUS claim plus context, C3 the handback. THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: the committed `.agent/authored/f262-r1.md` cmp's identical to the reviewer's own pre-round scratchpad `.remedy-wt/f262-r1-block.txt` (exit 0, zero bytes of difference), and `.agent/authored/f262-r1.md`/`.agent/last_block.md` share one sha256 digest, `2823aa0182b4f27f0bb10222c0658dd520b74163333114d2bab7dc280bdb7bb3`, over 242 lines. THE SLICES APPLIED BYTE FOR BYTE: `.agent/plan.md` at `31ecf29923543f6fc9a6edb5606201f19f7cb509` equals PLAN1 exactly at 41 lines, `^## Goal$` 1, `^## Next Steps$` 1, last byte `2e` not `0a`; `.agent/context.md` at `7ebdf78e556301ef12b0bbfe6832308ab7581fc4` equals CONTEXT1 exactly, `^## Active Branch$` 1, `^## Steps$` 1, `feature/` count 1, first `F` plus three digits matching `F262`, `pytest` present True, last byte `2e` not `0a`. THE STATUS PAIR IS A REWRITE, VERIFIED NOT ASSERTED: FROM count 1 to 0, TO count 0 to 1, `TO contains FROM: False`. THE SEVEN SUITES ARE THE REVIEWER'S OWN, run serially both BEFORE delegating this round (the base reading) and again independently after C3, every one a REAL exit 0 and IDENTICAL both times: `tests/docs/` 295, `test_roadmap_index` 30, `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42 — a round that shipped no test and no production code moved nothing. HYGIENE HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and the four content commits' insertion counts — 242, 221, 29, and 36 plus 1 across two files — match the handback's Commits table cell for cell, each measured independently via `git show --numstat` on `fd661a857540f937eeb5de6ed01427a3d472ef18`, `e261acbdd4e905f82d6ad2f769257c9b0668d960`, `31ecf29923543f6fc9a6edb5606201f19f7cb509` and `7ebdf78e556301ef12b0bbfe6832308ab7581fc4`. THE PUSH DISCHARGED — `git ls-remote origin refs/heads/feature/f262-list-commands-v2` and the local `git rev-parse HEAD` both read `9d15b7f2a23fb7234d7e2f33f043689363050eeb`, `gh pr list --state open` printed `[]`, and nothing was created or merged; the branch carries R1 unmerged. THE THREE DECLARED DEVIATIONS ARE ALL TOOLING, NONE A DEFECT ON DISK: scratch written under `.remedy-wt/` in place of `/tmp` (sandbox denial, same bytes either way), `git show --numstat` used throughout in place of `git commit`'s own rewrite-detected stat line for whole-file rewrites, and several compound Bash one-liners rejected by the sandbox and re-expressed as single unchained invocations — all three declared before review, none touching a committed byte. THE VERDICT IS PASS.
<<<END GATE1>>>

<<<BEGIN PLAN3>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 2, session 1 — T001 ships: the shared listing-option surface
attached to every list-shaped catalog command by construction
(`apps/cli/command_catalog.py`, `_with_list_options`), plus a
catalog-derived coverage test. The flags parse everywhere now; no
store's OUTPUT changes yet — that is T002/T003.

## Next Steps

- Round 3 (T002): audit which stores already record CREATED/UPDATED,
  surface both on every list row; an unknown date renders as unknown,
  never invented. Widest slice — plan the commit split before starting.
- T003: the behaviour behind the four flags (per-command `--sort`
  choices, `--since`/`--until` parsing, `--limit`, newest-first default)
  now that T001's flags exist to carry it.

## Risks

- T001 leaves the flags accepted but inert everywhere except
  `event.list`'s pre-existing `--since`/`--limit`, kept as-is rather
  than replaced to avoid an argparse collision (see round 2's handback).
- The mechanical rule catches 28 commands; `snapshot list-applies`
  (starts with, not ends with, `list`) is excluded — round 3 states
  whether it belongs, explicitly, rather than widening the rule.
<<<END PLAN3>>>
