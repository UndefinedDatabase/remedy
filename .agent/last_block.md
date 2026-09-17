# F281 Round 8 — step block

## Goal

Book round 7's PASS, and clear the highest-leverage 33 of the 65 Project-
bucket violations via FOUR shared-literal edits (one constant, three
duplicated literal ArgDef strings) rather than 33 separate located edits —
the same leverage round 4 found with `_LIST_DESC_ARG` and round 6 found with
the 8 identical `mission_id` ArgDefs. Zero introduced, pre-verified in a
disposable worktree against the real `tests/docs/test_vocabulary.py`
functions before authoring.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r8.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD7 + PLAN8 — one commit.
C2: CODE — 4 FROM/TO edits in `apps/cli/command_catalog.py`, each a global
find-and-replace of one exact literal string (edit 1 replaces the shared
`_PROJECT_SCOPE_OPT` constant definition, which is referenced by 21
CommandEntries; edits 2-4 each replace a duplicated literal `ArgDef(...)`
call that appears verbatim at multiple sites — not a Python constant, just
identical text repeated by the original authors). 33 violations clear as a
result, all in the `Project` word bucket.
C3: HANDBACK.

## C1 — RECORD7 + PLAN8

### RECORD7 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F281 R7 — the F281 round 7 entry. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `cc1cd3b0`..`d21b585b` (commits `79e4d8e2`, `147fcde9`, `fcf5d0b9`, `9f799af2`, `d21b585b`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r7.md` and `.agent/last_block.md` are byte-identical to the reviewer's own authored block, sha256 `6ae5a011fc997fcf0c880c149590d10e72b204bd806a3c345bd9b33776809ca7`, 19683 bytes, reproduced directly. THE CODE, reproduced by `git show 9f799af2`: all 30 FROM/TO edits landed exactly as ordered, clearing the full Run bucket across the `ci`, `teacher` and `test` groups and the `ci.run`, `integrity.check`, `teacher.ask`, `teacher.narrate`, `test.status`, `test.result`, `test.list`, `test.run`, `mission.run`, `mission.readiness`, `run.show`, `job.resume`, `job.run`, `job.apply`, `job.evidence`, `do.run` and `stats.bench` commands. THE MEASUREMENT, reproduced directly at HEAD against the real, committed catalog: `_meaning_violations()` reads 184, `_synonym_offenders()` reads 2 — both exactly matching the block's own prediction (216→184, 32 fixed: 30 Run bucket plus 2 Job-bucket bonus fixes on `test.list` and `test.status`, 0 introduced). THE GATES, reproduced directly: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` reads `74 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `python3 -m ruff check apps/cli/command_catalog.py` reads `All checks passed!`; `grep -c '(same task as --task-id)' apps/cli/command_catalog.py` reads `2`; `grep -c 'Dry-run by default' apps/cli/command_catalog.py` reads `0`. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `d21b585b` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every byte independently reproduces and the vocabulary-function measurement matches exactly.
```

### PLAN8 — replace the entire content of `.agent/plan.md` with exactly:

```
# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request 253
(F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 once F280 has pruned and renamed the
command tree (`docs/roadmap/features/T2_F281.md`). DONE when T001 and the
Acceptance list hold.

## Current Step

ROUND 8. C1 books round 7's PASS and re-points `.agent/plan.md`. C2 clears 33
of the 65 Project-bucket violations via FOUR shared-literal edits: the
`_PROJECT_SCOPE_OPT` constant (21 call sites — `job.list`, `teacher.ask`, all
11 `mission.*` commands, and all 7 `stats.*` commands that take a `--project`
option), the "Project slug or UUID" literal (3 sites: `project.current`,
`project.attach`, `project.adopt`), the "Project UUID scope" literal (3
sites: `memory.store`, `memory.recall`, `memory.list`), and the "Project ID
scope" literal (6 sites: the six `memory.card-*` commands).

After this round: Order remains 1 (`stats.bench`, unchanged), Mission, Task,
Evidence, Decision and Run all read 0. Project drops from 65 to 32 — the
remaining text is unique per command: `do.run`'s own `--project` ArgDef,
`init.run`'s `--project-name`, most of the `project.*` group's own
descriptions and `project_id` ArgDefs, `runtime.*`'s `--repo` ArgDefs,
`brain.*`'s descriptions, `status.run`'s description, `job.list`'s own
description, `stats.backfill-ledger`'s own description, and the `brain`,
`memory`, `runtime`, `status` and `test` group descriptions. Job stays at 118
— untouched this round, still the largest remaining bucket.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 9;
   expected: Project (~32) and Job (~118) are the only two buckets left
   (plus Order's 1 unfixed `stats.bench` collision), at approximately 150-151
   total (re-measure rather than trust). Job is now by far the largest;
   continue looking for shared constants there first (the many `job_id`
   ArgDefs are the obvious candidate) before writing per-command edits.
2. This session (session 1 of F281) has now run 8 delegated rounds, at the
   TOP of the operator's 6-to-8 target (amend0905-throughput). The session's
   own honest assessment governs whether it continues (context comfortably
   sufficing) or ends with a handoff; either is legitimate.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.

## Risks

- Same as rounds 2-7: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The Job bucket (~118) likely contains many shared constants (the repeated
  `job_id`/`Job ID` ArgDefs across dozens of commands) and many genuinely
  distinct descriptions; it will need several rounds and careful checking
  for the "fragment is itself a binding word" and "same word, different
  sense" traps this feature has already found twice.
```

## C2 — CODE (4 FROM/TO edits, all in `apps/cli/command_catalog.py`)

Apply each FROM → TO pair below EXACTLY, in order. Every FROM string must
appear verbatim at the cited occurrence count; if it does not match, STOP and
report the exact mismatch rather than guessing or forcing it.

1. The shared constant definition `_PROJECT_SCOPE_OPT` (near line 191).
Appears EXACTLY ONCE as a definition (it is then referenced by name — not by
this literal text — at 21 further call sites, all of which inherit the fix
automatically). FROM:
```
_PROJECT_SCOPE_OPT = ArgDef("--project", "Scope to project (slug or UUID)", required=False, is_option=True)
```
TO:
```
_PROJECT_SCOPE_OPT = ArgDef("--project", "Scope to a project's repo (slug or UUID)", required=False, is_option=True)
```

2. The literal `ArgDef("--project", "Project slug or UUID", required=False,
is_option=True)` — appears EXACTLY 3 TIMES (inside `project.current`,
`project.attach` and `project.adopt`). Replace ALL 3 occurrences with the
same new text — a global find-and-replace, not 3 separate located edits.
FROM (all 3 occurrences):
```
            ArgDef("--project", "Project slug or UUID", required=False, is_option=True),
```
TO (all 3 occurrences):
```
            ArgDef("--project", "Project's repo, slug or UUID", required=False, is_option=True),
```

3. The literal `ArgDef("--project", "Project UUID scope", required=False,
is_option=True)` — appears EXACTLY 3 TIMES (inside `memory.store`,
`memory.recall` and `memory.list`). Replace ALL 3 occurrences. FROM (all 3
occurrences):
```
            ArgDef("--project", "Project UUID scope", required=False, is_option=True),
```
TO (all 3 occurrences):
```
            ArgDef("--project", "Project's repo, UUID scope", required=False, is_option=True),
```

4. The literal `ArgDef("--project", "Project ID scope", required=False,
is_option=True)` — appears EXACTLY 6 TIMES (inside `memory.card-show`,
`memory.card-approve`, `memory.card-reject`, `memory.card-stale`,
`memory.card-supersede` and `memory.card-contradict`). Replace ALL 6
occurrences. FROM (all 6 occurrences):
```
            ArgDef("--project", "Project ID scope", required=False, is_option=True),
```
TO (all 6 occurrences):
```
            ArgDef("--project", "Project's repo, ID scope", required=False, is_option=True),
```

(4 distinct FROM/TO pairs, touching 1 + 3 + 3 + 6 = 13 lines in total.)

## Constraints

- `command:stats.bench:description` still carries the separate, UNCHANGED
  `Order`-word violation named in round 4 — not part of this round's scope.
  This round's edits touch none of `stats.bench`'s description text (only
  its `--project` ArgDef, via edit 1's constant, is affected).
- The C2 commit's path set is exactly one file:
  `apps/cli/command_catalog.py`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.
- `do.run`'s own `--project` ArgDef ("Project ID to use or create") is a
  DIFFERENT literal text from all four edits above — do not touch it, it
  stays open for a future round.

## Gates (at most six; run and record real exit codes)

- G1 VIOLATION DIFF: import `tests.docs.test_vocabulary` and report
  `_meaning_violations()` and `_synonym_offenders()` against the real,
  committed (post-edit) catalog. Expect meaning violations to read 151
  (184 minus 33), synonym offenders unchanged at 2. If it doesn't read
  exactly 151, STOP and report before committing (you may `git stash` your
  C2 edit to confirm the before-count reads 184, then restore).
- G2 TARGETED: `python3 -m pytest tests/docs/test_vocabulary.py
  tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` —
  expect 74 passed, unchanged.
- G3 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect 42
  passed, unchanged.
- G4 RUFF: `python3 -m ruff check apps/cli/command_catalog.py` reads `All
  checks passed!`.
- G5 SWEEP: `grep -c "Scope to a project's repo (slug or UUID)"
  apps/cli/command_catalog.py` reads 1; `grep -c "Project's repo, slug or
  UUID" apps/cli/command_catalog.py` reads 3; `grep -c "Project's repo, UUID
  scope" apps/cli/command_catalog.py` reads 3; `grep -c "Project's repo, ID
  scope" apps/cli/command_catalog.py` reads 6; and `grep -c "Project slug or
  UUID\|Project UUID scope\|Project ID scope" apps/cli/command_catalog.py`
  (the three OLD literals, unanchored) reads 0.
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

No mutation red-proof is ordered this round, for the same reason rounds 2-7
named: G1's own before/after diff against the real vocabulary-check functions
is the red/green proof for a prose-only catalog edit.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output, G1's delta matching exactly (184→151, 33 fixed, 0
introduced); the branch is pushed; `.agent/handoff.md` is rewritten as C3
naming this round, its commits, its verification results, and the next
expected action (round 9 addresses the two remaining buckets: Job at ~118,
Project at ~32).
