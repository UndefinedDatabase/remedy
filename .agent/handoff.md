# Handback — F133 round 4

## Session

SESSION 1 of feature F133 · round 4 · rounds so far 4.

Context self-assessment: every file this round's commits touch was read whole before editing (the
trust module, the stats view and both of their test files as round 3 left them, the plan-show
command and its test file, the calibration band-note helper held up as the model for a note that
never fails the view, the execution config and estimate-calibration modules named in the bundle,
and the acceptance test's model), the two registrations and DECISION F133 D4 were read from the
committed file after C1 rather than from the prepared snapshot, and every number below (insertion
counts, test counts, gate readings, the open-finding count) was produced by running the thing, not
recalled.

Fortschritt: ~75 % (T001, T002 and T003 landed · the closure sequence open) — Schätzung

For the operator: this round closed out the trust feature's building work. One real bug was fixed:
the clear-leader comparison used to refuse a leader for the most common real-world win margins,
because it compared two fractions in raw floating point and a mathematically exact ten-point lead
often reads as a hair less than ten due to ordinary rounding; it now compares in a much finer,
whole-number unit instead, so an honest ten-point lead is never refused by that rounding. Three
other behaviours that mutation testing had shown were already correct, but unguarded by any test,
each now have one. The feature's last planned piece also landed: when a person looks at a job's
plan before it runs, and the project's own history clearly shows another model does that job's role
better than the model the job is actually configured to use, the plan view now says so in one
sentence and says plainly that nothing was changed — the system never swaps models on its own, and
adopting a different one is still a configuration and documentation step for a person to take. A
guard now also watches, by construction, that the four trust figures and the module's own name
never grow a second home anywhere else in the codebase. Last, a full dress rehearsal of the whole
feature — a realistic constructed history, read through the actual command line, both for the
trust report and for the plan view — now exists and passes, and the feature's documentation page no
longer describes anything as still open that this round finished.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five prepared paths copied and proved byte-identical, then committed |
| C2 | done | the margin compared in whole hundredths of a point; the two exact-margin tests read red on the unfixed module and green after; the just-above case and the other two R-1433 survivor tests were already green, unfixed |
| C3 | done | `trust_routing_note` in the trust home; its caller in `job plan-show`, printed after the heading lines, never failing the view |
| C4 | done | the note's five conditions tested, the one-home guard reading `git ls-files`, the plan-show tests (contradiction fixture, none without one, none on a malformed setting, JSON unchanged, the evidence diff) |
| C5 | done | the command-line end-to-end (`tests/regression/test_f133_acceptance.py`), the docs page and its index row brought up to date; the retired-word guard needed no new registration |
| C6 | done | two `Landed:` paragraphs appended, no `Done:` line |
| C7 | done | this handback |
| R-1432 | done | `trust_leader`'s margin compared in whole hundredths of a point; red on the unfixed module, green after |
| R-1433 | done | one test per survivor: a partly-priced cost sum, the margin's `<=` boundary (shared with R-1432's tests), `--role`'s text-view recommendation filter |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, last line `ALL True` |
| Gate 2 | done | ruff over the 6 touched `.py` files: exit 0, `All checks passed!` |
| Gate 3 | done | exit 0, `10271 passed, 5 skipped`, no FAILED/ERROR, no "process(es) behind" line |
| Gate 4 | done | `fail_count` 0 |
| Gate 5 | done | `13` |
| Push | done | `git push origin feature/f133-provider-trust-score` run immediately after this commit |

## Range

Review of `0ccfa43d4`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `42503c9f4` F133 R4 C1: book round 3, resolve R-1429 to R-1431, register R-1432 and R-1433, DECISION F133 D4, the plan, the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f133-r4.md` | +126/-0 (new) | byte copy of the block, proved equal to it |
| `.agent/decisions.md` | +12/-0 | DECISION F133 D4 appended |
| `.agent/live_review.md` | +9/-3 | round 3's FAIL Gate entry booked, the three Landed lines replaced by Done, R-1432 and R-1433 registered |
| `.agent/plan.md` | +5/-5 | rewritten for round 4 |
| `.agent/prose_slips.md` | +1/-0 | one line for the round 3 reviewer's undeclared guard registration |

Every one of the five is a byte-for-byte copy of its prepared `c1-*` file under
`.remedy-wt/f133-r4/prep/`, each proved equal by a sha256 comparison before staging.

### `db1a87d73` F133 R4 C2: the clear leader at exactly the margin, and the three surviving mutations tested

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_trust_score.py` | +14/-1 | R-1432: `trust_leader` compares the lead and the margin in whole hundredths of a point (`_hundredths_of_a_point`) instead of raw floating point |
| `tests/orchestration/test_model_trust_score.py` | +49/-2 | the exact-margin test rewritten with 17 of 20 against 15 of 20, a second such pair (7 of 10 against 6 of 10), a just-above-the-margin case, and two R-1433 survivor (1) tests (a partly priced sum falling to `tokens`, and to `unknown` when a token count is also missing) |
| `tests/cli/test_stats_trust_cmd.py` | +18/-2 | `_row` extended with optional `role`/`model` (back-compatible), and R-1433 survivor (3): `--role` keeps the text view's recommendation to one role |

### `ba0d7d7cb` F133 R4 C3: trust suggests otherwise — the informational routing note and its caller in job plan-show

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_trust_score.py` | +28/-0 | `trust_routing_note(table, role, configured_model)` (DECISION F133 D4 (1)), the words exactly |
| `apps/cli/commands/job_plan_cmd.py` | +42/-0 | `_trust_routing_notes(job)` (D4 (2)): one line per role, builder then reviewer, printed after the plan's heading lines; never fails the view |

### `f4e1547d5` F133 R4 C4: the routing note's tests, the evidence diff and the one-home guard

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_model_trust_score.py` | +91/-0 | `TestTrustRoutingNote` (no leader, the configured model the leader, thin, absent, empty, the whole line) and `TestOneHomeGuard` (D4 (4), reading `git ls-files`) |
| `tests/cli/test_job_plan_cmd.py` | +109/-0 | `TestPlanShowTrustRoutingNote`: the note on a contradiction fixture, none when the configured model already leads, none and no failure on a malformed trust setting, the JSON unchanged, and the evidence diff (the job record's bytes and its configured models identical before and after) |

### `5d394e749` F133 R4 C5: the end-to-end through the command line, and the trust score page completed

| Path | +/- | Reason |
|---|---|---|
| `tests/regression/test_f133_acceptance.py` | +158/-0 (new) | a strong, a weak and a thin builder model in a constructed history; `stats trust` in text and JSON with `n` and the window on every figure, the recommendation naming the strong model; `job plan-show` on the weak builder printing the note, the strong builder printing none, the job record unchanged |
| `docs/system/model-trust-score-v1.md` | +36/-10 | the status banner rewritten to built; two new sections, "The informational routing note" and "The one-home guard"; the recommendation section's trailing sentence and the deliberate-absences bullet about the note not yet existing both removed |
| `docs/README.md` | +1/-1 | the page's index row rewritten to name the routing note as built, not open |

### `2a5bfc944` F133 R4 C6: Landed lines for R-1432 and R-1433

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | two `Landed:` paragraphs, each naming what changed and its commit; no `Done:` line |

## External actions

- Open PR Gate was run at session start: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  returned `[]`, and the branch was already `feature/f133-provider-trust-score`, so no new branch
  was created and no merge was needed.
- `git push origin feature/f133-provider-trust-score` → run immediately after this commit.
- No pull request created (the block orders none this round). No worktree added or removed.

## Verification

Interpreter: the repository's configured Python 3. All five gates were taken once, on `2a5bfc944`
(this commit's parent), after C6 and before this commit, per the block.

| Command | Exit | Decisive output |
|---|---|---|
| `git -C <repo> status --porcelain` | 0 | empty |
| `python3 .remedy-wt/f133-r4/prep/verify.py .` | 0 | every line `True`; last line `ALL True` |
| `python3 .remedy-wt/f133-r4/prep/ruff_touched.py .` | 0 | `ruff over 6 files: exit 0` / `All checks passed!` |
| `python3 .remedy-wt/f133-r4/prep/run_selection.py . .remedy-wt/f133-r4-worker/selection-output.txt` | 0 | `paths 214` / `10271 passed, 5 skipped, 1 warning in 102.69s (0:01:42)`; no FAILED, no ERROR, no "process(es) behind" line |
| `python3 -m apps.cli.main integrity check --json` | 0 | `"fail_count": 0, "ok": true, "passed": true` |
| `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` | 0 | `13` |

Gate 3's three `SKIPPED` lines, printed as they are:
```
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Before C2's fix was applied, the two new exact-margin tests were run against the unfixed module and
recorded red: `test_the_leader_at_exactly_the_margin` and `test_a_second_pair_at_exactly_the_margin`
both failed with `AssertionError: assert 'no_margin' == 'leader'`; every other test in both files,
including the other R-1433 survivor tests (already correct without a code change), passed — 2
failed, 60 passed. After the fix, the full pair of touched test files read 62 passed, 0 failed.

## Authored-text proofs

C1's five paths are all reviewer-authored text applied this round. Each was copied from its
prepared `c1-*` file under `.remedy-wt/f133-r4/prep/` and proved byte-identical by a sha256
comparison immediately after the copy, before `git add`; all five read `True`. The new file
`.agent/authored/f133-r4.md` was separately checked: `wc -l` reads `126` and its sha256 is
`bd994d93e0fc14c42c0b977049c6ee98bcdcc7210f44da2e2f31372c1e2b8dea`, identical to both
`.remedy-wt/f133-r4/prep/block.md`'s own `wc -l` and sha256 — confirmed by `verify.py`'s own
"the saved block equals block.md" check, which read `True`.

## Deviations & assumptions

1. No deviation from the block's ordered commit sequence: seven commits, C1 through C7, each
   exactly the paths and content its own heading names.
2. R-1433's survivor (2) — the margin's `<=` boundary — is held by the same `trust_leader` tests
   R-1432's own repair required (`test_the_leader_at_exactly_the_margin` and
   `test_a_second_pair_at_exactly_the_margin`), rather than by a fourth, separate test: the two
   findings share one code path and the registration's own text says the margin survivor's test is
   "written with R-1432's repair." This is named here because it is a reading of how one test
   serves two registrations, not because any test was skipped.
3. R-1433's survivors (1) and (3) were already correct on the unfixed module before this round (the
   mutations the registration names never existed in the committed code, only in the reviewer's
   disposable-worktree trial); their new tests therefore read green on both the unfixed and the
   fixed module, and only R-1432's two tests were run red-then-green, which is recorded above under
   Verification.
4. `tests/docs/test_retired_promote_word.py` needed no new registration this round: nothing written
   matched the guard's `promot` pattern except the already-registered "promotion rule" phrase this
   round left untouched, confirmed by running the guard's own five tests, all green, with no edit
   to its map.
5. No change outside the paths named per commit. No `Done:` line was written anywhere, only
   `Landed:`. No mutation red-proof was run (the reviewer's). The full suite was not run; only the
   ordered selection plus every `tests/test_*.py`, once, after C6.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 4's verdict in the next round's first commit.
4. The closure sequence: the integration gate.

Operator questions open: 0. Open findings: 13.
