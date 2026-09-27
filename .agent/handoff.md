# Handoff — F029, round 8

## Session

SESSION 2 of feature F029 · round 8 · rounds so far 8. Context remaining at
handback: ample — reading `mission_dossier.py` whole (PLAN_RISK_ID_TEMPLATE
through the end of `refresh_mission_dossier`, plus `DossierItem`,
`IterationFacts`, `_merge_by_id`, `dossier_sections`), the test file whole,
and `subtree_rerun.py`'s `fold_subtree_rerun` record, then writing S1-S3,
18 new tests, the mutation tool, and running every gate, all went clean on
the first pass with no repair round and no tool bug.

## Range

Review of `a5933b73e`..`HEAD` (`HEAD` is this handback's own commit, `F029 R8
C5`, on `feature/f029-subtree-rerun`).

## Commits

### 157fe2e1b F029 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r8-block.md | 195/0 | copy of this round's block |
| .agent/authored/f029-r8-booking.diff | 52/0 | copy of the booking diff payload |
| .agent/authored/f029-r8-plan.md | 31/0 | copy of the plan payload |

Measured insertions: 278 (block's own line count 195 + 83), matching the
block's expectation exactly, under the 500-line cap.

### 5eb975540 F029 R8 C2: book round 7 and record D7
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 34/0 | DECISION F029 D7 appended (booking.diff) |
| .agent/live_review.md | 2/0 | round 7's Gate entry appended (booking.diff) |
| .agent/plan.md | 5/9 | rewrite from the plan payload |

Matches the block's expected numstat (34/0, 2/0, 5/9) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of `booking.diff`,
followed by the `plan.md` rewrite via `shutil.copyfile`.

### 6b41f9532 F029 R8 C3: note a rerun in its mission's dossier
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/mission_dossier.py | 67/5 | S1: `RERUN_ID_TEMPLATE` after `ITERATION_ID_TEMPLATE`; `rerun_decision_items` beside `_ledger_decision_id`. S2: `mission_job_reruns` beside `refresh_mission_dossier`. S3: `mission_iteration_facts` gains the `reruns` keyword and appends `rerun_decision_items(reruns)` to its decisions; `refresh_mission_dossier` passes `reruns=mission_job_reruns(mission, root)` |
| tests/orchestration/test_mission_dossier.py | 191/0 | THE TESTS: `TestRerunDecisionItems` (13 cases: override, no override, blank override, singular, plural-none, plural-two, non-dict, missing/empty `rerun_id`, missing/empty `root_task_id`, missing optional fields, several in order), `TestMissionIterationFactsWithReruns` (2), `TestMissionJobReruns` (2), `TestRefreshNotesARerunInTheDossier` (1, end to end) |

258 total insertions/5 deletions, under the 500-line cap; measured before
committing (67+191=258), no split needed.

### d1ec54f86 F029 R8 C4: add the round 8 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r8-mutations.py | 214/0 | the G5 mutation (red-proof) tool: m1 `rerun_decision_items` returns `[]` always, m2 the outcome always reads "the job's own model", m3 `refresh_mission_dossier` stops passing `reruns`, m4 the plural suffix is always "s" — one pytest route against `tests/orchestration/test_mission_dossier.py` |

### (this commit) F029 R8 C5: rewrite handoff for round 8
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file |

## External actions

`git worktree add --detach .remedy-wt/f029-r8-mut d1ec54f86`, ran
`.agent/authored/f029-r8-mutations.py` against it (all 4 mutations caught on
the first run, see G5 below), then `git worktree remove --force
.remedy-wt/f029-r8-mut` and `git worktree prune`. `git worktree list | wc -l`
read 64 at step 4 and 64 again after the removal. `git push origin
feature/f029-subtree-rerun` — its real outcome is reported to the delegator,
since C5 cannot contain it. No PR opened, no merge, no branch checked out or
deleted, no force-push, no stash.

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty;
  `git branch --show-current` → `feature/f029-subtree-rerun`; `git log
  --oneline -1` → `a5933b73e`.
- Block bytes (R-0954): measured 195 lines, sha256
  `017da772f764376d873f8b0eeed61a250acf60f48abfaf5563689986ea7557d9` — both
  match the delegation message's readings exactly.
- `git worktree list | wc -l` → 64.

**PAYLOADS** — both matched the table exactly:
`booking.diff` 52 lines / 12822 bytes /
`2aac7defedfab8ff85ed0625483484a29d82968abe859a4aa97f1cad6b6759ae`;
`plan.md` 31 lines / 1086 bytes /
`1243204d604ff092bfe26b0357bb03141ab9d502887d6a7b9aa1e343a756710f`.

**G1 TRANSPORT** — each `.agent/authored/f029-r8-*` copy read via `git show
157fe2e1b:<path>` equals its source byte for byte: block copy ==
`.remedy-wt/f029-r8/block.md` (True); booking.diff copy ==
`.remedy-wt/f029-r8-payloads/booking.diff` (True); plan.md copy ==
`.remedy-wt/f029-r8-payloads/plan.md` (True).

**G2 THE RECORDS** — sha256 of each file read via `git show 5eb975540:<path>`
equals the reviewer's reading exactly:
`.agent/decisions.md` 2305437 bytes,
`3b5d7d9a94aaa3c50bee1f3380c79d2183a8fe419aa956440aae0d0ec1c90eea` — match.
`.agent/live_review.md` 332588 bytes,
`da9d083a9deddd4f9b8ae2607fa92289e1d138ddb0ad4c82fbacd5b2952d4953` — match.
`.agent/plan.md` 1086 bytes,
`1243204d604ff092bfe26b0357bb03141ab9d502887d6a7b9aa1e343a756710f` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over
`.agent/live_review.md`'s text: at `a5933b73e` → `[]`; at `5eb975540` → `[]`
— both match the reviewer's stated readings. `git diff --name-only
157fe2e1b 5eb975540` → exactly the three paths of the table, nothing else.

**G3 THE CODE** —
```
python3 -m ruff check packages/orchestration/mission_dossier.py tests/orchestration/test_mission_dossier.py
```
→ `All checks passed!`, exit 0 (run at C4, `d1ec54f86`). Quoted from the C3
diff (matches what is committed at HEAD):

```python
RERUN_ID_TEMPLATE = "RR-{job}-{rerun}"


def rerun_decision_items(
        job_reruns: Iterable[tuple[str, dict[str, Any]]]) -> list[DossierItem]:
    items: list[DossierItem] = []
    for job_id, record in job_reruns:
        if not isinstance(record, dict):
            continue
        rerun_id = record.get("rerun_id")
        root = record.get("root_task_id")
        if not rerun_id or not root:
            continue
        subtree = record.get("subtree")
        n = max(len(subtree) - 1, 0) if isinstance(subtree, (list, tuple)) else 0
        job8 = job_id[:8]
        reset12 = str(record.get("reset_commit") or "")[:12]
        model = record.get("model")
        override = model.get("override") if isinstance(model, dict) else ""
        override = override if isinstance(override, str) and override else ""
        text = (f"rerun of task {root} and {n} task{'' if n == 1 else 's'} "
                f"after it on job {job8}")
        outcome = (f"reset to {reset12}, run on {override}" if override
                  else f"reset to {reset12}, the job's own model")
        items.append(DossierItem(
            id=RERUN_ID_TEMPLATE.format(job=job8, rerun=rerun_id),
            text=text, resolved=True, outcome=outcome))
    return items
```

```python
def mission_job_reruns(
        mission: Any, root: Path | None = None) -> list[tuple[str, dict[str, Any]]]:
    from packages.orchestration.pingpong_job import load_job_plan

    pairs: list[tuple[str, dict[str, Any]]] = []
    for job_id in mission.job_ids():
        job = load_job_plan(job_id, root)
        if job is None:
            continue
        for record in job.reruns:
            if isinstance(record, dict):
                pairs.append((job_id, record))
    return pairs
```

`mission_iteration_facts` changed lines:
```diff
                            ledger: Sequence[dict[str, Any]] = (),
+                            reruns: Sequence[tuple[str, dict[str, Any]]] = (),
                             ) -> IterationFacts:
@@
-        for entry in ledger]
+        for entry in ledger] + rerun_decision_items(reruns)
```

`refresh_mission_dossier` changed lines:
```diff
     facts = mission_iteration_facts(
         mission, done_milestones=done_milestones(mission),
-        ledger=read_ledger(project_id, mission_id, root))
+        ledger=read_ledger(project_id, mission_id, root),
+        reruns=mission_job_reruns(mission, root))
```

**G4 THE TESTS** — the exact selection, serially, real exit code:
```
python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_mission_dossier.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_handoff.py tests/orchestration/test_subtree_rerun_prepare.py tests/orchestration/test_subtree_rerun.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
```
Run at C4 (`d1ec54f86`): `951 passed, 7 skipped`, real exit code 0. All seven
`SKIPPED` lines cite an F252 quarantine (six in `test_named_bugs.py`, one in
`test_agent_tooling.py`) — the same seven the reviewer's own base reading at
`a5933b73` already carried. Accounting for the difference from 933: this
round's file, `tests/orchestration/test_mission_dossier.py`, adds exactly 18
new pytest nodes (13 in `TestRerunDecisionItems`, 2 in
`TestMissionIterationFactsWithReruns`, 2 in `TestMissionJobReruns`, 1 in
`TestRefreshNotesARerunInTheDossier`). 933 + 18 = 951, exactly the passed
count above; no unexplained difference. `python3 -m pytest --collect-only -q
-p no:cacheprovider tests/orchestration/test_mission_dossier.py` at C4 →
`122 tests collected`, versus the reviewer's `104 tests collected` at
`a5933b73` — the same 18-node difference. Then `python3 -m apps.cli.main
integrity check --json` → all 6 checks `pass` (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`repo_root_hygiene`, `high_blockers_open`), `fail_count: 0`, `ok: true`.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f029-r8-mut
d1ec54f86`, then `python3 -B .agent/authored/f029-r8-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r8-mut`:
```
packages.orchestration.mission_dossier.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/f029-r8-mut/packages/orchestration/mission_dossier.py
module resolves inside the worktree: True
control: exit=0 failed=0
m1 rerun_decision_items answers an empty list whatever it is given: exit=1 failed=10 — 10 of TestRerunDecisionItems/TestMissionIterationFactsWithReruns/TestRefreshNotesARerunInTheDossier
m2 the outcome always reads "the job's own model": exit=1 failed=1 — test_an_override_is_named_in_the_outcome
m3 refresh_mission_dossier no longer passes reruns: exit=1 failed=1 — test_a_rerun_on_a_linked_job_is_noted_at_the_next_refresh
m4 the text's plural suffix is always "s": exit=1 failed=1 — test_the_singular_names_one_task_after_the_root
restored byte-identical: True (packages/orchestration/mission_dossier.py)
control (after): exit=0
git status --porcelain (primary checkout): '' (empty)
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All four mutations were red on the first run; no repair round needed for the
production code or the tool. Then `git worktree remove --force
.remedy-wt/f029-r8-mut`, `git worktree prune`; `git worktree list | wc -l` →
64, matching the step-4 reading.

**Constraint 3** — `git diff --name-only a5933b73e`, run once more after
writing this file, lists exactly the block's tracked path set plus
`.agent/handoff.md` itself: `.agent/authored/f029-r8-block.md`,
`.agent/authored/f029-r8-booking.diff`, `.agent/authored/f029-r8-mutations.py`,
`.agent/authored/f029-r8-plan.md`, `.agent/decisions.md`, `.agent/handoff.md`,
`.agent/live_review.md`, `.agent/plan.md`,
`packages/orchestration/mission_dossier.py`,
`tests/orchestration/test_mission_dossier.py` — 10 paths in total; no path
outside the set changed.

## Authored-text proofs

`.agent/authored/f029-r8-block.md`, `f029-r8-booking.diff` and
`f029-r8-plan.md` (C1, `157fe2e1b`): each read back via `git show` equals its
source (`.remedy-wt/f029-r8/block.md`, `.remedy-wt/f029-r8-payloads/booking.diff`,
`.remedy-wt/f029-r8-payloads/plan.md`) byte for byte — see G1 above.
`.agent/authored/f029-r8-mutations.py` (C4, `d1ec54f86`) is this session's
OWN tool, not reviewer-authored text, so it carries no fidelity comparison;
its behavior is proved instead by G5's live run above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| G1 transport | done | PASS — all copies byte-identical |
| G2 the records | done | PASS — sha256 and open_finding_ids both match |
| G3 the code | done | PASS — ruff exit 0, `rerun_decision_items`, `mission_job_reruns` and the changed lines of `mission_iteration_facts`/`refresh_mission_dossier` quoted from disk |
| G4 the tests | done | PASS — 951 passed, 7 skipped, exit 0; +18 nodes fully accounted (104→122 collected); integrity check all 6 pass |
| G5 the red proofs | done | PASS on the first run — all 4 mutations caught, control green before/after, restored byte-identical |
| S1 the items | done | `RERUN_ID_TEMPLATE`, `rerun_decision_items` — defensive reads, singular/plural text, override/no-override outcome |
| S2 the source | done | `mission_job_reruns` — `load_job_plan` imported inside the function, unloadable job skipped |
| S3 the wiring | done | `mission_iteration_facts` gains `reruns`; `refresh_mission_dossier` passes `mission_job_reruns(mission, root)` |

## Deviations & assumptions

None. Every gate passed on its first run; no test this round wrote needed
correction; no existing test went red; no commit was split, reordered or
dropped from the block's ordered C1-C5 sequence.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 8,
then the closure sequence: Built State and the checklist consolidation with
the one full suite, then the evidence job and review zip, then the ledger
rotation, the STATUS line and the pull request. Open findings: 0.
Operator-questions: 0.
