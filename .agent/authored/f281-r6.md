# F281 Round 6 — step block

## Goal

Book round 5's PASS, and clear the full "Mission" bucket (16 of 16) — the
last bucket before Order (already reduced to the one `stats.bench`
word-collision), leaving only Run/Project/Job as the three large remaining
buckets. Zero introduced, pre-verified against the real
`tests/docs/test_vocabulary.py` functions.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r6.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD5 + PLAN6 — one commit.
C2: CODE — 10 catalog text edits in `apps/cli/command_catalog.py` (one of
which, the shared literal `ArgDef("mission_id", "Mission id (or a unique
prefix)")`, appears 8 times and is replaced at all 8 sites with the same new
text — a global find-and-replace of that one exact string, not 8 separate
edits).
C3: HANDBACK.

## C1 — RECORD5 + PLAN6

### RECORD5 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F281 R5 — the F281 round 5 entry. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `4297a267`..`78d32152` (commits `04e27be3`, `68f1bf20`, `08d421d0`, `5ba830cc`, `78d32152`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r5.md` and `.agent/last_block.md` are byte-identical to the reviewer's own authored block, sha256 `a5a546865db909447a9fe3f09db329b2099ae4d0c167e92e6c64c0f257a2ddda`, 11968 bytes, reproduced directly. THE CODE, reproduced by `git show 5ba830cc`: all 12 FROM/TO edits landed exactly as ordered, including the 3-line `stats.verify-ledger` description concatenation. THE MEASUREMENT, reproduced directly at HEAD against the real, committed catalog: `_meaning_violations()` reads 232, `_synonym_offenders()` reads 2 — both exactly matching the block's own prediction (245→232, 13 fixed, 0 introduced). THE GATES, reproduced directly: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` reads `74 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `python3 -m ruff check apps/cli/command_catalog.py` reads `All checks passed!`. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `78d32152` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every byte independently reproduces and the vocabulary-function measurement matches exactly.
```

### PLAN6 — replace the entire content of `.agent/plan.md` with exactly:

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

ROUND 6. C1 books round 5's PASS and re-points `.agent/plan.md`. C2 clears the
full "Mission" bucket (16 of 16): 8 identical `mission_id` ArgDefs (abandon,
achieve, continue, pause, plan, resume, show, watchdog — one global
find-and-replace of the shared literal string), `mission.handoff`'s own
distinct `mission_id` ArgDef, `mission.run`'s `run_id` ArgDef,
`mission.start`'s `goal` ArgDef, and 5 command descriptions (`mission.handoff`,
`mission.pause`, `mission.resume`, `mission.run`, `mission.watchdog`).

After this round: Order reads 1 (`stats.bench`, unfixed per round 4's note),
Mission and Task and Evidence and Decision all read 0. Only Run, Project and
Job remain — the three largest buckets, ~29, 65 and 120 respectively before
this round's own measurement (which touches none of them directly, though
`mission.run` and `mission.watchdog`'s Run-fragment satisfaction was already
in place from round 3, so no cascade is expected here — confirm at round 7's
start).

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 7;
   expected: Run, Project, Job are the only three buckets left, at
   approximately 216 total (232 minus this round's 16 — re-measure rather
   than trust). Job (~120) is by far the largest; Project (~65) and Run
   (~29-30) are next. Given their size, a future round should look for
   shared constants (as `_LIST_DESC_ARG`/`_TASK_OPT`/the `mission_id` literal
   already proved out) before writing many per-command edits — grep for the
   most-repeated exact help strings among the violations first.
2. This session (session 1 of F281) has now run 6 delegated rounds, inside
   the operator's 6-to-8 target. The session's own honest assessment governs
   whether it continues or ends with a handoff; either is a legitimate
   outcome per the protocol, not a fixed count.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.

## Risks

- Same as rounds 2-5: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The Job bucket (~120, by far the largest) likely contains many shared
  constants and many genuinely distinct descriptions; it will need several
  rounds and careful checking for the "fragment is itself a binding word"
  and "same word, different sense" traps this feature has already found
  twice.
```

## C2 — CODE (10 catalog text edits, all in `apps/cli/command_catalog.py`)

Apply each FROM → TO pair below EXACTLY. Every FROM string must appear
verbatim at the cited location(s) and occurrence count; if it does not
match, STOP and report the exact mismatch.

1. The shared literal `ArgDef("mission_id", "Mission id (or a unique
prefix)"),` — appears EXACTLY 8 TIMES in the file (inside the
`mission.abandon`, `mission.achieve`, `mission.continue`, `mission.pause`,
`mission.plan`, `mission.resume`, `mission.show` and `mission.watchdog`
CommandEntries). Replace ALL 8 occurrences with the same new text — a
global find-and-replace of this one exact string, not 8 separate located
edits. FROM (all 8 occurrences):
```
            ArgDef("mission_id", "Mission id (or a unique prefix)"),
```
TO (all 8 occurrences):
```
            ArgDef("mission_id", "Mission id (or a unique prefix) that owns the jobs"),
```

2. `mission.handoff`'s own `mission_id` ArgDef (near line 902 — the ONLY
occurrence of this shorter text, distinct from edit 1's 8 identical sites).
FROM:
```
            ArgDef("mission_id", "Mission id"),
```
TO:
```
            ArgDef("mission_id", "Mission id that owns the jobs"),
```

3. `mission.run`'s `run_id` ArgDef (near line 872). FROM:
```
            ArgDef("run_id", "Mission id (F070 orchestrator)"),
```
TO:
```
            ArgDef("run_id", "Mission id (F070 orchestrator) that owns the jobs"),
```

4. `mission.start`'s `goal` ArgDef (near line 934). FROM:
```
            ArgDef("goal", "The persistent goal this mission exists for"),
```
TO:
```
            ArgDef("goal", "The persistent goal this mission exists for, before any job is created"),
```

5. `mission.run` CommandEntry description (near line 869). FROM:
```
        description="Run the F070 orchestrator for one mission. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
```
TO:
```
        description="Run the F070 orchestrator for one mission's jobs. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
```

6. `mission.watchdog` CommandEntry description (near line 885). FROM:
```
        description="Evaluate a mission's autonomy tripwires and report what fired, with the run's evidence behind it — read-only: it pauses nothing and answers no decision.",
```
TO:
```
        description="Evaluate a mission's autonomy tripwires over its jobs and report what fired, with the run's evidence behind it — read-only: it pauses nothing and answers no decision.",
```

7. `mission.handoff` CommandEntry description (near line 899). FROM:
```
        description="Compose this mission's handoff artifact — dossier, checkpoint reference, open decisions and next intent — so a fresh context can resume from it (F079).",
```
TO:
```
        description="Compose this mission's handoff artifact — dossier, checkpoint reference, open decisions, next intent and its jobs — so a fresh context can resume from it (F079).",
```

8. `mission.pause` CommandEntry description (near line 1029). FROM:
```
        description="Mark a mission paused — the goal still stands, work on it does not.",
```
TO:
```
        description="Mark a mission paused — the goal still stands, work on its jobs does not.",
```

9. `mission.resume` CommandEntry description (near line 1043). FROM:
```
        description="Mark a mission active again — the pause is lifted; the tripwire that caused it is not cleared.",
```
TO:
```
        description="Mark a mission active again — the pause on its jobs is lifted; the tripwire that caused it is not cleared.",
```

(Edits 5-9 are five separate single-line edits; edits 1-4 are ArgDef edits;
total 9 distinct FROM/TO pairs, edit 1 applying at 8 sites, giving 16 lines
touched in total across 9 pairs.)

## Constraints

- `command:stats.bench:description` stays UNCHANGED (still the word-sense
  collision round 4 named; not part of this round's scope).
- The C2 commit's path set is exactly one file:
  `apps/cli/command_catalog.py`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.

## Gates (at most six; run and record real exit codes)

- G1 VIOLATION DIFF: import `tests.docs.test_vocabulary` and report
  `_meaning_violations()` and `_synonym_offenders()` against the real,
  committed (post-edit) catalog. Expect meaning violations to read 216,
  synonym offenders unchanged at 2. If it doesn't read exactly 216, STOP and
  report before committing (you may `git stash` your C2 edit to confirm the
  before-count reads 232, then restore).
- G2 TARGETED: `python3 -m pytest tests/docs/test_vocabulary.py
  tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` —
  expect 74 passed, unchanged.
- G3 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect 42
  passed, unchanged.
- G4 RUFF: `python3 -m ruff check apps/cli/command_catalog.py` reads `All
  checks passed!`.
- G5 SWEEP: `grep -c 'Mission id (or a unique prefix)"' apps/cli/command_catalog.py`
  reads 0 (all 8 replaced); `grep -c 'that owns the jobs' apps/cli/command_catalog.py`
  reads 10 (8 from edit 1 + 1 from edit 2 (`mission.handoff`) + 1 from edit 3
  (`mission.run`'s `run_id`); none of the 5 description edits (5-9) use that
  exact phrase — recount if it doesn't match 10 and report the actual number
  rather than forcing it).
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

No mutation red-proof is ordered this round, for the same reason rounds 2-5
named: G1's own before/after diff against the real vocabulary-check functions
is the red/green proof for a prose-only catalog edit.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output, G1's delta matching exactly (232→216); the branch
is pushed; `.agent/handoff.md` is rewritten as C3 naming this round, its
commits, its verification results, and the next expected action (round 7
re-measures the remaining ~216 violations by word — Run, Project and Job are
the only buckets left).
