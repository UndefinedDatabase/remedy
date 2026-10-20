# Handback — F312 round 2 (book round 1, DECISION F312 D3, the listing's move, T002, T003)

## Session

SESSION 1 of feature F312 · round 2 · rounds so far 2

Context self-assessment: the session stayed inside the block and its reviewer amendment — every
prepared file was digest-checked with a Python reader before use, the structural move (C2) stayed
in its own commit, the stop after C3 on a pre-existing red test was reported rather than papered
over, and the one authorized test amendment landed in C4 exactly as the amendment named it.

State block:
Feature F312 (`[~]` in STATUS since round 1's C1), branch `feature/f312-scope-kinds`, base
`61096f5ea`. Head: this commit (C6), after C1 to C5.
Fortschritt: ~75 % (T001 to T003 landed · the answer path and the closure open) — Schätzung

## Range

Review of `61096f5ea`..HEAD (C1 to C5 below, then this commit, C6, which also carries this
handback).

## Commits

### cf2b76dd0 F312 R2 C1: book round 1, register R-1377, DECISION F312 D3, the plan
242 insertions, 9 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f312-r2.md` | +216 | byte copy of the block |
| `.agent/decisions.md` | +10 | byte copy of the prepared decisions (DECISION F312 D3 appended) |
| `.agent/live_review.md` | +4 | byte copy of the prepared ledger (round 1's booking, R-1377 registered) |
| `.agent/plan.md` | +11/-9 | byte copy of the prepared plan |
| `.agent/prose_slips.md` | +1 | byte copy of the prepared slips (one line appended) |

### 0f40f576d F312 R2 C2: the listing of the walk's jobs moves to do_summary.py (structure step)
33 insertions, 33 deletions; structural, no behaviour change. Amended once, locally, before C3 was
started (see Deviations): the first pass left `_cmd_do_order` at 162 lines against its line-neutral
pin (DECISION F055 D1); the amendment folds one existing two-line `fail(...)` call in that same
function onto one line, restoring it to 161.
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | +3/-3 | imports `do_job_task_listing` from `do_summary` instead of `do_sequence`; the amendment's one-line `fail("invalid_argument", "order must not be empty.", ...)` join, to keep `_cmd_do_order` at its pinned 161 lines |
| `docs/system/structure-ledger-v1.md` | +9/-8 | the `do_sequence.py` files bullet gains the F312 sentence naming the move, re-wrapped at 100 cols |
| `packages/orchestration/do_sequence.py` | -21 | `do_job_task_listing` removed (moved out) |
| `packages/orchestration/do_summary.py` | +20 | `do_job_task_listing` appended, byte for byte |
| `tests/cli/test_client_interface.py` | +1/-1 | the `_dict_literal_keys` call's path argument becomes `do_summary` |

### 264412f99 F312 R2 C3: an open order refused twice asks which files it means
176 insertions, 14 deletions. Amended once, locally, before the stop (see Deviations): the first
pass split two of `verify.py`'s required literal phrases across adjacent f-string lines, which
read correctly at runtime but failed the gate's literal-source-text check; the amendment rejoins
each phrase onto one line with no change in meaning.
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/do-run-v1.md` | +4 | the DECISION F312 D3 paragraph inserted right after its anchor |
| `packages/orchestration/do_scope.py` | +1/-1 | R-1377: the `ORDER_SCOPE_NAMES_FILES` comment reads "a file path" instead of "a tracked path of its own" |
| `packages/orchestration/do_sequence.py` | +20/-13 | `_first_pass_task_plan` wraps its deliverable check in `try`/`except OrderJobPlanError`, delegating a refused open order's second attempt to `scope_question.second_pass_task_plan`; `_step_shape` catches `ScopeQuestionRaised` before `OrderJobPlanError` |
| `packages/orchestration/scope_question.py` | +150 (new file) | `SCOPE_QUESTION_MARKER`, `SCOPE_QUESTION_STOP_REASON`, `scope_question_options`, `scope_question_text`, `ScopeQuestionRaised`, `raise_scope_question`, `second_pass_task_plan` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 | `packages.orchestration.scope_question` added — the reachability test asked for it |

### 6016db89b F312 R2 C4: the question after two refusals, tested
160 insertions, 2 deletions.
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_plan_approval.py` | +2/-2 | reviewer amendment 1: `test_llm_plan_holding_an_inspection_task_is_rejected`'s order becomes `Write notes.md about the repository` (kind `names_files`, confirmed before the commit) and its docstring names DECISION F312 D3; its `pytest.raises(..., match="is inspection")` and `assert list_job_plans() == []` stayed byte-identical |
| `tests/orchestration/test_scope_question.py` | +158 (new file) | `scope_question_options`/`scope_question_text` unit checks; an open order refused twice (2 calls, `ScopeQuestionRaised`, stopped job, one open decision); an open order whose second attempt passes (2 calls, planned with `style.css`); a fenced order refused once (1 call, `OrderJobPlanError`) |

### eed4fff0c F312 R2 C5: the three lab orders of 2026-10-20, walked through the real walk
175 insertions (new file).
| Path | +/- | Reason |
|---|---|---|
| `tests/regression/test_lab_orders_20261020.py` | +175 (new file) | the three lab order texts, all of kind `open`; the second walked through `apps.cli.grouped.main` (`apps.cli.main.main` itself takes no argv — see Deviations) with fake providers and a fake planner answering by model class: `milestones` shape, no failed step, every job's tasks deliver `style.css` then `index.html`; the same walk with a checking-only task planner stops the shape step and asks, naming `remedy decision resolve` |

### this commit (C6) F312 R2 C6: handback
2 files.
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file (a handoff cannot table its own commit) |
| `.agent/authored/f312-r2-amend1.md` | +23 (new file) | byte copy of the reviewer's amendment 1 (23 lines, sha256 `2a03e5f227cbcd405831a14a6d77b65f79b3c80a8fe876088a3d153ef7a9747c`, matching the amendment's own digest) |

## External actions

The push is run after this commit, so its outcome is reported in the final reply only. Before this
commit: no push, no `gh` command, no pull request (none was open at session start; none is opened
this round).

## Verification

1. Gate 1: `git status --porcelain` — empty. `python3 .remedy-wt/f312-r2/prep/verify.py .`:
   ```
   True	cf2b76dd0 single parent equal to the commit before it
   True	0f40f576d single parent equal to the commit before it
   True	264412f99 single parent equal to the commit before it
   True	6016db89b single parent equal to the commit before it
   True	eed4fff0c single parent equal to the commit before it
   True	every commit carries an F312 R2 Cn subject: 5 of 5
   True	C1 paths exactly [...]
   True	C2 paths inside its set: [...]
   True	C3 paths inside its set: [...]
   True	C4 paths all under tests/: [...]
   True	C5 paths all under tests/: [...]
   absent	C6
   True	C1 .agent/authored/f312-r2.md equals block.md
   True	C1 .agent/live_review.md equals dry-live_review.md
   True	C1 .agent/decisions.md equals dry-decisions.md
   True	C1 .agent/prose_slips.md equals dry-prose_slips.md
   True	C1 .agent/plan.md equals dry-plan.md
   True	C2 do_job_task_listing lives in do_summary.py only
   True	C2 the function's text is moved byte for byte
   True	C2 no import of do_job_task_listing from do_sequence remains:
   True	C2 ledger names the move
   True	C3 scope_question.py carries 'SCOPE_QUESTION_MARKER = "Which files does this order mean?"'
   True	C3 scope_question.py carries 'SCOPE_QUESTION_STOP_REASON = "scope_question"'
   True	C3 scope_question.py carries 'Remedy planned it twice and refused both plans; the last ref'
   True	C3 scope_question.py carries 'Answer with the names of the files you mean, separated by co'
   True	C3 scope_question.py carries 'No further planner call is made until this is answered.'
   True	C3 scope_question.py carries 'class ScopeQuestionRaised(Exception)'
   True	C3 _step_shape catches ScopeQuestionRaised
   True	C3 do_sequence.py stays under 1000 lines: 982
   True	C3 R-1377's comment is repaired
   True	C3 the guide paragraph stands right after its anchor
   True	C3 the guide is the base plus the paragraph and nothing else
   True	C3 leaves order_scope.py byte-identical (do not touch)
   True	C5 the fixture carries 'Bau jetzt eine minimale html showcase page nur zum testen'
   True	C5 the fixture carries 'Super, jetzt mach ein schickes design'
   True	C5 the fixture carries 'Bring die webseite auf prototyp niveau und füge funktionalität hinzu'
   ALL True
   ```
   (Per the reviewer's amendment note: at gate time C6 reads `absent`, so `verify.py`'s hardcoded
   `C6` path set — `.agent/handoff.md` alone — was never checked against this commit's actual two
   paths; the reviewer accounts for the added amendment copy.)
2. Gate 2: `python3 -m ruff check` over every Python file C2 to C5 touched (`apps/cli/commands/do_cmd.py`,
   `packages/orchestration/do_sequence.py`, `packages/orchestration/do_summary.py`,
   `tests/cli/test_client_interface.py`, `packages/orchestration/scope_question.py`,
   `packages/orchestration/do_scope.py`, `tests/cli/test_plan_approval.py`,
   `tests/orchestration/test_scope_question.py`, `tests/regression/test_lab_orders_20261020.py`):
   exit 0, `All checks passed!`.
3. Gate 3: `python3 .remedy-wt/f312-r2/prep/run_selection.py . .remedy-wt/f312-r2-worker/selection-output.txt`:
   `paths 93`, `exit 0`, `3915 passed, 2 skipped in 57.13s`; no FAILED or ERROR line, no
   "process(es) behind" line. SKIPPED lines:
   - `SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.`
   - `SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access`
4. Gate 4: `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing
   check `high_blockers_open`: `"13 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345,
   R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362, R-1369"` — the thirteen of DECISION
   F310 D7, no other.
5. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `88`.
6. Gate 6: `python3 -c "from pathlib import Path; print(len(Path('packages/orchestration/do_sequence.py').read_text().splitlines()))"` — `982`.

## Authored-text proofs

Byte copy of `block.md` to `.agent/authored/f312-r2.md` at C1, proved by a sha256 equality in the
copy script (216 lines, matching the prompt's digest and line count exactly) and confirmed again
by `verify.py`'s `C1 .agent/authored/f312-r2.md equals block.md` line above. The other four C1
copies (`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`)
are prepared-file byte copies, each proved equal by sha256 in the copy script and again by
`verify.py`. The reviewer's amendment 1 was byte-copied to `.agent/authored/f312-r2-amend1.md` at
this commit, proved by a sha256 equality in the copy script: 23 lines, sha256
`2a03e5f227cbcd405831a14a6d77b65f79b3c80a8fe876088a3d153ef7a9747c`, matching the amendment's own
stated digest and line count exactly.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | cf2b76dd0 |
| C2 | done | 0f40f576d (amended once, locally, before C3 started) |
| C3 | done | 264412f99 (amended once, locally, before the stop) |
| C4 | done | 6016db89b, including the reviewer's amendment-1 test edit |
| C5 | done | eed4fff0c |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 3915 passed, 2 skipped |
| Gate 4 | done | fail_count 1 on the standing thirteen |
| Gate 5 | done | 88 |
| Gate 6 | done | 982 |
| C6 | done | this commit |

## Deviations & assumptions

- Stop after C3, resolved by the reviewer's amendment 1: an EXISTING test,
  `tests/cli/test_plan_approval.py::TestTaskPlanLabel::test_llm_plan_holding_an_inspection_task_is_rejected`,
  went red because of C3 — its order `"test mission"` is of the kind `open`, and its planner mock
  always answers the same inspection-only plan, so C3's new second-attempt-then-question path fired
  where the test expected a single immediate `OrderJobPlanError`. Reported and stopped before C4 as
  the block ordered; the reviewer ruled the stop correct and, in amendment 1, authorized changing
  only that test's order text and docstring (to `"Write notes.md about the repository"`, kind
  `names_files`, confirmed before the C4 commit) so it keeps pinning DECISION F268 D6 for the two
  kinds refused at once, leaving its `pytest.raises` match and its `list_job_plans() == []`
  assertion byte-identical. Landed in C4.
- Two local commits were amended after they were first made, both before being pushed and both
  before any later commit depended on them, per the Commit Gate's self-review loop (not forbidden
  until the reviewer's amendment 1 rule 2, which took effect only from C4 on and was honoured: no
  commit from C4 on was amended, rebased or rewritten):
  - C2 (`0f40f576d`): the first pass moved `do_job_task_listing`'s import in `apps/cli/commands/do_cmd.py`
    from `do_sequence` to `do_summary`'s multi-line import block, which grew `_cmd_do_order` from
    161 to 162 lines against its "edits of this function are line-neutral (DECISION F055 D1)" ledger
    pin — caught by `tests/test_structure_ratchet.py::test_every_function_equals_its_row`, run as
    part of self-review though it is outside the gate-3 selection. The amendment joined one existing
    two-line `fail("invalid_argument", "order must not be empty.", ...)` call in that same function
    onto one line (precedented elsewhere in the file, lines 63 and 548) to restore 161 lines exactly.
  - C3 (`264412f99`): `scope_question_text`'s two required literal phrases were split across adjacent
    f-string lines — correct at runtime, but `verify.py`'s checks read the committed SOURCE text and
    require each phrase unbroken, so two checks read `False`. Rejoined each phrase onto one line, no
    change in the produced text, confirmed by re-running `verify.py` (`ALL True`) and by the module's
    own behaviour.
- `apps.cli.main.main` (the literal name the block and the amendment both use) takes no arguments —
  it is `apps/cli/main.py`'s thin `python -m` entry point, delegating to `apps.cli.grouped.main()`
  with no argv of its own. C5's walk calls `apps.cli.grouped.main(["do", <text>, ...])`, the real
  argv-accepting entry every sibling CLI test in this repository (e.g.
  `tests/cli/test_do_sequence_cli.py`) already uses, since it is the only callable the block's own
  call shape `main(["do", <text>, ...])` fits.
- The records of the operator's failed lab job were not read: the data root is not readable in this
  session, per DECISION F312 D1; the finding's text and the code are the evidence, as the block and
  the DECISION both state.
- `docs/README.md` was not touched: nothing in this round adds, moves or renames a doc.

## For the operator, in plain sentences

Remedy now gives a plain request like "make it look nice" a second attempt when its first plan is
refused, instead of failing outright; if that second attempt is refused too, Remedy stops and asks
which files the request is really about, offering the files its own planner had proposed, rather
than guessing a third time. A piece of the walk's reporting code that was living in the wrong file
moved to the one that already holds the rest of it, with no change in what it does. The three
original example requests that first exposed this problem were turned into a lasting test that
walks the whole system the normal way, with stand-in builders and reviewers instead of a real
network call, and it was proven to produce the same two outcomes by hand. One existing test about a
different, narrower rule had to have its one example request swapped for a more specific one so the
two rules stop colliding on the same example; nothing about what either rule checks for was
changed. What answering the new question actually does is left for the next round.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`); the Open PR Gate; book round 2's verdict and the
DECISION F312 D3 addendum naming the test amendment 1 changed in the next round's first commit;
DECISION F312 D4, the answer path.
Operator questions open: 1. Open findings: 88 (gate 5, `open_finding_ids`, read at C1's ledger).
