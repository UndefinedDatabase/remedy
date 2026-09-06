# Handoff — F260 One world: mission → job → run, end of session 2

## Session

`SESSION 2 of feature F260 · rounds 5–8 delegated and reviewed · rounds so far 8`

Well inside the 25-round / 7-session soft limit, so no scope report is owed.

Context self-assessment: the reviewer's context carried four rounds of authoring
plus four full independent re-verifications comfortably, but the session ends
deliberately at four rather than at the six-to-eight target for the two honest
reasons docs/agents/self_drive_protocol.md G7 names, both of which apply. FIRST,
the next round is one that explicitly needs a fresh session: the record move is a
hard schema change coupled to the resolver by DECISION F260 D4, and its
pre-emission work needs a fresh reading of nine `apps/cli/commands/` modules and
of `storage.load_job`'s signature. SECOND, the reviewer's own authoring errors
accumulated — six block defects across four rounds, every one caught by the
worker or by the reviewer's own pre-emission checks, which the 2026-09-05
throughput amendment names as exactly the signal to stop on rather than to push
through.

## State block

`~40 % (T001 ✅ · D1/D2/D4 ✅ · Layout-Spellings ✅ · Record-Move + Resolver + T003–T005 offen) — Schätzung`

Branch: `feature/f260-one-world`, cut from `main` at `b5cd6c20` (the merge commit
of pull request 240, F259). Branch tip and LAST REVIEWED commit: `607e2bec`,
pushed. 55 commits over eight rounds. NO pull request exists for this branch yet
— it is opened in the closure sequence, not now.

Open findings: **295** (299 `^- R-\d{4} — ` registrations minus 4
`^Done: R-\d{4} — ` lines). The reviewer additionally checked for duplicate
registration ids at `607e2bec`: 299 registration paragraphs carry 299 DISTINCT
ids, none repeated. Maximum id in use: **R-0814**, so the next id this feature
mints is R-0815. No id was minted this session.

## What this session did

Four delegated rounds, every one PASS, every gate re-run by the reviewer itself
rather than read from the handback.

| Round | Range | Verdict | What it did |
|---|---|---|---|
| 5 | `c5da84cb..3aaeb042` | PASS | T001's minting half at the CALL SITES: the four inline `uuid4().hex[:16]` mints that name a job, a run or an episode moved onto the round-4 functions; both modules stopped naming `uuid4`. |
| 6 | `3aaeb042..99ca6406` | PASS | DECISION F260 D4, and `data_paths` gained the one spelling of D1's target layout — `job_dir`, `job_record_path`, `job_evidence_dir`, `run_dir` — with `pingpong_job`'s two evidence paths on it. |
| 7 | `99ca6406..072b54ed` | PASS | The four remaining hand-built evidence paths onto `data_paths.job_evidence_dir`, and the guard widened from one module to the set that owns a job's evidence. |
| 8 | `072b54ed..607e2bec` | PASS | The PING-PONG store got one spelling too — `task_job_dir`, `task_job_record_path` — and `pingpong_job._jobs_dir` was DELETED, with its six users, `job_evidence`'s cross-module import and seventeen test sites moved onto the accessors. |

## THE ROUND 8 VERDICT — PASS, and it is owed to the record

This paragraph is the durable carrier operator amendment amend0827-process-diet
rule 1 provides for a verdict the reviewer's session cannot book itself. THE
FIRST COMMIT OF THE NEXT ROUND THAT IS HAPPENING ANYWAY MUST BOOK IT into
`.agent/live_review.md` as a `Gate: R8 — the F260 R8 entry.` paragraph, joining
the existing series of seventeen.

VERDICT PASS on range `072b54ed..607e2bec`, seven commits, all single-parent,
largest insertion count 349 (a single `.agent/**` state write), largest code
commit 257, both under the AGENTS.md 500-insertion cap.

- TRANSPORT: one digest
  `f362c984379e56fb99a3d1d6f58fb62cff55d7f02ebef6d26f4d15bf56209ed1` across the
  reviewer's scratch original, the saved copy at `.agent/authored/f260-r8.md` and
  the mirror at `.agent/last_block.md`. Per §3 item 37 that chain covers those
  three artefacts and is not a claim about the bytes emitted into the prompt.
- THE RECORD: `.agent/live_review.md` 893805 → 898817, growth 5012 equal to
  `"\n"` plus a 5010-byte slice plus `"\n"`; the pre-image is a byte-exact PREFIX,
  the last blank-line unit with the file's terminating newline stripped equals the
  slice, and the two negative controls each reject in its OWN region and only
  there. Units 425 → 426. Registrations 299, `Done:` 4, seventeen `Gate:` headers,
  all distinct.
- THE SLIP FILE, with the round-8 counter-measure working: 94802 → 97989, terminal
  byte before the append was a newline, and blank-line units rose 129 → 131, a
  rise of exactly TWO — one per slip. The `"\n\n"` separator between the two slips
  was itself a correction the reviewer's pre-emission check caught before
  emission: with single newlines throughout the count reaches 130, which is the
  round-6 defect recurring one position over.
- THE DELETED NAME IS GONE, AND THE STORE DID NOT MOVE.
  `hasattr(pingpong_job, "_jobs_dir")` is False. By AST, references resolving to
  exactly `_jobs_dir` number 0 in `pingpong_job.py` (6 at the base) and 0 in
  `job_evidence.py` (2 at the base). With `REMEDY_DATA_DIR` pointed at a scratch
  directory, `task_job_dir(j) == task_jobs_dir() / j` and
  `task_job_record_path(j) == task_jobs_dir() / j / "job.json"`, and the `root`
  override is honoured — the value-preservation property this round rests on.
- RUFF over exactly the eleven files C4 touched exits 0. It is scoped to those
  files on purpose: measured at `072b54ed`, `ruff check packages/` exits 1 with 2
  errors and `ruff check tests/orchestration/` exits 1 with 11, all PRE-EXISTING
  and none of them this feature's, so a directory-scoped gate here could not pass.
- THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY, in a disposable worktree at
  `b92d096f` with the module resolving from that worktree. Unmutated control exit
  0 at 46 passed. Ignoring `root` in `task_job_dir` fails
  `test_the_root_override_is_honoured_by_both_task_job_helpers`. Re-adding
  `_jobs_dir` as a `def` fails BOTH
  `test_pingpong_job_has_no_jobs_dir_attribute_at_all` AND
  `test_no_migrated_module_names_the_deleted_jobs_dir_helper[packages.orchestration.pingpong_job]`
  — which is the worker's guard fix working, and is the reading the reviewer's
  block got wrong. Control green after each restore.
- THE LOAD-BEARING IMPORT PROOF ALSO REPRODUCES: deleting the single
  function-scoped import at `pingpong_job.py:2853` gives
  `NameError: name 'task_job_dir' is not defined` at `pingpong_job.py:2883`,
  failing exactly the two `tests/orchestration/test_job_worktree_handoff.py` tests
  the block predicted, and the suite is green again on restore.
- THE SUITES, re-run serially by the reviewer, all exit 0: 58, 34, 26, 26, 13, 24,
  10, 46, 93, 178 and 42 — 550 tests — and `integrity check --json` returned
  `"passed": true` with `"fail_count": 0` over 5 checks.
- BOTH BLOCK DEFECTS THE WORKER DECLARED ARE UPHELD, and both were reproduced by
  the reviewer. They are recorded below as the two prose slips the next round
  appends.

## THE TWO ROUND-8 REVIEWER SLIPS — owed to `.agent/prose_slips.md`

The next round appends these as dated lines, with a `"\n\n"` separator between
them. Neither spends an R-id: both are reviewer-authored gate defects with
nothing wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`, which is
what operator amendment amend0827-process-diet rule 2 routes here, and the
precedent inside this feature is the round-3 vacuous clause, whose id was spent
on the separate on-disk defect and not on the clause.

1. G4(b) of the round-8 block ordered, as its NON-VACUITY control, that
   `_jobs_dir` AST references be NON-ZERO in `packages/orchestration/storage.py`.
   Measured at `607e2bec` and at the base `072b54ed` alike: ZERO. `storage.py`
   names `_resolve_jobs_dir`, a different symbol that merely contains the same
   substring — which the block's own DO-NOT-TOUCH paragraph says in as many words,
   forty lines above the gate that contradicted it. The control could not pass in
   any round. THE LESSON: §3 item 12 and finding R-0364 require a gate to be RUN
   AT ITS BASE before it is ordered; the reviewer ran `ruff` at the base and never
   ran the AST reading it was about to gate on, so the one clause whose whole job
   was to prove the search could find anything was the one clause never executed.
   A non-vacuity control is a gate like any other and is measured before emission.

2. G6(iii) of the same block ordered a revived `_jobs_dir` to fail BOTH the
   `hasattr` reading and "the same AST reference reading" the guard paragraph
   specified. A revived function is a `def`, so it parses to a `FunctionDef` node
   and produces no `ast.Name`, `ast.Attribute` or `ast.alias` at all — the
   reference reading round 7 built cannot see a definition, and the reviewer
   confirmed it independently on a two-line parse. The worker measured this at its
   first C4, added a `_names_of` helper covering binding forms, left round 7's
   reference helper untouched because that one is correct for ITS property, and
   re-measured green. THE LESSON: §3 item 18 asks that a recipe and the property
   it must establish be read against each other, and two guards that sound alike —
   "no module CALLS this" and "no module DEFINES this" — need different AST
   readings. The block reused a reading by name instead of by what it matches.

## Changed files this session

`git diff --numstat c5da84cb..607e2bec`, production and tests only:

| Path | +/- |
|---|---|
| apps/cli/commands/do_cmd.py | +2 / -2 |
| docs/roadmap/features/T2_F260.md | +38 / -0 |
| packages/orchestration/data_paths.py | +70 / -0 |
| packages/orchestration/job_evidence.py | +6 / -6 |
| packages/orchestration/pingpong_job.py | +44 / -24 |
| packages/orchestration/pingpong_loop.py | +3 / -2 |
| packages/orchestration/repair_attest.py | +2 / -2 |
| tests/orchestration/test_failure_wiring.py | +2 / -1 |
| tests/orchestration/test_job_promote_consistency.py | +3 / -2 |
| tests/orchestration/test_job_stop_integration.py | +3 / -3 |
| tests/orchestration/test_job_worktree_handoff.py | +6 / -5 |
| tests/orchestration/test_job_worktree_integration.py | +2 / -1 |
| tests/orchestration/test_job_worktree_integrity.py | +2 / -1 |
| tests/orchestration/test_mint_call_sites.py | +95 / -0 |
| tests/orchestration/test_pingpong_integration.py | +4 / -4 |
| tests/test_data_paths.py | +363 / -0 |

`.agent/` state files also moved: `authored/f260-r5..r8.md` (new), `handoff.md`,
`last_block.md`, `live_review.md`, `plan.md`, `prose_slips.md`.

## Verification at the branch tip

- `git status --porcelain` — empty.
- `git ls-files .remedy-wt` — empty; the scratch is untracked.
- `git worktree list` — eleven `remedy/job-*` worktrees, all predating this
  session; no worktree this session created survives.
- `python3 -m apps.cli.grouped integrity check --json` — `"passed": true`,
  `"fail_count": 0`, 5 checks.
- `origin/feature/f260-one-world` is at `607e2bec`, equal to the local tip.

## Item status

| Item | Status | Reason |
|---|---|---|
| Open PR Gate | done | no open pull request at session start; nothing to merge, no branch created |
| Book the round 4 verdict | done | round 5's first commit, `8fe90ef8` |
| Round 5 — T001 minting call sites | done | PASS, verdict booked in round 6's `b964fc18` |
| Round 6 — DECISION D4 + D1 layout spellings | done | PASS, verdict booked in round 7's `adc66ae4` |
| Round 7 — the four evidence paths + widened guard | done | PASS, verdict booked in round 8's `ec1defd0` |
| Round 8 — the ping-pong store spelling, `_jobs_dir` deleted | done | PASS; verdict carried in THIS file |
| Book the round 8 verdict | owed | the next round's first commit books it |
| Append the two round-8 reviewer slips | owed | same commit or the one after; `"\n\n"` between them |
| T001 the one resolver | deferred, ruled | DECISION F260 D4 moves it into T002 with the store it resolves over |
| R-0814 fix condition "no module-local `_jobs_dir`" | done | discharged in round 8 |
| R-0814 fix conditions "one root" and "a test asserts it" | open | need the record move |
| Open a pull request | not due | the closure sequence opens it |

## Next — the expected first actions of the next session

1. Read `.agent/STOP` from disk (Phase 1 rule 1), THEN run the Open PR Gate
   (rule 2). There is no open pull request, so the gate passes with nothing to
   merge and no branch is created — this session's branch is resumed.
2. Book the round-8 verdict above into `.agent/live_review.md` as
   `Gate: R8 — the F260 R8 entry.`, and append the two slips, in the first
   commits of a round that is happening anyway. A round whose whole change set is
   that booking is FORBIDDEN (amend0827 rule 1).
3. Round 9 is THE RECORD MOVE, and the reviewer measured its whole surface at
   `607e2bec` so the next session need not re-measure it:
   - The move itself is now small BY CONSTRUCTION: `data_paths.task_job_dir` and
     `task_job_record_path` collapse into `job_dir` and `job_record_path`, so
     `<data_root>/task_jobs/<16hex>/job.json` becomes
     `<data_root>/jobs/<16hex>/job.json`. That is why rounds 6 to 8 exist.
   - `data_paths._task_job_id_matches` (`data_paths.py`) globs `task_jobs_dir()`
     and is the ONLY thing that finds a ping-pong job. It MUST move in the SAME
     commit as the writer, or every ping-pong job becomes unresolvable and
     `remedy teach narrate` regresses to the 2026-08-25 dogfooding bug.
   - `<data_root>/jobs/` will then hold BOTH `<uuid>.json` FILES (classic) and
     `<16hex>/` DIRECTORIES (ping-pong). `_classic_job_id_matches` globs `*.json`
     and `_task_job_id_matches` reads directories holding a `job.json`, so the two
     do not collide; the classic store is deleted in T004.
   - SEVEN tests hard-code the literal `"task_jobs"` path and will NOT follow the
     writer: `tests/orchestration/test_job_budgets.py:1360`,
     `tests/orchestration/test_job_stop_integration.py:527`, `:558`, `:860`, and
     `tests/cli/test_teach_cmd.py:207`, `:255`. Those numbers were read at
     `607e2bec`; re-grep them.
4. The ONE resolver belongs to the same round group, per DECISION F260 D4.
   Measured: `resolve_job_id` returns `UUID` and has FORTY call sites across nine
   `apps/cli/commands/` modules, every one feeding
   `storage.load_job(job_id: UUID, ...)` (`storage.py:83`) or `load_job_safe`
   (`storage.py:100`); `resolve_any_job_id` returns `str` and has exactly two,
   both in `apps/cli/commands/teach_cmd.py` (lines 66 and 166).

## Standing measurements the next block should not re-derive

- RUFF IS ALREADY RED AT THE BASE over whole directories: `ruff check packages/`
  exits 1 with 2 errors and `ruff check tests/orchestration/` exits 1 with 11, all
  pre-existing and none of them this feature's. Gate ruff on the EXACT changed
  files, which was green at `072b54ed` and is green at `607e2bec`.
- `pingpong_job.py` imports `data_paths` ONLY inside function bodies, and this
  feature has not changed that. Every call site needs its own import, and the one
  at `pingpong_job.py:2884` sits inside a multi-line boolean `and` expression
  where the missing import is a RUNTIME `NameError` that only two integration
  tests reach.
- `.agent/prose_slips.md` and `.agent/live_review.md` both end with exactly one
  newline at `607e2bec`. An append recipe is a function of the target's terminal
  byte and is derived per target, never copied between them; two slips appended
  together need `"\n\n"` between them or they fuse into one blank-line unit.

## Open risks carried forward

- DECISION F260 D1 changes what `<data_root>/runs/` is keyed by, from job id to
  run id. Every reader of the old shape must move in the same commit as its
  writer, or a run log is unreadable between two commits.
- The feature file's original "rename `task_jobs/` to `runs/`" order is NOT
  performed; DECISION F260 D0 records why, measured. Anyone reading the Goal &
  Done section alone will still find the retired sentence — D0 sits below it and
  supersedes it.
- DECISION F260 D4 retires T001's clause "make every job-taking command resolve
  through it while both stores still exist". Anyone reading T001 alone will still
  find that sentence; D4 is in the same file and supersedes it.
- The T005 prototype-cluster deletion is large and reversible in one direction
  only. It runs last, behind a reachability test that is green BEFORE the first
  `git rm`.
