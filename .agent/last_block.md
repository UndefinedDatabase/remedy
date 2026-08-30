── STEP T003/3 — F258 Self-use track v2 ────────────────────────
Goal: Book round 5's reviewer verdict into the ledger, then build T003
("findings flow back"): a module that reads a self-use run's own `JobPlan`
and answers its defects verbatim, for the closing session to register.

Bundle:
1. Book `Gate: F258 R5` into `.agent/live_review.md` (round 5's own verdict
   was already written by the reviewer into `.agent/handoff.md` last round;
   this round is the "first commit of the next round" amend0827 rule 1
   names to persist it into the ledger).
2. Build `packages/orchestration/self_use_findings.py` (T003): reads the
   `JobPlan` `packages.orchestration.self_use_runner.run_next_self_use_item`
   returns and answers a tuple of plain strings, one per defect, quoting the
   job's and each task's own `error` field verbatim — never inventing or
   summarizing. Ships with `tests/orchestration/test_self_use_findings.py`.
3. Wire the new module's existence into the same two docs T001 and T002
   already wired into: `docs/roadmap/STATUS_closure_protocol.md`
   precondition 6, and `docs/system/self-use-track-v1.md`.

Change: exactly these eight paths, nothing else —
  .agent/authored/f258-r6.md (new)
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  docs/roadmap/STATUS_closure_protocol.md
  docs/system/self-use-track-v1.md
  packages/orchestration/self_use_findings.py (new)
  tests/orchestration/test_self_use_findings.py (new)
  .agent/handoff.md

Constraints:
1. If anything below looks wrong, apply it as given and DECLARE the
   problem in the handoff rather than silently fixing it — the reviewer
   corrects it at the next gate.
2. Every authored artifact below has already been prepared and verified by
   the reviewer as a scratch file under the gitignored
   `.remedy-wt/f258-r6/` directory, which is part of THIS SAME checkout
   (not a separate machine — there is no paste relay this session). Copy
   each with `shutil.copyfile`, byte for byte, from the scratch path named
   below to the target path. Never retype, never re-derive.
3. `packages/orchestration/self_use_findings.py` and
   `tests/orchestration/test_self_use_findings.py` were built and verified
   by the reviewer end to end BEFORE this block was written: full test
   suite green, ruff clean, and a mutation red-proof (removing the
   `if result.error:` block) confirmed to redden EXACTLY
   `test_a_blocked_run_surfaces_the_jobs_own_error_text` and
   `test_task_order_is_preserved`, and nothing else, run inside a
   disposable worktree that has since been removed. Re-run this mutation
   red-proof yourself, in your OWN disposable worktree (never the primary
   checkout — self_drive_protocol.md G5), purging `__pycache__` first and
   running `python3 -B`, before applying the real files — it is G7 below.
4. This module reads a `JobPlan` only — it must not call `run_job`,
   `plan_next_self_use_item`, or any function that mutates a target repo
   or persists a job. It must not write to `.agent/live_review.md` or
   anything else; registering the finding stays a human/session act.
5. `.agent/plan.md` must stay under 50 lines and carry `## Goal` and
   `## Next Steps` — the copied PLAN6 slice already satisfies this;
   verify, do not re-derive.
6. Single worktree only outside your own disposable red-proof scratch
   worktree, which you create and remove within this same round. Never
   force-push. Never touch `main`. Push at the end.
7. `.agent/authored/f258-r6.md` (C0a) is a byte-exact save of THIS ENTIRE
   BLOCK (from `── STEP T003/3` down to the closing line of dashes at the
   very end) — copy it with a plain file write from what you were given,
   not a retype, and mirror it into `.agent/last_block.md` (C0b).

Authored artifacts (all under `.remedy-wt/f258-r6/`, all already on disk in
this checkout):

  PLAN6 — `.remedy-wt/f258-r6/plan6.md`
    sha256 9ae922a0910d455df0d5dba31e5e81806f9edf40262ec78a962081743d550852
    1812 bytes, 39 lines, ends with a single `\n`.
    Rewrite `.agent/plan.md` from this file (shutil.copyfile).

  RECORD6 — `.remedy-wt/f258-r6/record6.txt`
    sha256 ffec3d9dc0464eb9e410570a0abc5e7df07e13b6925ae0f3579d937b015ba1d8
    3782 bytes, one paragraph, ends with a single `\n`.
    Append to `.agent/live_review.md`: read the CURRENT file, confirm it is
    1775310 bytes and ends with exactly one `\n` (not `\n\n`) — if either
    reading differs, STOP and declare it rather than appending — then write
    `base + b"\n" + record6_bytes`.

  MODULE — `.remedy-wt/f258-r6/self_use_findings.py`
    sha256 a6cc5f502031fbd032bf0891cefb1c45af11d8e8b006ad955992041cb83b60e2
    2677 bytes. Copy to `packages/orchestration/self_use_findings.py`.

  TEST — `.remedy-wt/f258-r6/test_self_use_findings.py`
    sha256 54681ccdfaad31477820d400de85a41621a8bc955878db8d3bdfbef915203322
    3122 bytes. Copy to `tests/orchestration/test_self_use_findings.py`.

  PAIR-STATUSPROTO3 (REWRITE — TO does not contain FROM verbatim), applied
  to `docs/roadmap/STATUS_closure_protocol.md`. FROM occurs exactly once
  today; TO occurs zero times today.
    FROM:
    "feature's id in the closure commit. If the queue holds NO pending item,"
    TO:
    "feature's id in the closure commit. Before that: every string
   `packages.orchestration.self_use_findings.describe_self_use_run_defects`
   returns for the run's own `JobPlan` (F258 T003) is registered as a normal
   R-id finding in `.agent/live_review.md` under the standard rules (red-proof
   required for a repair) before the close, and the closure paragraph names
   every finding raised and whether it was repaired; an empty tuple means
   nothing to register, not that nothing was checked. If the queue holds NO
   pending item,"

  Three pairs applied to `docs/system/self-use-track-v1.md`, in this order:

  PAIR-BANNER3 (APPEND — TO contains FROM verbatim as its prefix). FROM
  occurs exactly once today; TO occurs zero times today; after applying,
  FROM still occurs once (it is now a prefix of the new sentence) and TO
  occurs exactly once.
    FROM:
    "(T002); this page's job-path and consumption sections are updated to
> match."
    TO:
    "(T002); this page's job-path and consumption sections are updated to
> match. **Update (2026-08-30, F258 round 6):**
> `packages/orchestration/self_use_findings.py` now reads a run's own
> `JobPlan` and answers its defects verbatim, for the closing session to
> register as normal findings (T003); F258's three T-slices are now all
> built."

  PAIR-MODULES2 (APPEND — TO contains FROM verbatim as its prefix). FROM
  occurs exactly once today; TO occurs zero times today; after applying,
  FROM still occurs once and TO occurs exactly once.
    FROM:
    "| `packages/orchestration/self_use_runner.py` | runs the planned item via `run_job` under a small budget, in the isolated worktree the target repo gives it. Stops at the approval gate; never promotes, never marks consumed (F258 T002). |"
    TO:
    "| `packages/orchestration/self_use_runner.py` | runs the planned item via `run_job` under a small budget, in the isolated worktree the target repo gives it. Stops at the approval gate; never promotes, never marks consumed (F258 T002). |
| `packages/orchestration/self_use_findings.py` | reads the run's own `JobPlan` and answers each defect verbatim (job- and task-level `error` fields). Registers nothing itself — the closing session mints the finding (F258 T003). |"

  PAIR-CONSUMPTION2 (REWRITE). FROM occurs exactly once today; TO occurs
  zero times today.
    FROM:
    "closure commit. An EXHAUSTED queue never blocks a feature —
the close records `self-use NONE (queue exhausted)` and proceeds, which is the
track asking for curation rather than stopping work."
    TO:
    "closure commit. Any defect the run surfaced —
`packages.orchestration.self_use_findings.describe_self_use_run_defects`
read against the run's own `JobPlan` — is registered as a normal finding
under the standard ledger rules before the close (F258 T003). An EXHAUSTED
queue never blocks a feature — the close records
`self-use NONE (queue exhausted)` and proceeds, which is the track asking
for curation rather than stopping work."

Done when (every gate below runs for real, exit codes captured, at most
eight gates per amend0827 rule 5):

G1 TRANSPORT. sha256 of the committed `packages/orchestration/self_use_findings.py`
   equals a6cc5f502031fbd032bf0891cefb1c45af11d8e8b006ad955992041cb83b60e2
   (2677 bytes); sha256 of the committed `tests/orchestration/test_self_use_findings.py`
   equals 54681ccdfaad31477820d400de85a41621a8bc955878db8d3bdfbef915203322
   (3122 bytes); both equal their `.remedy-wt/f258-r6/` originals.

G2 THE PLAN. Committed `.agent/plan.md` sha256 equals
   9ae922a0910d455df0d5dba31e5e81806f9edf40262ec78a962081743d550852, 1812
   bytes, 39 lines, carries `## Goal` and `## Next Steps`, ends with `\n`.

G3 THE RECORD APPEND. Re-measure `.agent/live_review.md` immediately before
   C2 (do not trust the number above if the file has changed): confirm
   `base_bytes + 1 + 3782 == committed_bytes` where `base_bytes` is the
   freshly-measured pre-C2 size; confirm the committed file's last
   `\n\n`-delimited unit equals RECORD6's own bytes (paragraph-order
   reading); confirm the committed file ends with exactly one `\n`. Run a
   negative control in your own disposable worktree: flip one printable
   byte inside a copy of RECORD6 and confirm the reconstruction reading
   rejects it while accepting the true original.

G4 THE LEDGER. Before C2 and after C2, count `^- R-\d+ — ` distinct ids
   (expect 317 both times, ADDED `[]`), `^Done: R-\d+` distinct ids (expect
   55 both times, ADDED `[]`), `DECISION F258 D\d+` distinct ids (expect
   `['D1','D2']` both times, ADDED `[]`), and `^Gate: F258 R\d+` lines
   (expect `['F258 R1','F258 R2','F258 R3','F258 R4']` before,
   `[...,'F258 R5']` after — ADDED exactly `['F258 R5']`).

G5 THE FOUR PROSE PAIRS. For PAIR-STATUSPROTO3 and PAIR-CONSUMPTION2: FROM
   count 1 before / 0 after, TO count 0 before / 1 after. For PAIR-BANNER3
   and PAIR-MODULES2 (both append-shaped): FROM count 1 before / 1 after
   (survives as prefix), TO count 0 before / 1 after. `python3 -m pytest
   tests/docs/ -q` REAL exit 0, expect 295 passed. `python3 -m pytest
   tests/orchestration/test_roadmap_index.py -q` REAL exit 0, expect 30
   passed.

G6 THE NEW MODULE, ITS TEST, AND THE SUITES. `python3 -m ruff check
   packages/orchestration/self_use_findings.py
   tests/orchestration/test_self_use_findings.py` REAL exit 0, "All checks
   passed!". `python3 -m pytest tests/orchestration/test_self_use_findings.py
   tests/orchestration/test_self_use_runner.py
   tests/orchestration/test_self_use_generator.py
   tests/orchestration/test_self_use_queue.py
   tests/orchestration/test_self_use_job.py -q` REAL exit 0, expect 71
   passed (3 new). `python3 -m pytest tests/test_data_paths.py
   tests/orchestration/test_development_artifact_boundary.py
   tests/test_path_utils.py -q` REAL exit 0, expect 69 passed (this new
   module touches none of their guarded paths, so this is a sanity check,
   not an expected change).

G7 THE MUTATION RED-PROOF, inside your own disposable worktree, `__pycache__`
   purged, `python3 -B`. Remove the two-line block `    if result.error:`
   through its `defects.append(...)` line in
   `packages/orchestration/self_use_findings.py`; re-run
   `tests/orchestration/test_self_use_findings.py`; expect REAL exit 1,
   EXACTLY TWO failures
   (`test_a_blocked_run_surfaces_the_jobs_own_error_text`,
   `test_task_order_is_preserved`), 1 passed. Restore the file from the
   scratch original (`shutil.copyfile` from
   `.remedy-wt/f258-r6/self_use_findings.py`); re-run; expect REAL exit 0,
   3 passed again. Remove the disposable worktree afterward; `git worktree
   list` in the primary checkout shows only the primary checkout.

G8 THE STATE READERS AND CANARY. `python3 -m pytest tests/ui_server/ -q`
   REAL exit 0, 515 passed. `python3 -m pytest
   tests/orchestration/test_test_runner.py -q` REAL exit 0, 52 passed.
   `python3 -m pytest tests/regression/test_resource_safety.py -q` REAL
   exit 0, 21 passed. `python3 -m pytest
   tests/orchestration/test_integrity_gate.py -q` REAL exit 0, 16 passed.
   Canary `python3 -m pytest tests/cli/test_golden_path.py -q` REAL exit 0,
   42 passed. `git status --porcelain` empty at the end; `git worktree
   list` shows only the primary checkout; every commit's `git diff
   --numstat` insertion total under 500.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md and self_drive_protocol.md's "Ending a
session" section — feature and round (SESSION 2 of F258, round 6), branch,
commit SHAs, the changed-files table, every gate's REAL result (one line
per gate, per checklist item 31, run each at a commit strictly before the
handoff commit), open-findings count (unchanged: 317 registered / 55
resolved / 262 open), the DECISION F258 id list (unchanged `['D1','D2']`),
and next expected action: F258's closure sequence — all three T-slices
(T001, T002, T003) are now built against the feature file's own text, so
the next round is the reviewer's own design of the closure round (evidence
job, fresh review zip, STATUS line, PR), not more T-slice work. Push
`feature/f258-self-use-v2` at the end (no force push). No PR is opened this
round — the reviewer decides closure readiness at the next round, not this
worker.
──────────────────────────────────────────────────────────────
