## What

F268 — `remedy do "<order>"`, the one-command start. Every `remedy do`, with or without the word `run`, walks one sequence held as data — init, study, plan, shape, run, ui, apply. It registers an unregistered repository, studies it once, plans a mission whose tasks each name the deliverable they produce, runs the first job, and stops before apply unless `--apply`.

## Why

`do` had three internal modes, and the operator saw all three in tests.md Level 4. One command that runs one sequence, honestly, is the usability promise the product was built around (`docs/roadmap/features/T2_F268.md`).

## Key decisions (all in `.agent/decisions.md`)

- **D1–D4:** the sequence is data (`packages/orchestration/do_sequence.py`, `DO_SEQUENCE`).
- **D5, D6:** the planner's shape, with `--force-job` and `--force-mission`; a deliverable for every task, enforced by a validator.
- **D8:** `--step-by-step` and `--plan-only`.
- **D9:** the cockpit opens detached. `--contract`, `--commit*` and `--push` exit 2 and name the feature that brings them.
- **D11:** measured tokens per role and cost at the end; the builder's context reaches `context_strategy.json`.
- **D12:** a multi-job walk runs job 1; every other job waits, with the commands that continue it.
- **D13:** the job evidence export writes the four flow artifacts the review-package check requires (R-0892).
- **D14, D15:** a five-line quick start in `remedy --help` and the README, run by a test.
- **D16, D17:** one route under `do`. The autorun branch, its four flags and the `do` v1 flow are deleted. `do` now honours `--project`, the budget flags and the builder, reviewer and planner model flags (R-0933).

## How to review

1. Read `packages/orchestration/do_sequence.py` top-down.
2. Read `apps/cli/commands/do_cmd.py` `_cmd_do_order`.
3. Run the tests:
   ```
   python3 -m pytest -q tests/cli/test_do_sequence_cli.py tests/cli/test_do_flags.py tests/cli/test_quick_start.py tests/cli/test_do_evidence_package.py
   ```

The closure suite was run once, as `python3 -m pytest -n auto -q`. Its transcript is `.agent/authored/f268-closure-suite.txt`: 3 failed, and repair round 1 fixed all three. The review package is `remedy-review-20260918-140632-READY_FOR_REVIEW.zip`, SHA-256 `2c4ed9fa9d3c2e762dbf19a069cc378dfc7c46d973f9334e656f4dc9e873d86a`. It covers accepted HEAD `5883bccb2b2d4362815215c6a24a71b67f9016f9`.

## Latest verdict

PASS_WITH_RISKS (`Gate: F268 R12` in `.agent/live_review.md`).

The risks:
- **R-0892 is half done.** The `.claude/skills/remedy-evidence-review/SKILL.md` edit was refused by the session's permission system. The finding is re-assigned to F273, and the prepared page is `.agent/authored/f268-r7-skill.md`.
- **R-0807 has an F260 half still open**, owned by F273.
- **Operator questions Q2 and Q3** are open in `.agent/operator_questions.md`.

## Open findings

125 by distinct id.

## Runtime actuals (observed)

- 13 rounds over two sessions on 2026-09-18.
- Branch commits from 09:00 to 14:08 (+0200), before the closure commits.
- Every commit co-authored by Claude Opus 5.
- Tokens and cost: not measured.

## Changed files

`git diff --stat 8e075bbe...feature/f268-remedy-do` gives the full table. The production changes are:
- `packages/orchestration/do_sequence.py`
- `packages/orchestration/task_deliverables.py`
- `packages/orchestration/job_evidence.py`
- `packages/orchestration/do_run.py` (cut down to the `Next:` contract)
- `packages/orchestration/autorun.py`
- `apps/cli/commands/do_cmd.py`
- `apps/cli/grouped.py`
- `apps/cli/command_catalog.py`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
