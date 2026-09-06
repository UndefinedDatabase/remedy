── STEP T002 — F260 One world · ROUND 15 · ONE RUN PER INVOCATION ────────────

Goal:        `timeline.append_run_event` mints a NEW run id on every call, so a
             single invocation's events become one run EACH. Give the process
             ONE run id, so all of a job's events from one invocation land in
             one run — which is what `RunLogWriter`'s own docstring already
             promises and what DECISION F260 D1's run-keyed layout needs before
             `Job.run_refs` can mean anything.

Bundle:      C0a  save this block verbatim to `.agent/authored/f260-r15.md`
             C0b  mirror it to `.agent/last_block.md`
             C1   rewrite `.agent/plan.md` from the PLAN slice
             C2   append GATE_R14 then FIND816 to `.agent/live_review.md`, and
                  DEC_D7 to `.agent/decisions.md`, in ONE commit
             C3   append SLIP18 and SLIP19 to `.agent/prose_slips.md`
             C4   SPEC (1): `packages/orchestration/timeline.py` takes one run
                  id per process; SPEC (2): its three new tests
             C5   the handback

Change:      EXACTLY the files named here and nothing else. The `.agent/**`
             writes are `.agent/authored/f260-r15.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
             `.agent/prose_slips.md` and `.agent/handoff.md`. The code writes
             are:

               packages/orchestration/timeline.py
               tests/test_timeline.py

             Nothing else. No other module, no other test file, no `docs/`,
             no `scripts/`. `packages/orchestration/run_log.py` is NOT edited
             this round: its docstring is already correct and this round makes
             the CALLER honour it.

SPEC (1) — `packages/orchestration/timeline.py`

  (a) The module-level import block currently ends with
      `from packages.orchestration.data_paths import run_log_dir`. ADD one
      line importing BOTH names this module needs from the run log:

          from packages.orchestration.run_log import RunLogWriter, new_run_id

      Place it where `ruff` `I001` accepts it and let `ruff` decide the order;
      do not hand-sort the block.

  (b) DELETE the function-local import inside `append_run_event` that reads
      `from packages.orchestration.run_log import RunLogWriter`. That name now
      comes from (a). Re-grep the file first: if any OTHER function in
      `timeline.py` imports `RunLogWriter` function-locally, delete that one
      too and say so in the handback — the point is ONE spelling of the import
      in this module, not a fixed number of deletions.

  (c) Immediately BELOW the import block and ABOVE the first `# ---` banner,
      add the module constant with its one-line WHY comment directly above the
      definition, which is where a reader searches (AGENTS.md, Code
      Discoverability Conventions):

          # One run per PROCESS: every event one invocation appends to a job belongs to the
          # same run, which is what RunLogWriter's docstring promises and what DECISION F260
          # D1's run-keyed layout needs to stay bounded.
          _PROCESS_RUN_ID = new_run_id()

  (d) In `append_run_event`, the construction currently reads

          writer = RunLogWriter(jid, data_root=Path(data_dir))

      and becomes

          writer = RunLogWriter(jid, run_id=_PROCESS_RUN_ID, data_root=Path(data_dir))

      Nothing else in the function changes: `jid` is resolved exactly as today,
      and the `writer.log(event, **(metadata or {}))` line is untouched.

  NOT CHANGED BY THIS SPEC: `load_run_events`, `summarize_timeline`, every
  other function in the module, and `RunLogWriter` itself. The run id stays a
  `str`; no signature changes anywhere.

SPEC (2) — `tests/test_timeline.py`

  Add ONE new test class, `TestOneRunPerInvocation`, carrying THREE tests. Put
  it after the existing class that covers `append_run_event`; if no such class
  exists, put it directly after the last `append_run_event` test. Each test
  uses `tmp_path` as the DATA root, so the run-log directory it reads is
  `tmp_path / "runs" / str(job_id)` — spell that right-hand side LITERALLY, as
  `tests/test_run_log.py` does, so these tests remain an independent observer
  of the accessor (this is the same reason DECISION F260 D6 gives, and it is
  what makes G6 below able to fail).

  (i)  `test_all_events_of_one_invocation_share_one_run`: append FIVE events
       for ONE job id through `append_run_event`, then assert the job's
       directory holds EXACTLY ONE `*.jsonl` file, that the file holds FIVE
       event lines, and that the set of `run_id` values across those lines has
       exactly ONE member.
  (ii) `test_two_jobs_do_not_share_a_run_file`: append one event for each of
       TWO job ids in the same test, then assert each job has its OWN
       directory and each directory holds exactly one `*.jsonl` file.
  (iii)`test_events_come_back_in_append_order`: append the five events of (i),
       then assert `load_run_events` returns their `event` names in the order
       they were appended.

  Write the assertions against the BYTES on disk — read the `.jsonl` and parse
  its lines — not against the writer object, because the writer is what this
  round changes and a test that asks the writer what it did proves nothing.

Constraints:

  1. APPLY EVERY SLICE BYTE FOR BYTE. If a slice contradicts what you measure,
     apply it anyway and DECLARE the contradiction in the handback. Never edit
     a slice to make a gate read as ordered. This is the rule every earlier
     round of this feature followed and it is why their deviations are
     trustworthy.
  2. All three `.agent` append targets end with EXACTLY ONE newline at
     `1d344b48`, measured by the reviewer by trailing-`\n` enumeration on the
     raw bytes: `.agent/live_review.md` at 937682 bytes, `.agent/decisions.md`
     at 842038, `.agent/prose_slips.md` at 117457. DERIVE each recipe from its
     OWN target's measured terminal byte anyway, and assert the count is 1
     before writing — the sentence above is a courtesy, not the authority, and
     the last two rounds of this feature both got one of these three wrong.
  3. `.agent/plan.md` is a WHOLE-FILE replacement by the PLAN slice plus one
     trailing newline. It must stay under the 50-line AGENTS.md cap and must
     carry `## Goal` and `## Next Steps` (§4 item 11's contract readers).
  4. C2 is ONE commit carrying BOTH files, `.agent/live_review.md` appended
     FIRST and `.agent/decisions.md` second. Findings persist before any code
     moves (§4 item 4), so C2 lands before C4.
  5. FIND816 registers a finding the REVIEWER measured; do not write a `Done:`
     or `Landed:` paragraph for it and do not attempt to fix it beyond what
     SPEC (1) orders. A worker-authored `Done:` is a finding however hedged.
  6. Do not touch `tests/test_run_log.py`, `tests/test_data_paths.py`,
     `tests/test_patch_apply.py` or any file under `tests/orchestration/`.
     They are this round's OBSERVERS and G6 needs them unmoved.
  7. Imports: follow what `timeline.py` already does and introduce no second
     convention. `ruff` decides placement; if `I001` disagrees with the spec's
     wording, follow `ruff` and declare it.
  8. Every destructive check runs inside a disposable `git worktree` created
     and removed BY EXACT PATH — never by glob, never in the primary checkout,
     which satisfies `git status --porcelain` empty at the handback.
  9. `cmp` and `remedy` are denied in this sandbox and the bash guard rejects
     `$?`, `$( )` and shell loop forms BY FORM. Use `filecmp.cmp(shallow=False)`
     plus sha256, invoke the CLI as `python3 -m apps.cli.grouped` and `ruff` as
     `python3 -m ruff`, and take every exit code from a Python
     `subprocess.run(...).returncode` written into a capture file under
     `.remedy-wt/`. Nothing under `.remedy-wt/` is ever `git add`ed.
 10. The handback cannot table the commit that writes it; measure C5's own
     insertion count at the next gate, not in the file itself.

Done when:   EIGHT gates, each executed with its REAL exit code recorded, one
             line per gate in the handback (amend0827 rule 5 caps a round at
             eight).

  G1 TRANSPORT — ONE comparison, not a chain. `sha256sum` over
     `.agent/authored/f260-r15.md` and `.agent/last_block.md`: both equal the
     digest the DELEGATION names for this block, checked BEFORE staging. The
     digest cannot be printed inside the bytes it measures, so it reaches you
     through the delegation and never through this file. C0a and C0b are both `shutil.copyfile` from the delegation's
     source path, each proved additionally by `filecmp.cmp(shallow=False)`.

  G2 THE RECORD — for `.agent/live_review.md`: (a) exact-image byte equality,
     `post == pre + b"\n" + GATE_R14 + b"\n\n" + FIND816 + b"\n"`, plus the
     prefix check `post[:len(pre)] == pre`; (b) structural — split the whole
     file on `"\n\n"`, report the unit count before and after and show the LAST
     TWO units equal GATE_R14 then FIND816 in that order; (c) a negative
     control run IN MEMORY on a `bytes` object — flip one byte inside the
     appended region, show BOTH readers reject, restore, show both accept and
     the restored image equals the disk image. For `.agent/decisions.md`: the
     same (a), (b) and (c) over `post == pre + b"\n" + DEC_D7 + b"\n"`.
     (d) CENSUS after C2, counted by the script and not by eye: `^Gate: `
     lines, registration lines and their DISTINCT id count, `^Done: ` lines and
     their DISTINCT id count, and the OPEN SET BY DISTINCT ID. The base reading
     at `1d344b48` is 23 / 300 over 300 / 5 over 3 / open 297; this round adds
     ONE registration, so the expected post reading is 24 / 301 over 301 /
     5 over 3 / OPEN 298. Report what you measure; if it differs, the
     measurement wins and the difference is a declared deviation.

  G3 THE PROSE FILES — `.agent/plan.md`: disk bytes `== PLAN slice + b"\n"`,
     with its byte count and line count reported and the presence of `## Goal`
     and `## Next Steps` shown. `.agent/prose_slips.md`:
     `post == pre + b"\n" + SLIP18 + b"\n\n" + SLIP19 + b"\n"`, with the
     blank-line unit count before and after and the last TWO units shown to
     equal SLIP18 then SLIP19 in that order. Both files re-read afterwards and
     shown to contain ZERO lines beginning `BEGIN ` or `END `.

  G4 THE DEFECT IS REAL AT THE BASE — run this BEFORE C4, in a disposable
     worktree at the base, `python3 -B`, `__pycache__` purged and re-enumerated
     at 0, module resolution printed and confirmed to that worktree: append
     FIVE events for one job through the SHIPPED `timeline.append_run_event`
     into a temporary data root, then PRINT the number of `*.jsonl` files, the
     number of event lines and the number of DISTINCT `run_id` values found in
     the bytes. The reviewer measured 5 / 5 / 5 at `1d344b48`. Print the three
     numbers; do not print a verdict word. This gate establishes that FIND816
     describes the disk and not a reading of the source.

  G5 THE FIX IS REAL AT THE HEAD — the SAME probe, same shape, run in the
     primary checkout after C4 with `python3 -B`: print the number of `*.jsonl`
     files, the event-line count and the DISTINCT `run_id` count for one job,
     and then the per-job file count for TWO different jobs appended in the
     same process. The ordered property is ONE file, FIVE lines, ONE distinct
     run id for the single job, and ONE file EACH in TWO separate directories
     for the two jobs. G4 and G5 are a PAIR and the pair is the proof; neither
     number alone is.

  G6 MUTATION RED-PROOF — inside a disposable `git worktree` at the round's
     head, created BY EXACT PATH, `python3 -B`, `PYTHONDONTWRITEBYTECODE=1`,
     `__pycache__` purged and re-enumerated at 0, and module resolution
     confirmed to that worktree's own `timeline.py` by printing
     `timeline.__file__` and the LIVE source line of the construction.
     Selection: `tests/test_timeline.py tests/test_run_log.py
     tests/test_data_paths.py`.
       (i)   CONTROL, unmutated: record the exit code and the counts.
       (ii)  Count the exact revert-target bytes `run_id=_PROCESS_RUN_ID, `
             and show they occur EXACTLY ONCE before mutating. Then DELETE
             those bytes — which restores the pre-round behaviour exactly —
             re-print the LIVE construction line to prove the mutation is the
             one the interpreter sees, and re-run. The ORDERED property is
             that the run goes RED and that the failures include the three
             tests SPEC (2) adds. Report the exit code, the failure count and
             the failing node ids; the COLOUR is what is ordered, never a
             particular count.
       (iii) Restore, show the mutated byte count back at 0 and the original
             at 1, purge and re-enumerate `__pycache__` at 0, re-run the
             control to the same reading as (i), show that worktree's
             `git status --porcelain` and `git diff HEAD --stat` both EMPTY,
             then remove the worktree BY EXACT PATH and `git worktree prune`.
     If the mutation does NOT go red, STOP and say so in the handback rather
     than adjusting the test — a green mutation means SPEC (2) built no
     observer, which is a finding about this block and not about your work.

  G7 THE SUITES — run SERIALLY, never two at once, each captured to its own
     file under `.remedy-wt/` and read from the capture:
       (1) `python3 -m pytest tests/test_timeline.py tests/test_run_log.py
           tests/test_data_paths.py tests/test_patch_apply.py -q -p no:randomly`
       (2) `python3 -m pytest tests/orchestration/ -q -p no:randomly` — the
           reviewer measured 12805 passed and 10 skipped at `1d344b48`
       (3) `python3 -m pytest tests/cli/ -q -p no:randomly` — 1537 passed at
           `1d344b48`; confirm the canary is inside the selection by running
           `python3 -m pytest tests/cli/test_golden_path.py --collect-only`
           and reporting the collected count
       (4) `python3 -m apps.cli.grouped integrity check --json` — report
           `passed`, `fail_count` and `check_count`
     Report `^FAILED` and `^ERROR` line counts for (2) and (3) rather than
     trusting the summary line alone.

  G8 LINT AND TREE — `python3 -m ruff check` over the code files this round
     edited. COUNT THEM YOURSELF from your own change set and lint exactly what
     you counted; do not take a number from this block. Then
     `git status --porcelain` and `git ls-files .remedy-wt`, both shown EMPTY.
     Two errors pre-exist and are NOT in this change set — `UP035` at
     `dag_schedule.py:36` and `F821` at `gauntlet_injection.py:286`; do not
     approach either file.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             It carries: the SESSION NUMBER (this is SESSION 6 of F260) and the
             round, the branch, the commit table with `+/-` taken from
             `git log --numstat` and never re-derived by eye, the external
             actions table, ONE LINE PER GATE with its real exit code, the
             authored-text proof table, every deviation, the item-status table
             covering C0a through C5 and G1 through G8, the open-findings count
             BY DISTINCT ID, and one sentence of context self-assessment
             (amend0905-throughput). There is NO length cap. Push after the
             handback commit; the push's own transcript cannot appear in the
             commit that carries it.

──────────────────────────────────────────────────────────────────────────────

BEGIN PLAN
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 14 are reviewed and 2 to 14 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, the ping-pong run store has one spelling on both sides,
and the run-log store has one spelling on the whole production side.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE RUN PER INVOCATION. `timeline.append_run_event` mints a new run id on every
call, so five events of one resume become five runs in five files — measured on
the shipped function. The module takes ONE run id for the life of the process
and passes it, which is what `RunLogWriter`'s docstring already promises. This
is registered as finding R-0816 and ruled by DECISION F260 D7.

## Next Steps

- `Job.run_refs`, the plural run list D1 names and nothing on disk carries yet.
  It is meaningful only once a run is an invocation rather than an event, which
  is what this round buys.
- THE RE-KEY ITSELF: `run_log_dir` and `pingpong_run_dir` collapse onto
  `run_dir`, keyed by RUN id — DECISION F260 D1. The reader side needs a job to
  name its runs, so `run_refs` above is its prerequisite.
- The rest of T002: the unified record's own administrative fields — eight of
  D1's eleven have no counterpart in `JobPlan` — and the Mission extension.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- The test side of the run-log spelling is DECLINED, not forgotten: DECISION
  F260 D6 records why, and the re-key inherits those sites.
- The soft limit is 25 rounds or 7 sessions. This is round 15 of session 6, so
  the SESSION limit is reached next session and split-and-close is the endgame.
  Every round leaves a self-consistent tree so that close is available at any
  point.
END PLAN

BEGIN GATE_R14
Gate: R14 — the F260 R14 entry. R14 GAVE `RunLogWriter` A DATA ROOT AND DELETED THE LAST PRODUCTION HAND-SPELLING OF THE JOB-KEYED RUN-LOG JOIN. VERDICT PASS. Range `4f265f91cbdf2f4c327e9dd303b8cd78c146618d`..`1d344b485ce6c4e5e7768c6ab001a10bf8ab69d2`, ten commits, all single-parent, of which nine are the Bundle's ordered sequence C0a to C6 plus the handback and one is the declared extra commit `c296ee97`; pushed to `origin/feature/f260-one-world`, which the reviewer confirmed points at the same object as `HEAD`, and no pull request created. Largest insertion count 397, a single `.agent/**` state write exempt under AGENTS.md DECISION F104 D1; largest CODE commit 35. THE REVIEWER RE-RAN EVERY GATE ITSELF AND REPRODUCED EVERY NUMBER THE HANDBACK REPORTED, INCLUDING THE MUTATION SPLIT DIGIT FOR DIGIT. TRANSPORT: the reviewer's scratchpad original `.remedy-wt/f260-r14-block.md` still existed at review time, so the PRIMARY disk-to-disk proof was available and the §4 item 9 digest fallback was NOT used: all three of that file, `.agent/authored/f260-r14.md` and `.agent/last_block.md` hash to `59fb3c47a421fa4e14fe13f8afa6761a3a97caebc764ca0101bf8b22935e0d57`. THE SLICES WERE VERIFIED DISK TO DISK against the COMMITTED `.agent/authored/f260-r14.md`, never against a retype: `.agent/plan.md` equals the PLAN slice plus one newline exactly at 2530 bytes and 48 lines, carrying `## Goal` and `## Next Steps`; `.agent/live_review.md` equals its pre-image plus `"\n"` plus GATE_R13 plus `"\n"` exactly, 931365 to 937682 bytes, units 434 to 435; `.agent/decisions.md` equals its pre-image plus `"\n"` plus DEC_D6 plus `"\n"` exactly, 839361 to 842038 bytes, units 1892 to 1893; `.agent/prose_slips.md` equals its pre-image plus `"\n"` plus SLIP14, SLIP15, SLIP16 and SLIP17 joined by `"\n\n"` plus a final `"\n"`, exactly, 115506 to 117457 bytes, units 144 to 148, a rise of exactly four. All fourteen marker lines occur exactly once and NONE of them reached any target file, which the reviewer re-measured at zero `BEGIN `/`END ` lines per target. THE CENSUS: `^Gate: ` 23, registrations 300 over 300 DISTINCT ids, `^Done: ` 5 lines over THREE distinct ids, OPEN SET 297 BY DISTINCT ID — identical to the base, which is correct, because GATE_R13 is a `Gate:` record and this round registered and resolved nothing; no worker-authored `Done:` paragraph was added. G5 REPRODUCED IN FULL over 1030 tracked `.py` files enumerated from `git ls-files` in Python: the literal join `root / self._job_id` 1 to 0, word-bounded `_runs_dir_default` 2 to 0, the AST reading of calls to `run_log_dir` in `run_log.py` 0 to 1, and word-bounded `runs_root` from 41 occurrences in 11 files to ZERO in ZERO files — no survivor. G4 WAS REPRODUCED AND STRENGTHENED: rather than compare two accessors the reviewer ran the SHIPPED `RunLogWriter` and read the bytes it left, under an explicit root and under `REMEDY_DATA_DIR`, and both land at `<data_root>/runs/<job_id>/<run_id>.jsonl` — so "no layout change" is a measurement of the writer's own output and not an inference from its source. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY in the reviewer's own disposable worktree at `1d344b48`, `python3 -B`, `__pycache__` enumerated at 0, module resolution confirmed to that worktree's own `data_paths.py`, and the revert target counted at EXACTLY 1 before anything was changed: control exit 0 at 261 passed; with `run_log_dir` appending `"_MUTATED"` to the job id and the mutated body re-printed from the live module, exit 1 at 32 FAILED and 229 passed, the split falling in `tests/test_patch_apply.py` 18, `tests/test_timeline.py` 8, `tests/test_run_log.py` 3 and `tests/test_data_paths.py` 3 — the handback's split exactly; after restore, control exit 0 at 261 again, that worktree's `git status --porcelain` empty, and the worktree removed BY EXACT PATH and pruned, leaving the twelve rows that are the primary checkout and the eleven pre-existing `remedy/job-*` worktrees. THE SUITES, re-run serially by the reviewer at the branch tip: `tests/orchestration/` exit 0 at 12805 passed and 10 skipped in 720.62 s, `tests/cli/` exit 0 at 1537 passed in 302.73 s, the five-file selection exit 0 at 304 passed, and `integrity check --json` `"passed": true` with `"fail_count": 0` over 5 checks all passing. RUFF over the eleven edited `.py` paths: `All checks passed!`. TWELVE DEVIATIONS WERE DECLARED AND ALL TWELVE ARE UPHELD. The three needing a ruling are 1, 2 and 3. Deviations 1 and 2 are the block's own numerals disagreeing with the disk — the base `runs_root` count is 41 occurrences where the gate said 37, because the gate stated a LINE count while its own words ordered an OCCURRENCE count, and SPEC (3) said "eight constructions" over a list of seven constructions plus one comment — and the reviewer re-measured both and confirms the worker's readings, 41 in 11 files and seven constructions in `prompt_trace.py`'s comment's company. In both the gate's BINDING clause was met with nothing left on disk to repair, so per operator amendment amend0827-process-diet rule 2 they are dated lines in `.agent/prose_slips.md` and spend no id. Deviation 3 is the only departure from the ordered commit sequence and is ACCEPTED: the worker reworded ITS OWN comment, not a test, an assertion or a line of code, so that G5(a)'s word-bounded reading — which does not strip comments — read the ordered 0, and it reported BOTH readings rather than only the final one. Nothing was reshaped to make a gate pass and no gate went red. SEPARATELY, AND NOT A DEFECT OF THIS ROUND: while re-running the round's own G4 the reviewer measured a defect this round did not introduce and could not have seen, registered immediately below as `R-0816`.
END GATE_R14

BEGIN FIND816
- R-0816 — Medium, `timeline.append_run_event` MINTS A NEW RUN ID ON EVERY CALL, SO ONE INVOCATION'S EVENTS BECOME ONE RUN EACH AND `RunLogWriter`'s STATED CONTRACT IS FALSE FOR EVERY CALLER OF IT. Measured by the reviewer at `1d344b485ce6c4e5e7768c6ab001a10bf8ab69d2` by RUNNING THE SHIPPED FUNCTION, not by reading it: appending the five events `event_replay` emits for one resume — `resume_blocked`, `resume_started`, `resume_test_started`, `resume_test_completed`, `resume_completed` — for a single job id into a temporary data root produces FIVE `.jsonl` files under `<data_root>/runs/<job_id>/`, FIVE event lines in total, and FIVE DISTINCT `run_id` values, one per event. `packages/orchestration/timeline.py:62` constructs `RunLogWriter(jid, data_root=Path(data_dir))` with no `run_id`, and `RunLogWriter.__init__` therefore calls `new_run_id()` per construction, while `RunLogWriter`'s own class docstring states "One instance should be used per CLI invocation. All events from a single invocation share the same run_id, forming a chronological session trail." PRODUCT EFFECT, which is why this spends an id rather than a `.agent/prose_slips.md` line under operator amendment amend0827-process-diet rule 2: the wrong state is on disk under `packages/`, the run-log directory of any job grows one FILE per event without bound, and the word "run" is left naming two different things in one store — an invocation for `RunLogWriter`'s direct callers and an event for `append_run_event`'s, which are `autorun.py`, `event_persistence.py`, `event_replay.py`, `repair_loop.py`, `source_apply.py` and `source_context.py` among others. IT ALSO FALSIFIES A LANDED DECISION'S STATED PREMISE. DECISION F022 D2 rejected giving each budget tick its own run id on the ground that "those writers are one-per-invocation while this one is one-per-safe-point, and the file count is unbounded in the length of the job"; the first half of that sentence is not true of `append_run_event`, and the unbounded file count the decision declined to create on the safe-point path already exists on the event path. The decision's CHOSEN option is unaffected and stays correct — a fixed `BUDGET_TICK_RUN_ID` is the right answer either way — so nothing is reversed by this finding; what is corrected is a premise, and it is recorded here because F260's remaining design leans on it. IT IS ALSO LOAD-BEARING FOR THIS FEATURE. DECISION F260 D1 re-keys the store to `<data_root>/runs/<run_id>/`, which under today's behaviour would create one DIRECTORY per event, and it gives the Job a plural `run_refs`, which under today's behaviour would be a list of events wearing the name of runs. MEDIUM rather than High because no data is lost and no reader is broken — `timeline.load_run_events` globs the job directory and sorts by timestamp, so it returns all five events in order regardless — and rather than Low because the defect is in production code under `packages/`, grows without bound and would be inherited and amplified by the re-key. SEARCHED BEFORE MINTING per §3 item 30: the open set was grepped for `append_run_event`, for `new_run_id`, and for the phrases "run id per event", "one run per event" and "per CLI invocation", and no open finding describes this defect; the nearest neighbours are this feature's own store findings and none names the writer's id cardinality. FIX: give the process ONE run id and pass it, so an invocation is a run. Resolved when five events appended for one job in one process land in ONE file under ONE `run_id`, proved by reading the bytes rather than by asking the writer, and when two different jobs in that same process still get their own directories.
END FIND816

BEGIN DEC_D7
### DECISION F260 D7 (2026-09-06, F260 round 15) — a run is an INVOCATION, not an event, and the run id is one module constant
Routed to planning under §4 item 7: the reviewer authored this ruling and proceeded under it rather than asking. It rules the repair of finding `R-0816` and it re-orders this feature's remaining plan. THE PLAN AT `1d344b48` named `Job.run_refs` as the next step and the re-key as the one after it. Measured against the disk, `run_refs` cannot be built first: `timeline.append_run_event` mints a run id per EVENT, so a run list assembled today would enumerate events, and DECISION F260 D1's `<data_root>/runs/<run_id>/` would hold one directory per event. The cardinality of a run is therefore a PREREQUISITE of both, and it is repaired first. CHOSEN: `timeline.py` holds ONE module-level `_PROCESS_RUN_ID = new_run_id()`, computed once at import, and `append_run_event` passes it to every `RunLogWriter` it constructs. A run is then exactly what `RunLogWriter`'s docstring has always said it is — one invocation — and different jobs stay in different directories because the job id, not the run id, keys the directory today. The mechanism was DRY-RUN by the reviewer against the SHIPPED writer before being ordered: five events for one job under one fixed run id produce ONE file, FIVE lines, ONE distinct `run_id`, in append order, while a second job in the same process gets its own directory and its own file. ALTERNATIVES CONSIDERED. A per-`(data root, job id)` cache of writers in a module dict — rejected: it is process-global mutable state that needs an eviction rule and a test-visible reset, and it buys nothing the constant does not, since the directory is already keyed by job. Giving each caller its own run id to pass — rejected: it moves the decision to eleven call sites and is the shape this feature exists to remove. Deriving the run id from the job id — rejected: it would make a job's runs indistinguishable from each other, which is precisely what D1's plural `run_refs` needs to be able to tell apart. Leaving it and letting the re-key absorb it — rejected: the re-key would then be written against a cardinality nobody had measured, and the finding's own product effect would ship one directory per event. KNOWN CONSEQUENCE, STATED RATHER THAN HIDDEN: a long-lived process — `ui_server.py` is the case — keeps ONE run id for its lifetime, so its events form one long run rather than many. That is a strict improvement on one run per event and it is the same trade `BUDGET_TICK_RUN_ID` already makes on the safe-point path; if a server ever needs a run per request, the run id becomes a parameter of the request and this constant is its default. NOT CHANGED BY THIS RULING: D1's target layout, `RunLogWriter`'s signature and docstring, `load_run_events`, and DECISION F022 D2's chosen option. REVERSE by deleting this paragraph, removing `_PROCESS_RUN_ID` and its argument, at which point `R-0816` is open again and `run_refs` returns to being the plan's next step.
END DEC_D7

BEGIN SLIP18
2026-09-06 · F260 R14 (reviewer) · Gate G5(c) of the round-14 block ordered a word-bounded `runs_root` search and stated its base count as 37, while the same search over the same 1030-file enumeration returns 41 in 11 files — the reviewer re-measured both readings and the worker's 41 is correct. The gap is four LINES that carry the token TWICE, so the block stated a LINE count where its own words ordered an OCCURRENCE count; the gate's binding clause was "any survivor FAILS", which the C6 reading of 0 in 0 files meets under either reading. Reviewer-authored numeral disagreeing with the disk, nothing wrong under `packages/`, `apps/`, `tests/` or `docs/` as a result; no id spent (amend0827-process-diet rule 2).
END SLIP18

BEGIN SLIP19
2026-09-06 · F260 R14 (reviewer) · SPEC (3) of the round-14 block said "eight constructions pass `runs_root`" while its own enumeration beneath it listed seven `RunLogWriter(...)` constructions plus `prompt_trace.py:215`, which is a COMMENT and constructs nothing — checklist item 16's shape, a hand-counted numeral stated over a list the reader can count, and the second instance of that shape in two rounds. All eight SITES moved and the reviewer confirms seven constructions; the worker applied the slice byte for byte and declared the disagreement, which is what constraint 1 asks. No id spent (amend0827-process-diet rule 2).
END SLIP19
