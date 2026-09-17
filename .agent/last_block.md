# F281 Round 5 — step block

## Goal

Book round 4's PASS, and clear the full "Evidence" bucket (12 of 12) plus one
side-effect fix (`mission.report`'s Job violation, on the same description) —
13 total violations cleared, zero introduced, pre-verified against the real
`tests/docs/test_vocabulary.py` functions.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r5.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD4 + PLAN5 — one commit.
C2: CODE — 12 catalog text edits in `apps/cli/command_catalog.py`.
C3: HANDBACK.

## C1 — RECORD4 + PLAN5

### RECORD4 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F281 R4 — the F281 round 4 entry. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `2318dba4`..`4297a267` (commits `9944f7ce`, `4036fb58`, `64aad85f`, `aa5a127e`, `4297a267`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r4.md` and `.agent/last_block.md` are byte-identical to the reviewer's own authored block, sha256 `73fa1a19a51115538008ce1b1313c31f335f4751440dbf47cb0ffb45df614a33`, 13405 bytes, reproduced directly. THE CODE, reproduced by `git show aa5a127e`: all 9 FROM/TO edits landed exactly as ordered, including the two shared constants `_LIST_DESC_ARG` (fixing all 12 of its call sites at once) and `_TASK_OPT`, whose neighbouring comment stayed byte-unchanged and still quotes a true substring of the new text. THE MEASUREMENT, reproduced directly at HEAD against the real, committed catalog: `_meaning_violations()` reads 245, `_synonym_offenders()` reads 2 — both exactly matching the block's own prediction (267→245, 22 fixed, 0 introduced). THE GATES, reproduced directly: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` reads `74 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `python3 -m ruff check apps/cli/command_catalog.py` reads `All checks passed!`. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `4297a267` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every byte independently reproduces and the vocabulary-function measurement matches exactly.
```

### PLAN5 — replace the entire content of `.agent/plan.md` with exactly:

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

ROUND 5. C1 books round 4's PASS and re-points `.agent/plan.md`. C2 clears the
full "Evidence" bucket (12 of 12: `group:stats:description`,
`group:self:description`, `arg:job.stop:--reason:description`,
`command:mission.report:description`, `command:mission.abandon:description`,
`arg:job.run:--no-stream-evidence:description`,
`arg:stats.failures:--job:description`,
`arg:stats.backfill-ledger:evidence_dir:description`,
`command:stats.verify-ledger:description`,
`arg:stats.verify-ledger:evidence_dir:description`,
`command:self.inspect:description`, `command:self.report:description`) plus
one side-effect fix (`mission.report`'s Job violation, since its rewrite
already needed the word "mission" nearby, which is one of Job's own three
fragments) — 13 total, zero introduced.

After this round the ONLY remaining Order violation is `stats.bench`'s
(unfixed, per round 4's note — mathematical "order", not the vocabulary
concept), and Task and Evidence both read zero.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 6;
   expected counts after this round: Mission 16 (unchanged — none of this
   round's fixes touched a standalone Mission violation), Order 1
   (`stats.bench`, unfixed), Run ~29-30, Project 65, Job ~120 — 232 total
   (measured directly this round; re-measure rather than trust). Take the
   next-smallest bucket (Mission, 16, unless a fresh measurement disagrees).
2. Continue watching for the "fragment is itself a binding word" trap
   (Mission's own fragments are order/job/contract — all three ARE binding
   words) and the "same word, different sense" trap (`stats.bench`'s
   mathematical order): every rewrite is checked against the FULL before/after
   diff of the real `_meaning_violations()`/`_synonym_offenders()` functions,
   never assumed safe from reading the text alone.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone. This session (session 1 of F281) has now run 5 delegated rounds,
   at the operator's 4-to-5 default and approaching the 6-to-8 target; the
   next round may be this session's last if a natural stopping point is
   reached, per a session's own honest self-assessment rather than a fixed
   count.

## Risks

- Same as rounds 2-4: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
```

## C2 — CODE (12 catalog text edits, all in `apps/cli/command_catalog.py`)

Apply each FROM → TO pair below EXACTLY. Every FROM string must appear
verbatim, once, at the cited location; if it does not match, STOP and report
the exact mismatch.

1. GROUPS["stats"] (near line 125). FROM:
```
    "stats": GroupDef("stats", "Stats", "Honest counts from the evidence on disk."),
```
TO:
```
    "stats": GroupDef("stats", "Stats", "Honest counts from the run evidence on disk."),
```

2. GROUPS["self"] (near line 135). FROM:
```
    "self": GroupDef("self", "Self", "Self-dogfood — inspect own evidence.", user_facing=False),
```
TO:
```
    "self": GroupDef("self", "Self", "Self-dogfood — inspect Remedy's own run evidence.", user_facing=False),
```

3. `job.stop`'s `--reason` ArgDef (near line 321). FROM:
```
            ArgDef("--reason", "Why the job is being stopped (recorded in the evidence)", required=False, is_option=True, default=""),
```
TO:
```
            ArgDef("--reason", "Why the job is being stopped (recorded in the run's evidence)", required=False, is_option=True, default=""),
```

4. `mission.report` CommandEntry description (near line 912). FROM:
```
        description="Read-only morning-style report built from the job's current evidence.",
```
TO:
```
        description="Read-only morning-style report for a mission, built from its job's current run evidence.",
```

5. `mission.abandon` CommandEntry description (near line 1015). FROM:
```
        description="Mark a mission abandoned — the goal is dropped; its jobs and their evidence stay.",
```
TO:
```
        description="Mark a mission abandoned — the goal is dropped; its jobs and their run evidence stay.",
```

6. `job.run`'s `--no-stream-evidence` ArgDef (near line 1614). FROM:
```
            ArgDef("--no-stream-evidence", "Explicitly disable raw stream evidence (overrides a persisted true). Omitted keeps the persisted/default mode", required=False, is_option=True),
```
TO:
```
            ArgDef("--no-stream-evidence", "Explicitly disable this run's raw stream evidence (overrides a persisted true). Omitted keeps the persisted/default mode", required=False, is_option=True),
```

7. `stats.failures`'s `--job` ArgDef (near line 1647). FROM:
```
            ArgDef("--job", "Only this job's evidence export", required=False, is_option=True),
```
TO:
```
            ArgDef("--job", "Only this job's evidence export, from its run", required=False, is_option=True),
```

8. `stats.backfill-ledger`'s `evidence_dir` ArgDef (near line 1769). FROM:
```
            ArgDef("evidence_dir", "Path to the job evidence directory to scan"),
```
TO:
```
            ArgDef("evidence_dir", "Path to the job evidence folder to scan"),
```

9. `stats.verify-ledger` CommandEntry description (near lines 1781-1785, a
3-line string concatenation). FROM:
```
        description=(
            "Reconcile the evidence files against the token ledger rows (read-only). "
            "Exits 0 on a clean reconcile and non-zero when drift is found, so it is "
            "usable as a check."
        ),
```
TO:
```
        description=(
            "Reconcile the run evidence files against the token ledger rows (read-only). "
            "Exits 0 on a clean reconcile and non-zero when drift is found, so it is "
            "usable as a check."
        ),
```

10. `stats.verify-ledger`'s `evidence_dir` ArgDef (near line 1790). FROM:
```
            ArgDef("evidence_dir", "Path to the job evidence directory to reconcile"),
```
TO:
```
            ArgDef("evidence_dir", "Path to the job evidence folder to reconcile"),
```

11. `self.inspect` CommandEntry description (near line 1887). FROM:
```
        description="Read-only: inspect Remedy's own evidence for self-improvement items.",
```
TO:
```
        description="Read-only: inspect Remedy's own run evidence for self-improvement items.",
```

12. `self.report` CommandEntry description (near line 1978). FROM:
```
        description="Read-only: self-dogfood report (what Remedy thinks is wrong + evidence).",
```
TO:
```
        description="Read-only: self-dogfood report (what Remedy thinks is wrong, with the run evidence behind it).",
```

## Constraints

- `command:stats.bench:description` stays UNCHANGED (unrelated to this
  round's scope; still the word-sense collision round 4 named).
- The C2 commit's path set is exactly one file:
  `apps/cli/command_catalog.py`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.

## Gates (at most six; run and record real exit codes)

- G1 VIOLATION DIFF: import `tests.docs.test_vocabulary` and report
  `_meaning_violations()` and `_synonym_offenders()` against the real,
  committed (post-edit) catalog. Expect meaning violations to read 232,
  synonym offenders unchanged at 2. If it doesn't read exactly 232, STOP and
  report before committing (you may `git stash` your C2 edit to confirm the
  before-count reads 245, then restore).
- G2 TARGETED: `python3 -m pytest tests/docs/test_vocabulary.py
  tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` —
  expect 74 passed, unchanged.
- G3 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect 42
  passed, unchanged.
- G4 RUFF: `python3 -m ruff check apps/cli/command_catalog.py` reads `All
  checks passed!`.
- G5 SWEEP: `grep -c 'directory to scan\|directory to reconcile'
  apps/cli/command_catalog.py` reads 0 (both became "folder").
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

No mutation red-proof is ordered this round, for the same reason rounds 2-4
named: G1's own before/after diff against the real vocabulary-check functions
is the red/green proof for a prose-only catalog edit.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output, G1's delta matching exactly (245→232); the branch
is pushed; `.agent/handoff.md` is rewritten as C3 naming this round, its
commits, its verification results, and the next expected action (round 6
re-measures the remaining ~232 violations by word and takes the
next-smallest bucket per PLAN5's "Next Steps").
