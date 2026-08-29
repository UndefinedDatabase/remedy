# Handback — F040 · SESSION 1 · round 3 — THE DIGEST COMPOSITION MODULE (T001 PART 1)

> Written by the WORKER in C6, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe.

## Session

SESSION 1 of feature F040 · round 3 · rounds so far 3.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed.

## Range

Review of `8e013dc5`..`HEAD` on branch `feature/f040-completion-digest`. The
base is round 2's handback commit and was the tip of the branch when this round
opened. No new branch was cut, no pull request opened, nothing merged, nothing
force-pushed.

## Commits

### f8ebe0b3 chore(f040): save the round 3 step block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f040-r3.md` | +321 −0 | C0a — the block, copied with `shutil.copyfile` from `.remedy-wt/f040-r3-block.md`, never retyped |

### e738d51d chore(f040): mirror the round 3 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +263 −291 | C0b — the same bytes, the same `shutil.copyfile` call |

### 4f721ca6 docs(f040): retarget the plan at the composition module

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +18 −18 | C1 — rewritten from slice PLAN3; the first substantive commit, ahead of the ledger append, per constraint 3 |

### 3c34134a docs(f040): book the round 2 verdict, R-0752 and decision D5

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +6 −0 | C2 — slice RECORD3 appended after one separator newline; three paragraphs, append-only |

### d78097f3 docs(f040): record the three round 2 prose slips

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +6 −0 | C3 — slice SLIP3 appended with NO separator of its own; it opens with a blank line by construction |

### b13baa69 feat(f040): compose the job digest from the report and the inbox

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_digest.py` | +239 −0 | C4 — the new pure composition, written from the SPEC; `JOB_DIGEST_VERSION`, `build_job_digest`, and the four private helpers behind it |

### 0e412274 test(f040): pin the digest envelope and its one-source action

| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_job_digest.py` | +492 −0 | C5 — 40 tests over the four named state shapes, written from the SPEC |

### C6 — this file (self-reference)

A handback cannot table the commit that writes it (R-0149 pattern). C6 rewrites
`.agent/handoff.md` and touches nothing else; its insertion count is the one
reading in this table the reviewer must take for itself.

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add --detach .remedy-wt/f040r3/wt-g3 HEAD` | exit 0 — G3's negative control |
| `git worktree remove --force .remedy-wt/f040r3/wt-g3` | exit 0 — removed; `git worktree list` then held the primary checkout alone |
| `git worktree add --detach .remedy-wt/f040r3/wt-g6 HEAD` | exit 0 — G6's mutation red-proof |
| `git worktree remove --force .remedy-wt/f040r3/wt-g6` | exit 0 — removed; `git worktree list` then held the primary checkout alone, and the directory is gone from disk |
| `git reset --soft HEAD~1` + `git restore --staged` | exit 0 — C5 was first committed at +501 insertions, one over the AGENTS.md cap; the commit was unwound before any push and re-made at +492. See the deviations. |
| `git push -u origin feature/f040-completion-digest` | run after C6; outcome in the round report |

No pull request was created, edited or merged. No `gh` command was run. The
`remedy` console script is denied in this sandbox and was never invoked; nothing
this round needed it.

## Verification

One line per gate, every exit code REAL from `subprocess.run(...).returncode`.

| Gate | At | Command | REAL exit |
|------|----|---------|-----------|
| G1 TRANSPORT | C0b | `python3 -B .remedy-wt/f040r3/g1.py` | 0 |
| G2 THE PLAN | C1 | `python3 -B .remedy-wt/f040r3/g2.py` | 0 |
| G3 THE RECORD APPEND | C2 | `python3 -B .remedy-wt/f040r3/g3.py` | 0 |
| G3 NEGATIVE CONTROL | C2 | `python3 -B .remedy-wt/f040r3/g3_control.py` | 0 |
| G4 THE LEDGER AND THE SLIPS | C2, C3 | `python3 -B .remedy-wt/f040r3/g4.py` | 0 |
| G5 THE MODULE | C4 | `python3 -B .remedy-wt/f040r3/g5.py` | 0 |
| G6 THE TESTS AND THE RED PROOF | C5 | `python3 -B .remedy-wt/f040r3/g6.py` | 0 |
| G7 THE SUITES AND THE TREE | C5 | `python3 -B .remedy-wt/f040r3/g7.py` | 0 |

**G1 TRANSPORT, at C0b.** One sha256 over three files, all three EQUAL at
**24441 bytes**, sha256
`f43b5ab338bf700e879df1a1c3ab1cb00e918051dbaa20f82ff7c51e03a0ab8f`:
`.remedy-wt/f040-r3-block.md`, `git show HEAD:.agent/authored/f040-r3.md` and
`git show HEAD:.agent/last_block.md`. Both `git show` calls returned 0. This
block states no expected digest; the reviewer holds the original.

**G2 THE PLAN, at C1.** The committed `.agent/plan.md` is BYTE-EQUAL to PLAN3:
both 1815 bytes at sha256
`752f9656a51dd4d485c6d637043a6242a4336cc021d157a71de543e62bbe6c45`. 38 lines
(under 50). `## Goal` present, `## Next Steps` present.

**G3 THE RECORD APPEND, at C2.** The pre-commit length was re-measured here, not
taken from the block: `.agent/live_review.md` read **1655733** bytes at
`8e013dc5` (sha256 `e73ff7aa9b016b3569ca82c6a53b1b1e87fb8ef6c8eb015f5bf1341d54a4988f`),
which is the number the reviewer reported. RECORD3 is 6933 bytes. The
arithmetic `1655733 + 1 + 6933 = 1662667` equals the committed length exactly.
Two readings, both taken with the base and the slice read from `.remedy-wt/`
scratch rather than from the file under test:

- (a) WHOLE RECONSTRUCTION against the ENTIRE committed file — `base + b"\n" +
  RECORD3 == committed` — **True**.
- (b) PARAGRAPH ORDER — **N counted by the script as 3**, and the last three
  blank-line units of the committed file equal RECORD3's three paragraphs IN
  ORDER: `Gate: F040 R2 — …`, `- R-0752 — Low, …`, `DECISION F040 D5 — …`, each
  **True**.

NEGATIVE CONTROL, in the disposable worktree
`.remedy-wt/f040r3/wt-g3`: byte 1655774 — inside the FIRST appended paragraph,
which spans bytes 1655734..1658988 — was flipped from `U` to `u`. Both readings
REJECTED the flipped file, REAL exit **1**, with (a) False and (b) False on
paragraph 1 while paragraphs 2 and 3 still matched, which is the discriminating
detail. The unflipped bytes were then re-read in the same worktree and both
readings ACCEPTED, REAL exit **0**. The worktree was removed (exit 0) and
`git worktree list` printed the primary checkout alone.

**G4 THE LEDGER AND THE SLIPS, at C2 and C3.** Measured with `git show HEAD:…`
against the scratch copies of the base bytes:

- distinct `^- R-\d+ — ` ids: **312 → 313**, ADDED `['R-0752']`, REMOVED `[]`.
- resolved ids: the record's own convention is `^Done: R-\d+` (55 lines, 53
  distinct ids at the base) — **53 → 53**, ADDED `[]`. The first draft of this
  gate used `^- R-\d+ — RESOLVED`, which matches nothing in this file and would
  have been a blind reading; it was corrected to the real pattern before the
  number above was taken.
- distinct `^DECISION F040 D\d+ — `: `['D1','D2','D3','D4']` →
  `['D1','D2','D3','D4','D5']`, ADDED `['D5']`.
- `^Gate: F040 R2 — ` lines: **1**.
- `^Done: R-0570` lines: **0**. `^Done: R-0752` lines: **0**.
- `.agent/prose_slips.md`: the committed file EQUALS the pre-commit bytes
  followed EXACTLY by SLIP3 with no separator of its own —
  `32312 + 1085 = 33397` and the committed file is 33397 bytes at sha256
  `133623a0bb553a0a816d4451a7bebb39293cdb6761bedcaaf79df50c8da29f2b`. Lines
  **284 → 290**: the six lines are SLIP3's own, which opens with the blank
  separator every other entry in that file carries and which the R2 block's G4
  had forbidden.

**G5 THE MODULE, at C4.** Three commands, each REAL exit **0**:
`ruff check packages/orchestration/job_digest.py` ("All checks passed!");
`python3 -m compileall -q packages/orchestration/job_digest.py`; and the import
probe, which reports `JOB_DIGEST_VERSION = 1` and the envelope's top-level key
set for a minimal fake job as
`['cost','decisions','headline','job_id','ownership','primary_action','state','version']`
— EXACTLY the eight keys the SPEC names, for the fake job and again for a bare
`object()`.

PURITY, measured rather than asserted.
`grep -n "open(\|Path(\|subprocess\|socket\|requests\|urllib"
packages/orchestration/job_digest.py` returned **one** hit:

    4:writes no file, starts no subprocess and opens no socket: it reads the report's

That hit is line 4 of the module DOCSTRING — the sentence declaring the absence,
not code. There is no other hit: the module opens no file, builds no `Path`,
starts no subprocess and touches no socket, HTTP client or URL library. Its only
imports are `typing.Any` and four named seams —
`decision_inbox.build_decision_inbox`, `decision_inbox.decision_urgency`,
`run_report.{NOT_RECORDED, ReportSources, build_report_sources,
recommended_next_action}` at module level, and, inside the one guarded cost
helper, `budget_guard.{BudgetCounters, counters_from_persisted,
decode_persisted_budget_actuals}` and `pingpong_job.load_job_plan`, which is the
function-local form `run_report._evidence_sources` uses at the same seam.

This round's path set, from `git diff --name-only 8e013dc5 HEAD` (exit 0), is
exactly the six change-set paths plus this file:
`.agent/authored/f040-r3.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md`,
`packages/orchestration/job_digest.py`, `tests/orchestration/test_job_digest.py`.
**`packages/orchestration/ui_server.py` is NOT in this round's path set.**
Nothing under `apps/` changed and no existing module under `packages/` was
edited.

**G6 THE TESTS AND THE RED PROOF, at C5.** In the primary checkout,
`python3 -m pytest tests/orchestration/test_job_digest.py -q` gave REAL exit
**0**, **40 passed**.

Then, inside the disposable worktree `.remedy-wt/f040r3/wt-g6` at C5, with
`__pycache__` purged before every run and `python3 -B` throughout — the
UNMUTATED CONTROL REPORTED FIRST, because a colour with no baseline is not
evidence:

| Step | REAL exit | Result |
|------|-----------|--------|
| UNMUTATED CONTROL | **0** | 40 passed |
| ONE MUTATION | **1** | **6 failed, 34 passed** |
| RESTORED bytes | **0** | 40 passed |

The mutation replaced the single line

    action = recommended_next_action(sources)

with

    from packages.orchestration.run_report import NextAction; action = NextAction(rule_id="all-green", action="Nothing to do.")

— one line for one line, asserted unique in the file before substitution. The
six failures are exactly the one-source tests:
`test_the_primary_action_is_the_reports_own_recommendation` for all four shapes,
`test_the_four_shapes_reach_four_different_rules` (which reported
`{'budget_stopped': 'all-green'} != {'budget_stopped': 'blocked-failed'}` and the
same for the blocked and mid-run shapes) and
`test_the_blocked_shape_reaches_the_open_decision_rule`. Nothing else moved: the
34 other tests stayed green, so the mutation breaks the one-source property and
NOTHING ELSE, which is what makes it a proof that the property is pinned rather
than merely described. The worktree path was
`/home/decodeux/Repos/remedy/.remedy-wt/f040r3/wt-g6`; it was removed with
`git worktree remove --force` (exit 0), `git worktree list` then printed the
primary checkout alone, and the directory no longer exists on disk.

**G7 THE SUITES AND THE TREE, at C5.** Six suites, serially, each its own REAL
exit code:

| Suite | REAL exit | Result | Reviewer's base count |
|-------|-----------|--------|-----------------------|
| `tests/orchestration/test_run_report.py` | 0 | 81 passed | 81 |
| `tests/orchestration/test_decision_inbox.py` | 0 | 43 passed | 43 |
| `tests/ui_server/` | 0 | 508 passed | 508 |
| `tests/orchestration/test_integrity_gate.py` | 0 | 16 passed | 16 |
| `tests/regression/test_resource_safety.py` | 0 | 21 passed | 21 |
| `tests/cli/test_golden_path.py` (canary) | 0 | 42 passed | 42 |

Every count matches the base exactly. Then the tree:
`git status --porcelain` returned 0 with **0 lines (EMPTY)**;
`git ls-files --others --exclude-standard` returned 0 with **count 0**.

Per-commit insertions, C0a through C5, from `git diff --numstat <sha>^ <sha>`:

| Commit | Insertions |
|--------|-----------|
| f8ebe0b3 C0a | 321 |
| e738d51d C0b | 263 |
| 4f721ca6 C1 | 18 |
| 3c34134a C2 | 6 |
| d78097f3 C3 | 6 |
| b13baa69 C4 | 239 |
| 0e412274 C5 | 492 |

Every one is under 500.

**SUPPLEMENTARY, not ordered by the block but run because `job_digest.py` is a
NEW file under `packages/orchestration/` and constraint 8 names repo-wide guards
that name no path.** Thirteen further suites, each its own REAL exit code, every
one **0**: `tests/test_no_interactive_guard.py` 6, `tests/orchestration/test_autonomy.py`
81, `tests/orchestration/test_development_artifact_boundary.py` 18,
`tests/orchestration/test_model_aliases.py` 24,
`tests/orchestration/test_review_subject_resolution.py` 27,
`tests/test_data_paths.py` 23, `tests/test_path_utils.py` 28,
`tests/regression/test_named_bugs.py` 64 passed with 6 skipped,
`tests/orchestration/test_test_runner.py` 52,
`tests/orchestration/test_bench_never_runs_implicitly.py` 6,
`tests/ui_contracts/test_humanize_catalog.py` 9,
`tests/cli/test_project_current.py` 18, `tests/test_imports.py` 7. These are the
suites whose guards glob `packages/orchestration/*.py` or `packages/**/*.py`: the
`REMEDY_DATA_DIR` single-reader invariant, the path-utils single-implementation
invariant, the `except Exception: pass` ban, the development-artifact boundary,
the no-interactive-input guard, the model-alias ban and the `shell=True` /
`0.0.0.0` bans. The module satisfies all of them by construction, not by repair.
`ruff check tests/orchestration/test_job_digest.py` also returned 0.

## Authored-text proofs

Three reviewer-authored units were applied this round. All three were extracted
from `.remedy-wt/f040-r3-block.md` by script (`extract.py`, matching the
`<<<BEGIN NAME` / `<<<END NAME` marker lines exactly and taking the bytes
between them), never retyped, and each was applied byte for byte:

| Slice | Bytes | sha256 | Applied to | Disk-to-disk result |
|-------|-------|--------|------------|---------------------|
| PLAN3 | 1815 | `752f9656a51dd4d485c6d637043a6242a4336cc021d157a71de543e62bbe6c45` | `.agent/plan.md` (rewrite) | committed file BYTE-EQUAL to the slice |
| RECORD3 | 6933 | `378fa96dbe456baa898d6366d1dad20c41bcbe283cea3947e8487ef30c53551e` | `.agent/live_review.md` (append) | `base + "\n" + RECORD3 == committed`, whole-file |
| SLIP3 | 1085 | `b3e0c10e021b1c62c468b9384b86afb18e442a2d2450f2e95bd2bc885d4693af` | `.agent/prose_slips.md` (append) | `base + SLIP3 == committed`, whole-file, no separator added |

The block itself: `.agent/authored/f040-r3.md` and `.agent/last_block.md` are
both byte-equal to `.remedy-wt/f040-r3-block.md` at 24441 bytes, sha256
`f43b5ab338bf700e879df1a1c3ab1cb00e918051dbaa20f82ff7c51e03a0ab8f`. Both copies
were made with `shutil.copyfile`, per constraint 2.

## Deviations & assumptions

**D1 — C5 WAS COMMITTED ONCE AT +501 INSERTIONS, ONE OVER THE CAP, AND WAS
UNWOUND AND RE-MADE AT +492.** The first `tests/orchestration/test_job_digest.py`
came to 501 lines. AGENTS.md's Commit Discipline caps a commit at 500
INSERTIONS and G7 of this block asks for "every one under 500", so 501 failed
both readings and the declared-overage exception does not apply to a test file,
which is separable by construction. The commit was undone with
`git reset --soft HEAD~1` + `git restore --staged` before any push — no history
was rewritten, because nothing had left this machine — and one redundant test,
`test_the_peak_urgency_ignores_the_lesser_card`, was deleted before the file was
re-committed at 492. That test asserted the peak is neither the lesser card nor
the sum of the two; both propositions are already implied by
`test_the_peak_urgency_is_the_maximum_over_the_open_cards`, which asserts the
peak equals `(3 + 1) * 600 == 2400` exactly, while the lesser card scores 120 and
the sum 2520. No coverage was lost. The bundle's ordered sequence is otherwise
exactly as ordered.

**D2 — THE PERSISTED COST ROUTE CANNOT PRODUCE `lower_bound` OR `actual` TODAY,
SO TWO OF THE THREE COST TESTS STAND IN FOR A PRODUCER THAT DOES NOT EXIST
YET.** This is the round's one substantive finding and it is stated here rather
than buried in the test file. MEASURED at this commit:
`budget_guard.counters_from_persisted` (`packages/orchestration/budget_guard.py:793-815`)
constructs its `BudgetCounters` with EIGHT keyword arguments and none of them is
`measured_cost_usd`, `unpriced_call_count` or `priced_call_count` — the three
F104 money fields. `decode_persisted_budget_actuals` does not decode them either:
`_PERSISTED_ACTUALS_FIELDS` (line 674) is a closed set of seven names that
carries no cost at all, and an unknown field is rejected outright. So a
`BudgetCounters` built the way the SPEC dictates — the way
`run_report._evidence_sources` builds it — ALWAYS has `measured_cost_usd is
None`, `cost_description()` always returns `not-measured`, and by DECISION F040
D4's own rule the digest's `cost.basis` can only ever be `absent` in production.
`collect_counters_from_actuals` (line 545) is the only constructor that accepts
the money, and no per-job read route calls it.

The SPEC asks for three cost tests, one per basis. Two of them are therefore
unreachable through the real route. Rather than fake the seam, the two tests
persist a REAL `JobPlan` with a REAL actuals record, let the shipped
`decode_persisted_budget_actuals` and `counters_from_persisted` run for real, and
monkeypatch only a thin wrapper that `dataclasses.replace`s the three money
fields onto the counters object the shipped function returned — standing in for
the producer that will set them. Everything the digest does with that object is
the shipped code path. `test_the_persisted_cost_route_carries_no_money_today`
pins the measurement itself, so the day the route learns to price a run that
test reddens and sends the next reader here to delete the stand-in. I did not
mint an R-id: the block gives the worker no authority to register findings, and
the reviewer may judge this an unbuilt-producer gap (the F035 shape of DECISION
F040 D3) rather than a defect. It is flagged for the verdict either way.

**D3 — `_cost_counters` RETURNS AN EMPTY `BudgetCounters()` WHEN NO ACTUALS ARE
PERSISTED, RATHER THAN None.** The SPEC says "when there are no actuals at all
the value is the report's own `not-measured` spelling and the basis is
`absent`", and it also says to take the value from `counters.cost_description()`
"so the digest never re-derives a number". Those two clauses only hold together
if there IS a counters object in the no-actuals case, so the helper returns
`BudgetCounters()` — whose `cost_description()` is itself `not-measured` — and
the literal `COST_NOT_MEASURED` survives only for the branch where `budget_guard`
could not be imported at all. `test_the_absent_spelling_is_the_counters_own`
pins `COST_NOT_MEASURED == BudgetCounters().cost_description()` so the constant
cannot drift from the function it mirrors.

**D4 — THE TESTS FREEZE `decision_inbox`'s CLOCK.** `build_job_digest` takes no
`now` argument, by the SPEC's signature, so a card's age comes from the wall
clock. Two readings taken either side of a second boundary differ by one second,
which multiplies by `(blocked + 1)` in the urgency formula and would make the
peak-urgency assertions flaky rather than wrong. An autouse fixture replaces
`decision_inbox.datetime` with a `datetime` subclass whose `now()` returns a
fixed instant. Nothing the digest composes is patched; only the clock is fixed.

**D5 — THE MODULE EXPORTS FOUR CONSTANTS THE SPEC DID NOT NAME.** The SPEC names
`JOB_DIGEST_VERSION` and `build_job_digest` as "the public surface". The module
also defines `COST_BASIS_ACTUAL`, `COST_BASIS_LOWER_BOUND`, `COST_BASIS_ABSENT`,
`COST_NOT_MEASURED` and `OPEN_CARD_STATUS` at module level, and the tests import
them. They are the vocabulary DECISION F040 D4 fixes and the card status the
inbox writes; naming them beats five string literals scattered across a module
and a test file, and it is what lets the tests assert the D4 vocabulary without
restating it. The `Public API::` docstring block lists only the two the SPEC
named, which is what "the public surface" meant; the constants are spelled out
in the docstring's own prose beside them.

**D6 — THE `remedy` CONSOLE SCRIPT WAS NOT USED.** It is denied in this sandbox,
per constraint 10. Nothing this round needed it; no CLI was added.

**D7 — G4's RESOLVED-ID PATTERN WAS CORRECTED MID-GATE.** The block names the
reading ("ADDED resolved `[]`") but not the pattern. The first draft used
`^- R-\d+ — RESOLVED`, which matches ZERO lines in `.agent/live_review.md` and
would have reported an empty ADDED set from an empty base set — a gate that
cannot fail. The file's real convention is `^Done: R-\d+`, 55 lines and 53
distinct ids at the base. The gate was corrected to that pattern and re-run
before the number in the Verification section was taken. No commit was affected.

No assumption_log entry was owed: nothing here is a UI or visual deviation.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f040-r3.md` | done | `shutil.copyfile`, f8ebe0b3 |
| C0b mirror the same bytes into `.agent/last_block.md` | done | `shutil.copyfile`, e738d51d |
| C1 rewrite `.agent/plan.md` from PLAN3 | done | 4f721ca6, byte-equal, 38 lines |
| C2 append RECORD3 to `.agent/live_review.md` | done | 3c34134a |
| C3 append SLIP3 to `.agent/prose_slips.md` | done | d78097f3 |
| C4 create `packages/orchestration/job_digest.py` | done | b13baa69, written from the SPEC |
| C5 create `tests/orchestration/test_job_digest.py` | deviated | 0e412274; first committed at +501 and unwound before push, re-made at +492 — see deviation D1 |
| C6 rewrite `.agent/handoff.md` | done | this file |
| G1 TRANSPORT | done | REAL exit 0 |
| G2 THE PLAN | done | REAL exit 0 |
| G3 THE RECORD APPEND (both readings + negative control) | done | REAL exit 0; control REAL exit 1 on the flipped byte, 0 on the unflipped |
| G4 THE LEDGER AND THE SLIPS | deviated | REAL exit 0, but the resolved-id pattern was corrected mid-gate — see deviation D7 |
| G5 THE MODULE | done | REAL exit 0; the one purity hit is a docstring line |
| G6 THE TESTS AND THE RED PROOF | done | REAL exit 0; control 0 / mutated 1 (6 failed, 34 passed) / restored 0 |
| G7 THE SUITES AND THE TREE | done | REAL exit 0; six suites, all base counts matched; tree empty |

## Open findings

| Id | Severity | State |
|----|----------|-------|
| R-0570 | Low | OPEN, routed OFF this branch — its fix edits `README.md` and `tests/docs/test_docs_consistency.py`, which F040 does not own |
| R-0752 | Low | OPEN, routed OFF this branch — its fix edits thirteen feature files, none of which F040 owns; registered this round in C2 |
| R-0751 | — | FIXED at round 2 (the stale rule-table comment in `run_report.py`) |

Both open ids route to the same paydown branch. AGENTS.md's Scope Control
forbids mixing either repair into this feature branch.

## Next

The reviewer re-runs G1 through G7 at `8e013dc5..HEAD`, reads the committed diff
of `packages/orchestration/job_digest.py` and its tests, and rules on deviation
D2 — whether the unreachable `lower_bound` and `actual` bases are a finding
against `counters_from_persisted` or an unbuilt-producer gap like F035's. On a
PASS, the next round wires the digest endpoint into
`packages/orchestration/ui_server.py`'s handlers dict and adds its route tests
and goldens; nothing under `apps/` moves until T002.
