OUTCOME: executed

# Received block — F056 R2 (SPLIT round, post-PASS remainder)

Read docs/agents/split_workflow.md (worker role) and AGENTS.md and act
accordingly. SPLIT round on the existing branch feature/f056-missions —
you execute, the reviewer gates. No push, no PR, no merge, no verdict
writing beyond applying the authored text below.

── STEP R2 — F056 (post-PASS remainder: status-transition surface) ───
Goal:        Persist the R1 verdict + R-0163, then give mission status
             transitions the explicit command surface the feature file
             promises: remedy mission achieve/abandon/pause.

Bundle (ordered):
0. Bookkeeping FIRST actions: record this block in .agent/last_block.md
   (OUTCOME: pending; update at handback). Save the two authored texts
   below VERBATIM to .agent/authored/f056-r2-1.md and
   .agent/authored/f056-r2-2.md; verify `sha256sum` of each saved file
   against its BEGIN-marker hash BEFORE committing — on mismatch STOP:
   report the mismatch and the received bytes, commit nothing.
1. FIRST COMMIT (own commit, before any fix): apply f056-r2-1 as the
   FULL replacement of .agent/live_review.md (byte-copy from the saved
   authored file). Update .agent/plan.md Current Step/Next Steps
   yourself (keep `## Goal` + `## Next Steps`; R-0162 reader
   discipline unchanged).
2. Fix R-0163:
   - Apply f056-r2-2 to docs/roadmap/features/T1_F056.md: replace the
     two lines currently reading exactly
     `- CLI: mission start/continue/list/show (show renders the chain with each`
     `  job's terminal state).`
     with the authored bytes (byte-copy from the saved authored file).
   - Add three catalog entries mission.achieve / mission.abandon /
     mission.pause (group mission, action_class write_metadata, args:
     mission_id positional + --project + --json, supports_json,
     related to mission.show/list) and their handlers in
     apps/cli/commands/mission_cmd.py as thin wrappers over
     set_mission_status: resolve project (same exit-3 wording), resolve
     the id (unique prefix affordance), call set_mission_status with
     the status the verb names, print the mission id + new status
     (JSON: {"version": 1, "mission": …} like show). Errors: unknown
     mission → same not-found wording as show, exit 1; MissionError →
     exit 1. NO new transition rules — any valid status may follow any
     other, exactly as set_mission_status allows today; nothing
     auto-transitions.
   - Tests: catalog presence/action-class/handler coverage (extend the
     existing TestCatalog patterns), one happy path per verb, unknown
     mission, prefix resolution, --json shape, and the facade guard
     still green. Mark `Done: R-0163` in the ledger's finding entry
     (append the Done line — the Resolved wording stays reviewer-owned).
3. Gates, each exit code + tail recorded in the handoff:
   - python3 -m pytest tests/orchestration/test_mission_state.py
     tests/cli/test_mission_cmd.py tests/cli/test_worker_facade_cmd.py
     tests/test_command_catalog.py -q
   - python3 -m pytest tests/docs/ -q   (feature file touched)
   - python3 -m pytest tests/cli/test_golden_path.py -q   (canary)

Change:      docs/roadmap/features/T1_F056.md (authored lines only),
             apps/cli/command_catalog.py, apps/cli/commands/
             mission_cmd.py, tests/cli/test_mission_cmd.py,
             .agent state. Nothing beyond — mission_state.py itself
             needs NO change.
Constraints: Do-not-touch unchanged (orchestrator loop, lineage UI,
             dossier content). Commits <500-line diffs. Stop-on-red.
             Mutation checks only in disposable worktrees; porcelain
             empty at handback. Every applied string verified
             disk-to-disk against the saved .agent/authored/ files.
Done when:   All three gate commands green; `git status --porcelain`
             empty.
Handback:    Completion report in chat AND rewrite .agent/handoff.md:
             "Review of e8c3c147..HEAD (branch feature/f056-missions)",
             per-commit changed-files tables, raw gate transcripts,
             deviations & assumptions. Update .agent/last_block.md
             OUTCOME. Then stop — the reviewer gates; the
             integration-gate round and the closure round follow as
             their own rounds.
──────────────────────────────────────────────────────────────────────

--- BEGIN f056-r2-1 sha256=009a544230f8e5ed38368365e9a445869926d57619afec5a876e444b3aa3fd67 ---
# Live Review — F056 Missions: persistent goal, jobs as execution units (Tier 1)

Branch: feature/f056-missions
Scope: a MISSION is a thin persistent record above jobs — a
persistent goal plus an ordered chain of linked jobs. Follow-up jobs
are forced to verify the previous state FIRST (injected verify task,
not prompt hope). Missions never auto-create — explicit human opt-in
only (plan-approval payload defaulting to NO, or `remedy mission
start`). Closure is its own later round.

## Steps
- R1 (LARGE): T001 record + store + link/list/show → T002 intake
  hint + approval opt-in (default NO) → T003 continue + injected
  verify-first + two-job fixture end-to-end — PASS.
- R2: persist this ledger → status-transition surface
  (mission achieve/abandon/pause) + feature-file amendment
  (R-0163) → gates → handback.
- Then: integration-gate round; closure round (each its own round).

## Findings
- Open: R-0163 (planning, Low, registered 2026-07-31): the feature
  file's Design bullet promises explicit status-transition commands
  (achieve/abandon/pause), but its CLI line omits them; R1 shipped
  set_mission_status fully tested yet with no command surface, so
  no "explicit command" can actually move a mission's status — the
  worker declared exactly this as an A9 assumption and awaited the
  order. DECISION (§4.7): amend the feature file's CLI line and add
  mission achieve/abandon/pause as thin wrappers over
  set_mission_status. Alternatives considered: defer the surface to
  F070 (leaves the module's promise dead until then); a single
  set-status subcommand (one verb where the feature file names
  three). Reversible by any later relay.
- Next free ID: R-0164.

## Verdicts
- R1: PASS (SPLIT round, 2026-07-31). Range 78f5f608..e8c3c147.
  Reviewer re-ran at HEAD: mission gates 117 passed, T002 extended
  set 292 passed (worker's 260 was the earlier slice HEAD — tests
  added later in the bundle), tests/docs 293 passed, canary 42
  passed, facade guard 49 passed, state-file readers 7 passed — all
  exit 0; tree porcelain-empty. Transport: both authored texts cmp
  0 disk-to-disk against the reviewer scratchpad originals; the
  STATUS line occurs exactly once. Declared A9 defaults ACCEPTED:
  unverifiable is recorded and named, never passed; work execution
  belongs to a caller-supplied work_runner; the facade-test repair
  (guard by name, not group size) is an accepted in-scope repair.
  Round tier: scoped gates + canary + docs gate. The worker's own
  full-suite run (14727 passed) is noted, but the integration gate
  remains its own later round. R-0163 registered (planning);
  repair ordered in R2. No mutation checks ran.
  LAST_REVIEWED_SHA = e8c3c147.
--- END f056-r2-1 ---

--- BEGIN f056-r2-2 sha256=ae3d8e9de2b22507ad48f907edca104b7703f3f22d84e8efa2f4a49482ee3a17 ---
- CLI: mission start/continue/list/show (show renders the chain with each
  job's terminal state); status transitions are their own explicit
  subcommands — mission achieve/abandon/pause (R-0163 amendment,
  reviewer DECISION 2026-07-31).
--- END f056-r2-2 ---
