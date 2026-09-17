# F281 Round 3 — step block

## Goal

Book round 2's PASS, and clear the full "Decision" meaning-violation bucket (6
of 6) plus two side-effect fixes (`patch.approve-hunks`'s Job violation,
`mission.watchdog`'s Evidence violation) that landed on the same descriptions
— 8 total violations cleared, zero introduced, verified against the real
`tests/docs/test_vocabulary.py` functions before authoring.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r3.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD2 + PLAN3 — one commit.
C2: CODE — the 5 catalog text edits in `apps/cli/command_catalog.py`.
C3: HANDBACK.

## C1 — RECORD2 + PLAN3

### RECORD2 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F281 R2 — the F281 round 2 entry. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `01fb61d1`..`b0fdf0f4` (commits `6f2cc453`, `ad4ede85`, `2920f75a`, `2241bc79`, `b0fdf0f4`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r2.md` and `.agent/last_block.md` are byte-identical to the reviewer's own authored block, sha256 `d39ff134e77b1e69acdac7042d0e9c7f63d2c5525bdce8c0863a489c5f0748eb`, 21967 bytes, reproduced directly by `cmp` and `sha256sum`. THE RECORD: `Gate: F281 R1` and DECISION F281 D2 are present verbatim in `.agent/live_review.md` and `.agent/decisions.md`, reproduced by `git show 2920f75a`. THE CODE, reproduced by `git show 2241bc79`: all 18 FROM/TO edits landed exactly as the block ordered, at the exact lines named (the `do.run`-scoped `--dry-run` ArgDef and the `self.plan`-scoped `--job-id` ArgDef, not their same-named siblings elsewhere), `dev.agent-loop`'s command_id and `--fixture-builder`'s `repair-loop` value both byte-unchanged. THE MEASUREMENT, reproduced directly at HEAD by importing `tests.docs.test_vocabulary` and calling its own `_synonym_offenders()`/`_meaning_violations()` against the real, committed catalog (no monkeypatching): synonym offenders read 2 (`arg:do.run:--fixture-builder:description`, `command:dev.agent-loop:command_id`), meaning violations read 275 — both exactly matching the block's own G1 prediction (6→2, 294→275, zero introduced). THE GATES, reproduced directly: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` reads `74 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `grep -n "F070 orchestrator loop\|repair-loop\|dev.agent-loop" apps/cli/command_catalog.py` reads exactly two lines, the untouched `--fixture-builder` ArgDef and the untouched `dev.agent-loop` command_id — no surviving "F070 orchestrator loop" text; `python3 -m ruff check apps/cli/command_catalog.py` reads `All checks passed!`. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `b0fdf0f4` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every byte independently reproduces, the vocabulary-function measurement (not a hand grep) is the strongest available proof for an 18-site prose rewrite, and it matches exactly.
```

### PLAN3 — replace the entire content of `.agent/plan.md` with exactly:

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

ROUND 3. C1 books round 2's PASS and re-points `.agent/plan.md`. C2 clears the
full "Decision" meaning-violation bucket (6 of 6: `group:decision:description`,
`command:decision.show:description`, both `decision_id` ArgDefs of
`decision.show`/`decision.resolve`, `command:patch.approve-hunks:description`,
`command:mission.watchdog:description`) plus two side-effect fixes that landed
on the same two multi-violation descriptions (`patch.approve-hunks`'s Job
violation, `mission.watchdog`'s Evidence violation) — 8 total, zero
introduced, pre-verified against the real `_meaning_violations()`/
`_synonym_offenders()` functions before authoring.
`mission.watchdog`'s OWN Mission violation is deliberately left open this
round: its only three meaning fragments (`order`, `job`, `contract`) are
THEMSELVES binding words needing their own fragment nearby, so naming any of
them bare would trade one violation for another (measured directly: an
earlier draft using "against its contract" introduced a new Contract
violation) — it stays in the Mission bucket for a round that can afford a
longer rewrite bringing a fragment's own fragment along with it.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 4;
   expected counts after this round: Decision 0 (was 6), Evidence 12 (was
   13), Job 121 (was 122), Mission 16 (unchanged), Order 14, Run 30, Task 9,
   Project 65 — 267 total. Take the next-smallest bucket (Task, 9, unless a
   fresh measurement disagrees).
2. The "fragment is itself a binding word" trap (this round's own finding,
   above) applies whenever a rewrite reaches for Mission's, Job's or Run's own
   fragment list, since each of those three lists is built entirely or partly
   from other binding words (Mission: order/job/contract; Job: mission/
   budget/fence/task; Run: task/evidence) — always re-run the before/after
   diff against the real catalog functions, never assume a single targeted
   fix is isolated.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor), and the README
   quickstart's R-0895 line remain entirely undone.

## Risks

- Same as round 2's: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced, never just checked for the one word first targeted.
```

## C2 — CODE (the 5 catalog text edits, all in `apps/cli/command_catalog.py`)

Apply each FROM → TO pair below EXACTLY. Every FROM string must appear
verbatim at the cited location before editing; if it does not match, STOP
and report the exact mismatch.

1. Line 112 (GROUPS["decision"], appears exactly once in the file). FROM:
```
    "decision": GroupDef("decision", "Decision", "Human decision queue."),
```
TO:
```
    "decision": GroupDef("decision", "Decision", "The queue of decisions Remedy cannot answer for itself."),
```

2. `patch.approve-hunks` CommandEntry description (near line 559, appears
exactly once). FROM:
```
        description="Record a hunk-level approve and reject decision over a job's diff.",
```
TO:
```
        description="Record a hunk-level approve-or-reject answer over one of a job's tasks.",
```

3. `mission.watchdog` CommandEntry description (near line 885, appears
exactly once). FROM:
```
        description="Evaluate a mission's autonomy tripwires and report what fired, with the evidence behind it (read-only: it pauses nothing and raises no decision).",
```
TO:
```
        description="Evaluate a mission's autonomy tripwires and report what fired, with the run's evidence behind it — read-only: it pauses nothing and answers no decision.",
```

4. `decision.show` CommandEntry description (near line 1453, appears exactly
once — do not confuse with `decision.resolve`'s own description two entries
below, which is untouched). FROM:
```
        description="Show a single decision by ID.",
```
TO:
```
        description="Show a single decision — its question and answer, if any.",
```

5. The `decision_id` ArgDef help text — appears EXACTLY TWICE, byte-identical,
once inside `decision.show` (near line 1457) and once inside `decision.resolve`
(near line 1470); both occurrences change to the same replacement, so a
`replace_all`/global substitution of this exact line is correct and expected
to change 2 occurrences, not 1. FROM (both occurrences):
```
            ArgDef("decision_id", "Decision ID"),
```
TO (both occurrences):
```
            ArgDef("decision_id", "ID of the decision to answer or resolve"),
```

## Constraints

- `decision.resolve`'s OWN description (`"Resolve a decision (if backed by a
  resolvable record).",` near line 1466) is UNCHANGED — it is not in this
  round's target list (it already carries no meaning violation: "resolvable"
  contains the Decision fragment "resolve").
- The C2 commit's path set is exactly one file:
  `apps/cli/command_catalog.py`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.

## Gates (at most six; run and record real exit codes)

- G1 VIOLATION DIFF: write a small Python script importing
  `tests.docs.test_vocabulary` (no monkeypatching needed this time — measure
  the REAL committed catalog before and after the edit, e.g. by running the
  script once on the pre-edit worktree state via `git stash`/a throwaway
  branch, or simply trust the reviewer's own pre-registered expectation and
  measure only the AFTER state) and report `_meaning_violations()` and
  `_synonym_offenders()` counts. Expect: meaning violations 275 → 267 (8
  fixed, ZERO introduced), synonym offenders unchanged at 2. If the after-edit
  count doesn't read exactly 267, STOP and report before committing —
  recompute the diff against the pre-edit count you measure yourself, don't
  just trust this block's arithmetic blindly.
- G2 TARGETED: `python3 -m pytest tests/docs/test_vocabulary.py
  tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` —
  expect all pass (74, same as round 2 — no test was added or removed).
- G3 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect 42
  passed, unchanged.
- G4 RUFF: `python3 -m ruff check apps/cli/command_catalog.py` reads `All
  checks passed!`.
- G5 SWEEP: `grep -c '"Decision ID"' apps/cli/command_catalog.py` reads 0 (both
  replaced); `grep -c "Human decision queue" apps/cli/command_catalog.py`
  reads 0.
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

No mutation red-proof is ordered this round, for the same reason round 2
named: G1's own before/after diff against the real vocabulary-check functions
is the red/green proof for a prose-only catalog edit.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output, G1's delta matching exactly; the branch is pushed;
`.agent/handoff.md` is rewritten as C3 naming this round, its commits, its
verification results, and the next expected action (round 4 takes the next-
smallest remaining bucket per PLAN3's "Next Steps").
