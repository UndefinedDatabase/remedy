# Handoff — F276 Data-root hygiene & disk budget · Round 8

## Session

SESSION 2 of feature F276 · round 8 · rounds so far 8

Context self-assessment: the worker verified the step block's bytes before doing anything else — 246 lines, sha256 `20aef44c5d1717d58e91b42ff30600351acd09f7f6a370a9d03baad30cf1da59`, both readings identical to the digest the delegation message named — then read AGENTS.md in full, `docs/agents/handback_template.md` and `docs/roadmap/STATUS_closure_protocol.md` including precondition 6 word for word, then all four remaining payloads with their digests checked before use; every numeral below is the output of a command run in this round, never a recollection, and the two exit codes that decide the round were taken from a subprocess object rather than from a pipeline.

## Range

Review of 9fb2ab65..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 8 is the closure sequence's SECOND HALF minus its last round. It books round 7's verdict, resolves R-1006, spends this feature's ONE repair round on the integration gate — which is now GREEN — and consumes the one self-use item closure precondition 6 requires.
- C1 books round 7's PASS over the five commits ending at `9fb2ab65`, writes the reviewer-authored `Done: R-1006`, appends DECISION F276 D9, adds two prose-slip lines, rewrites the plan, and saves byte copies of the five reviewer payloads.
- C2 is the repair run. `apps/ui` was BUILT FIRST, then `python3 -m pytest -n auto -q` ran ONCE in the primary checkout: `17639 passed, 20 skipped, 1 warning in 219.97s`, exit 0. `.agent/authored/f276-closure-suite.txt` is rewritten in place and states the previous bad set of three beside its own empty one.
- C3 is the self-use item. The generator supplied SU-024, the runner ran it against a REAL provider (ollama / muse-glimmer:latest) to the approval gate, never applied, and the run's two defect strings are recorded verbatim. NOTHING IS REGISTERED — that is round 9's reviewer-authored text.
- C4 is this handoff. No pull request was opened, STATUS was not flipped, the ledger was not rotated, no evidence job was built and `consumed_by` was NOT set.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | five payload copies + four state files; 440 insertions, 9 paths |
| C2 the repair run | done | one path; the suite is GREEN at exit 0 and the transcript says so |
| C3 the self-use item | done | seven paths; SU-024 generated, planned, run for real, defects recorded |
| C4 handoff | done | this file |
| G1 transport + state | done | 9 readings, every one True; saved block matches the delegation digest |
| G2 the UI build | done | exit 0, `✓ built in 1.45s`, `git status --porcelain` EMPTY afterwards |
| G3 the repair run | done | exit 0 from the process, `17639 passed, 20 skipped`; bad set EMPTY; 0 still bad of 3, 0 newly bad |
| G4 the canary | done | `42 passed in 132.99s (0:02:12)`, exit 0, run AFTER the real self-use job |
| G5 push, tree, job leftovers | done | pushed; tree EMPTY; no `.agent/STOP`; job branches 38 → 39, worktrees 2 → 3 |
| R-1006 | **resolved** | `Done: R-1006` written by the reviewer in P2 and applied at C1 |
| R-1003 | resolved in round 6 | untouched this round |
| R-1004 | open | Medium, re-assigned to F282 by round 9; not fixed here |
| R-1005 | open | Medium, re-assigned to F282 by round 9; not fixed here |
| SU-024 defect string 1 | recorded, NOT registered | `job c1dba9c3d7874968 (stopped): stop_reason=budget_exhausted:max_provider_calls; stop_source=budget` |
| SU-024 defect string 2 | recorded, NOT registered | `T001 (pending): final_status=stopped` |

## Commits

### b926615b F276 R8 C1: the round 8 bookkeeping
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r8-block.md | +246/-0 | byte copy of P1, the step block |
| .agent/authored/f276-r8-decisions.md | +58/-0 | byte copy of P3 |
| .agent/authored/f276-r8-ledger.md | +4/-0 | byte copy of P2 |
| .agent/authored/f276-r8-plan.md | +43/-0 | byte copy of P4 |
| .agent/authored/f276-r8-prose-slips.md | +2/-0 | byte copy of P5 |
| .agent/decisions.md | +58/-0 | DECISION F276 D9 appended |
| .agent/live_review.md | +4/-0 | round 7 verdict PASS + `Done: R-1006` |
| .agent/plan.md | +23/-22 | rewritten to round 8 |
| .agent/prose_slips.md | +2/-0 | two dated lines |

Insertions by `git show --numstat`: **440**, under 500.

### fd23710f F276 R8 C2: the integration gate's repair run
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-closure-suite.txt | +56/-39 | the green transcript replaces the red one, same path |

Insertions by `git show --numstat`: **56**, under 500.

### 8039555d F276 R8 C3: the self-use item
| Path | +/- | Reason |
|------|-----|--------|
| .agent/selfuse_f276/SU-024.md | +7/-0 | the job file the planner rendered |
| .agent/selfuse_f276/execution_config.json | +1/-0 | which provider actually ran |
| .agent/selfuse_f276/job_plan_state.txt | +7/-0 | the returned JobPlan's state |
| .agent/selfuse_f276/queue_entry_and_job_file.txt | +8/-0 | the entry and the job file path |
| .agent/selfuse_f276/run_defects.txt | +9/-0 | every defect string, verbatim |
| .agent/selfuse_f276/self_use_run_console_transcript.txt | +43/-0 | the full console transcript of the run |
| scripts/self_use_queue.json | +8/-0 | the generated pending entry only; `consumed_by` NOT set |

Insertions by `git show --numstat`: **83**, under 500.

### (this commit) F276 R8 C4: the round 8 handoff
A handoff cannot table the commit that writes it (R-0149 pattern). Its path set is exactly `.agent/handoff.md`.

## External actions

| Command | Outcome |
|---------|---------|
| `git push origin feature/f276-data-root-hygiene` | performed at G5, after this commit; the reading is in the round report |
| `cd apps/ui && npm run build` | exit 0, `✓ built in 1.45s`; writes only the gitignored `apps/ui/dist` |
| self-use job `c1dba9c3d7874968` | a REAL job: created branch `remedy/job-c1dba9c3d7874968` and a worktree under `.remedy-wt/`, both LEFT ALONE by design |
| `gh` | never run. No pull request was created, edited or merged. |
| worktree add / remove | none by this worker; the only new worktree is the self-use job's own |

## Verification

**G1 TRANSPORT AND STATE, at C1** — exit 0, 9 readings, every one True.

    True  .agent/authored/f276-r8-block.md == payload block.md
    True  .agent/authored/f276-r8-ledger.md == payload ledger.md
    True  .agent/authored/f276-r8-decisions.md == payload decisions.md
    True  .agent/authored/f276-r8-plan.md == payload plan.md
    True  .agent/authored/f276-r8-prose-slips.md == payload prose_slips.md
    True  .agent/live_review.md == 9fb2ab65 bytes + ledger.md bytes
    True  .agent/decisions.md == 9fb2ab65 bytes + decisions.md bytes
    True  .agent/prose_slips.md == 9fb2ab65 bytes + prose_slips.md bytes
    True  .agent/plan.md == plan.md bytes
    readings: 9
    all True: True
    SAVED BLOCK on disk : lines 246  sha256 20aef44c5d1717d58e91b42ff30600351acd09f7f6a370a9d03baad30cf1da59
    DELEGATION message  : lines 246  sha256 20aef44c5d1717d58e91b42ff30600351acd09f7f6a370a9d03baad30cf1da59

**G2 THE UI BUILD, at C2 and BEFORE the suite run** — exit 0.

    COMMAND: npm run build
    CWD: /home/decodeux/Repos/remedy/apps/ui
    EXIT CODE FROM THE PROCESS: 0
    last line: ✓ built in 1.45s
    git status --porcelain immediately afterwards: (no output — EMPTY)

No `npm install` was run and none was needed; the build took 1.45s against the `node_modules` already in this checkout, matching the reviewer's own measurement of `built in 1.41s`.

**G3 THE REPAIR RUN, at C2** — exit 0, taken from the subprocess object, never from a pipe.

    COMMAND: python3 -m pytest -n auto -q
    CWD: /home/decodeux/Repos/remedy
    EXIT CODE FROM THE PROCESS: 0
    WALL CLOCK SECONDS: 304.96
    17639 passed, 20 skipped, 1 warning in 219.97s (0:03:39)

    BAD NODE IDS: none
    (searched mechanically over the captured output for `^FAILED `, `^ERROR `,
     `=== FAILURES ===` and `=== ERRORS ===` — zero matches)

    THE SHRINKING RULE, as numbers:
      of round 7's 3 bad nodes, still bad now : 0
      nodes bad now that were not bad then    : 0
    Rule 2 asks the first to be smaller than 3 and the second to be zero. 0 < 3
    and 0 == 0, so the bad set strictly shrank — to empty — with no node newly bad.

The two runs reconcile: 3 + 17636 + 20 = 17659 outcomes then, 17639 + 20 = 17659 now.

**G4 THE CANARY, after C3, in the primary checkout** — exit 0.

    COMMAND: python3 -m pytest tests/cli/test_golden_path.py -q
    CWD: /home/decodeux/Repos/remedy
    EXIT CODE FROM THE PROCESS: 0
    42 passed in 132.99s (0:02:12)

Run deliberately AFTER the real self-use job, which is the state a canary exists to check.

**G5 PUSH, TREE AND WHAT THE JOB LEFT, after C4** — the readings are in the round report; the push, the empty `git status --porcelain`, the absent `.agent/STOP`, the full `git worktree list` and the job-branch counts taken before C3 and after C4 (38 and 39) are all recorded there.

**THE OPEN SET**, measured at HEAD by both readings:

    count_open_findings() -> 16
    OPEN BY DISTINCT ID   -> 16
    severities: High 0, Medium 9, Low 7
    R-1006 in the Done set: True

Registrations added over `9fb2ab65..HEAD`: **0** lines matching `^\+- R-`. Resolutions added: exactly one, `Done: R-1006`, which is P2's and reviewer-authored.

## Authored-text proofs

Five reviewer-authored texts were applied this round; each committed `.agent/authored/` copy was compared to its payload on disk byte for byte, and all five are equal (G1 readings 1–5). Digests, identical on both sides:

| Payload | Lines | sha256 |
|---------|-------|--------|
| P1 block.md | 246 | `20aef44c5d1717d58e91b42ff30600351acd09f7f6a370a9d03baad30cf1da59` |
| P2 ledger.md | 4 | `6ba01f3ef232816e86c7850f6ddf4799d68273a40584ff04e8d090f5bb99cb93` |
| P3 decisions.md | 58 | `7f71b167601c5d198fdd31a76c77c9ec582c2e2d517f7b4bee78394e16c114ba` |
| P4 plan.md | 43 | `8df1095f45da9ec7c42f72948caba7b06db88987fef3087f569c9437ba693b3d` |
| P5 prose_slips.md | 2 | `1a9a44a01a0d05b4f875b870ac0b9d4a849ed80a8ee0a9fb35522fe7bc512b03` |

Containment test before emission, one reading per pair, all four False as the block predicted: `.agent/live_review.md` contains P2 — False; `.agent/decisions.md` contains P3 — False; `.agent/prose_slips.md` contains P5 — False; `.agent/plan.md` contains P4 — False.

## The self-use outcome

Closure precondition 6, consumed by this round and recorded for round 9 to register.

- The queue held NO pending item: `pending_self_use_items()` answered `()`, length 0.
- `generate_and_append_if_empty()` answered `SU-024`, "Address ledger finding R-0662", provenance `generated (self-use-generator tier 1, ledger scan, R-0662)`. It is NOT None, so the track is not exhausted.
- `run_next_self_use_item(dest_dir=Path(".agent/selfuse_f276"), repo_path=".")` was called with NO `builder_name` and NO `reviewer_name`, so the runner resolved its own roles.
- The resolved `execution_config` records `builder='ollama', builder_source='cli', reviewer='ollama', reviewer_source='cli'` on `muse-glimmer:latest` at effort `medium`. A real provider ran; nothing was faked.
- The returned `JobPlan`: `state = stopped`, `job_id = c1dba9c3d7874968`, `error = ''`. Never applied.
- `describe_self_use_run_defects(result)` returned a tuple of length **2**. Both strings, verbatim:

      job c1dba9c3d7874968 (stopped): stop_reason=budget_exhausted:max_provider_calls; stop_source=budget
      T001 (pending): final_status=stopped

- NOTHING WAS REGISTERED. No `- R-` line and no `Done:` line beyond P2's was written this round. Turning these two strings into R-id findings is reviewer-authored text and is round 9's first commit.
- `consumed_by` for SU-024 is still `""`. Precondition 6 puts that edit in the closure commit.

## Deviations & assumptions

1. **The UI build ran TWICE, and the second run is the one G2 reports.** The first invocation was made directly and its exit code was therefore only inferable from the absence of an error rather than read from the process. Rather than report an inferred code, the build was re-run once through the same no-pipe subprocess wrapper the suite uses, and G2's `EXIT CODE FROM THE PROCESS: 0` and last line `✓ built in 1.45s` are that second run's. The build is idempotent and writes only the gitignored `apps/ui/dist`; `git status --porcelain` was EMPTY after it. Constraint 8's ONCE rule binds the full suite, not the build, and the full suite ran exactly once. Declared because the block says "Report its exit code and its last line" and a reader is entitled to know which of two runs the numbers belong to.

2. **The self-use console transcript is named `self_use_run_console_transcript.txt`, not `run_transcript.txt`.** The block orders "the full transcript of the run" recorded under `.agent/selfuse_f276/`, each file "named for what it holds". The obvious name is ignored by this repository: `.gitignore` line 230 is a bare `run_transcript.txt`, which matches that basename in EVERY directory, so the file staged as untracked-and-ignored and would have been silently absent from C3. `.gitignore` is outside this round's change set, so the file was renamed instead of the ignore rule edited. `git check-ignore -v .agent/selfuse_f276/run_transcript.txt` reported `.gitignore:230:run_transcript.txt`, which is the measurement behind this.

3. **No finding is registered for either self-use defect string, by instruction.** They are recorded verbatim in `.agent/selfuse_f276/run_defects.txt` and quoted above and in the round report. This is the block's own order, declared here because a reader auditing precondition 6 will look for R-ids and must know why there are none yet.

4. **The self-use job left a branch and a worktree behind.** `remedy/job-c1dba9c3d7874968` and `/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968`. The job-branch count went 38 → 39 and `git worktree list` went 2 → 3 entries. A job that does not complete retains both BY DESIGN; neither was deleted and neither makes the primary checkout dirty — `git status --porcelain` there is empty.

5. **The commit sequence was C1, C2, C3, C4 in exactly that order**, with no extra commit, none dropped and none reordered.

6. **No path outside the change set was written.** `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F276.md`, `docs/agents/planner_reviewer_prompt.md`, `.agent/candidates.md` and the `consumed_by` field of `scripts/self_use_queue.json` are all untouched. `.agent/STOP` was read from disk before the first commit and does not exist.

7. **No destructive verification was ordered and none was performed**; no disposable worktree was created by this worker.

## Next

Round 9, the closure's last round, authored by the reviewer: book round 8's verdict and register the two SU-024 defect strings as R-ids; `remedy integrity check --json`; the ledger rotation as its own commit; re-assign every still-open finding to F282 after that rotation; the §3 checklist consolidation pass; the evidence job and a fresh review package; then the STATUS `[x]` flip with the README counters and the `consumed_by` edit in ONE commit as the last commit on the branch, and the pull request into `main`.
