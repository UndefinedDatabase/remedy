── STEP T001/3 — F275 ROUND 11 — the SIXTH module group: the four-module `builder_routing` component ──

Goal:
Delete the second strongly connected COMPONENT of the prototype cluster — `builder_routing`,
`candidate_quality`, `local_candidate_generator` and `model_route_tournament` — whole, in ONE
commit, under DECISION F275 D2 and operator amendment amend0908-f275-finish RULE 1; book round
10's PASS and the four prose slips the handback carries; register R-0847, R-0848 and R-0849;
close F260's second carry-over as a finding NOTE rather than a rebuild; and release DECISION
F274 D4's hold on the builder-routing cockpit section by a dated DECISION before the commit
that cuts that section.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r11.md`
  C0b  mirror the same bytes to `.agent/last_block.md`
  C1   `.agent/plan.md` replaced WHOLE by the PLAN11 slice
  C2   append LEDGER11 to `.agent/live_review.md` and SLIPS11 to `.agent/prose_slips.md`
  C3   append DECISION11 to `.agent/decisions.md`
  C4   the deletion — all 49 paths, ONE commit
  C5   `.agent/handoff.md` rewritten whole

WHY THIS BLOCK DOES NOT CARRY FROM/TO PAIRS FOR THE DELETION. Operator amendment
amend0906-triage-throughput rules a deletion round verified by four measurements and nothing
else, and `docs/roadmap/features/T2_F275.md` rules that such a block "is at most sixty lines and
lists the paths". The change set below is therefore a PATH LIST WITH A SPEC PER PATH, measured by
the reviewer's own applied dry run, and the worker derives the bytes. Every figure in it was
produced by APPLYING this deletion in a disposable worktree at `cb89bbc3` and running the suite
to green; none is estimated. The reviewer's dry-run commit is `9e43bb40` in a worktree that has
since been removed, so it is named as the source of the numerals and is NOT a commit the worker
can read.

BLOCK SIZE, DECLARED BY THE REVIEWER SO THE WORKER DOES NOT HAVE TO. Measured on these final
bytes: 396 lines TOTAL and 277 of PROSE, against DECISION F085 D6's 490 and DECISION F085 D5's
400, and the LEDGER11 record slice is 9 lines against D6's budget of 140. The sixty-line
guidance `docs/roadmap/features/T2_F275.md` gives a DELETION-ROUND block is EXCEEDED and the
reason is stated rather than hidden: the change set alone is 49 paths, so a bare path list
reaches sixty before a single gate is written, and this round additionally books a verdict,
three registrations, a NOTE and a DECISION. The guidance bounds ceremony, and every line above
sixty here is either a path or a measurement a gate consumes. This is the reviewer's own text
and leaves nothing wrong on disk, so it is one dated `.agent/prose_slips.md` line and not an
id, per operator amendment amend0827-process-diet rule 2.

Change set — 49 paths. DELETED WHOLE, 22, each followed by its line count at `cb89bbc3`:
  packages/orchestration/builder_routing.py · 1085
  packages/orchestration/candidate_quality.py · 796
  packages/orchestration/local_candidate_generator.py · 778
  packages/orchestration/model_route_tournament.py · 729
  apps/cli/commands/builder_routing_cmd.py · 113
  apps/cli/commands/candidate_quality_cmd.py · 146
  apps/cli/commands/local_candidate_cmd.py · 87
  apps/cli/commands/tournament_cmd.py · 101
  tests/orchestration/test_builder_routing.py · 318
  tests/orchestration/test_candidate_quality.py · 285
  tests/orchestration/test_local_candidate_generator.py · 300
  tests/orchestration/test_model_route_tournament.py · 253
  tests/orchestration/test_model_route_tournament_integration.py · 43
  tests/cli/test_builder_routing_cli.py · 114
  tests/cli/test_candidate_quality_cli.py · 73
  tests/cli/test_local_candidate_cli.py · 115
  tests/cli/test_tournament_cli.py · 98
  docs/system/expensive-builder-routing-v0.md · 122
  docs/system/local-candidate-generator-v0.md · 106
  docs/system/candidate-quality-evaluation-v1.md · 97
  docs/system/model-route-tournament-harness-v0.md · 87
  docs/guides/model-route-tournament-user-guide-v0.md · 65

`tests/orchestration/test_model_route_tournament_integration.py` goes WHOLE and not surgically:
its only remaining test class is `TestRoutingIntegration`, and once that goes the file holds a
fixture and a `TestSafeSurfaces` class with a `_job` helper and NO test method at all. Round 10
had already emptied it of everything else.

EDITED, 27 — the spec per path, with the measured numstat as `+/-`:
  apps/cli/command_catalog.py · 0/205 · the 14 `CommandEntry(` blocks whose
      `command_id` is one of `builder-routing.decide`, `builder-routing.report`,
      `local-candidate.status`, `local-candidate.generate`, `candidate-quality.evaluate`,
      `candidate-quality.show`, `candidate-quality.scorecard`, `candidate-quality.report`,
      `candidate-quality.integrity`, `tournament.report`, `tournament.show`, `tournament.list`,
      `tournament.integrity` and `external-builder.evaluate`, plus the four `GroupDef` lines of
      `builder-routing`, `local-candidate`, `candidate-quality` and `tournament`.
      DO NOT touch any surviving entry's `related=(...)` tuple: `related` has NO reader anywhere
      in the repository (its only occurrence outside a literal is its own field declaration at
      `command_catalog.py:92`), and round 10 already left `related=(…, "dogfood.run-loop")` at
      line 1594 pointing at a command it deleted, with the suite green. Cleaning them is a
      separate concern and widening the change set for it is forbidden by constraint 3.
  apps/cli/commands/__init__.py · 1/5 · the four handler imports and the four
      names inside the `for mod in (…)` tuple.
  apps/cli/commands/external_builder_cmd.py · 0/26 · `_cmd_external_builder_evaluate` whole
      and its `"external-builder.evaluate":` row in `COMMAND_HANDLERS`. THE FILE SURVIVES: it
      holds eight handlers and exactly one imports `candidate_quality`; the other seven drive
      `external_builder_sandbox`, which is component line 2 of the order file and dies later.
  packages/orchestration/ui_server.py · 0/28 · `_build_builder_routing_section` whole
      and its `"builder_routing": _build_builder_routing_section(job),` row in the dashboard
      dict. DECISION11 releases the hold that protects this section and lands at C3, before C4.
  packages/orchestration/worker_registry.py · 4/2 · `_worker_next_action`'s
      `if spec.kind in (WorkerKind.LOCAL_CANDIDATE,):` branch and its
      `remedy builder-routing report` return, replaced by a comment saying that no surviving
      command reports a local candidate route, so the kind falls through to the function's own
      `remedy worker registry-list --json` default. This site is in NO inherited map; the
      reviewer found it by sweeping the spaced `remedy <group> <sub>` form. R-0847 registers it.
  pyproject.toml · 0/2 · the `packages.orchestration.builder_routing`
      and `packages.orchestration.local_candidate_generator` mypy module entries.
  docs/README.md · 0/9 · every row whose LINK TARGET is one of
      the five deleted pages — four quick-find rows and five index rows. KEY THE REMOVAL ON THE
      LINK TARGET, never on the slug: `expensive-builder-routing-v0` is a substring of the
      SURVIVING `archive/expensive-builder-routing-v0-plan.md`.
  docs/system/local-model-advisor-v0.md · 0/2 · see-also bullets linking a deleted page
  docs/system/orchestrator-brain-v0.md · 0/2 · see-also bullets linking a deleted page
  docs/system/repair-request-builder-v0.md · 0/2 · see-also bullets linking a deleted page
  docs/system/self-dogfood-execution-v0.md · 0/1 · see-also bullet linking a deleted page
  docs/system/development-artifact-boundary-v0.md · 0/2 · the `builder_routing.py` row and the
      `candidate_quality.py` row of its two tables
  docs/system/external-builder-sandbox-v0.md · 0/2 · the `remedy candidate-quality evaluate`
      line and its continuation inside the fenced flow block
  docs/system/external-builder-worker-contract-v0.md · 1/13 · section `## 5. Quality is judged
      later, from evidence` whole — its fenced `remedy external-builder evaluate` command and
      its paragraph, which links a deleted page — and `## 6.` renumbered to `## 5.`
  docs/system/provider-trust-verification-v1.md · 7/10 · the `## Next` section's three paragraphs
      rewritten: they link two deleted pages and name a third. The replacement states what
      survives (every external candidate still enters the Trust Gate and Verification pipeline)
      and records the absence where a reader would search for it, naming F110 as the owner of
      routing configuration from here.
  docs/system/worker-registry-route-policy-v0.md · 0/5 · the `### Builder Routing integration`
      section whole; its subject is a deleted module.
  .agent/f275_deletion_order.md · 2/3 · REGENERATED from `measured_order()` in
      `tests/orchestration/test_cluster_deletion_order.py`, never hand-edited, with the 26-line
      comment header carried byte for byte. Eleven components became ten at round 10 and become
      NINE here. IT IS NOT A PURE DELETION: removing the component also reorders two surviving
      single-module components, so the measured numstat is `2 3` and a gate demanding `0 1`
      would be unmeetable.
  tests/orchestration/cluster_deletion_map.txt · 0/1 · the one
      `packages.orchestration.builder_routing <- packages/orchestration/ui_server.py` edge
  tests/orchestration/import_reachability_allowlist.txt · 0/8 · four modules and four handlers
  tests/orchestration/test_cluster_deletion_map.py · 1/9 · four `CLUSTER_MODULES` lines, four
      handler-path lines, and the `_cluster_module_of` docstring example re-pointed from
      `builder_routing` to a SURVIVING cluster module.
  tests/orchestration/test_development_artifact_boundary.py · 0/1 · the `builder_routing.py`
      allowlist string
  tests/orchestration/test_external_builder_sandbox.py · 0/26 · `class TestQualityIntegration`
      WHOLE, with the banner comment above it. Its single member `test_external_evaluation` is
      the only thing in it, so removing the method alone leaves a class with no body and the
      file stops parsing.
  tests/orchestration/test_token_economy_integration.py · 0/43 · `class TestRoutingIntegration`
      whole. `TestSafeSurfaces.test_cockpit_section_readonly` covers `_build_token_economy_section`
      and SURVIVES; `TestPlaceholderHardening` survives untouched.
  tests/orchestration/test_worker_route_integration.py · 3/52 · the module-level
      `from packages.orchestration.builder_routing import (…)`, the whole
      `class TestRoutingPolicyConstraint`, the now-unused
      `from packages.orchestration.worker_registry import default_route_policy, save_route_policy`,
      the THREE orphan banner comments round 10's own deletions left behind plus the one this
      round orphans, and the module docstring re-scoped to what the file still tests. Leaving the
      unused import is not an option: it is two `F401`s and the repo-wide ruff count is a pinned
      ceiling. This is the R-0841 fix clause doing its work.
  tests/cli/test_cli_ux.py · 2/4 · `"tournament"`, `"local-candidate"` and
      `"candidate-quality"` out of `_INTERNAL_GROUPS`, and `"builder-routing"` out of the list in
      `TestNoInternalInDefault.test_no_internal_names`.
  tests/cli/test_external_builder_cli.py · 0/5 · the `# evaluate` leg of its submit test
      — the comment, the `run_grouped_cli([… "evaluate" …])` call and its two assertions — and
      the `sid = d["submission_id"]` binding, which nothing else in the test uses.
  tests/ui_server/test_dashboard_cockpit_truth.py · 0/12 · `test_builder_routing_section_present`
      whole. This is the test DECISION F274 D4's hold was protecting.

Constraints:
  1. Apply every BEGIN/END slice BYTE FOR BYTE. Do not edit, reflow, rewrap, correct or renumber
     one. If a slice looks wrong, apply it anyway and DECLARE it in the handback.
  2. The worker writes NO verdict, NO `Done:` paragraph, NO finding and NO registration of its
     own. `Done:` is reserved for reviewer-authored text (§4 item 4).
  3. The change set is exactly the 49 paths above plus the six `.agent/` paths of C0a, C0b, C1,
     C2 and C5. Touch nothing else. If a gate reveals a 50th path is needed, STOP and report it
     in the handback rather than widening.
  4. C2 and C3 both precede C4. DECISION11 releases the hold on the cockpit section, so it must
     be on disk before the commit that cuts that section.
  5. `.agent/plan.md` is advanced at C1, the first substantive commit, per §3 item 23.
  6. Read `.agent/STOP` from disk before C0a. If it exists, write the handback and stop.
  7. Every destructive check runs ONLY in a disposable `git worktree` under `.remedy-wt/`, never
     in the primary checkout, which satisfies `git status --porcelain` == empty at the handback.
     Never read a base revision by overwrite-and-restore; use `git show <sha>:<path>` or a
     disposable worktree (§3 item 29).
  8. C4 is ONE commit carrying all 49 paths. RULE 1 forbids splitting a module group, and
     DECISION F275 D2 makes this four-module cycle one group. Its measured shape is 21
     insertions against 6391 deletions, well under the 500-insertion cap.

Done when — EIGHT gates, every one RUN, every exit code read from the process object and never
through a pipe. Report ONE line per gate in the handback.

  G1 TRANSPORT. `.agent/authored/f275-r11.md` at C0a and `.agent/last_block.md` at C0b are each
     byte-identical to the delegation's source file, by `shutil.copyfile` and a re-read sha256.
     State the byte count and the digest, and that all three compare equal.
  G2 THE PLAN. `.agent/plan.md` at C1 is byte-identical to the PLAN11 slice; report its byte
     count, its sha256 and its line count against the AGENTS.md cap of 50.
  G3 THE RECORD, read from the COMMITTED blobs at C1 (pre) and C3 (post), never the worktree.
     (a) `.agent/live_review.md` and `.agent/prose_slips.md` at C2 and `.agent/decisions.md` at
     C3: for each, growth == 1 + len(slice), the pre-blob a byte-exact PREFIX and the slice a
     byte-exact SUFFIX of the post-file, and the joining byte re-read as `b'\n'`.
     (b) N COUNTED BY YOUR SCRIPT from each slice — never a number this block asserts — and the
     file's last N blank-line-separated units equal the slice's N paragraphs IN ORDER, with a
     per-unit sha256 printed for both sides.
     (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended paragraph of each
     of the three files and require BOTH readers to REJECT it; then re-read all three tracked
     files from disk and show them byte-equal to the committed post-blobs.
     (d) `^Gate: ` 32 → 33; `^Gate: F275 R10 `, `^Note: F275 R11 `, `^- R-0847 — `,
     `^- R-0848 — `, `^- R-0849 — ` and `^## DECISION F275 D5 ` exactly 1 each.
     (e) THE OPEN SET BY DISTINCT ID, by DECISION F085 D7: 75/4/71 open before, 78/4/74 after.
  G4 THE DELETION IS COMPLETE. `git ls-tree -r <C4> --name-only` prints False for all 22 deleted
     paths. Then a whole-word sweep for `builder_routing`, `candidate_quality`,
     `local_candidate_generator` and `model_route_tournament` over every tracked file EXCLUDING
     `.agent/` and `.data/`, printing EVERY remaining line IN FULL and never truncating. Every
     remaining line must be a must-not-touch item under `docs/roadmap/features/` or
     `docs/archive/`. The reviewer measured FOUR such lines in its applied dry run, all in
     `docs/roadmap/features/` — `T2_F260.md` at lines 340, 341 and 365 and `T2_F272.md` at
     line 744. Report the count YOU measure; a remaining line in any other directory is a
     real miss and ends the round. Zero-gated symbols, each counted AFTER deleting
     backtick-quoted spans from the line (§3 item 20's R-0586 clause, and the R-0584 class that
     cost round 10 a declared deviation): `select_builder_routing_decision`,
     `evaluate_candidate_quality`, `_build_builder_routing_section` and `BuilderRoutingPolicy`
     must each be 0.
  G5 THE FOUR MEASUREMENTS OF A DELETION ROUND, at C4.
     (a) RATCHETS: `python3 -B -m pytest tests/orchestration/test_import_reachability.py
         tests/orchestration/test_cluster_deletion_map.py
         tests/orchestration/test_cluster_deletion_order.py tests/docs/
         tests/cli/test_advertised_commands.py -q` → exit 0. The reviewer measured 317 passed.
     (b) THE SHIPPED READERS, through `apps.cli.command_catalog` and `apps.cli.commands`, never
         by grep: `len(_BASE_CATALOG)` 296 → 282, `len(collect_all_handlers())` 296 → 282,
         `len(GROUPS)` 56 → 52, duplicate command ids 0. All 14 deleted ids ABSENT from both
         readers and all four deleted groups absent from `GROUPS`, printed one per line; and
         `external-builder.submit`, `external-builder.integrity`, `route-policy.show`,
         `worker.registry-list` and `token.estimate` PRESENT in both.
     (c) THE ORDER FILE: `.agent/f275_deletion_order.md` holds NINE components against ten at the
         base; its 26-line comment header is unchanged; the body equals
         `", ".join(component)` over `measured_order()`, and you regenerate it rather than
         editing it.
     (d) THE CANARY: `python3 -B -m pytest tests/cli/test_golden_path.py -q` → exit 0.
  G6 RUFF AND BASH. `python3 -m ruff check` over exactly the `.py` files that
     `git diff --name-only cb89bbc3..<C4>` names and that still exist at C4 → `All checks
     passed!`, exit 0. Then repo-wide `python3 -m ruff check .` at C4 AND at the base `cb89bbc3`
     read in a disposable worktree: both must read `Found 26 errors.`, the ceiling
     `tests/orchestration/test_ci_budgets.py` holds. This round adds none, and the reviewer's dry
     run confirms that only after the unused import in `test_worker_route_integration.py` is
     removed — leaving it reads 28. `bash -n scripts/remedy_test_fast.sh` → exit 0.
  G7 THE FULL SUITE, `python3 -B -m pytest tests/ -q` SERIALLY — no `-n auto` — in the PRIMARY
     CHECKOUT, exit code from the process object. The reviewer measured, in a disposable
     worktree at this change set: 19042 passed, 29 skipped, 2 failed, both proven artefacts of
     the worktree rather than defects — `test_vitest_passes` fails identically at the BASE in a
     fresh worktree because `apps/ui/node_modules` is gitignored, and
     `test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`
     failed only while the change was UNCOMMITTED and PASSED once committed. In the primary
     checkout, where `node_modules` exists and your change IS committed, the suite must be GREEN
     at exit 0; a single failure is a red gate and ends the round under G8 of the protocol.
     CLOSE THE ARITHMETIC BY THE ID SET, not by a file-level count: `--collect-only tests/` is
     19232 at the base and 19073 at C4 in the reviewer's measurement, a fall of 159 with 0 ids
     gained. Take the base-side id set in a disposable worktree at `cb89bbc3`. Report the fall
     you measure, attributed, and if it differs from 159 say so rather than restating this
     number — `tests/test_grouped_cli.py` parametrises over the catalog and contributes ids no
     file-level reading of the deleted list predicts.
  G8 THE TREE. `.agent/STOP` re-read from disk: absent. `git status --porcelain`: empty.
     `git worktree list`: the primary checkout ALONE. Branch:
     `feature/f275-one-world-completion-part-three`. `git diff --name-only <C3>..<C4>` names
     EXACTLY the 49 paths of the change set — report it as a set comparison, nothing extra and
     nothing missing. Every commit C0a through C4 single-parent, with its insertion count under
     500. C5's own numbers belong to the next round's ledger entry (§3 items 14 and 31) and are
     not claimed here.

Handback: rewrite `.agent/handoff.md` WHOLE — the state block with `SESSION 7 of feature F275 ·
round 11 · rounds so far 11`, the one-sentence context self-assessment amend0905-throughput
requires, the per-commit changed-files table, one line per gate with its real exit code, the
deviations, the item-status table over the bundle above, the open-findings count, and the next
expected action. It has NO length cap (amend0827 rule 3). Then push once.

BEGIN-PLAN11 — the whole new text of `.agent/plan.md`, replacing it entirely
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 11 books round 10's PASS and four prose slips, registers R-0847, R-0848 and R-0849,
closes F260's SECOND carry-over as a NOTE on R-0831 — the route-policy audit re-measured, a
finding update and never a rebuild — releases DECISION F274 D4's hold on the builder-routing
cockpit section as DECISION F275 D5, and deletes the SIXTH module group and the second that is
a strongly connected COMPONENT: `builder_routing`, `candidate_quality`,
`local_candidate_generator` and `model_route_tournament`, whole, in ONE commit under DECISION
F275 D2. With them go four handler files, 14 catalog entries, the `builder-routing`,
`candidate-quality`, `local-candidate` and `tournament` groups WHOLE, nine test files, five doc
pages and nine index rows. `apps/cli/commands/external_builder_cmd.py` SURVIVES and loses one
of its eight handlers; `packages/orchestration/worker_registry.py` SURVIVES and loses the
next-action it gave a local-candidate worker. Both losses are registered.

## Next Steps

1. The `execution_approval_policy` component, which this round's regeneration makes the order
   file's first line. It is a SINGLE module, so it is an ordinary group commit.
2. The remaining components in the recorded order — after this round every one is a single
   module except the `provider_trust` / `provider_trust_verification` pair, which is the last
   cycle in the cluster.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844, R-0845, R-0846, R-0848 and R-0849 named among the ideas deleted
   rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 71 by distinct id at this round's base `cb89bbc3`; the ledger commit this
  block fixes as C2 registers three, taking it to 74. Four are High — R-0803, R-0804, R-0806
  and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 is a GATE defect, not only a code defect: `tests/cli/test_advertised_commands.py`
  cannot see an advertisement whose group has been deleted, so this round's four whole-group
  deletions widen a blind spot the same round registers. No later deletion round may rely on
  that guard to catch its own dead advertisements.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`, absent from any worktree.
END-PLAN11

BEGIN-LEDGER11 — appended to `.agent/live_review.md` after one blank-line separator
Gate: F275 R10 — the F275 round 10 entry. VERDICT PASS, booked by round 11 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, and carried here from the pushed `.agent/handoff.md` at `cb89bbc3`, which that rule makes a durable carrier. EVERY ONE OF THE EIGHT GATES WAS RE-RUN BY THE REVIEWER ITSELF against the committed blobs; the worker's report was evidence for nothing. Range `982d016b`..`57058636`, six commits C0a `d6c7694a`, C0b `bf9ffe68`, C1 `ccf684bd`, C2 `eac1082e`, C3 `e9944c64` and C4 `57058636`, each parent read from `git rev-list --parents`, per-commit insertions 444, 417, 28, 12, 31 and 339, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK, because the block travelled as a FILE the worker copied rather than as text it retyped: the reviewer's own scratchpad original and the committed `.agent/authored/f275-r10.md` and `.agent/last_block.md` are all 41781 bytes at `cd016eb03ec8698d0b61eee5bf1a5fb1e42d78750eef66c41ff150e605d2ca10` and compare byte-equal, so this round's chain does reach the emitted bytes — which §3 item 37 rules the digest-only form cannot. G2: `.agent/plan.md` byte-identical to PLAN10 at 2948 bytes, 49 lines against the cap of 50. G3: `.agent/live_review.md` 559516 to 569448, growth 9932 = 1 + 9931; `.agent/prose_slips.md` 175541 to 177821, growth 2280 = 1 + 2279; both edges byte-exact with the joining byte read back as a newline; N counted from each slice by the reviewer's own reader as 3 and 3, ordered equality holding over the WHOLE appended region with a per-unit sha256 printed for all six units; and BOTH negative controls, flipped in memory inside the FIRST appended paragraph per §3 item 36, REJECTED by both readers, with the tracked files re-read from disk afterwards and byte-equal to the committed post-blobs. `^Gate: ` 31 to 32, and `^Gate: F275 R9 `, `^- R-0845 — ` and `^- R-0846 — ` exactly 1 each, with THE OPEN SET 69 TO 71 BY DISTINCT ID against registrations 73 to 75 and resolutions 4 to 4. G4: all 27 whole-file removals absent from `git ls-tree` at C3 over 4606 tracked files, and the whole-word sweep for the six module names over the 1726 tracked files outside `.agent/` and `.data/` printed IN FULL — 15 module-name hits on 12 DISTINCT lines, every one a must-not-touch item, eleven in `docs/roadmap/features/` and one at `docs/system/vocabulary.md` line 245. G5: the four ratchets 60 passed at exit 0, `tests/docs/` 303 passed, the canary 42 passed; through the SHIPPED readers `_BASE_CATALOG` and `collect_all_handlers()` both fell 334 to 296 and `GROUPS` 59 to 56, with all 38 deleted ids ABSENT from both readers, all ten named survivors PRESENT, and zero duplicate ids; the regenerated order file held TEN components against eleven at a `0 1` numstat with its 26-line header intact. THE RED-PROOF WAS RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE at `e9944c64`: control exit 0 at 60 passed, three mutations exit 1 at 2, 1 and 1 failures, control exit 0 again, each FROM string counted unique in its named file first and each file reverted byte-identically by sha256. G6: ruff `All checks passed!` over the 18 edited Python files still existing at C3, and repo-wide `Found 26 errors.` at BOTH the base — read in a disposable worktree, never by writing to the primary checkout — and the tip; `bash -n` exit 0. G7: THE FULL SUITE RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT at exit 0, 19209 passed and 23 skipped, and the arithmetic closes exactly: `--collect-only` 19613 at the base and 19232 at C3, a fall of 381 = 325 for the eleven deleted test files plus 32 over the ten swept files plus 24 in `tests/test_grouped_cli.py`, with ZERO ids gained, and 19209 + 23 = 19232. G8: `.agent/STOP` absent, porcelain empty, one worktree, branch correct, and `eac1082e..e9944c64` naming 55 paths in an EXACT SET MATCH. WHAT THE ROUND ACHIEVED: the fifth module group and the first that is a strongly connected COMPONENT — `dogfood_run`, `feature_planner`, `overnight_mission`, `progress_ledger`, `repair_loop_v2` and `self_repair_proposal`, 7952 module lines — in ONE commit at 31 insertions against 14365 deletions over 55 paths, taking five handler files, 38 catalog entries, three whole command groups, eleven test files and five doc pages with them. SIX DEVIATIONS WERE DECLARED AND ALL SIX ARE SUSTAINED; four are the reviewer's own block text and none earns an id, per amend0827 rule 2, because none reached this record and none left anything wrong on disk. They are the four `.agent/prose_slips.md` lines this same commit books. THE MOST INSTRUCTIVE IS DEVIATION 3, THE R-0584 CLASS: G4 gated the bare symbol `build_mission_morning_report` to ZERO and it read 1, at `tests/cli/test_mission_cmd.py` line 1469, where the line is an ABSENCE GUARD that must quote the symbol in order to forbid it — so the gate as worded was unmeetable by any correct round, the guard is right, and the worker was right to declare rather than delete it. A zero-gate over a bare symbol must strip quoted spans first, exactly as §3 item 20's R-0586 clause already requires of the record scan, and the round 11 block's G4 is the first to order it. NO FINDING IS RESOLVED BY THIS GATE.

Note: F275 R11 — F260's SECOND CARRY-OVER IS CLOSED AS A FINDING UPDATE ON R-0831 AND NOTHING IS REBUILT, which is what `docs/roadmap/features/T2_F275.md` T001 words as "a finding update, not a rebuild". THE RULE. F260's Design section, "Two carry-overs before deletion", item 2, orders every user-settable route-policy knob checked against F110's config keys and rules the outcome in advance: existing knob → delete; missing knob → register as a finding, never rebuild. R-0831 is that registration and it stays OPEN, because what resolves it is DECISION F260 D3 naming route policy among the ideas deleted rather than inherited. THE RE-MEASUREMENT, taken by the reviewer at `cb89bbc3` rather than trusted from R-0831's own text, because R-0831 was measured at `4ba5e0f6` and many rounds have landed since. `BuilderRoutingPolicy` in `packages/orchestration/builder_routing.py` declares SIXTEEN knobs, and the candidate configuration surfaces `packages/orchestration/role_config.py` (16 keys), `packages/orchestration/model_routing.py` (77) and `packages/orchestration/config.py` (30) contain an equivalent for NONE of them. Four knobs produce a NEAR-NAME match and all four were checked individually and rejected as substring artifacts: `max_builder_attempts_per_failure`, `max_builder_attempts_per_self_item` and `max_external_builder_attempts_per_day` match only the token `builder`, which is a ROLE NAME in `role_config.py` and a role-to-task-class key at `model_routing.py:1261`; and `max_estimated_cost` matches only `cost` at `model_routing.py:796`, which is a `float` FIELD TYPE in a schema rather than a ceiling. So the audit REPRODUCES R-0831 exactly at a much later commit and WIDENS it from the eight instances R-0831 counted to all sixteen knobs. WHY THIS IS A NOTE AND NOT A NEW ID, per §3 item 30: the defect is R-0831's, the open set was searched for it before this paragraph was written, and a second id would be a second thing to resolve for one defect. WHY IT IS NOT A `Done:` EITHER: the carry-over OBLIGATION is discharged — the audit was to be done before the first `git rm` and it is done — while the FINDING it produced is resolved only by DECISION F260 D3. The knobs die with their module in this round's C4, and nothing anywhere gains a stub, a shim, an alias or a compatibility reader; AGENTS.md Scope Control forbids all four by name.

- R-0847 — Medium, THE ADVERTISEMENT GUARD CANNOT SEE AN ADVERTISEMENT WHOSE COMMAND GROUP HAS BEEN DELETED, SO EVERY WHOLE-GROUP DELETION WIDENS A BLIND SPOT, AND ONE DEAD `remedy feature plan` ADVERTISEMENT IS ALREADY LIVE IN PRODUCTION CODE BECAUSE OF IT. Raised by the reviewer while authoring F275 round 11, by sweeping the spaced `remedy <group> <sub>` form by hand rather than trusting the guard. THE GATE. `tests/cli/test_advertised_commands.py` exists, in its own docstring's words, so that "any `remedy <group> <sub>` string in tracked production code whose pair the catalog does not carry fails the sweep here rather than in an operator's terminal". Its scanner `scan_advertised_commands` skips every match whose group is not in `GROUPS` — `if group not in GROUPS: continue`. THE MEASUREMENT, taken at `cb89bbc3` by importing the shipped reader and the guard's own function: `feature`, `dogfood`, `progress` and `self-repair` are all ABSENT from `GROUPS`, because F275 rounds 9 and 10 deleted those groups whole; `scan_advertised_commands` returns the EMPTY LIST for the line `return "remedy feature plan --agent --json"`; and `collect_command_advertisements()` reads 488 advertisements seen and ZERO unresolved. Yet `packages/orchestration/worker_registry.py` line 710 IS that line — the next action `_worker_next_action` hands an operator for a PLACEHOLDER worker — and `remedy feature plan` has not existed since round 10 deleted `feature_planner.py` and the `feature` group; the shipped catalog carries no id beginning `feature` at all. So a user following the advertised next action gets nothing, and the guard whose whole purpose is that class reports a clean sweep. THIS IS THE DEFECT CLASS THE GUARD WAS BUILT FOR, ARRIVING THROUGH ITS OWN FILTER: the group check is there to stop ordinary prose matching, and it happens to be exactly false for the one case a deletion feature produces on every round. THIS ROUND MAKES IT WORSE BEFORE IT MAKES IT BETTER, and that is stated rather than hidden: C4 deletes `builder-routing`, `candidate-quality`, `local-candidate` and `tournament` WHOLE, so from C4 onward no advertisement of any of their commands is visible to the guard either. The reviewer therefore swept all five corpora by hand at `cb89bbc3` and this round removes every hit it found — one in production code, one in `docs/system/external-builder-sandbox-v0.md` and four in the two `model-route-tournament` pages it deletes whole. WHY MEDIUM: nothing false is claimed about what Remedy can do, and the loss is one broken next-action string plus a guard that under-reports; it is not Low because the guard's blindness is unbounded going forward and this feature has six more group deletions to run. WHAT WOULD RESOLVE IT, and it is not this round's work — amend0906-triage-throughput scopes a deletion round to deleted files, deleted catalog entries, deleted cockpit sections and the edits those force, and a change to the scanner's logic is none of those. THE FIX CLAUSE, binding on the first round that may edit `tests/cli/test_advertised_commands.py`: the scanner keeps a set of DELETED group names beside `GROUPS`, or resolves the pair against the catalog without the group pre-filter and narrows false positives by the existing command-tail rule instead; and the same round deletes the `remedy feature plan --agent --json` return at `worker_registry.py` line 710 together with the `via the feature planner` clause in `_worker_next_action`'s docstring, both of which name a command and a module round 10 deleted. Until that lands, no deletion round may cite a green `test_advertised_commands.py` as evidence that its own dead advertisements are gone; it must sweep by hand, as this round did.

- R-0848 — Medium, DELETING THE FOUR-MODULE COMPONENT REMOVES 13 COMMANDS AND FOUR WHOLE COMMAND GROUPS, AND NO SURVIVING COMMAND CARRIES ANY OF IT. Raised by the reviewer while authoring F275 round 11, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherits the idea. THE MEASUREMENT, taken at `cb89bbc3` by an APPLIED dry run of the whole deletion in a disposable worktree, through the SHIPPED readers rather than by grep: `len(apps.cli.command_catalog._BASE_CATALOG)` and `len(apps.cli.commands.collect_all_handlers())` both fall 296 to 282, and `len(GROUPS)` falls 56 to 52. THE FOUR GROUPS DIE WHOLE, which is what distinguishes this round from round 10, where `overnight` and `repair` survived partially: `builder-routing` loses `decide` and `report`, `local-candidate` loses `status` and `generate`, `candidate-quality` loses `evaluate`, `show`, `scorecard`, `report` and `integrity`, and `tournament` loses `report`, `show`, `list` and `integrity` — 13 ids, four `GroupDef`s, and no partial group left behind for `tests/test_command_catalog.py::TestCatalogIntegrity::test_every_group_has_at_least_one_command` to catch. WHAT A USER LOSES, named rather than counted: the local-first routing decision that chose between a deterministic fix, a local model candidate and an expensive external builder, with its policy knobs and its loop guard; the automated local candidate generator and its status view; the evidence-based candidate scorecard, which was the only surface that scored a generated patch against verification evidence; and the model/route tournament, the only surface that compared two routes on recorded outcomes. WHICH FEATURES INHERIT WHICH IDEA, as RULE 3 requires and without rebuilding anything: routing and its configuration go to F110, which owns model routing and whose config keys R-0831 has already audited knob by knob against these exact policies; the candidate scorecard and the tournament comparison go to F082, which owns the benchmark; and the local candidate generator has NO inheritor by design, because F260's Design deletes the prototype rather than carrying it. THE FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that paragraph names all 13 ids and all four groups among the ideas DELETED rather than inherited, states for each of the three families above which feature took it, and names this id. A stub, a shim, an alias or a compatibility reader is forbidden by AGENTS.md Scope Control by name, and this finding is not resolved by providing one.

- R-0849 — Medium, `remedy external-builder evaluate` IS DELETED WHILE ITS SEVEN SIBLING COMMANDS SURVIVE, SO THE EXTERNAL BUILDER INGRESS KEEPS EVERY STEP EXCEPT THE ONE THAT JUDGES WHAT CAME BACK. Raised by the reviewer while authoring F275 round 11, under the same operator RULE 3 as R-0848 and registered separately because the defect, the file and the fix are different: R-0848 is about four groups dying whole, and this one is about a SURVIVING group losing exactly one member. THE MEASUREMENT, taken at `cb89bbc3`. `apps/cli/commands/external_builder_cmd.py` holds EIGHT handlers; exactly one, `_cmd_external_builder_evaluate`, imports `packages.orchestration.candidate_quality`, and the other seven drive `packages.orchestration.external_builder_sandbox`, which is component line 2 of `.agent/f275_deletion_order.md` and dies in a LATER round. So the FILE survives this round and loses one handler, one `COMMAND_HANDLERS` row and one catalog entry, `external-builder.evaluate`; deleting the file whole would take seven working commands with it. WHAT IS ACTUALLY LOST. The external-builder pipeline still runs `package-create`, `submit`, `package-show`, `package-list`, `submission-show`, `submission-list` and `integrity`, so a candidate can still be packaged, relayed, quarantined, trust-checked, verified and materialised into a human-approvable intent — but nothing scores it. `evaluate` was the only command that turned an external submission into an evidence-based outcome, and `docs/system/external-builder-worker-contract-v0.md` carried a whole section, `## 5. Quality is judged later, from evidence`, describing precisely that step; this round deletes that section and renumbers the one after it, so the contract page no longer promises a judgement no command can deliver. THE SAFETY PROPERTY IS UNCHANGED AND THAT IS WHY THIS IS MEDIUM RATHER THAN HIGH: scoring never gated anything. Trust, verification and human approval are what stand between a submission and an applied patch, and all three survive untouched; a submission that used to score badly was still refused by the same gates that refuse it now. WHICH FEATURE INHERITS THE IDEA: F082, which owns the benchmark, takes evidence-based scoring of a candidate, the same inheritor R-0848 names for the local scorecard, because they are one idea applied to two sources. THE FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that paragraph names `external-builder.evaluate` among the deleted ideas and F082 as its inheritor, and records that the external ingress deliberately ships without a scoring step until F082 provides one — Remedy deliberately does not judge an external candidate's quality today, and the contract page says so where a reader would search for it.
END-LEDGER11

BEGIN-SLIPS11 — appended to `.agent/prose_slips.md` after one blank-line separator
2026-09-09 · F275 R11 · The round 10 block's step (8) ordered the string `"progress"` removed from `_INTERNAL_GROUPS` in `tests/cli/test_cli_ux.py`, and the reviewer confirmed against the blob at `982d016b` that the string was never there — an order with no target, which the worker declared rather than inventing a target for, and the block's own `+3/-3` prediction was reached exactly without it.

2026-09-09 · F275 R11 · The round 10 block's G4 predicted 28 remaining sweep lines against a measured 12 distinct; the figure was taken from an intermediate state of the reviewer's dry run, before that same dry run's docs pass was applied, so it described a tree the round never shipped. The gate's real condition — that every remaining line is a must-not-touch item — held on all twelve.

2026-09-09 · F275 R11 · The round 10 block's G4 gated the bare symbol `build_mission_morning_report` to ZERO and it reads 1: `tests/cli/test_mission_cmd.py` line 1469 is an ABSENCE GUARD that must quote the symbol in order to forbid it, so the gate was unmeetable by any correct round. A zero-gate over a bare symbol must delete backtick-quoted spans first, which is what §3 item 20's R-0586 clause already requires of the record scan and what that gate did not do; the round 11 block's G4 orders it.

2026-09-09 · F275 R11 · The round 10 block's G8 ordered a 55-path SET MATCH over `982d016b..<C3>`, a range that also spans C0a through C2 and therefore names 60; the reviewer re-measured 60 over that range and exactly 55 over `eac1082e..e9944c64`, with the set match holding on the second. The §3 item 16 / R-0585 shape — a count resolved against the wrong list — inside a gate the same block wrote.

2026-09-09 · F275 R11 · The round 11 map session 6 handed forward named TWO dying doc pages and the reviewer's own applied dry run at `cb89bbc3` measured FIVE, because the map swept the module NAMES through page CONTENT while two of the pages carry the dying subject only in their FILENAME and in the spaced `remedy <group> <sub>` commands they advertise. A content sweep for a deletion must be paired with a filename sweep and an advertisement sweep, and the same omission cost round 10 the identical slip.

2026-09-09 · F275 R11 · The same map stated 37 paths, 18 deleted whole and 19 edited, and the applied dry run measured 49 — 22 deleted whole and 27 edited. It missed `packages/orchestration/worker_registry.py`, a surviving production module advertising a dying command; it called `tests/orchestration/test_model_route_tournament_integration.py` an EDITED file when removing its last test class leaves it with no test at all; and it predicted four `docs/README.md` rows where the five deleted pages own nine. Nothing was wrong on disk, because the map was a plan and was never applied to the repository.

2026-09-09 · F275 R11 · The round 11 block exceeds the sixty-line guidance `docs/roadmap/features/T2_F275.md` gives a deletion-round block, and declared its own measured size rather than leaving the worker to discover the contradiction. The change set is 49 paths, so a bare path list passes sixty before a gate is written, and the round also books a verdict, three registrations, a NOTE and a DECISION. The round 10 block ran to 444 lines under the same guidance and declared nothing, which is why this line exists.
END-SLIPS11

BEGIN-DECISION11 — appended to `.agent/decisions.md` after one blank-line separator
## DECISION F275 D5 — DECISION F274 D4's hold on the builder-routing cockpit section is RELEASED, and the section dies with its subject module (2026-09-09)

Ruled by the reviewer while authoring F275 round 11, under docs/agents/planner_reviewer_prompt.md
§4 item 7, which routes a ruling to a loud, persisted, reversible decision rather than to a
question the operator is never asked. Reverse it by deleting this section, which restores D4's
hold and makes `_build_builder_routing_section` undeletable until the carry-over is discharged by
some other route.

WHAT WAS HELD, AND WHY. DECISION F274 D4 deleted six cockpit sections and explicitly HELD two —
`_build_builder_routing_section` and `_build_overnight_section` — on the ground that their modules
still owed a carry-over that F260's Design orders BEFORE the deletion. For the builder-routing
section that carry-over is the second of F260's two: every user-settable route-policy knob checked
against F110's config keys, with F260's Design ruling the outcome in advance — existing knob →
delete, missing knob → register as a finding, never rebuild.

WHY THE HOLD IS RELEASED NOW. The carry-over is DISCHARGED. R-0831 registered the audit at
`4ba5e0f6`, and the reviewer RE-RAN it at `cb89bbc3` rather than trusting the finding, because
many rounds had landed in between: `BuilderRoutingPolicy` declares sixteen knobs and the candidate
configuration surfaces `role_config.py`, `model_routing.py` and `config.py` carry an equivalent for
none of them, with the four near-name matches individually checked and rejected as substring
artifacts. The re-measurement is recorded as a `Note:` on R-0831 in `.agent/live_review.md` in the
same round as this decision. F260's rule therefore lands on the "missing knob" branch for all
sixteen, the outcome is a finding rather than a rebuild, and the finding exists. Nothing further is
owed before the section may go.

CHOSEN: the hold is released and `_build_builder_routing_section` is deleted in the SAME commit as
`packages/orchestration/builder_routing.py`, together with its dashboard-dict row and
`tests/ui_server/test_dashboard_cockpit_truth.py::TestDashboardShape::test_builder_routing_section_present`,
which is the test that goes red if the section is cut. `_build_overnight_section` is NOT touched by
this decision: D4 held two sections, this releases exactly one, and the overnight carry-over stands
on its own record.

ALTERNATIVES CONSIDERED AND REJECTED. (a) Keep the section and delete only the module, letting the
section's `try/except ImportError` swallow the missing import and report `source: "unavailable"` —
rejected because a cockpit panel that structurally cannot ever carry data is a false live indicator,
which docs/agents/planner_reviewer_prompt.md §4 item 5 makes a block condition, and because
AGENTS.md Scope Control forbids leaving a replaced mechanism alive beside nothing. (b) Delete the
section in a later round, after the module — rejected because operator RULE 1 makes the module
group ATOMIC in one commit and names the `ui_server.py` section as part of the group, so splitting
it is the half-deleted state RULE 1 exists to forbid. (c) Carry the knobs into F110's configuration
first — rejected because F260's Design rules "never rebuild" for exactly this case, and F110 owns
routing configuration on its own schedule rather than on this deletion's.

CONSEQUENCE, stated plainly. The cockpit loses its routing panel and no surviving section replaces
it; a reader of the dashboard has no routing view until F110 provides one. That loss is registered
as R-0848 rather than mitigated, and DECISION F260 D3 will name it among the ideas deleted rather
than inherited. Nothing on disk becomes inconsistent under the reversal above, because the section
and its module are recoverable from git and no later commit depends on their absence.
END-DECISION11
