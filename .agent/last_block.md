── STEP T002/3 — F258 Self-use track v2 ────────────────────────
Goal: Book round 4's reviewer verdict into the ledger, then build T002
("consumed means executed"): a new module that RUNS a planned self-use
item through the real job path to the normal approval gate.

Bundle:
1. Book `Gate: F258 R4` into `.agent/live_review.md` (round 4's own verdict
   was already written by the reviewer into `.agent/handoff.md` last
   session; this round is the "first commit of the next round" amend0827
   rule 1 names to persist it into the ledger).
2. Build `packages/orchestration/self_use_runner.py` (T002): composes
   `packages.orchestration.self_use_job.plan_next_self_use_item` with
   `packages.orchestration.pingpong_job.run_job` under a small
   `packages.core.models.JobBudgets`, stopping at whatever status `run_job`
   returns (`JOB_COMPLETED` or `JOB_BLOCKED`) — NEVER calling
   `packages.orchestration.job_promote.promote_job`. Ships with
   `tests/orchestration/test_self_use_runner.py`.
3. Wire the new module's existence into the same two docs T001 already
   wired the generator into: `docs/roadmap/STATUS_closure_protocol.md`
   precondition 6, and `docs/system/self-use-track-v1.md`.

Change: exactly these eight paths, nothing else —
  .agent/authored/f258-r5.md (new)
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  docs/roadmap/STATUS_closure_protocol.md
  docs/system/self-use-track-v1.md
  packages/orchestration/self_use_runner.py (new)
  tests/orchestration/test_self_use_runner.py (new)
  .agent/handoff.md

Constraints:
1. If anything below looks wrong, apply it as given and DECLARE the
   problem in the handoff rather than silently fixing it — the reviewer
   corrects it at the next gate.
2. Every authored artifact below has already been prepared and verified by
   the reviewer as a scratch file under the gitignored
   `.remedy-wt/f258-r5/` directory, which is part of THIS SAME checkout
   (not a separate machine — there is no paste relay this session). Copy
   each with `shutil.copyfile`, byte for byte, from the scratch path named
   below to the target path. Never retype, never re-derive.
3. `packages/orchestration/self_use_runner.py` and
   `tests/orchestration/test_self_use_runner.py` were built and verified by
   the reviewer end to end BEFORE this block was written: full test suite
   green, ruff clean, and a mutation red-proof (removing the
   `JOB_BLOCKED` guard) confirmed to redden EXACTLY
   `test_a_blocked_plan_raises_rather_than_running` and nothing else, run
   inside a disposable worktree that has since been removed. Re-run this
   mutation red-proof yourself, in your OWN disposable worktree (never the
   primary checkout — self_drive_protocol.md G5), purging
   `__pycache__` first and running `python3 -B`, before applying the real
   files — it is G7 below.
4. NEVER call `packages.orchestration.job_promote.promote_job` anywhere in
   the new module, its tests, or any exploration you do — the target repo
   must never be mutated by this round's own verification.
5. `.agent/plan.md` must stay under 50 lines and carry `## Goal` and
   `## Next Steps` — the copied PLAN5 slice already satisfies this;
   verify, do not re-derive.
6. Single worktree only outside your own disposable red-proof scratch
   worktree, which you create and remove within this same round. Never
   force-push. Never touch `main`. Push at the end.
7. `.agent/authored/f258-r5.md` (C0a) is a byte-exact save of THIS ENTIRE
   BLOCK (from `── STEP T002/3` down to the closing line of dashes at the
   very end) — copy it with a plain file write from what you were given,
   not a retype, and mirror it into `.agent/last_block.md` (C0b).

Authored artifacts (all under `.remedy-wt/f258-r5/`, all already on disk in
this checkout):

  PLAN5 — `.remedy-wt/f258-r5/plan5.md`
    sha256 2bee9077ba14d65ce3f19fc1872b16e1054dbd2c8101dd98a6a4d96f2acb350e
    1935 bytes, 41 lines, ends with a single `\n`.
    Rewrite `.agent/plan.md` from this file (shutil.copyfile).

  RECORD5 — `.remedy-wt/f258-r5/record5.txt`
    sha256 bee07dbf283cdfd13f056ff3956f998898591b7ada9d55054eccb3c6fa882b16
    3401 bytes, one paragraph, ends with a single `\n`.
    Append to `.agent/live_review.md`: read the CURRENT file, confirm it is
    1771908 bytes and ends with exactly one `\n` (not `\n\n`) — if either
    reading differs, STOP and declare it rather than appending — then write
    `base + b"\n" + record5_bytes`. The reviewer has independently confirmed
    this reproduces the ledger's normal `\n\n` paragraph convention (round
    4's dropped-newline defect self-healed exactly as that round's own
    verdict predicted) and that the appended paragraph is delimited on both
    sides.

  MODULE — `.remedy-wt/f258-r5/self_use_runner.py`
    sha256 77036196d3e31fdd22320b95174395c70d05d455fcfd8f6ddbeeca06dddcb0cb
    5079 bytes. Copy to `packages/orchestration/self_use_runner.py`.

  TEST — `.remedy-wt/f258-r5/test_self_use_runner.py`
    sha256 1172f6cae620f6dba4266d3b0ec1e03c6ae08993e272f6ada4de55c64d6e288d
    7110 bytes. Copy to `tests/orchestration/test_self_use_runner.py`.

  PAIR-STATUSPROTO2 (REWRITE — TO does not contain FROM verbatim), applied
  to `docs/roadmap/STATUS_closure_protocol.md`. FROM occurs exactly once
  today; TO occurs zero times today.
    FROM (verbatim, including the three leading spaces of each line):
    "   been planned through `packages.orchestration.self_use_job`, taken to the
   normal approval gate like any other job, and its `consumed_by` set to this"
    TO:
    "   been planned through `packages.orchestration.self_use_job` and RUN
   through `packages.orchestration.self_use_runner.run_next_self_use_item`
   (F258 T002) to the normal approval gate like any other job — never
   promoted — and its `consumed_by` set to this"

  Four pairs applied to `docs/system/self-use-track-v1.md`, in this order:

  PAIR-BANNER2 (APPEND — TO contains FROM verbatim as its prefix). FROM
  occurs exactly once today; TO occurs zero times today; after applying,
  FROM still occurs once (it is now a prefix of the new sentence) and TO
  occurs exactly once.
    FROM: "> the track as a whole is no longer discovery-free."
    TO:
    "> the track as a whole is no longer discovery-free. **Update (2026-08-30,
> F258 round 5):** `packages/orchestration/self_use_runner.py` now RUNS a
> planned item through the real job path (builder/reviewer loop, isolated
> worktree) under a small budget, stopping at the normal approval gate
> (T002); this page's job-path and consumption sections are updated to
> match."

  PAIR-WHYEXISTS (REWRITE). FROM occurs exactly once today; TO occurs zero
  times today.
    FROM:
    "maintenance jobs, exactly ONE of which is consumed per feature close, planned
through the job path Remedy already has and taken to the normal approval gate."
    TO:
    "maintenance jobs, exactly ONE of which is consumed per feature close, planned
through the job path Remedy already has and RUN through it — builder/reviewer
loop, isolated worktree, small budget — to the normal approval gate (F258
T002)."

  PAIR-MODULES (REWRITE — the whole heading+table structure, per the arity
  rule: adding a table row spans the WHOLE table, not a prefix of it).
  FROM occurs exactly once today; TO occurs zero times today.
    FROM:
    "## The two modules

| Module | Role |
|--------|------|
| `packages/orchestration/self_use_queue.py` | the READ side — loads, validates, answers the next pending item. Owns no writer. |
| `packages/orchestration/self_use_job.py` | renders one item to `<dest_dir>/<id>.md` and plans it via `plan_job_from_file`. Plans only; never runs, never promotes. |"
    TO:
    "## The self-use modules

| Module | Role |
|--------|------|
| `packages/orchestration/self_use_queue.py` | the READ side — loads, validates, answers the next pending item. Owns no writer. |
| `packages/orchestration/self_use_job.py` | renders one item to `<dest_dir>/<id>.md` and plans it via `plan_job_from_file`. Plans only; never runs, never promotes. |
| `packages/orchestration/self_use_runner.py` | runs the planned item via `run_job` under a small budget, in the isolated worktree the target repo gives it. Stops at the approval gate; never promotes, never marks consumed (F258 T002). |"

  PAIR-CONSUMPTION (REWRITE). FROM occurs exactly once today; TO occurs
  zero times today.
    FROM:
    "is planned, taken to the approval gate, and its `consumed_by` set to the
feature's id in the closure commit."
    TO:
    "is planned, RUN through
`packages.orchestration.self_use_runner.run_next_self_use_item` (F258 T002) to
the approval gate, and its `consumed_by` set to the feature's id in the
closure commit."

Done when (every gate below runs for real, exit codes captured, at most
eight gates per amend0827 rule 5):

G1 TRANSPORT. sha256 of the committed `packages/orchestration/self_use_runner.py`
   equals 77036196d3e31fdd22320b95174395c70d05d455fcfd8f6ddbeeca06dddcb0cb
   (5079 bytes); sha256 of the committed `tests/orchestration/test_self_use_runner.py`
   equals 1172f6cae620f6dba4266d3b0ec1e03c6ae08993e272f6ada4de55c64d6e288d
   (7110 bytes); both equal their `.remedy-wt/f258-r5/` originals.

G2 THE PLAN. Committed `.agent/plan.md` sha256 equals
   2bee9077ba14d65ce3f19fc1872b16e1054dbd2c8101dd98a6a4d96f2acb350e, 1935
   bytes, 41 lines, carries `## Goal` and `## Next Steps`, ends with `\n`.

G3 THE RECORD APPEND. Re-measure `.agent/live_review.md` immediately before
   C2 (do not trust the number above if the file has changed): confirm
   `base_bytes + 1 + 3401 == committed_bytes` where `base_bytes` is the
   freshly-measured pre-C2 size; confirm the committed file's last
   `\n\n`-delimited unit equals RECORD5's own bytes (paragraph-order
   reading); confirm the committed file ends with exactly one `\n`. Run a
   negative control in your own disposable worktree: flip one printable
   byte inside a copy of RECORD5 and confirm the reconstruction reading
   rejects it while accepting the true original.

G4 THE LEDGER. Before C2 and after C2, count `^- R-\d+ — ` distinct ids
   (expect 317 both times, ADDED `[]`), `^Done: R-\d+` distinct ids (expect
   55 both times, ADDED `[]`), `DECISION F258 D\d+` distinct ids (expect
   `['D1','D2']` both times, ADDED `[]`), and `^Gate: F258 R\d+` lines
   (expect `['F258 R1','F258 R2','F258 R3']` before, `[...,'F258 R4']`
   after — ADDED exactly `['F258 R4']`).

G5 THE FIVE PROSE PAIRS. For PAIR-STATUSPROTO2, PAIR-WHYEXISTS,
   PAIR-MODULES and PAIR-CONSUMPTION: FROM count 1 before / 0 after, TO
   count 0 before / 1 after. For PAIR-BANNER2: FROM count 1 before / 1
   after (it survives as the new sentence's prefix), TO count 0 before / 1
   after. `python3 -m pytest tests/docs/ -q` REAL exit 0, expect 295
   passed. `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`
   REAL exit 0, expect 30 passed.

G6 THE NEW MODULE, ITS TEST, AND THE SUITES. `python3 -m ruff check
   packages/orchestration/self_use_runner.py
   tests/orchestration/test_self_use_runner.py` REAL exit 0, "All checks
   passed!". `python3 -m pytest tests/orchestration/test_self_use_runner.py
   tests/orchestration/test_self_use_generator.py
   tests/orchestration/test_self_use_queue.py
   tests/orchestration/test_self_use_job.py -q` REAL exit 0, expect 68
   passed (7 new). `python3 -m pytest tests/test_data_paths.py
   tests/orchestration/test_development_artifact_boundary.py
   tests/test_path_utils.py -q` REAL exit 0, expect 69 passed (this new
   module touches none of their guarded paths, so this is a sanity check,
   not an expected change).

G7 THE MUTATION RED-PROOF, inside your own disposable worktree, `__pycache__`
   purged, `python3 -B`. Remove the five-line block
   `    if plan.status == JOB_BLOCKED:` through its closing `        )` in
   `packages/orchestration/self_use_runner.py`; re-run
   `tests/orchestration/test_self_use_runner.py`; expect REAL exit 1,
   EXACTLY ONE failure, `test_a_blocked_plan_raises_rather_than_running`,
   6 passed. Restore the file from the scratch original
   (`shutil.copyfile` from `.remedy-wt/f258-r5/self_use_runner.py`); re-run;
   expect REAL exit 0, 7 passed again. Remove the disposable worktree
   afterward; `git worktree list` in the primary checkout shows only the
   primary checkout.

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
session" section — feature and round (SESSION 2 of F258, round 5), branch,
commit SHAs, the changed-files table, every gate's REAL result (one line
per gate, per checklist item 31, run each at a commit strictly before the
handoff commit), open-findings count (unchanged: 317 registered / 55
resolved / 262 open), the DECISION F258 id list (unchanged `['D1','D2']`),
and next expected action: T003 (findings flow back). Push
`feature/f258-self-use-v2` at the end (no force push). No PR is opened this
round — closure has not been reached.
──────────────────────────────────────────────────────────────
