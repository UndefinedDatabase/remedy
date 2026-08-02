# Handoff — F069 Mission compiler, R1 (SPLIT, LARGE bundle)
## Range
Review of 53ac3efa..HEAD — feature/f069-mission-compiler, 12 commits.
## Commits
### 6048fbe4 chore(f069): claim F069 + reset live review
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/{authored/f069-r1-1,-2,context,last_block,live_review,plan}.md, docs/roadmap/STATUS.md | +316/-304 | reviewer texts, round state, claim `[~]` |
### 62ef95fa refactor(f069): extract the shared repo-facts prompt helper
| Path | +/- | Reason |
| --- | --- | --- |
| prompt_facts.py (new), flight_plan.py | +44/-21 | `repo_facts_block`: one copy, per the brief |
### 39be19f5 feat(f069): MissionPlan schema with milestone-DAG validation
| Path | +/- | Reason |
| --- | --- | --- |
| mission_plan_schema.py (new), schemas/models.py, schemas/test_schemas.py, decisions.md | +303/-4 | `mission_plan_v1`+draft, registry, tag exemption (dev. 1) |
### 20633b5a feat(f069): the mission compiler with its deterministic fallback
| Path | +/- | Reason |
| --- | --- | --- |
| mission_compiler.py (new) | +250 | compile + honest fallback; writes nothing |
### 4c60943b test(f069): three long-goal golden fixtures for the mission compiler
| Path | +/- | Reason |
| --- | --- | --- |
| fixtures/mission/*.json (3), test_mission_compiler.py | +900 | goldens (goals 531–606 chars) + T001 proof |
### 98b28c0c feat(f069): persist a mission plan on the mission record
| Path | +/- | Reason |
| --- | --- | --- |
| mission_state.py | +52/-1 | additive `mission_plan` + evidence dir (dev. 3) |
### ddc2ac1e feat(f069): per-milestone DoD hand-off and mission plan rendering
| Path | +/- | Reason |
| --- | --- | --- |
| mission_compiler.py | +204/-1 | `compile_dod` view → dod_ref, mission_plan.md (dev. 4) |
### 40100796 test(f069): DoD hand-off, persistence and the no-autostart guarantee
| Path | +/- | Reason |
| --- | --- | --- |
| test_mission_compiler.py | +309/-1 | hand-off, persistence, zero jobs/processes |
### f2461dbc feat(f069): recompile versioning and the in-progress refusal
| Path | +/- | Reason |
| --- | --- | --- |
| mission_compiler.py | +147 | `plan_mission`, version retention, refusal (dev. 2) |
### 60c07d0d feat(f069): remedy mission plan command
| Path | +/- | Reason |
| --- | --- | --- |
| command_catalog.py, commands/mission_cmd.py | +88/-1 | `mission.plan` entry + handler |
### d5bbda6c test(f069): CLI plan paths, version retention and the refusal
| Path | +/- | Reason |
| --- | --- | --- |
| tests/cli/test_mission_cmd.py, test_mission_compiler.py | +310/-1 | CLI paths + compiler-level retention |
### <handoff> chore(f069): handback R1 — grouped self-reference (R-0149)
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/{handoff,plan,decisions,last_block}.md | rewrite | this file; step=R1 done; dev. 2/4; OUTCOME |
## External actions
- `gh pr list --state open` → exactly PR #174, f062 → main, not draft.
- `gh pr merge 174 --merge --delete-branch` → exit 1, yet the merge LANDED (MERGED,
  53ac3efa); gh's local checkout aborted on a dirty last_block.md. Branch removed by
  hand: `git push origin --delete` + `git branch -D`, both OK.
- `git push -u origin feature/f069-mission-compiler` → OK, 4 pushes (one/slice). No
  F069 PR (R1 hands back first). No worktree added or removed.
## Verification
    $ pytest tests/docs/ -q → 293 passed; tests/cli/test_golden_path.py -q → 42 passed (canary, ×3)   both exit 0
    $ pytest …/test_mission_compiler.py -q                90 passed   exit 0
    $ pytest …/test_mission_compiler.py …/test_mission_state.py -q      160 passed  exit 0
    $ pytest …/test_mission_compiler.py tests/cli/test_mission_cmd.py -q 156 passed  exit 0
    $ pytest tests/cli/ -q -x -p no:randomly           1244 passed   exit 0
    $ pytest tests/orchestration/ -q -n auto           9285 passed, 7 skipped  exit 0
    $ pytest tests/docs/ …/test_dashboard_contract.py -q 363 passed   exit 0
    $ ruff check --output-format=concise                 13 errors   exit 1 — all
      pre-existing, in 7 files never touched here; every touched file → exit 0.
    $ git status --porcelain                           (empty)       exit 0
## Authored-text proofs
- f069-r1-1: sha256 b6e33228…804c7 = BEGIN hash; its TO line occurs exactly 1× in
  STATUS.md (byte-compared to the authored file's line 4), FROM line 0×.
- f069-r1-2: sha256 17966426…90049 = BEGIN hash; `cmp` vs `git show
  6048fbe4:.agent/live_review.md` → exit 0, byte-identical.
## Deviations & assumptions
1. `mission_plan_v1` is 15 chars vs the compact-tag guard's 6: the NAMED exemption
   list grew to 2, its bound to 15. General limit untouched, tag not renamed.
2. **"In progress" is per-MISSION** — the deviation the block anticipated.
   `MissionJobLink` holds job_id/role/created_at only, so nothing attributes a job to
   a milestone, and adding that field means touching job creation (forbidden). Rule at
   `milestones_in_progress`, 5 tests: any linked job ⇒ every milestone of the current
   plan is in progress ⇒ recompile refused; with no plan yet the FIRST compile is
   always allowed.
3. No schema bump: `mission_plan` is written only when one exists, so pre-F069 record
   bytes are unchanged and MISSION_SCHEMA_VERSION stays 1 (pinned).
4. DoD via a flight-plan VIEW (`milestone_flight_plan`) — `compile_dod` takes
   (intake, FlightPlan). Never persisted, never scheduled; a milestone-shaped DoD
   builder here would be the second mechanism A6 forbids.
5. Two defects the new tests caught and fixed: a dict-shaped mission stringified the
   record into the prompt (`mission_goal` now reads attr→key→value); one lint fixture
   used a verb outside the documented closed list (corrected — that gap is now its own
   documented test).
6. Stash incident, fully reverted: a stash/pop run to compare ruff baselines stashed
   nothing (only untracked files were dirty) and popped an unrelated pre-existing
   `stash@{0}`. `git reset --hard HEAD` + removing the 5 restored untracked files
   restored the branch; `git stash show stash@{0}` confirms it intact and unconsumed.
## Next
Reviewer verdict on R1, then the integration gate per docs/agents/integration_gate.md.
F069 R1 complete — awaiting review.
