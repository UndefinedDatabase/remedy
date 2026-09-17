# F281 Round 4 — step block

## Goal

Book round 3's PASS, and clear the full "Order" bucket (via one shared
constant fixing 12 of its occurrences at once) plus the full reachable
"Task" bucket (8 of 9 — `stats.bench`'s own Order/Run violations use "order"
in an unrelated mathematical sense and are left open, noted below) — 22
total violations cleared, zero introduced, pre-verified against the real
`tests/docs/test_vocabulary.py` functions.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r4.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD3 + PLAN4 — one commit.
C2: CODE — 9 catalog text edits in `apps/cli/command_catalog.py`.
C3: HANDBACK.

## C1 — RECORD3 + PLAN4

### RECORD3 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F281 R3 — the F281 round 3 entry. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `b0fdf0f4`..`2318dba4` (commits `d724af14`, `54459a06`, `9e2e0e6e`, `ea111204`, `2318dba4`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r3.md` and `.agent/last_block.md` are byte-identical to the reviewer's own authored block, sha256 `1a6f5de8bb29e99fe0d5628a10b09186f6dea49dc0de5f3c50ccb78e63843397`, 11187 bytes, reproduced directly. THE CODE, reproduced by `git show ea111204`: all 5 FROM/TO edits landed exactly as ordered, including both identical `decision_id` ArgDef occurrences (`decision.show` and `decision.resolve`); `decision.resolve`'s own description line, not in scope, is byte-unchanged. THE MEASUREMENT, reproduced directly at HEAD against the real, committed catalog (no monkeypatching): `_meaning_violations()` reads 267, `_synonym_offenders()` reads 2 — both exactly matching the block's own prediction (275→267, 8 fixed, 0 introduced). THE GATES, reproduced directly: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` reads `74 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `python3 -m ruff check apps/cli/command_catalog.py` reads `All checks passed!`. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `2318dba4` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every byte independently reproduces and the vocabulary-function measurement matches exactly.
```

### PLAN4 — replace the entire content of `.agent/plan.md` with exactly:

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

ROUND 4. C1 books round 3's PASS and re-points `.agent/plan.md`. C2 clears the
full "Order" bucket in one edit (the shared `_LIST_DESC_ARG` constant's help
text, referenced by all 12 `--desc` list-sort flags, fixes all 12 occurrences
at once — a stronger leverage point than the per-command edits every prior
round used) plus 8 of the 9 "Task" bucket violations (`brain.continue
--task-type`, `job.context --task` via the shared `_TASK_OPT` constant,
`job.run --max-rounds`, `job.run --repair-rounds`, `job.show --full`,
`job.context`'s own description, `mission.continue`'s own description,
`self.execute --job-id`, `self.execute proposed_task_id`) — 22 total
(1 shared-constant Order fix covering 12 sites, plus 9 Task-word edits,
plus one more the diff found as a side effect), zero introduced.

`command:stats.bench:description`'s Order AND Run violations are DELIBERATELY
LEFT OPEN this round: its text — "a regression warning naming the order and
both numbers" — uses "order" in the sense of a trend/regression's
mathematical order (its degree), not DECISION amend0905-vocab D1's Order
concept (what the human gave Remedy), and "runs" the same way ("the last
run" is a bench execution, correctly the Run concept, but "Never runs the
bench" is a verb use with no natural home for a fragment). Forcing either
concept's fragment into a sentence about regression math would misdescribe
the command. This is the same class of finding as DECISION F281 D2's two
floor items — a genuine word-sense collision — but is NOT yet formalized as
its own DECISION; a future round either writes one (accepting `stats.bench`
as a second permanent floor item, or finding an honest rewording this
session didn't) or clears it with a rewrite that actually works.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 5;
   expected counts after this round: Task 0 or 1 (`stats.bench` may remain),
   Order 0 or 1 (`stats.bench`'s own Order violation, same caveat), Evidence
   12, Mission 16, Run ~29 (stats.bench's Run violation may still count),
   Project 65, Job ~120 — 245 total (measured directly by this round's own
   dry run; re-measure rather than trust this arithmetic). Take the
   next-smallest bucket.
2. When a bucket's violations share a single catalog-module CONSTANT (like
   `_LIST_DESC_ARG` or `_TASK_OPT` this round), fixing the constant once
   clears every command that references it — check for this BEFORE writing
   N per-command edits; it is faster and structurally guarantees no site is
   missed or drifts from its siblings.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly a third if
   `stats.bench` becomes one), and the README quickstart's R-0895 line
   remain entirely undone.

## Risks

- Same as rounds 2-3: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- A word can appear in the catalog in a sense DECISION amend0905-vocab D1
  does not define (`stats.bench`'s mathematical "order"; possibly others
  waiting in the Job/Project/Run buckets, which are large enough that a
  false-positive-sense collision is likely) — when a fragment cannot be
  added without misdescribing the command, the violation is LEFT OPEN and
  named, never forced.
```

## C2 — CODE (9 catalog text edits, all in `apps/cli/command_catalog.py`)

Apply each FROM → TO pair below EXACTLY. Every FROM string must appear
verbatim, once, at the cited location; if it does not match, STOP and report
the exact mismatch.

1. The shared `_LIST_DESC_ARG` constant (near line 2191-2193, referenced by
all 12 `--desc` list flags — editing it once fixes every site). FROM:
```
_LIST_DESC_ARG = ArgDef(
    "--desc", "Reverse the sort order",
    required=False, is_option=True, is_flag=True)
```
TO:
```
_LIST_DESC_ARG = ArgDef(
    "--desc", "Reverse the sort direction",
    required=False, is_option=True, is_flag=True)
```

2. The shared `_TASK_OPT` constant (near line 155-157, referenced by
`job.context`'s `--task` argument). FROM:
```
_TASK_OPT = ArgDef(
    "--task", "Task to select: planned id (T001) or task-id prefix",
    required=False, is_option=True)
```
TO:
```
_TASK_OPT = ArgDef(
    "--task", "Task to select from the job plan: planned id (T001) or task-id prefix",
    required=False, is_option=True)
```
(The comment at line 165, `#: \`_TASK_OPT\`, which promises "planned id (T001) or task-id prefix":`, is UNCHANGED — its quoted phrase is still a literal substring of the new text, so it stays truthful.)

3. `brain.continue`'s `--task-type` ArgDef (near line 749). FROM:
```
            ArgDef("--task-type", "Task type for the child job", required=False, is_option=True),
```
TO:
```
            ArgDef("--task-type", "Task type for the child job's next step", required=False, is_option=True),
```

4. `job.run`'s `--max-rounds` ArgDef (near line 1609). FROM:
```
            ArgDef("--max-rounds", "Max ping-pong rounds per task (default: 3, persisted on continuation)", required=False, is_option=True, default=None),
```
TO:
```
            ArgDef("--max-rounds", "Max ping-pong rounds per task's run (default: 3, persisted on continuation)", required=False, is_option=True, default=None),
```

5. `job.run`'s `--repair-rounds` ArgDef (near line 1610). FROM:
```
            ArgDef("--repair-rounds", "Max repair attempts per task (default: 2, 0=disabled, persisted on continuation)", required=False, is_option=True, default=None),
```
TO:
```
            ArgDef("--repair-rounds", "Max repair attempts per task's run (default: 2, 0=disabled, persisted on continuation)", required=False, is_option=True, default=None),
```

6. `job.show`'s `--full` ArgDef (near lines 247-250, a 3-line string
concatenation — match the exact three source lines including their
indentation). FROM:
```
            ArgDef("--full", "Print every finding of a blocked task instead of the first ten, "
                   "and the job's sections (its permissions, fences, assumptions, "
                   "completion digest, summary, status, report and Definition of Done)",
                   required=False, is_option=True, is_flag=True),
```
TO:
```
            ArgDef("--full", "Print every finding of a blocked task — a step in the job's plan — "
                   "instead of the first ten, and the job's sections (its permissions, fences, "
                   "assumptions, completion digest, summary, status, report and Definition of Done)",
                   required=False, is_option=True, is_flag=True),
```

7. `job.context`'s own description (near lines 366-367, a 2-line
parenthesized string). FROM:
```
        description=("Show the compiled context for one task — what it "
                     "receives and what was omitted (F107)."),
```
TO:
```
        description=("Show the compiled context for one task in the job plan "
                     "— what it receives and what was omitted (F107)."),
```

8. `mission.continue`'s own description (near line 955). FROM:
```
        description="Add the next job to a mission — its plan always begins with a task that verifies the previous job's Definition of Done.",
```
TO:
```
        description="Add the next job to a mission — its plan always begins with a task (a step) that verifies the previous job's Definition of Done.",
```

9. `self.execute`'s two ArgDefs (near lines 1931-1932 — both edits are in the
same CommandEntry, apply both). FROM:
```
            ArgDef("proposed_task_id", "Approved self-dogfood proposed task id"),
            ArgDef("--job-id", "Job that owns the proposed task", required=False, is_option=True),
```
TO:
```
            ArgDef("proposed_task_id", "Approved self-dogfood proposed task id (a step awaiting execution)"),
            ArgDef("--job-id", "Job that owns the proposed task (a step in its plan)", required=False, is_option=True),
```

## Constraints

- `command:stats.bench:description` is UNCHANGED this round — do not attempt
  to fix its Order/Run violations; PLAN4 explains why.
- The C2 commit's path set is exactly one file:
  `apps/cli/command_catalog.py`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.

## Gates (at most six; run and record real exit codes)

- G1 VIOLATION DIFF: import `tests.docs.test_vocabulary` and report
  `_meaning_violations()` and `_synonym_offenders()` against the real,
  committed (post-edit) catalog. Expect meaning violations to read 245,
  synonym offenders unchanged at 2. If it doesn't read exactly 245, STOP and
  report before committing (you may `git stash` your C2 edit to measure the
  before-count as 267 for confidence, then restore).
- G2 TARGETED: `python3 -m pytest tests/docs/test_vocabulary.py
  tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` —
  expect 74 passed, unchanged.
- G3 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect 42
  passed, unchanged.
- G4 RUFF: `python3 -m ruff check apps/cli/command_catalog.py` reads `All
  checks passed!`.
- G5 SWEEP: `grep -c '"Reverse the sort order"' apps/cli/command_catalog.py`
  reads 0; `grep -c '"--desc", "Reverse the sort direction"'
  apps/cli/command_catalog.py` reads 1 (the one shared constant).
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

No mutation red-proof is ordered this round, for the same reason rounds 2-3
named: G1's own before/after diff against the real vocabulary-check functions
is the red/green proof for a prose-only catalog edit.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output, G1's delta matching exactly (267→245); the branch
is pushed; `.agent/handoff.md` is rewritten as C3 naming this round, its
commits, its verification results, and the next expected action (round 5
re-measures the remaining ~245 violations by word and takes the
next-smallest bucket per PLAN4's "Next Steps").
