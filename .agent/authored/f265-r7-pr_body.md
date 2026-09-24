## What

F265 — Teacher learning UI v1 (post-task lessons). After each task of a job finishes, Remedy's
teacher can write a short lesson from the change that task really made: what was built, which
functions and language features it uses, what each does, why it fits there, and whether that is
good practice, stated as the teacher's opinion. The cockpit's right panel opens a learning sheet
with the job's lessons on the left, the chosen lesson on the right, previous and next, and a
Commands mode that lists the Remedy commands the change touched with the descriptions Remedy ships
today.

## Why

A build's waiting time is when a person is both idle and most curious about the code being
written. A lesson written from the recorded change, never from the plan, teaches what shipped.

## Key decisions (in `.agent/decisions.md`)

- F265 D1 — a lesson is a sealed record per Run beside that Run's diff, written from the whole diff
  or not at all, grounded in the diff's added lines, billed as role `teacher` inside a per-job pot
  read from the ledger, and written only while `teacher.lessons` is on (off by default).
- F265 D2 — a stored lesson is announced on the job's run log; the stream carries its Run and status
  only, and `GET /api/jobs/<job_id>/lessons` lists every task's lesson or the reason it has none.
- F265 D3 — the learning overlay is a right-anchored dialog sheet the right panel opens, reading the
  route through one pure module and reading it again only when the stream announces a lesson.
- F265 D4 — the Commands mode names the commands whose handler module or catalog line the diff
  changed, with the catalog's shipped description, computed at read time and never stored.

## Operator question

`.agent/operator_questions.md` Q1 asks whether lessons should start switched off. The
recommendation, off until switched on, is already executed and stands until the operator says
otherwise.

## How to review

Start with `docs/guides/teacher-lessons-user-guide-v1.md` for the behaviour, then
`packages/orchestration/lessons.py` (generate, pot, grounding, overview, commands), the hook
`_teach_task_lesson` in `packages/orchestration/pingpong_job.py`, the route and stream field in
`packages/orchestration/ui_server.py`, and the cockpit modules `apps/ui/src/api/lessons.ts` and
`apps/ui/src/components/lessons/LessonsOverlay.tsx`. The acceptance proofs are named test by test
in the Built State of `docs/roadmap/features/T5_F265.md`; the central one is
`tests/orchestration/test_lessons.py::test_a_real_job_teaches_its_completed_task_from_the_runs_own_diff`.

## Changed files

| Path | +/- |
|---|---|
| `README.md` | +11/-2 |
| `apps/ui/src/api/humanizeCatalog.ts` | +1/-0 |
| `apps/ui/src/api/lessons.test.ts` | +151/-0 |
| `apps/ui/src/api/lessons.ts` | +192/-0 |
| `apps/ui/src/api/remedyApi.ts` | +24/-0 |
| `apps/ui/src/components/lessons/LessonsOverlay.module.css` | +117/-0 |
| `apps/ui/src/components/lessons/LessonsOverlay.tsx` | +164/-0 |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | +8/-1 |
| `apps/ui/src/components/shell/RemedyShell.tsx` | +18/-1 |
| `docs/README.md` | +2/-0 |
| `docs/agents/planner_reviewer_prompt.md` | +4/-0 |
| `docs/guides/environment.md` | +3/-0 |
| `docs/guides/teacher-lessons-user-guide-v1.md` | +73/-0 |
| `docs/roadmap/STATUS.md` | +1/-1 |
| `docs/roadmap/features/T5_F265.md` | +67/-0 |
| `docs/ui/design_reference/assumption_log.md` | +2/-0 |
| `packages/orchestration/config.py` | +32/-0 |
| `packages/orchestration/event_names.py` | +1/-0 |
| `packages/orchestration/lessons.py` | +453/-0 |
| `packages/orchestration/pingpong_job.py` | +43/-0 |
| `packages/orchestration/ui_server.py` | +27/-0 |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 |
| `tests/orchestration/test_lessons.py` | +478/-0 |
| `tests/ui_contracts/test_lessons_overlay_contract.py` | +110/-0 |
| `tests/ui_server/test_lessons_route.py` | +123/-0 |

## Verification

- The one full suite, in the closure's integration gate: `18901 passed, 20 skipped` at exit 0,
  no bad node (`.agent/authored/f265-closure-suite.txt`).
- Evidence job `f265r6e1001` against the fork point `0236e3c3`: 751 selected tests passed at exit 0.
- Review package `remedy-review-20260924-092513-READY_FOR_REVIEW.zip`, SHA-256
  `e6d848bab17468e2ccf6cad002b0612534d3337d826961cd6deb0e8fededb813`, READY_FOR_REVIEW.
- Every production change carried mutation red-proofs in its round: 12, 9, 9 and 8 mutations,
  each red with the unmutated control green before and after.

## Findings

R-1046 was registered: `teacher.model` does not reach `remedy teacher ask`, which this feature's
Do-not-touch list kept it from repairing; it is owned by the next findings paydown. Open findings:
4.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
