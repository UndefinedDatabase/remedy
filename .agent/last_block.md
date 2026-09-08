-------------------- (20 hyphens) F275 ROUND 9 -------------------- (20 hyphens)
STEP T001 — F275 ROUND 9 — DELETE THE `review_bundle` MODULE GROUP

Goal:
  Book round 8's PASS, resolve R-0841, register R-0843 and R-0844, and delete the FOURTH
  prototype-cluster module group: `packages/orchestration/review_bundle.py` with everything
  that exists ONLY for it (operator RULE 1, `docs/roadmap/features/T2_F275.md` T001). What
  that rule EXCLUDES is the scope line that matters this round.
  `apps/cli/commands/review_cmd.py` holds FIVE handlers. Only `_cmd_review_bundle` imports the
  deleted module; the other four import `packages.orchestration.reviewer`, which SURVIVES and
  is not on F260's Design list. So THE FILE SURVIVES, the `review` group and its `GroupDef`
  survive, and four of its five catalog entries survive. The reviewer applied the over-wide
  reading in a disposable worktree before authoring: RED at fifteen failures, and it destroys
  four working commands.

Bundle (ordered; the worker commits in exactly this order):
  C0a  save this block verbatim as `.agent/authored/f275-r9.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   `.agent/plan.md` <- the PLAN9 slice, byte for byte (first substantive commit, item 23)
  C2   `.agent/live_review.md` <- append LEDGER9; `.agent/prose_slips.md` <- append SLIPS9
  C3   the deletion, ONE commit, steps (1) to (17) below
  C4   `.agent/handoff.md`, the round 9 handback

Change (45 paths, and nothing outside this list; `·` separates paths):
  .agent/: authored/f275-r9.md · last_block.md · plan.md · live_review.md · prose_slips.md ·
    handoff.md · f275_deletion_order.md
  packages/orchestration/: review_bundle.py · ui_server.py
  apps/cli/: command_catalog.py · commands/review_cmd.py · commands/worker_facade_cmd.py
  root/scripts: pyproject.toml · scripts/remedy_test_runtime.sh
  docs/: README.md · system/review-bundle-v1.md ·
    system/review-bundle-structured-error-reporting-v1.md · system/test-lanes-v0.md ·
    system/development-artifact-boundary-v0.md · system/run-contract-v1.md ·
    system/snapshot-rollback-v1.md · system/run-replay-to-self-repair-proposal-v0.md ·
    guides/self-repair-proposal-user-guide-v0.md
  tests/cli/: test_review_bundle_runtime.py · test_worker_facade_cmd.py · test_product_spine.py
  tests/: test_test_categories.py · orchestration/import_reachability_allowlist.txt
  tests/orchestration/: test_review_bundle.py · test_cluster_deletion_map.py · test_config.py ·
    test_development_artifact_boundary.py · test_do_continue.py ·
    test_external_builder_sandbox.py · test_job_fulfillment.py · test_progress_redaction.py ·
    test_model_route_tournament_integration.py · test_overnight_executor.py ·
    test_overnight_mission_integration.py · test_provider_patch_material.py ·
    test_provider_trust.py · test_repair_request_builder.py · test_self_dogfood.py ·
    test_self_dogfood_execution.py · test_token_economy_integration.py ·
    test_worker_route_integration.py

THE DELETION, STEPS (1) TO (17), ALL IN COMMIT C3:

 (1) `git rm` these five files, whole:
       packages/orchestration/review_bundle.py                          (2254 lines)
       tests/orchestration/test_review_bundle.py                        (1358 lines)
       tests/cli/test_review_bundle_runtime.py                          ( 327 lines)
       docs/system/review-bundle-v1.md                                  (  73 lines)
       docs/system/review-bundle-structured-error-reporting-v1.md       (  96 lines)

 (2) `apps/cli/commands/review_cmd.py` — delete the function `_cmd_review_bundle` whole,
     together with the blank run that follows it, and delete the single handler-table line
       `    "review.bundle": lambda args: _cmd_review_bundle(args),`
     THE FILE STAYS. The other four handlers and the `COMMAND_HANDLERS` dict stay.

 (3) `apps/cli/command_catalog.py` — delete the ONE `CommandEntry(` whose `command_id` is
     `"review.bundle"`, from its `    CommandEntry(` line through the line before the
     `    CommandEntry(` whose `command_id` is `"review.run"`. The `# ── review ──` group
     comment STAYS, the `"review": GroupDef(...)` line at line 150 STAYS, and the four other
     entries STAY. No other entry names `review.bundle` in a `related=` tuple; the reviewer
     grepped for it and the only occurrence was inside the deleted entry itself.

 (4) `tests/orchestration/import_reachability_allowlist.txt` — delete the single line
     `packages.orchestration.review_bundle`. DO NOT delete `apps.cli.commands.review_cmd`:
     that module survives. Do not re-sort the file.

 (5) `tests/orchestration/test_cluster_deletion_map.py` — delete the single `CLUSTER_MODULES`
     member line `    "packages.orchestration.review_bundle",`.

 (6) `apps/cli/commands/worker_facade_cmd.py` — delete the single line
       `    _try_import("review_bundle", "packages.orchestration.review_bundle", "build_review_bundle")`
     This is the ONE surviving importer and no import graph can see it: it is a STRING key
     handed to `importlib.import_module`, which is why `cluster_deletion_map.txt` has no
     `review_bundle` line at all. It is the R-0832 class.

 (7) `tests/cli/test_worker_facade_cmd.py` — in `test_mnt_tmp_users_redacted`, replace
       `            if name == "packages.orchestration.review_bundle":`
     with
       `            if name == "packages.orchestration.run_contract":`
     The test makes a fake `ImportError` and asserts the doctor redacts its paths. With step
     (6) applied and this line unchanged the branch is unreachable and the assertions pass
     while proving nothing; `run_contract` is a probe the surviving doctor still runs.

 (8) THE R-0841 SWEEP — text this deletion falsifies, in files this change set already edits.
     R-0841's fix clause binds this block. Three sites, each a one-line edit:
     (a) `packages/orchestration/ui_server.py` — in the comment, replace
           `the same catalog in `do_run`, `proof_chain` and `review_bundle`: the`
         with
           `the same catalog in `do_run` and `proof_chain`: the`
     (b) `tests/orchestration/test_development_artifact_boundary.py` — rename
         `test_review_bundle_structured_sections_no_agent` to
         `test_execution_approval_policy_summary_no_agent` and replace its docstring
         `"""Structured review bundle sections do not require .agent/live_review.md."""`
         with
         `"""The execution approval policy summary does not require .agent/live_review.md."""`
         Its BODY calls `execution_approval_policy_summary` and never touches the deleted
         module, so the test survives and only its name was false.
     (c) `tests/orchestration/test_progress_redaction.py` — rename
         `test_review_bundle_progress_no_raw_secrets` to
         `test_progress_ledger_export_no_raw_secrets`. Its body asserts
         `build_progress_ledger` / `export_progress_ledger_json` and nothing else.

 (9) `pyproject.toml` — delete both lines:
       `"packages/orchestration/review_bundle.py" = ["F402"]  # loop var `field` shadows dataclass import — safe`
       `    "packages.orchestration.review_bundle",`

(10) `scripts/remedy_test_runtime.sh` — delete the array member line
       `    tests/cli/test_review_bundle_runtime.py`
     and rewrite the three-line header comment that names the deleted file to:
       `# Subprocess-heavy suites run per-node to isolate hangs at the individual`
       `# test level. Other suites run as whole-file invocations.`
     KEEP the `NODE_ISOLATED_FILES=(` array itself, now empty:
     `tests/cli/test_product_spine.py::TestFastLaneSelfTest` pins that it is DEFINED, and
     bash 5.1 expands an empty array under `set -u` without error. Two tests in that file
     die at step (13) instead.

(11) `tests/orchestration/test_development_artifact_boundary.py` — delete the `_ALLOWED_LEGACY`
     member line `    "packages/orchestration/review_bundle.py",`.

(12) THE TWO LANE ROSTERS that name the deleted test file:
     (a) `tests/test_test_categories.py` — delete BOTH occurrences of the roster line
         `        "test_review_bundle_runtime.py",` (there are exactly two, one per lane test).
     (b) `tests/cli/test_product_spine.py` — delete the single roster line
         `            "test_review_bundle_runtime.py",` from the `heavy` list.
     The tests themselves SURVIVE: they still assert the other three suites.

(13) DELETE THESE 27 TEST FUNCTIONS, each with the blank run that follows it. Every one of
     them imports the deleted module or has it as its whole subject. Format `file :: class ::
     function`:
       tests/cli/test_product_spine.py :: TestFastLaneSelfTest :: test_runtime_lane_review_bundle_is_node_isolated
       tests/cli/test_product_spine.py :: TestFastLaneSelfTest :: test_runtime_lane_includes_review_bundle_runtime
       tests/orchestration/test_config.py :: TestRedactionClosure :: test_r0122_is_optional_is_bug_used
       tests/orchestration/test_config.py :: TestRedactionClosure :: test_r0122_bug_category
       tests/orchestration/test_config.py :: TestRedactionClosure :: test_r0123_structured_error_in_production
       tests/orchestration/test_development_artifact_boundary.py :: TestFunctionalNoAgent :: test_real_review_bundle_build_no_agent
       tests/orchestration/test_development_artifact_boundary.py :: TestFunctionalNoAgent :: test_real_review_bundle_export_no_agent
       tests/orchestration/test_do_continue.py :: TestContinuationIntegrations :: test_review_bundle_continuation_summary
       tests/orchestration/test_external_builder_sandbox.py :: TestSmoke :: test_full_flow_state_transitions
       tests/orchestration/test_external_builder_sandbox.py :: TestRedactionTorture :: test_public_surfaces_never_expose
       tests/orchestration/test_job_fulfillment.py :: TestReviewBundleFulfillment :: test_fulfillment_summary_in_bundle
       tests/orchestration/test_job_fulfillment.py :: TestReviewBundleSafeError :: test_error_no_raw_traceback
       tests/orchestration/test_job_fulfillment.py :: TestIntegrityReadOnlyV07 :: test_build_integrity_summary_no_run_integrity_checks
       tests/orchestration/test_job_fulfillment.py :: TestIntegrityReadOnlyV07 :: test_build_integrity_summary_no_subprocess
       tests/orchestration/test_job_fulfillment.py :: TestChangedFilesSafeScope :: test_scope_field_present
       tests/orchestration/test_model_route_tournament_integration.py :: TestSafeSurfaces :: test_review_bundle_summary_safe
       tests/orchestration/test_overnight_executor.py :: TestRedaction :: test_no_raw_leak
       tests/orchestration/test_overnight_mission_integration.py :: TestSafeSurfaces :: test_review_bundle_summary_no_contract
       tests/orchestration/test_overnight_mission_integration.py :: TestSafeSurfaces :: test_review_bundle_with_contract
       tests/orchestration/test_provider_patch_material.py :: TestRedaction :: test_no_raw_leak_across_surfaces
       tests/orchestration/test_provider_trust.py :: TestRedaction :: test_no_raw_leak_across_surfaces
       tests/orchestration/test_repair_request_builder.py :: TestRedaction :: test_no_raw_leak
       tests/orchestration/test_self_dogfood.py :: TestRedaction :: test_no_raw_leak
       tests/orchestration/test_self_dogfood_execution.py :: TestRedaction :: test_no_raw_leak
       tests/orchestration/test_token_economy_integration.py :: TestSafeSurfaces :: test_review_bundle_summary_safe
       tests/orchestration/test_token_economy_integration.py :: TestSafeSurfaces :: test_no_verified_savings_claim
       tests/orchestration/test_worker_route_integration.py :: TestSafeSurfaces :: test_review_bundle_summary_safe
     `test_public_surfaces_never_expose` is parametrized over EIGHT cases, so these 27
     functions are 34 collected test ids. That is the number the arithmetic in G7 uses.

(14) DELETE THESE 10 CLASS HEADERS, which step (13) leaves with no member, each together with
     its docstring, its comment banner and the blank run around it:
       tests/orchestration/test_external_builder_sandbox.py :: TestSmoke
       tests/orchestration/test_external_builder_sandbox.py :: TestRedactionTorture
       tests/orchestration/test_job_fulfillment.py :: TestReviewBundleFulfillment
       tests/orchestration/test_job_fulfillment.py :: TestReviewBundleSafeError
       tests/orchestration/test_job_fulfillment.py :: TestChangedFilesSafeScope
       tests/orchestration/test_overnight_executor.py :: TestRedaction
       tests/orchestration/test_provider_trust.py :: TestRedaction
       tests/orchestration/test_repair_request_builder.py :: TestRedaction
       tests/orchestration/test_self_dogfood.py :: TestRedaction
       tests/orchestration/test_self_dogfood_execution.py :: TestRedaction
     After step (13) these files do not PARSE, so this step is line-based, not `ast`-based.

(15) NARROW THESE 10 IMPORTS, which steps (13) and (14) orphan. Each FROM occurs exactly once
     in its named file; the reviewer counted each. `->` separates FROM from TO:
       tests/orchestration/test_external_builder_sandbox.py
           `from uuid import UUID, uuid4` -> `from uuid import uuid4`
       tests/orchestration/test_model_route_tournament_integration.py   `import json` -> delete
       tests/orchestration/test_overnight_executor.py                   `import json` -> delete
       tests/orchestration/test_overnight_mission_integration.py        `import json` -> delete
       tests/orchestration/test_repair_request_builder.py               `import json` -> delete
       tests/orchestration/test_self_dogfood_execution.py               `import json` -> delete
       tests/orchestration/test_token_economy_integration.py            `import json` -> delete
       tests/orchestration/test_self_dogfood.py                         `import json` -> delete
       tests/orchestration/test_self_dogfood.py
           `from uuid import UUID, uuid4` -> `from uuid import uuid4`
       tests/orchestration/test_self_dogfood.py
           `from packages.orchestration.storage import load_job, save_job`
             -> `from packages.orchestration.storage import save_job`

(16) THE DOCS. In `docs/README.md` delete the three rows naming the two deleted pages — one
     quick-find row and two index rows. In `docs/system/test-lanes-v0.md` delete the
     `test_review_bundle_runtime.py` table row and rewrite the paragraph naming it so only the
     parenthetical goes. Delete one line each in `development-artifact-boundary-v0.md` (the
     `Review bundle artifact inclusion` row), `run-contract-v1.md` (the `- **review_bundle**:`
     bullet), `snapshot-rollback-v1.md` (the `| `review_bundle.py` |` row), and both
     `self-repair-proposal-user-guide-v0.md` and `run-replay-to-self-repair-proposal-v0.md`
     (the `- `review_bundle:<section_name>`` bullet in each).

(17) REGENERATE `.agent/f275_deletion_order.md`. Do NOT hand-edit it. Run the SHIPPED
     `measured_order()` from `tests/orchestration/test_cluster_deletion_order.py` against the
     live graph AFTER steps (1) to (16) are on disk, keep the file's comment header VERBATIM
     (every line from the top through the last line that starts with `#` or is blank), and
     write the rendered body under it, one component per line, members joined by `, `. The
     result must be ELEVEN components where the base has twelve, and the diff for this file
     must be a PURE DELETION — `+0/-1`. Insertions here would mean a component moved.

WHAT THIS ROUND MUST NOT TOUCH, measured rather than assumed:
  - `review_cmd.py` beyond step (2), and `tests/cli/test_review_cmd.py` at all — its four
    tests drive `review.list` and none names the bundle.
  - `packages/orchestration/reviewer.py` — it survives and keeps a PRODUCTION importer,
    `apps/cli/commands/dev.py` line 125, plus the four surviving handlers.
  - `scripts/remedy_smoke.sh`, `dev.py`, `ui_view_model.py`, `overnight_mission.py`,
    `tests/cli/test_job_commands.py`, `tests/test_cli_execution_loop_closure.py`,
    `simple-operator-quickstart-v0.md`, `core-product-spine-v0.md` — all name
    `remedy review run/list/accept/reject`, which SURVIVE.
  - `scripts/build_review_manifest.py` — it produces `review_bundle_integrity` from its own
    `_check_bundle_integrity` and imports nothing from the deleted module, so THE CLOSURE
    EVIDENCE PRODUCER SURVIVES. The five tests reading that key are deliberately NOT swept:
    `test_job_evidence.py::TestEvidenceHygiene::test_bundle_integrity_stays_packaging_layer`
    and the four in `tests/test_do_job_flow.py::TestReviewBundleIntegrity`.
  - `self_repair_proposal.py` — its three references sit in a CLUSTER module on the FIRST
    line of the regenerated order file, so RULE 2 defers them to that group's own commit.
  - `docs/roadmap/features/T2_F260.md` and `T2_F272.md` — the specification, unedited.

Constraints:
  1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it anyway and
     declare the disagreement in the handback. Never edit reviewer-authored text.
  2. Write nothing outside the 45-path change set. If a step seems to need another path,
     stop and declare it rather than widening.
  3. The worker writes NO `Done:` paragraph of its own. `Done: R-0841` is inside LEDGER9 and
     is reviewer-authored; that is the only resolution text this round lands.
  4. Commit order is fixed: C0a, C0b, C1, C2, C3, C4. C1 is the first substantive commit.
  5. C3 is ONE commit. A module group is never split across commits (operator RULE 1).
  6. Every destructive check runs ONLY in a disposable `git worktree` under `.remedy-wt/`.
     `/tmp` is denied in this environment. Remove and prune it before the handback.
  7. Run the full suite SERIALLY — no `-n auto` — in the PRIMARY checkout, which is the only
     tree holding `apps/ui/node_modules`.
  8. The `remedy` CLI is denied in this environment. No gate needs it; do not invoke it.

Done when — EIGHT gates, every one RUN, with real exit codes and real numbers:

  G1 TRANSPORT. sha256 of the committed `.agent/authored/f275-r9.md` equals sha256 of the
     committed `.agent/last_block.md` equals the digest stated in the delegation. ONE digest
     comparison over three artefacts, all of them this worker's own output; per §3 item 37
     state that it claims nothing about the emitted bytes.

  G2 THE PLAN. Committed `.agent/plan.md` is BYTE-IDENTICAL to PLAN9. Report byte count,
     sha256, line count against the AGENTS.md cap of 50, `^## Goal$` × 1, `^## Next Steps$` × 1.

  G3 THE RECORD. Read from the COMMITTED blobs at C1 (pre) and C2 (post), never the worktree.
     For `.agent/live_review.md` with LEDGER9 and `.agent/prose_slips.md` with SLIPS9:
     (a) byte growth is exactly 1 + the slice's byte count (one newline joins the append);
     (b) the pre-blob is a byte-exact PREFIX of the post-file and the slice a byte-exact
         SUFFIX of it;
     (c) an INDEPENDENT structural reader: count N from the slice yourself, then compare the
         file's LAST N blank-line-separated units against the slice's N paragraphs IN ORDER;
     (d) a negative control on the FIRST appended paragraph of each — flip one byte IN MEMORY
         ONLY and confirm BOTH readers (b) and (c) REJECT it; re-read the tracked files from
         disk afterwards and confirm they are unchanged;
     (e) `^Gate: ` +1, `^Gate: F275 R8 ` = 1, `^Done: R-0841 ` = 1, `^- R-0843 — ` = 1,
         `^- R-0844 — ` = 1;
     (f) THE OPEN SET BY DISTINCT ID: 68 before, 69 after (two registrations, one resolution).
         Report registrations and resolutions separately.

  G4 THE DELETION IS COMPLETE. At C3: `git ls-tree -r <C3> --name-only` finds NONE of the five
     files of step (1). Over the TRACKED tree, EXCLUDING `.agent/` and `.data/`, these strings
     are at ZERO: `build_review_bundle`, `export_review_bundle_json`, `summarize_review_bundle`,
     `ReviewBundleResult`, `packages.orchestration.review_bundle`, `_cmd_review_bundle`,
     `"review.bundle"`, `test_review_bundle_runtime`, `review-bundle-v1`,
     `review-bundle-structured-error-reporting`. Then the whole-word token `review_bundle`
     over that same scope must read EXACTLY FIVE lines, and PRINT ALL FIVE: two in
     `docs/roadmap/features/T2_F260.md` and `T2_F272.md` (the specification) and three in
     `packages/orchestration/self_repair_proposal.py` (a cluster module RULE 2 defers). Any
     sixth line is a FAIL.

  G5 RATCHETS, READERS AND THE RED-PROOF. In the primary checkout, all at C3:
     (a) `python3 -m pytest tests/orchestration/test_import_reachability.py
         tests/orchestration/test_cluster_deletion_map.py
         tests/orchestration/test_cluster_deletion_order.py -q` — exit 0, report the count.
     (b) `python3 -m pytest tests/docs/ -q` and the canary
         `python3 -m pytest tests/cli/test_golden_path.py -q` — exit 0, report both counts.
     (c) THROUGH THE SHIPPED READERS, not by grep: `len(apps.cli.command_catalog._BASE_CATALOG)`
         and `len(apps.cli.commands.collect_all_handlers())` are BOTH 335 at C3 against 336 at
         the base, with `review.bundle` ABSENT from both and `review.run`, `review.list`,
         `review.accept` and `review.reject` PRESENT in both. Print the four survivors.
     (d) `.agent/f275_deletion_order.md` holds ELEVEN components against twelve at the base,
         and `git show --numstat <C3> -- .agent/f275_deletion_order.md` reads `0  1`.
     (e) RED-PROOF, in a disposable worktree at C3 and NOWHERE ELSE, `__pycache__` purged and
         `python3 -B` before every run. Take the UNMUTATED control FIRST and report its exit
         code beside each mutation. Selection = the three-test command of (a). Each mutation is
         applied ALONE and reverted byte-identically, re-checked by sha256, and each FROM
         string counted 1 in its own named file first. Restore, one at a time:
           (i) `    "packages.orchestration.review_bundle",` to `CLUSTER_MODULES` in
               `tests/orchestration/test_cluster_deletion_map.py`; (ii) the line
           `packages.orchestration.review_bundle` as the FIRST body line of
           `.agent/f275_deletion_order.md`; (iii) that same line to
           `tests/orchestration/import_reachability_allowlist.txt`.
         EXPECTED: control exit 0, then (i) (ii) (iii) each exit 1, then the control exit 0
         again. Report the failure COUNT for each, then remove and prune the worktree and show
         `git worktree list` naming the primary checkout alone.

  G6 RUFF AND BASH. `python3 -m ruff check` over EVERY `.py` file this round edits (name them
     from `git diff --name-only`): `All checks passed!`. Then
     `python3 -m ruff check packages/ apps/cli/ tests/` reads 24 at C3, and read the SAME
     command at the base `aae6d313dbedc64c84703eae7a782e67439ccdec` WITHOUT writing to the
     primary checkout — use a disposable worktree, never overwrite-and-restore — and report
     that it is also 24. `bash -n scripts/remedy_test_runtime.sh` exits 0.

  G7 THE FULL SUITE. In the PRIMARY checkout, SERIALLY: `python3 -m pytest tests/ -q`,
     reporting the REAL exit code read from the process (do NOT pipe to `tail` and read `$?`
     of the pipe). Then the arithmetic, which must close exactly: `--collect-only` reads 19751
     at the base and 19613 at C3, a fall of 138; 138 = 104 + 34, where 104 is the collected
     count of the two deleted test files at the base and 34 the collected-id fall over the 16
     files of step (13); and the suite's own pass+skip total falls by that same 138. Report all
     four numbers. If any disagrees, do not adjust it — report it.

  G8 THE TREE. `.agent/STOP` does not exist (re-read from disk). `git status --porcelain` is
     EMPTY. `git worktree list` names the primary checkout ALONE. The branch is
     `feature/f275-one-world-completion-part-three`. `git diff --name-only
     aae6d313dbedc64c84703eae7a782e67439ccdec..<C3>` names EXACTLY the 44 paths of the change
     set other than `.agent/handoff.md`, none extra and none missing. Every commit in the range
     is single-parent, in the order C0a, C0b, C1, C2, C3, C4. Report per-commit INSERTIONS —
     the `+` column only, per AGENTS.md DECISION F104 D1 — for C0a through C3 against the cap
     of 500; C4's own numbers belong to the next round's ledger entry (§3 item 31).

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, carrying the state
  block, the per-commit changed-files table with `+/-` from `git diff --numstat`, ONE LINE PER
  GATE with its real numbers, the item-status table, the deviations, the line `SESSION 5 of
  feature F275 · round 9 · rounds so far 9`, and the one-sentence context self-assessment
  amend0905-throughput requires. NO length cap. Push after C4; create no pull request.
-------------------- (20 hyphens) END OF STEP -------------------- (20 hyphens)

BEGIN PLAN9 bytes=2616 sha256=8f034865f73fda9287f167b16e80871f06e38b07f3c39d16ced2e204cf63279f
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 9 books round 8's PASS, resolves R-0841, registers R-0843 and R-0844, and deletes the
FOURTH module group, `review_bundle` — the module, its ONE catalog entry `review.bundle`, the
one handler function inside `apps/cli/commands/review_cmd.py` that imports it, its two test
files, the two `docs/system/` pages whose subject it is, the string-keyed doctor probe no
import graph can see, and the surviving test call sites. The file `review_cmd.py`, the
`review` command group and its four other commands SURVIVE: they drive
`packages/orchestration/reviewer.py`, which is not on F260's Design list.

## Next Steps

1. The `dogfood_run` / `feature_planner` / `overnight_mission` / `progress_ledger` /
   `repair_loop_v2` / `self_repair_proposal` component, which this round's regeneration makes
   the order file's first line. Its six modules import each other, so DECISION F275 D2 makes
   the whole component one commit.
2. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842 and R-0844 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 68 by distinct id at this round's base `aae6d313`; the ledger commit this
  block fixes as C2 resolves R-0841 and registers R-0843 and R-0844, taking it to 69. Four are
  High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per
  DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only. `review_bundle` has NO line in
  `cluster_deletion_map.txt` and yet has a live importer: a STRING-keyed `importlib` probe in
  `apps/cli/commands/worker_facade_cmd.py`. An AST sweep sees none of it.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel tests
  race for a server port and the vitest node needs `apps/ui/node_modules`.
END PLAN9

BEGIN LEDGER9 bytes=7235 sha256=10c3aedcfe88e74046fa1e92c95c99ac64a113b85f0eaf84627252c6904d10a8
Gate: F275 R8 — the F275 round 8 entry. VERDICT PASS, booked by round 9 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier is the committed and pushed `.agent/handoff.md` at `aae6d313dbedc64c84703eae7a782e67439ccdec`. THE VERDICT WAS ISSUED BY THE REVIEWER OF SESSION 4, which re-ran every one of the eight gates itself against the COMMITTED blobs over the range `65409e647b04939746ff010a687c48621022b9e3`..`d9cae0b6c36c9f3dbb01b31caee22ee245fba768`; that session's own account of what it re-measured is the handback text this entry books, and this paragraph does not restate those readings as if session 5 had taken them. THE ROUND DELETED THE THIRD MODULE GROUP, `context_pack`, in one commit `d85f65e6` at 13 insertions against 955 deletions over 24 paths, with the full suite at 19728 passed and 23 skipped — down exactly the 32 tests that commit removes — and the regenerated `.agent/f275_deletion_order.md` falling from thirteen components to twelve as a PURE DELETION in the diff. WHAT SESSION 5 VERIFIED ITSELF BEFORE BOOKING THIS PASS, and the only readings in this paragraph taken by session 5: the two repairs R-0841 ordered are on disk at `aae6d313`, `tests/test_remedy_smoke_script.py` line 1339 now reading `# --- Step 64: Worker show (step 12v) ---` with the `explain (steps 12v-12w)` half gone, and `tests/storage/test_persistence.py` line 180 now reading `"""Token Economy v1 — the token policy."""` with the `context pack modes, worker recommend` half gone. Those two readings are what the `Done: R-0841` paragraph below rests on.

Done: R-0841 — RESOLVED. The two comments the round 7 deletion falsified are repaired, both by commit `d85f65e6` of round 8, and the reviewer of session 5 re-read both at `aae6d313` before writing this paragraph rather than accepting the worker's `Landed:` line. `tests/test_remedy_smoke_script.py` carries `# --- Step 64: Worker show (step 12v) -------------------------------------` where it carried `Worker show + explain (steps 12v-12w)`, and `tests/storage/test_persistence.py` carries `"""Token Economy v1 — the token policy."""` where it carried `"""Token Economy v1 — context pack modes, worker recommend."""`. THE WIDER COUNTER-MEASURE THE FIX CLAUSE ORDERED IS ALSO DISCHARGED, and that is the half worth recording: the clause required a deletion round to sweep the SECTION COMMENTS above the deleted units in EVERY file of its change set rather than only in the file the block happened to name, and the F275 round 9 block carries that sweep as a numbered step, which found and repaired a comment in the SURVIVOR `packages/orchestration/ui_server.py` naming `review_bundle` beside `do_run` and `proof_chain`, plus two test function names whose subjects survive the deletion their names advertise. Three occurrences in three rounds is what made this a class rather than an instance, and the sweep is what closes it.

- R-0843 — Low, THE `Groups` TABLE IN `docs/system/architecture.md` STILL ADVERTISES THE DELETED `context.pack` COMMAND AS THE `context` GROUP'S PURPOSE. Raised by the reviewer at the F275 round 8 gate, on the worker's own declared deviation 4. Measured at `d9cae0b6c36c9f3dbb01b31caee22ee245fba768`: the row reads `| context | 1 | Build token-budgeted context packs |`, and the only command left in that group is `context.inspect`, whose catalog description is `Inspect what a worker will see — paths, budget, policy gates.` The COUNT is now accidentally right — it was 1 against a real 2 before this round — and only the DESCRIPTION is wrong, which is why no count gate could catch it. It is an id rather than a `.agent/prose_slips.md` line because the wrong state is on disk under `docs/`. It is LOW because the whole table is an already-stale snapshot of a twelve-group CLI that no longer exists: the reviewer measured `worker | 1` and `memory | 4` against a live catalog of 335 commands at the same commit, so a reader is already told this section describes an early state. FIX CLAUSE, BINDING ON THE NEXT BLOCK THAT TOUCHES `docs/system/architecture.md`: repair the WHOLE table or give the section a `> **Status (…)**` banner naming it a historical snapshot — do not fix the one row, which is the instance-fix the checklist's staleness family exists to prevent. WIDER COUNTER-MEASURE, which is why this is not folded into R-0841: R-0841's clause sweeps SECTION COMMENTS ABOVE THE DELETED UNITS, and this row is neither a comment nor above a deleted unit — it is ordinary prose elsewhere in a file the change set already edits. Sweep EVERY file in the change set for text the deletion falsifies, not only the neighbourhood of the deleted lines.

- R-0844 — Medium, DELETING `review_bundle` REMOVES `remedy review bundle`, THE ONLY COMMAND THAT EXPORTS A SAFE PER-JOB REVIEW BUNDLE, AND REMOVES THE `review_bundle` ROW FROM `remedy worker doctor-core`; NO SURVIVING COMMAND CARRIES EITHER READING. Raised by the reviewer while authoring F275 round 9, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherits the idea. THE MEASUREMENT, taken at `aae6d313` by an APPLIED dry run of the whole deletion in a disposable worktree. `review.bundle` is one of 336 catalog entries and its handler `_cmd_review_bundle` is one of five in `apps/cli/commands/review_cmd.py`; it is the ONLY one of the five that imports the deleted module, and the catalog reader falls 336 to 335 with `review.bundle` absent and `review.run`, `review.list`, `review.accept` and `review.reject` all still PRESENT. Its behaviour was a zip under `.data/review_bundles/` plus a JSON export, both redacted, described by the two `docs/system/` pages this round deletes. SEPARATELY, `apps/cli/commands/worker_facade_cmd.py` probed the module by STRING through `importlib` and printed a `review_bundle` availability row in `remedy worker doctor-core`; that row is gone and the doctor's check list is one shorter. WHAT INHERITS THE IDEA, and why this is Medium rather than High: the operator's review window is `scripts/make_review_zip.sh` with `scripts/build_review_manifest.py`, which `docs/roadmap/STATUS_closure_protocol.md` already makes the mandatory closure evidence and which this deletion does NOT touch — the reviewer measured that `build_review_manifest.py` produces its `review_bundle_integrity` key from its own `_check_bundle_integrity` function and imports nothing from the deleted module, so the closure evidence producer survives intact and the five tests that read that key are deliberately NOT swept. WHAT IS NOT INHERITED: the per-job CLI export itself, and the doctor row. FIX CLAUSE, BINDING ON THE ROUND THAT DRAFTS DECISION F260 D3: name both readings in D3 among the ideas DELETED rather than inherited, beside R-0831's route-policy knobs, R-0840's run-keyed dogfood fields and R-0842's three cockpit readings, and state the review-zip pipeline as the inheritor of the safe-bundle idea itself. No stub, no shim and no copy of cluster code into a survivor may close this, per AGENTS.md Scope Control and RULE 3's own wording.
END LEDGER9

BEGIN SLIPS9 bytes=1615 sha256=d2443a066f5e2c85241cdbfa1ad5d85256f24c02ebb9cf10434d33b4911c7f90
2026-09-08 · F275 R8 · The round 8 block's step (3) ordered the `context.pack` catalog entry deleted "through its closing `    ),` and the blank line that follows it", and that blank line was the SEPARATOR before the `# ── change ──` group comment rather than padding inside the entry, so the surviving `context.inspect` entry now abuts that comment; the reviewer's own account of the shape then miscounted its precedent, writing that eleven other group boundaries in `apps/cli/command_catalog.py` already carried it when the measured figure is NINE — counted as the group comments whose immediately preceding line is a closing `    ),`, ten including the boundary round 8 itself created.

2026-09-08 · F275 R9 · The round 9 map that session 4 wrote into `.agent/handoff.md` prescribed deleting `apps/cli/commands/review_cmd.py` whole, the entire `review` catalog group with its `GroupDef`, the smoke script's section 12ap, three surviving command-string emitters and about eighteen further tests, on the reading that the handler file dies with the module; session 5 applied that map in a disposable worktree before authoring and measured it RED at fifteen failures, because only ONE of the five handlers in that file imports `review_bundle` and the other four drive `packages/orchestration/reviewer.py`, a module that survives and is not on F260's Design list — so the map would have deleted four working commands, and the correctly scoped deletion needs none of that surgery and runs green. Nothing reached disk: the map was corrected before delegation, which is why this is a slip and not an id.
END SLIPS9
