STEP T001/1 — F275 ROUND 10 — the fifth module group, and the first that is a CYCLE

Every horizontal rule in this block is exactly sixty U+2500 characters (§3 item 37).

Goal: Book round 9's PASS, register R-0845 and R-0846, and delete the strongly connected
component `dogfood_run` + `feature_planner` + `overnight_mission` + `progress_ledger` +
`repair_loop_v2` + `self_repair_proposal` — the six modules, their five handler files, 38
catalog entries, three `GroupDef`s, eleven test files, five doc pages and every surviving
call site — in ONE commit, because DECISION F275 D2 and operator RULE 1 make the component
the atomic unit and its members import each other.

Base: `982d016b`. Everything numbered below was measured by the reviewer at that commit, by
APPLYING this whole deletion in a disposable worktree and running the suite to green before
this block was authored. Where a numeral here disagrees with what you measure, REPORT the
disagreement in your deviations and do not adjust the work to fit it.

────────────────────────────────────────────────────────────
Bundle — six commits, in this order and no other

  C0a  save this block verbatim to `.agent/authored/f275-r10.md` with `shutil.copyfile`
  C0b  mirror the SAME bytes to `.agent/last_block.md` with `shutil.copyfile`
  C1   `.agent/plan.md` replaced whole by the PLAN10 slice
  C2   append LEDGER10 to `.agent/live_review.md` and SLIPS10 to `.agent/prose_slips.md`
  C3   the deletion — ONE commit, all 55 paths of the change set below
  C4   `.agent/handoff.md`, rewritten

────────────────────────────────────────────────────────────
Change set — 55 paths in C3, plus six `.agent/` paths across C0a, C0b, C1, C2 and C4.
Nothing outside this list is written. The list is the half that gets executed; where the
prose above and this list disagree, this list wins (§3 item 35).

DELETED WHOLE — 27 paths, by `git rm`:

  the six modules, under `packages/orchestration/`
    dogfood_run.py · feature_planner.py · overnight_mission.py · progress_ledger.py ·
    repair_loop_v2.py · self_repair_proposal.py
  their five handlers, under `apps/cli/commands/`
    dogfood_cmd.py · overnight_mission_cmd.py · progress_cmd.py · repair_loop_v2_cmd.py ·
    self_repair_cmd.py
  eleven test files whose SUBJECT is a dying module
    tests/orchestration/test_dogfood_run.py · test_feature_planner.py ·
    test_overnight_mission.py · test_progress_ledger.py · test_repair_loop_v2.py ·
    test_self_repair_proposal.py · test_progress_redaction.py ·
    tests/cli/test_self_repair_cmd.py · test_overnight_mission_cli.py ·
    test_repair_loop_v2_cli.py · test_progress_feature_runtime.py
  five doc pages whose SUBJECT is a dying module
    docs/system/open-ended-dogfood-run-orchestrator-replay-analyzer-v0.md ·
    docs/system/token-aware-repair-loop-v1-v2.md ·
    docs/system/overnight-mission-contract-review-repair-spine-v0.md ·
    docs/guides/overnight-mission-user-guide-v0.md ·
    docs/guides/token-aware-repair-loop-user-guide-v1.md

EDITED — 28 paths. The `+/-` beside each is what the reviewer's applied dry run produced;
report yours and declare any difference.

  +0/-489  apps/cli/command_catalog.py            the 38 `CommandEntry(` blocks and 3 `GroupDef` lines
  +1/-6    apps/cli/commands/__init__.py          the 5 handler imports and the `for mod in (…)` tuple
  +14/-61  apps/cli/commands/worker_facade_cmd.py `_names_a_mission`, `_cmd_mission_run`, 2 probes
  +5/-2    packages/orchestration/main_builder_adapter.py   the `repair evaluate` next-action
  +0/-1    .agent/f275_deletion_order.md          REGENERATED, never typed — see step (9)
  +0/-1    tests/orchestration/cluster_deletion_map.txt     the one `dogfood_run <- …` edge
  +0/-11   tests/orchestration/import_reachability_allowlist.txt   6 modules + 5 handlers
  +1/-7    tests/orchestration/test_cluster_deletion_map.py 6 `CLUSTER_MODULES` lines + a docstring
  +5/-2    tests/orchestration/test_main_builder_adapter.py the assertion R-0846 describes
  +3/-3    tests/cli/test_cli_ux.py               3 group names out of two rosters
  +1/-27   tests/cli/test_worker_facade_cmd.py    1 test, 1 assertion, `MagicMock`, `_MISSION_LOOP`
  +0/-94   tests/orchestration/test_builder_routing.py
  +0/-27   tests/orchestration/test_development_artifact_boundary.py
  +0/-43   tests/orchestration/test_do_continue.py
  +0/-18   tests/orchestration/test_local_model_advisor.py
  +0/-44   tests/orchestration/test_model_route_tournament_integration.py
  +0/-28   tests/orchestration/test_overnight_mission_integration.py
  +0/-40   tests/orchestration/test_real_test_execution.py
  +0/-59   tests/orchestration/test_token_economy_integration.py
  +0/-45   tests/orchestration/test_worker_route_integration.py
  +0/-5    pyproject.toml
  +0/-2    scripts/remedy_test_fast.sh
  +0/-1    tests/test_test_categories.py
  +0/-5    docs/README.md
  +1/-5    docs/system/development-artifact-boundary-v0.md
  +0/-2    docs/system/run-contract-v1.md
  +0/-2    docs/system/snapshot-rollback-v1.md
  +0/-6    docs/system/real-test-execution-snapshot-rollback-proof-v1.md

────────────────────────────────────────────────────────────
The deletion, step by step. Steps (1) to (12) are ONE commit, C3.

 (1) `git rm` the 27 whole files listed above.

 (2) `apps/cli/command_catalog.py`. Remove the `CommandEntry(` block of each of these 38
     command ids, from its own `    CommandEntry(` line through its matching `    ),`:
       dogfood.brainstorm · dogfood.checkpoints · dogfood.create · dogfood.evaluate ·
       dogfood.morning-report · dogfood.next · dogfood.replay · dogfood.run-loop ·
       dogfood.show · dogfood.status · dogfood.step · dogfood.stop ·
       overnight.contract-create · overnight.contract-readiness · overnight.contract-show ·
       overnight.cycles · overnight.evaluate · overnight.integrity · overnight.next-action ·
       progress.checklist · repair.attempts · repair.context-pack · repair.evaluate ·
       repair.integrity · repair.item-create-from-failure · repair.item-create-from-review ·
       repair.item-list · repair.item-show · repair.policy-set · repair.policy-show ·
       repair.route-recommend · self-repair.proposal-approve · self-repair.proposal-create ·
       self-repair.proposal-deny · self-repair.proposal-edit · self-repair.proposal-list ·
       self-repair.proposal-show · self-repair.worker-prompt
     Then remove the three `GroupDef` lines whose key is `"progress"`, `"dogfood"` and
     `"self-repair"`. THE `overnight` AND `repair` GROUPS AND THEIR `GroupDef`s SURVIVE, with
     four and six ids left: `overnight.plan`, `overnight.readiness`, `overnight.report`,
     `overnight.run`, `repair.failure-show`, `repair.propose`, `repair.request`,
     `repair.request-show`, `repair.start`, `repair.status`.

 (3) `apps/cli/commands/__init__.py`. Remove the five import lines `dogfood_cmd,`,
     `overnight_mission_cmd,`, `progress_cmd,`, `repair_loop_v2_cmd,`, `self_repair_cmd,`
     and remove those same five names from the single-line `for mod in (…)` tuple.

 (4) `apps/cli/commands/worker_facade_cmd.py`. Delete the two `_try_import` lines naming
     `packages.orchestration.dogfood_run` and `packages.orchestration.self_repair_proposal`
     (three source lines, the second call is wrapped). Then delete `_names_a_mission` whole
     and REPLACE `_cmd_mission_run` whole with CODE1 below, keeping the
     `# mission run facade (Step 2624)` banner comment above it untouched.

 (5) `packages/orchestration/main_builder_adapter.py`. Replace the two lines of CODE2-FROM
     with CODE2-TO. FROM count in that file at `982d016b` is 1.

 (6) `tests/orchestration/test_main_builder_adapter.py`. Replace CODE3-FROM with CODE3-TO.
     FROM count in that file at `982d016b` is 1.

 (7) The ratchet inputs. From `tests/orchestration/import_reachability_allowlist.txt` remove
     the 11 lines naming the six `packages.orchestration.<module>` and the five
     `apps.cli.commands.<handler>`. From `tests/orchestration/cluster_deletion_map.txt` remove
     the one line `packages.orchestration.dogfood_run <- apps/cli/commands/worker_facade_cmd.py`.
     From `tests/orchestration/test_cluster_deletion_map.py` remove the six `CLUSTER_MODULES`
     entries naming the dying modules, and in `_cluster_module_of`'s docstring change
     `from packages.orchestration.dogfood_run import run` to
     `from packages.orchestration.builder_routing import run` — that example names a module
     this commit deletes and the sweep at G4 reads it.

 (8) The surviving tests. Remove exactly these definitions, each with the blank run that
     FOLLOWS it, and nothing else. Every one was measured RED by the reviewer's applied dry
     run at `982d016b`; NOTHING here is removed because its name matched a grep.
       tests/orchestration/test_overnight_mission_integration.py     class TestProgressLedger
       tests/orchestration/test_model_route_tournament_integration.py classes TestProgressLedger, TestFeatureSuggestions
       tests/orchestration/test_worker_route_integration.py          classes TestProgressLedgerItems, TestFeatureSuggestions
       tests/orchestration/test_token_economy_integration.py         classes TestProgressLedger, TestFeatureSuggestions
       tests/orchestration/test_real_test_execution.py               class TestMissionGates
       tests/orchestration/test_do_continue.py                       class TestContinuationIntegrations
       tests/orchestration/test_builder_routing.py                   class TestEmittedCommandsRunnable
       tests/orchestration/test_development_artifact_boundary.py     methods TestFunctionalNoAgent.test_real_mission_morning_report_no_agent and .test_real_doctor_core_imports_no_agent
       tests/orchestration/test_local_model_advisor.py               method TestAdvisorImpact.test_advisor_dict_redacted_for_downstream
       tests/cli/test_worker_facade_cmd.py                           method TestMissionRun.test_run_calls_loop
     Then in `tests/cli/test_worker_facade_cmd.py` also: narrow
     `from unittest.mock import MagicMock, patch` to `from unittest.mock import patch`, delete
     the whole line beginning `_MISSION_LOOP = `, and delete the single line
     `        assert "mission_facade" in check_names`. `TestMissionRun` keeps
     `test_run_no_run_id` and MUST NOT be left empty.
     Then in `tests/orchestration/test_development_artifact_boundary.py` remove the three
     allowlist string lines `"packages/orchestration/overnight_mission.py",`,
     `"packages/orchestration/repair_loop_v2.py",` and
     `"apps/cli/commands/progress_cmd.py",`.
     Then in `tests/cli/test_cli_ux.py` remove the string entries `"self-repair"`, `"dogfood"`
     and `"progress"` from `_INTERNAL_GROUPS` and the entries `"self-repair"` and `"dogfood"`
     from the list inside `TestNoInternalInDefault.test_no_internal_names`.

 (9) `.agent/f275_deletion_order.md` is REGENERATED, never hand-edited: keep its 26-line
     comment header byte for byte, import `measured_order()` from
     `tests/orchestration/test_cluster_deletion_order.py`, and render one component per line
     as `", ".join(component)`. It must fall from ELEVEN components to TEN, with
     `packages.orchestration.builder_routing, …candidate_quality, …local_candidate_generator,
     …model_route_tournament` as the new first body line, and its numstat must read `0 1`.

(10) `pyproject.toml`: remove the five lines naming `progress_ledger.py` (a
     `per-file-ignores` entry) and `feature_planner`, `dogfood_run`, `progress_ledger`,
     `progress_cmd` (mypy `module = [` entries).
     `scripts/remedy_test_fast.sh`: remove the two `test_dogfood_run.py` and
     `test_self_repair_proposal.py` lines. `tests/test_test_categories.py`: remove the one
     `"test_dogfood_run.py",` line.

(11) `docs/README.md`: remove the five index rows for the five deleted pages.
     `docs/system/development-artifact-boundary-v0.md`: remove the `overnight mission` and
     `repair loop` table rows, the `- \`dogfood_run.py\` (new policy paths)` bullet and the
     `| Operator next action |` row, and change the `| Mission status |` row's sources to
     `| Mission status | Mission records | \`mission_state.py\` |`.
     `docs/system/run-contract-v1.md`: remove the `- **progress_ledger**:` and
     `- **feature_planner**:` bullets.
     `docs/system/snapshot-rollback-v1.md`: remove the `progress_ledger.py` and
     `feature_planner.py` table rows.
     `docs/system/real-test-execution-snapshot-rollback-proof-v1.md`: remove the whole
     `## Mission contract gate relationship` section, heading and trailing blank included.
     `docs/system/vocabulary.md` IS NOT TOUCHED: its line 245 names
     `packages/orchestration/overnight_mission.py` in the past tense as the prototype this
     deletion performs, which is the documented-absence convention AGENTS.md Code
     Discoverability asks for, and G4 names it as a survivor rather than gating it to zero.

(12) MUST NOT BE TOUCHED, because they are the specification or another feature's plan:
     `docs/roadmap/features/T1_F034.md`, `T2_F260.md`, `T2_F269.md`, `T2_F272.md`,
     `T2_F277.md`.

────────────────────────────────────────────────────────────
CODE1 — the whole replacement body of `_cmd_mission_run`, applied verbatim:

def _cmd_mission_run(ns: argparse.Namespace) -> None:
    """Run the F070 orchestrator loop for one mission, keyed on a MISSION id.

    Until F275 T001 this command carried a SECOND mode on the same name: a
    facade over the prototype cluster's dogfood run loop, keyed on a RUN id
    and selected by resolving the positional against the mission records. The
    cluster is deleted, so the resolution has nothing left to choose between
    and the command resolves exactly one object.
    """
    run_id = getattr(ns, "run_id", "")
    if not run_id:
        _err("run_id required")

    from apps.cli.commands.mission_cmd import _cmd_mission_run_loop
    _cmd_mission_run_loop(
        run_id,
        project=getattr(ns, "project", None),
        iterations=getattr(ns, "iterations", None),
        json_output=getattr(ns, "json", False),
        no_llm=getattr(ns, "no_llm", False),
    )

CODE2-FROM (two lines, in `main_builder_adapter.py`):
    # Intake complete ≠ repaired — downstream gates still required.
    session.next_safe_action = f"remedy repair evaluate {session.repair_id} --json" if session.repair_id else ""

CODE2-TO (five lines):
    # Intake complete ≠ repaired — downstream gates still required. The
    # command this pointed at, `remedy repair evaluate`, was deleted with the
    # prototype cluster (F275 T001) and Remedy deliberately does not name a
    # replacement here: no surviving command evaluates a repair WORK ITEM.
    session.next_safe_action = ""

CODE3-FROM (two lines, in `tests/orchestration/test_main_builder_adapter.py`):
        # Next action should point to repair evaluate, not claim done.
        assert "repair evaluate" in updated.next_safe_action

CODE3-TO (five lines):
        # Intake complete must not CLAIM done. It used to say so by naming
        # `remedy repair evaluate`; that command was deleted with the prototype
        # cluster (F275 T001) and no surviving command evaluates a repair work
        # item, so the honest next action is now the empty one.
        assert updated.next_safe_action == ""

CODE1, CODE2-TO and CODE3-TO are the ONLY insertions this round makes into `packages/`,
`apps/` or `tests/`; every other edit is a pure removal. The reviewer's applied dry run
produced 31 insertions against 14365 deletions over these 55 paths.

────────────────────────────────────────────────────────────
Constraints

 1. Every slice between a BEGIN and an END marker is applied BYTE FOR BYTE. Do not edit,
    reflow, rewrap, correct or renumber a slice, not even where you believe it is wrong.
    Verify each slice's byte count and sha256 against its own BEGIN line BEFORE using it.
 2. You write no `Done:` paragraph, no `Landed:` line, no verdict, no finding and no
    registration of your own. `Gate: F275 R9`, `- R-0845` and `- R-0846` are inside LEDGER10
    and are the reviewer's text.
 3. C3 IS ONE COMMIT. Operator RULE 1 and DECISION F275 D2 forbid splitting a component, and
    its six modules import each other. Deletions carry no insertions, so the AGENTS.md
    DECISION F104 D1 cap of 500 counts only the 31 insertions of CODE1, CODE2-TO and CODE3-TO.
 4. C2 precedes C3. R-0846 in LEDGER10 states a fact about a change C3 makes and names THIS
    constraint rather than a sha, because that commit does not exist when the slice is
    written (§3 item 20, the R-0524 carve-out).
 5. `.agent/plan.md` is advanced at C1, the first substantive commit, per §3 item 23.
 6. All destructive verification — the G5 red-proof and any base-side reading — runs in a
    disposable worktree under `.remedy-wt/`, never in the primary checkout (protocol G5).
    Read a base-side blob with `git show <sha>:<path>` or in such a worktree; never by
    overwrite-and-restore (§3 item 29).
 7. Create no pull request, merge nothing, push no force. Push once, after C4.
 8. Re-read `.agent/STOP` from disk before C0a and again at G8. It does not exist at
    `982d016b`.

────────────────────────────────────────────────────────────
Done when — eight gates, every one RUN, real exit codes reported, one line per gate in the
handback. G1 to G7 all run at or before C3, so C4 can quote them (§3 item 31).

G1 TRANSPORT. `.agent/authored/f275-r10.md` at C0a and `.agent/last_block.md` at C0b are
   each the byte count and sha256 the delegation states for this block file, and equal each
   other. Per §3 item 37 this claims nothing about the bytes the reviewer emitted: all three
   artefacts are your own output, so the chain detects a fault in your copying and nothing
   upstream of it.

G2 THE PLAN. The committed `.agent/plan.md` at C1 is BYTE-IDENTICAL to the PLAN10 slice:
   2948 bytes, sha256 8e583c36e2f8f12a29f7ac446ed822d8492a3e37d092ae5f6dfea1e7eba65643,
   49 lines against the AGENTS.md cap of 50.

G3 THE RECORD, read from the committed blobs at C1 (pre) and C2 (post), never from the
   worktree. (a) `.agent/live_review.md` 559516 -> 569448, growth 9932 = 1 + 9931;
   `.agent/prose_slips.md` 175541 -> 177821, growth 2280 = 1 + 2279. (b) the pre-blob is a
   byte-exact PREFIX and the slice a byte-exact SUFFIX of each post-file, and the joining byte
   reads back as a newline. (c) an INDEPENDENT structural reader: count N from the slice
   itself, then show that the file's LAST N blank-line-separated units equal the slice's N
   paragraphs IN ORDER, printing a per-unit sha256 — do not assert N, count it (§3 item 36).
   (d) a NEGATIVE CONTROL flipping one byte IN MEMORY inside the FIRST appended paragraph of
   each file is REJECTED by both readers (b) and (c); re-read both tracked files from disk
   afterwards and show they are byte-equal to the committed post-blobs. (e) `^Gate: ` 31 -> 32,
   and `^Gate: F275 R9 `, `^- R-0845 — ` and `^- R-0846 — ` exactly 1 each. (f) THE OPEN SET
   BY DISTINCT ID: registrations `^- R-\d+ — ` minus resolutions `^Done: R-\d+ — `, 73/4/69
   open before and 75/4/71 open after — two registrations, no resolution.

G4 THE DELETION IS COMPLETE. At C3, `git ls-tree -r <C3> --name-only` contains NONE of the 27
   deleted paths (print False for each). Then, over the tracked tree EXCLUDING `.agent/` and
   `.data/`, report the whole-word count of each of the six module names and PRINT EVERY
   REMAINING LINE — never a truncated sweep. The reviewer measured at the dry run, after the
   whole change set: `dogfood_run` 6, `feature_planner` 3, `overnight_mission` 7,
   `progress_ledger` 8, `repair_loop_v2` 3, `self_repair_proposal` 1, and EVERY one of those
   28 lines is a must-not-touch item — 18 in `docs/roadmap/features/`, one in
   `docs/system/vocabulary.md` per step (11), and the rest in `docs/system/` pages naming a
   module in a superseded-history sentence. If your sweep finds a line that is NOT one of
   those, that is a real miss: fix it and say so. Additionally these must be at ZERO:
   `_cmd_mission_run` occurrences in `apps/cli/commands/dogfood_cmd.py` (the file is gone),
   `_names_a_mission` 0, `run_mission_loop` 0, `build_mission_morning_report` 0,
   `list_self_repair_proposals` 0, `build_progress_ledger` 0, `build_feature_plan` 0.

G5 RATCHETS, READERS AND THE RED-PROOF.
   (a) `python3 -B -m pytest tests/orchestration/test_import_reachability.py
       tests/orchestration/test_cluster_deletion_map.py
       tests/orchestration/test_cluster_deletion_order.py
       tests/orchestration/test_main_builder_adapter.py -q` -> exit 0. The reviewer read
       60 passed at the dry run.
   (b) `python3 -B -m pytest tests/docs/ -q` -> exit 0, and the canary
       `python3 -B -m pytest tests/cli/test_golden_path.py -q` -> exit 0.
   (c) THROUGH THE SHIPPED READERS, not by grep: `len(apps.cli.command_catalog._BASE_CATALOG)`
       and `len(apps.cli.commands.collect_all_handlers())` are 296 at C3 against 334 at the
       base, and `len(apps.cli.command_catalog.GROUPS)` is 56 against 59. Print that all 38
       ids of step (2) are ABSENT from both readers, that the ten survivors named in step (2)
       are PRESENT in both, and that `dogfood`, `progress` and `self-repair` are absent from
       `GROUPS` while `overnight` and `repair` are present.
   (d) `.agent/f275_deletion_order.md` holds TEN components at C3 against eleven at the base,
       and `git show --numstat <C3> -- .agent/f275_deletion_order.md` reads `0 1`.
   (e) RED-PROOF, in a disposable worktree at C3 and NOWHERE ELSE, `__pycache__` purged before
       every run and `python3 -B` throughout. Selection = the four-file command of (a). Count
       each FROM string in its own named file first and require exactly 1 (§3 item 25); apply
       each mutation ALONE, revert it, and re-check the revert by sha256:
         (i)   add `    "packages.orchestration.dogfood_run",` to `CLUSTER_MODULES` in
               `tests/orchestration/test_cluster_deletion_map.py`
         (ii)  add the line `packages.orchestration.dogfood_run` to
               `tests/orchestration/import_reachability_allowlist.txt`
         (iii) in `packages/orchestration/main_builder_adapter.py` restore CODE2-FROM's second
               line in place of `    session.next_safe_action = ""`
       Report the UNMUTATED control on BOTH sides. The reviewer measured, at the dry run:
       control exit 0 at 60 passed, then exit 1 at 2, 1 and 1 failures, then control exit 0
       again. ORDER THE COLOUR SEQUENCE, and report failure counts as measured.

G6 RUFF AND BASH. `python3 -m ruff check` over exactly the `.py` files that
   `git diff --name-only 982d016b..<C3>` names AND that still exist at C3 -> `All checks
   passed!`, exit 0, and name the count you linted. Then `python3 -m ruff check .` reads
   `Found 26 errors.` at C3, which is the ceiling
   `tests/orchestration/test_ci_budgets.py` holds — the reviewer read 26 at the base too, so
   this round adds none. Read the base side with a disposable worktree, never by writing to
   the primary checkout. `bash -n scripts/remedy_test_fast.sh` -> exit 0.

G7 THE FULL SUITE, run SERIALLY (no `-n auto`) in the PRIMARY checkout, exit code read from
   the process object and never from a pipe. The reviewer measured 19209 passed and 23 skipped
   at the dry run, against 19590 passed and 23 skipped at the base. Close the arithmetic:
   `--collect-only tests/` is 19613 at the base and 19232 at C3, a fall of 381, and that 381
   is 325 + 32 + 24 — 325 collected ids in the eleven deleted test files, 32 lost across the
   ten files of step (8), and 24 in `tests/test_grouped_cli.py`, which the deletion never
   names and which parametrises over the catalog. Take the base-side collections in a
   disposable worktree or before C3 while the code tree is still byte-identical to `982d016b`;
   say which you did.

G8 THE TREE. `.agent/STOP` re-read from disk and absent; `git status --porcelain` empty;
   `git worktree list` naming the primary checkout ALONE; branch still
   `feature/f275-one-world-completion-part-three`;
   `git diff --name-only 982d016b..<C3>` naming EXACTLY the 55 paths of the change set above,
   as a SET comparison printing anything extra and anything missing; and every commit in the
   range single-parent with its insertion count, for C0a through C3 only — C4's own numbers
   belong to the next round's ledger entry (§3 items 14 and 31).

Handback: rewrite `.agent/handoff.md` with the mandated sections — the state block carrying
`SESSION 6 of feature F275 · round 10`, the per-commit changed-files table, one line per gate
with its real exit code, the deviations, the item-status table and the next steps. It has no
length cap. Do not create or merge a PR.

────────────────────────────────────────────────────────────
Slices. Each is the bytes STRICTLY BETWEEN its BEGIN and END marker lines; the
marker lines themselves are never applied. Verify byte count and sha256 against the
BEGIN line before use (constraint 1).

BEGIN PLAN10 — 2948 bytes — sha256 8e583c36e2f8f12a29f7ac446ed822d8492a3e37d092ae5f6dfea1e7eba65643 — replaces .agent/plan.md WHOLE at C1
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 10 books round 9's PASS, registers R-0845 and R-0846, and deletes the FIFTH module
group and the first that is a strongly connected COMPONENT: `dogfood_run`, `feature_planner`,
`overnight_mission`, `progress_ledger`, `repair_loop_v2` and `self_repair_proposal`, whole,
in ONE commit under DECISION F275 D2. With them go their five handler files, 38 catalog
entries, the `dogfood`, `progress` and `self-repair` groups, eleven test files, five doc
pages and the surviving call sites. `apps/cli/commands/worker_facade_cmd.py` SURVIVES and
loses the dogfood mode of `mission run`; `packages/orchestration/main_builder_adapter.py`
SURVIVES and loses its `remedy repair evaluate` next-action. Both losses are registered.

## Next Steps

1. The `builder_routing` / `candidate_quality` / `local_candidate_generator` /
   `model_route_tournament` component, which this round's regeneration makes the order
   file's first line. Its four modules import each other, so DECISION F275 D2 makes the
   whole component one commit.
2. The remaining components in the recorded order, the single-module ones as ordinary
   group commits and the two-module `provider_trust` pair as one.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and
   R-0831, R-0840, R-0842, R-0844, R-0845 and R-0846 named among the ideas deleted rather
   than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 69 by distinct id at this round's base `982d016b`; the ledger commit this
  block fixes as C2 registers R-0845 and R-0846, taking it to 71. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- The two carry-overs F260's Design orders before the first `git rm` ARE DONE: `mission
  readiness` landed in round 3 and `mission report` in round 4, and `Gate: F275 R4` records
  both. No carry-over work is owed by this round or any later one.
- `tests/test_grouped_cli.py` parametrises over the catalog, so 24 of this round's 381
  collected-id fall come from a file the deletion never names. A file-level reading of the
  fall cannot close; only the id-set difference can.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel
  tests race for a server port and the vitest node needs `apps/ui/node_modules`.
END PLAN10

BEGIN LEDGER10 — 9931 bytes — sha256 e21bd30fc4a05ca3e41e19942096e40b1a5ee3e4e20d31096f03b0f7c6a6a611 — APPENDED to .agent/live_review.md at C2
Gate: F275 R9 — the F275 round 9 entry. VERDICT PASS, booked by round 10 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 9 handback committed at `1300bd3dd46977d766885862f9831597564df860` with the verdict appended at `982d016b`. Range `aae6d313dbedc64c84703eae7a782e67439ccdec`..`1300bd3d`, six commits — C0a `b3db8d01`, C0b `effecd77`, C1 `2901e0b2`, C2 `ea039fc8`, C3 `6c601b35`, C4 `1300bd3d` — every one single-parent, per-commit insertions 400, 372, 19, 12, 11 and 365, all under the AGENTS.md DECISION F104 D1 cap of 500. THE FOURTH MODULE GROUP IS GONE: `review_bundle`, its two test files, its two `docs/system/` pages, its ONE `review.bundle` catalog entry, the ONE handler function that imported it, and 27 test functions across 16 surviving files, at 11 insertions against 4694 deletions over 40 paths. G1 TRANSPORT covers the chain this workflow can walk, per §3 item 37, and not the emitted bytes: the reviewer's own scratchpad original, `.agent/authored/f275-r9.md` and `.agent/last_block.md` all 36871 bytes at `178bd6cae149517cab73a806385dd9bd608176e4416247713b3c6ca34333d7fe`. G2: `.agent/plan.md` byte-identical to PLAN9 at 2616 bytes and 45 lines. G3 THE RECORD: `.agent/live_review.md` 552280 to 559516, growth 7236 = 1 + 7235; `.agent/prose_slips.md` 173925 to 175541, growth 1616 = 1 + 1615; both edges byte-exact, N counted from each slice by the reviewer's own reader as 4 and 2 with ordered equality over the WHOLE appended region, both negative controls flipped on the FIRST appended paragraph and REJECTED by both readers; `^Gate: ` 30 to 31 and THE OPEN SET 68 TO 69 BY DISTINCT ID against registrations 71 to 73 and resolutions 3 to 4. G4: all five deleted files absent from `git ls-tree` at C3 over 4632 tracked files, all ten gated strings at ZERO over the 1753 tracked files outside `.agent/` and `.data/`, and the whole-word token `review_bundle` at EXACTLY FIVE lines, every one a must-not-touch item. G5: the three ratchets 9 passed at exit 0; through the SHIPPED readers `_BASE_CATALOG` and `collect_all_handlers()` both fell 335 to 334 with `review.bundle` ABSENT and all four survivors PRESENT; the regenerated order file held ELEVEN components at a `0 1` numstat. THE RED-PROOF WAS RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE: control exit 0 at 9 passed, three restorations exit 1 at 2, 2 and 1 failures, control exit 0 again. G6: ruff `All checks passed!` over the 24 edited Python files, and repo-wide `Found 24 errors.` at BOTH the base and the tip. G7: THE FULL SUITE RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT at exit 0, 19590 passed and 23 skipped, with `--collect-only` 19751 at the base and 19613 at C3 — a fall of 138 = 104 + 34. G8: `.agent/STOP` absent, tree clean, one worktree, 45 paths in an EXACT SET MATCH. THE ROUND'S REAL CONTENT IS A SCOPE CORRECTION: the session-4 map prescribed deleting `apps/cli/commands/review_cmd.py` whole and measured RED at FIFTEEN failures when applied, because only ONE of its five handlers imported the deleted module; the counter-measure, stated as a reading rather than a habit, is that a `*_cmd.py` handler file belongs to a module group only for the handlers that IMPORT the module, and the group's boundary is established by APPLYING the deletion. THREE DEVIATIONS WERE DECLARED AND ALL THREE ARE SUSTAINED; two are the reviewer's own numerals — the block's `45 paths` heading over a body of 46 and the R-0844 paragraph's catalog figures of 336 and 335 where the measured pair is 335 and 334 — and both are dated `.agent/prose_slips.md` lines rather than ids, per amend0827 rule 2, because nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong and R-0844's substance holds at either count. The third, three single-blank-line seams left by step (13)'s wording, is cosmetic and unreachable by any configured ruff rule. NO FINDING IS RESOLVED BY THIS GATE and none is minted here; R-0843 and R-0844 were minted by round 9's own C2.

- R-0845 — Medium, DELETING THE SIX-MODULE COMPONENT REMOVES 38 COMMANDS, THREE WHOLE COMMAND GROUPS AND HALF OF `remedy mission run`, AND NO SURVIVING COMMAND CARRIES ANY OF IT. Raised by the reviewer while authoring F275 round 10, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherits the idea. THE MEASUREMENT, taken at `982d016b` by an APPLIED dry run of the whole deletion in a disposable worktree, through the SHIPPED readers rather than by grep: `len(apps.cli.command_catalog._BASE_CATALOG)` and `len(apps.cli.commands.collect_all_handlers())` both fall 334 to 296, and `len(apps.cli.command_catalog.GROUPS)` falls 59 to 56. The 38 ids are the whole of `dogfood` (12), the whole of `self-repair` (7), the whole of `progress` (1 — `progress.checklist`), seven of the eleven `overnight` ids (`contract-create`, `contract-readiness`, `contract-show`, `cycles`, `evaluate`, `integrity`, `next-action`) and eleven of the seventeen `repair` ids (`attempts`, `context-pack`, `evaluate`, `integrity`, `item-create-from-failure`, `item-create-from-review`, `item-list`, `item-show`, `policy-set`, `policy-show`, `route-recommend`). The `overnight` and `repair` groups and their `GroupDef`s SURVIVE with four and six ids each; `dogfood`, `progress` and `self-repair` lose their `GroupDef` too, which `tests/test_command_catalog.py::TestCatalogIntegrity::test_every_group_has_at_least_one_command` is what would catch. THE HALF NO CATALOG READING SHOWS: `apps/cli/commands/worker_facade_cmd.py` SURVIVES this round and its `_cmd_mission_run` carried TWO modes on one name — the F070 orchestrator loop keyed on a mission id, and a facade over `packages.orchestration.dogfood_run.run_mission_loop` keyed on a RUN id, resolved between by `_names_a_mission`. The second mode and the resolver both die here, so `remedy mission run` stops accepting a dogfood run id and resolves exactly one object. That coupling is a real `from packages.orchestration.dogfood_run import run_mission_loop` statement inside the function body and NOT the string-keyed `importlib` probe the round 9 handback's map recorded, which is why an inherited map understated it. WHICH FEATURES INHERIT WHICH IDEA, named as RULE 3 requires and not rebuilt here: the mission contract and its readiness, evaluation and next-action views go to F269, which `docs/system/vocabulary.md` already records as the feature that builds the contract; the repair work item, its route recommendation and its policy knobs go to F110, which owns routing configuration, with R-0831 already holding the knob-by-knob audit; the self-repair proposal queue and its approve/deny/edit gate go to the approval gate F017 owns; and the dogfood run orchestrator and its replay analyser have NO inheritor by design, because F260's Design deletes the prototype rather than carrying it. THE FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that paragraph names all 38 ids and the `mission run` mode among the ideas DELETED rather than inherited, and states for each of the four groups above which feature took it — a stub, a shim, an alias or a compatibility reader is forbidden by AGENTS.md Scope Control by name, and this finding is not resolved by providing one.

- R-0846 — Low, A SURVIVING PRODUCTION MODULE'S `next_safe_action` BECOMES PERMANENTLY EMPTY BECAUSE THE ONLY COMMAND IT COULD NAME IS DELETED. Raised by the reviewer while authoring F275 round 10, under the same operator RULE 3 as R-0845 and registered separately because the defect, the file and the fix are different: R-0845 is about the CLI surface a user invokes, and this one is about a value a surviving module writes into a record. THE MEASUREMENT, taken at `982d016b`. `record_builder_session_intake_complete` in `packages/orchestration/main_builder_adapter.py` sets `session.next_safe_action` to `f"remedy repair evaluate {session.repair_id} --json"` whenever the session carries a `repair_id`, and `remedy repair evaluate` is one of the eleven `repair` ids R-0845 measures as dying. `main_builder_adapter` is NOT deleted by this round — it is a single-module component further down `.agent/f275_deletion_order.md` — so the assignment survives its target and would advertise a command the catalog no longer carries, which `tests/cli/test_advertised_commands.py::test_every_advertised_command_exists_in_the_catalog` reads production code for and fails on. THE CHANGE THIS ROUND MAKES, whose commit is fixed by constraint 4 of the round 10 block rather than by a sha, because the commit does not exist while this paragraph is written: the assignment becomes the empty string with a comment stating that no surviving command evaluates a repair WORK ITEM, and `tests/orchestration/test_main_builder_adapter.py::TestSessionLifecycle::test_intake_complete_does_not_satisfy_repair` keeps its subject — intake complete must not CLAIM done — by asserting the empty value instead of the command string. WHAT IS ACTUALLY LOST: a builder session that completed intake only now tells its reader nothing about what to do next, where it used to name the evaluation step. It is LOW rather than Medium because the STATUS the test guards is unchanged — `BuilderSessionStatus.COMPLETED_INTAKE_ONLY` still distinguishes intake from repair, so no caller can mistake one for the other — and only the human-readable hint is gone. THE FIX CLAUSE, binding on F110 when it takes the repair work item R-0845 routes to it: the intake-complete next action is restored to name whatever command F110 gives the repair work item, and until then the empty value is the honest one — Remedy deliberately does not name a replacement command here, and the comment in the source says so where a reader would search for it.
END LEDGER10

BEGIN SLIPS10 — 2279 bytes — sha256 cda11055a3d76353fcea0ffa8c219b7cfc19d4614b867e75f87f09016145ce45 — APPENDED to .agent/prose_slips.md at C2
2026-09-09 · F275 R10 · The round 10 map that session 5 wrote into `.agent/handoff.md` states that the two carry-overs F260's Design orders before the first `git rm` — overnight readiness and the overnight report becoming `mission readiness` and `mission report` — have not landed, and orders the next session to settle their ordering as a dated DECISION before any deletion; both had in fact landed at F275 rounds 3 and 4, `Gate: F275 R4` in `.agent/live_review.md` records that DECISION F274 D2's coupling was honoured exactly and that the carry-over and the death of the old holder were one commit `d045eaf6`, and at `982d016b` `mission.readiness` and `mission.report` are live catalog entries whose handlers in `apps/cli/commands/mission_cmd.py` read `packages/orchestration/mission_readiness.py` and never the cluster, so the DECISION the map ordered is owed by nobody and round 10 does not write it.

2026-09-09 · F275 R10 · The same map records the surviving coupling from `apps/cli/commands/worker_facade_cmd.py` to the dying component as two STRING-keyed `importlib` doctor probes of the R-0832 class, and there is a third site it does not name: `_cmd_mission_run` carries a real `from packages.orchestration.dogfood_run import run_mission_loop` statement in its body at line 326 of that file at `982d016b`, which is the dogfood-facade half of `remedy mission run` and a user-observable behaviour rather than a diagnostic row — so a round that had trusted the map would have deleted the module out from under a live production code path, and the applied dry run rather than the map is what found it.

2026-09-09 · F275 R10 · The same map names two `docs/system/` pages as dying whole and predicts the collected-id fall from the test files it lists; the applied dry run measured FIVE pages whose subject is a dying module, three of them found only because `tests/cli/test_advertised_commands.py` reads operator-facing pages for command strings the catalog no longer carries, and measured the fall as 381 collected ids of which 24 belong to `tests/test_grouped_cli.py`, a file the deletion never names and that parametrises over the catalog — so a fall predicted from a file list cannot close, and only the id-set difference between the two collections can.
END SLIPS10
