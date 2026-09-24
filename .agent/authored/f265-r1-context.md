# Context — F265 Teacher learning UI v1 (post-task lessons)

## Active Branch
feature/f265-teacher-learning-ui, cut from `main` at `0236e3c3`
(the merge commit of pull request 271, F264 Steering channel).

## Scope
F265 (Tier 5), registered 2026-08-31 by operator order
amend0831-vocab-registrations. After every completed task the teacher
writes a lesson from the task's real diff (T001); a learning overlay over
the cockpit lists the lessons with next and previous navigation (T002);
and a Commands mode explains the CLI commands the diff touched (T003), as
`docs/roadmap/features/T5_F265.md` specifies. F255 built the teacher role,
its Ollama transport and its ledger rows; F021 built the activity feed.

## Do not touch
The write channel (F009): the overlay is read-only and adds no mutating
route. The builder and reviewer role configs. `remedy teacher narrate` and
`remedy teacher ask`, which keep working unchanged. The v2 live mode,
which generates during the build, is a separate future feature.

## Active assumptions
- A lesson is keyed on the Run, beside that Run's `result.diff`, and names
  its Mission when the job has one (DECISION F265 D1).
- Lessons are off unless `teacher.lessons` is on, and the pot per job is
  measured from the ledger's `teacher` rows (DECISION F265 D1).

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new module under `apps/` or `packages/` joins
  `tests/orchestration/import_reachability_allowlist.txt` in the same round.
- A new config key regenerates `docs/guides/environment.md` in the same
  commit.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.

The overlay (T002, T003) is UI work and binds `docs/ui/design_reference`;
round 1 touches no UI component.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
