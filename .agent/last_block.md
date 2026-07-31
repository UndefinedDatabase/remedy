OUTCOME: executed

# Received block — F056 R1 (LARGE, SPLIT round)

Read docs/agents/split_workflow.md (worker role) and AGENTS.md and act
accordingly. This is a SPLIT round: you execute, the reviewer gates.
You never write `## Verdicts` entries, never set findings Resolved,
never push/PR/merge this round — handback ends your turn.

── STEP T001+T002+T003/1 — F056 (LARGE round R1) ─────────────────────
Goal:        Build the whole F056 feature — missions as thin persistent
             records above jobs (persistent goal + ordered job chain),
             verify-first follow-ups, strictly opt-in creation — in one
             bundle with per-slice verification, stop-on-red.

Bundle (ordered):
0. Bookkeeping FIRST actions: record this block in .agent/last_block.md
   (OUTCOME: pending; update at handback). Save the two authored texts
   at the end of this block VERBATIM to .agent/authored/f056-r1-1.md
   and .agent/authored/f056-r1-2.md; verify `sha256sum` of each saved
   file against its BEGIN-marker hash BEFORE committing — on mismatch
   STOP: report the mismatch and the received bytes, commit nothing.
1. Open PR Gate (verify-only this time): `gh pr list --state open`
   must be empty — PR #170 merged same-session under the standing
   single-session approval. `git checkout main && git pull`; HEAD must
   be 78f5f608 or a descendant; `git status --porcelain` empty.
2. Branch: `git checkout -b feature/f056-missions`.
3. State commit (own commit, first on the branch):
   - Apply f056-r1-1 to docs/roadmap/STATUS.md: replace the single
     line currently reading exactly
     `- [ ] F056 — Missions: persistent goal, jobs as execution units`
     with the authored bytes (byte-copy from the saved authored file).
   - Apply f056-r1-2 as the FULL replacement of .agent/live_review.md
     (byte-copy from the saved authored file).
   - Rewrite .agent/plan.md and .agent/context.md yourself for the new
     feature/branch. R-0162 discipline before writing either: run
     `rg -ln 'plan\.md|context\.md' tests/`, collect ALL reader
     assertions, validate your draft against the full list — known
     minimum: plan.md keeps `## Goal` + a heading containing "Steps";
     context.md keeps `## Active Branch`, a `feature/` slug, a roadmap
     F-id, and the word "resource" or "pytest"; no state file may
     present feature/f007-runtime-harness as current.
   - Gate for this commit: `python3 -m pytest tests/docs/ -q` green.
4. T001 — mission record + store + link/list/show:
   - New module mission_state.py (place it beside the existing
     job/checkpoint state modules; inspect current shape first, per the
     feature file). Mission record: id, project id, goal text, status
     (active|paused|achieved|abandoned), ordered job links (job id,
     role: initial|follow_up, created_at), dossier reference field
     reserved now but unfilled.
   - Storage like other entities: atomic JSON per record under a
     project-scoped area of the data root.
   - `remedy mission start <goal>` creates directly; mission
     list/show; show renders the chain with each job's terminal state;
     a linked job that no longer exists renders "(missing job)" —
     listings never crash. Corrupt-record honesty like other listings.
   - Validators: one job belongs to at most one mission; mission goals
     immutable — a changed goal is a new mission.
   - Unit tests in tests/orchestration/test_mission_state.py and CLI
     tests in tests/cli/test_mission_cmd.py (ordering, scoping,
     corrupt-record honesty, missing-job rendering, validators).
   - Slice gate: `python3 -m pytest
     tests/orchestration/test_mission_state.py
     tests/cli/test_mission_cmd.py -q` green.
5. T002 — intake hint + approval opt-in:
   - Intake may set mission_candidate=true for goals that smell
     long-lived; the plan-approval payload then carries "run as
     mission?" DEFAULTING TO NO — explicit opt-in; yes creates the
     mission and links the job as role initial. No new human
     touchpoint: same single approval as clarifications.
   - Negative test REQUIRED: a plain do-flow (no opt-in, no command)
     creates no mission.
   - Slice gate: the T001 command plus every intake/approval test file
     you touched, `-q`, green.
6. T003 — continue + injected verify-first + two-job fixture:
   - `remedy mission continue <id> "<next step>"` creates a job linked
     role follow_up whose plan is REQUIRED to begin with a verify task
     (run the previous job's DoD/tests/smoke against the current
     state) — enforced structurally by injecting the verify task, not
     by prompt hope.
   - Two-job fixture end-to-end: job 1 green → continue → verify task
     runs first and passes → follow-up work runs; broken previous
     state → verify fails, follow-up never starts, failure message
     names what broke. Lineage correct in `mission show`.
   - Slice gate: the T001 command (now including the e2e tests), -q,
     green.
7. Round close: canary `python3 -m pytest tests/cli/test_golden_path.py
   -q` and docs gate `python3 -m pytest tests/docs/ -q` (this round
   touches docs/roadmap/**) — both green; `git status --porcelain`
   empty.

Change:      packages/ (or the established source root — inspect
             first) mission_state module + CLI wiring + intake/
             approval payload touch + the two suggested test files +
             docs/roadmap/STATUS.md + .agent state. Nothing beyond.
             (later feature), lineage UI, dossier CONTENT — only
             reserve the field. Nothing auto-transitions mission
             status in this feature; transitions are explicit
             commands (achieve/abandon/pause). Commits small
             (<500-line diffs), multiple commits per slice expected
             and welcome. Stop-on-red: if a slice gate stays red
             after in-scope repair, STOP the bundle at the last green
             commit and hand back with the raw failing output — do
             not start the next slice. Mutation red-proofs, if any,
             ONLY inside a disposable git worktree; primary checkout
             porcelain-empty at handback. Every string you applied
             from this block is verified disk-to-disk against the
             saved .agent/authored/ files.
Done when:   All slice gates green + canary green + docs gate green,
             raw transcripts (command, exit code, output tail) for
             each recorded in the handoff; tree porcelain-empty.
Handback:    Completion report in chat AND rewrite .agent/handoff.md:
             first line block "Review of <main-merge-base-sha>..HEAD
             (branch feature/f056-missions)", per-commit changed-files
             tables (path, +/-, reason), verification transcripts,
             deviations & A9 assumptions, external actions taken.
             Update .agent/last_block.md OUTCOME. Then stop — the
             reviewer takes over.
──────────────────────────────────────────────────────────────────────

--- BEGIN f056-r1-1 sha256=617f083eee54821635dc97822cc25b3b10fc9e5873c9280e4a3a55aea01ca0dd ---
- [~] F056 — Missions: persistent goal, jobs as execution units
--- END f056-r1-1 ---

--- BEGIN f056-r1-2 sha256=0fc3cbd8945228c629a817b1810f3368be7d5208e5fb659f24b4bc7d27c95593 ---
# Live Review — F056 Missions: persistent goal, jobs as execution units (Tier 1)

Branch: feature/f056-missions
Scope: a MISSION is a thin persistent record above jobs — a
persistent goal plus an ordered chain of linked jobs. Follow-up jobs
are forced to verify the previous state FIRST (injected verify task,
not prompt hope). Missions never auto-create — explicit human opt-in
only (plan-approval payload defaulting to NO, or `remedy mission
start`). LARGE round per operator directive: T001+T002+T003 in one
bundle, per-slice verification, stop-on-red. Closure is its own
later round.

## Steps
- R1 (LARGE): STATUS claim [~] + state reset → branch → T001 record
  + store + link/list/show + unit tests → T002 intake
  mission-candidate hint + approval opt-in (default NO) + tests →
  T003 continue + injected verify-first task + two-job fixture
  end-to-end → per-slice gates + canary + tests/docs → handback.

## Findings
- (none registered yet this feature)
- Next free ID: R-0163.

## Verdicts
- R1: awaiting handback.
--- END f056-r1-2 ---
