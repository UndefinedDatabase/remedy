── STEP T001/3 — F275 ROUND 12 — the SEVENTH module group: `execution_approval_policy` ──

Goal:
Delete `packages/orchestration/execution_approval_policy.py` and everything that exists only
for it, in ONE commit under operator amendment amend0908-f275-finish RULE 1; book round 11's
PASS and two prose slips; register R-0850 and R-0851; and record, as a dated DECISION before
the deletion commit, the reading under which this module may be deleted at all — F275's "Do not
touch" protects THE APPROVAL GATE, and this module is not it.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r12.md`
  C0b  mirror the same bytes to `.agent/last_block.md`
  C1   `.agent/plan.md` replaced WHOLE by the PLAN12 slice
  C2   append LEDGER12 to `.agent/live_review.md` and SLIPS12 to `.agent/prose_slips.md`
  C3   append DECISION12 to `.agent/decisions.md`
  C4   the deletion — all 16 paths, ONE commit
  C5   `.agent/handoff.md` rewritten whole

THE NUMERALS BELOW ARE MEASURED, NOT ESTIMATED. The reviewer applied this whole deletion in a
disposable worktree at the base `21c90fe5` and ran the suite to a FULLY GREEN result — 18935
passed, 23 skipped, ZERO failed — before authoring a line of this block. That worktree and its
commit `86511630` have since been removed; they are named as the source of the figures and are
not commits you can read. Where your own measurement disagrees with a figure here, REPORT YOURS
and declare the difference; do not bend an edit to reach a number.

BLOCK SIZE, DECLARED BY THE REVIEWER. Measured on these final bytes: 320 lines TOTAL and 208 of
PROSE, against DECISION F085 D6's 490 and DECISION F085 D5's 400; the LEDGER12 record slice is 5
lines against D6's budget of 140. This exceeds the sixty-line guidance
`docs/roadmap/features/T2_F275.md` gives a deletion-round block, for the reason round 11's block
also recorded: the round books a verdict, two registrations and a DECISION beside the deletion.
One dated `.agent/prose_slips.md` line covers it and no id, per amend0827 rule 2.

WHAT MAKES THIS ROUND DIFFERENT FROM ROUND 11, and it is the thing to get right: the dying
module has NO handler file of its own. Its six commands live inside
`apps/cli/commands/worker_facade_cmd.py`, a SURVIVING facade that also serves `worker.doctor`,
`worker.add`, `worker.disable`, `mission.run` and `doctor.core`. The file therefore loses six of
its eleven handlers and keeps five. `doctor.core` — `remedy doctor`, a USER-FACING group — reads
the dying module ONLY through a string-keyed `_try_import` diagnostic probe, so it survives and
loses one probe line. Deleting the file whole would take `remedy doctor` with it.

Change set — 16 paths. DELETED WHOLE, 3, each followed by its line count at `21c90fe5`:
  packages/orchestration/execution_approval_policy.py · 957
  tests/orchestration/test_execution_approval_policy.py · 1197
  docs/system/execution-approval-policy-v0.md · 115

EDITED, 13 — the spec per path, with the measured numstat as `+/-`:
  apps/cli/commands/worker_facade_cmd.py · 0/190 · the SIX contiguous handlers
      `_cmd_approval_policy_list`, `_cmd_approval_policy_show`, `_cmd_approval_policy_enable`,
      `_cmd_approval_policy_disable`, `_cmd_approval_policy_evaluate` and
      `_cmd_approval_policy_grant`; their six `COMMAND_HANDLERS` rows; and the single
      `_try_import("approval_policy", …, "evaluate_execution_approval_policy")` probe line pair
      inside `_cmd_doctor_core`. `_cmd_doctor_core` ITSELF SURVIVES, as do the other four
      handlers and every `worker.*` and `mission.*` command.
  apps/cli/command_catalog.py · 0/75 · the six `CommandEntry(` blocks whose `command_id` is
      `approval.policy-list`, `approval.policy-show`, `approval.policy-enable`,
      `approval.policy-disable`, `approval.policy-evaluate` or `approval.policy-grant`, plus the
      one `"approval": GroupDef(…)` line. The group dies WHOLE. Leave every surviving entry's
      `related=(...)` tuple alone, for the reason round 11's block gives: the field has no
      reader anywhere in the repository.
  tests/cli/test_worker_facade_cmd.py · 3/217 · the five module-level `_POLICY_*` patch-target
      constants and the seven `TestApprovalPolicy*` classes, as one contiguous region, plus the
      orphaned `# Approval CLI handlers (Steps 2781-2785)` banner above them; and THREE guards
      that pin the dying ids by name — `TestHandlerRegistry.test_all_handlers_present`'s
      `expected` set, `TestCollectHandlers.test_facade_in_collected`'s tuple, and
      `TestCatalogIntegration.test_all_facade_commands_have_handlers`, whose
      `assert len(facade_cmds) == 11` becomes `== 5`.
  tests/cli/test_product_spine.py · 1/16 · the six ids out of
      `TestOperatorCommandsExist.test_all_operator_commands_have_handlers`'s tuple, and the two
      tests `test_approval_group_in_catalog` and `test_approval_commands_in_catalog` WHOLE,
      whose only subject is the dying group. THIS FILE IS IN NO INHERITED MAP AND NO TARGETED
      GATE NAMED IT: the reviewer's first dry-run suite went RED on exactly these three tests
      and nothing else, which is why the applied run happens before the block is written.
  tests/orchestration/test_development_artifact_boundary.py · 0/64 · the
      `"execution_approval_policy"` entry of `_PRODUCT_MODULES`;
      `TestProductModulesNoLiveReview.test_execution_approval_policy`;
      `class TestMissionReportNoDevTruth` WHOLE, whose one member reads the dying module's
      source; `class TestApprovalCLINoDevTruth` WHOLE, whose subject is the dying CLI and whose
      assertion is byte-for-byte the surviving `TestDoctorCoreNoDevTruth`'s; and four of the
      five members of `class TestFunctionalNoAgent`.
      `TestFunctionalNoAgent.test_worker_doctor_core_no_agent` SURVIVES and loses ONE entry from
      its `for mod_name in (…)` tuple — `managed_builder_execution` and `main_builder_adapter`
      stay. Do not delete that class: a grep for the module name matches all five members and
      only reading them shows the fifth is about something else.
  tests/orchestration/cluster_deletion_map.txt · 0/1 · the one
      `packages.orchestration.execution_approval_policy <- apps/cli/commands/worker_facade_cmd.py`
      edge
  tests/orchestration/import_reachability_allowlist.txt · 0/1 · the allowlist entry
  tests/orchestration/test_cluster_deletion_map.py · 0/1 · the `CLUSTER_MODULES` row
  scripts/remedy_test_fast.sh · 0/1 · the deleted test file's lane
  docs/README.md · 0/1 · the index row whose LINK TARGET is the deleted page
  docs/system/test-lanes-v0.md · 0/1 · the deleted test file's row
  docs/system/development-artifact-boundary-v0.md · 0/4 · the two table rows and the two bullets
      naming the deleted module
  .agent/f275_deletion_order.md · 2/3 · REGENERATED from `measured_order()` in
      `tests/orchestration/test_cluster_deletion_order.py`, never hand-edited, with the 26-line
      comment header carried byte for byte. NINE components become EIGHT. It is NOT a pure
      deletion: removing the component also reorders two surviving single-module components, so
      the measured numstat is `2 3`.

Constraints:
  1. Apply every BEGIN/END slice BYTE FOR BYTE. Never edit, reflow or renumber one. If a slice
     looks wrong, apply it anyway and DECLARE it in the handback.
  2. Write NO verdict, NO `Done:` paragraph, NO finding and NO registration of your own.
  3. The change set is exactly the 16 paths above plus the six `.agent/` paths of C0a, C0b, C1,
     C2 and C5. If a gate shows a 17th is needed, STOP and report it rather than widening.
  4. C2 and C3 both precede C4: DECISION12 records the reading that authorises the deletion, so
     it is on disk before the deletion lands.
  5. `.agent/plan.md` is advanced at C1, the first substantive commit, per §3 item 23.
  6. Read `.agent/STOP` from disk before C0a. If it exists, write the handback and stop.
  7. Every destructive check runs ONLY in a disposable `git worktree` under `.remedy-wt/`, never
     in the primary checkout. Read a base revision with `git show <sha>:<path>` or in such a
     worktree, never by overwrite-and-restore (§3 item 29).
  8. C4 is ONE commit carrying all 16 paths. Its measured shape is 6 insertions against 2844
     deletions, far under the 500-insertion cap.

Done when — EIGHT gates, every one RUN, every exit code read from the process object and never
through a pipe. Report ONE line per gate in the handback.

  G1 TRANSPORT. `.agent/authored/f275-r12.md` at C0a and `.agent/last_block.md` at C0b are each
     byte-identical to the delegation's source file, by `shutil.copyfile` and a re-read sha256.
     Report the byte count, the digest, and that all three compare equal.
  G2 THE PLAN. `.agent/plan.md` at C1 is byte-identical to the PLAN12 slice. Report its byte
     count, sha256 and line count against the AGENTS.md cap of 50.
  G3 THE RECORD, from the COMMITTED blobs at C1 (pre) and C3 (post), never the worktree.
     (a) `.agent/live_review.md` and `.agent/prose_slips.md` at C2 and `.agent/decisions.md` at
     C3: growth == 1 + len(slice), the pre-blob a byte-exact PREFIX and the slice a byte-exact
     SUFFIX, and the joining byte re-read as `b'\n'`.
     (b) N COUNTED BY YOUR SCRIPT from each slice — never a number this block asserts — and the
     file's last N blank-line-separated units equal the slice's N paragraphs IN ORDER, with a
     per-unit sha256 printed for both sides.
     (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended paragraph of each
     of the three files and require BOTH readers to REJECT it; then re-read all three tracked
     files from disk and show them byte-equal to the committed post-blobs.
     (d) `^Gate: ` 33 → 34; and `^Gate: F275 R11 `, `^- R-0850 — `, `^- R-0851 — ` and
     `^## DECISION F275 D6 ` exactly 1 each.
     (e) THE OPEN SET BY DISTINCT ID, by DECISION F085 D7: 78/4/74 before, 80/4/76 after.
  G4 THE DELETION IS COMPLETE. `git ls-tree -r <C4> --name-only` prints False for all 3 deleted
     paths. Then a whole-word sweep for `execution_approval_policy` over every tracked file
     EXCLUDING `.agent/` and `.data/`, printing EVERY remaining line IN FULL and never
     truncating, and run it TWICE because the two readings answer different questions.
     RAW, matching the line as it stands: the reviewer measured exactly ONE line,
     `docs/roadmap/features/T2_F260.md:345`, a must-not-touch spec file, and a line outside
     `docs/roadmap/features/` and `docs/archive/` is a real miss that ends the round.
     STRIPPED, with backtick-quoted spans DELETED from each line before matching: the reviewer
     measured ZERO lines anywhere, and that count is the binding zero-gate — a token a document
     QUOTES is not a token it USES, which is the R-0584 class, and round 11's own G4 ordered the
     strip for its symbols but not for its module sweep and cost that round an amended commit
     over a comment that was correct.
     Zero-gated symbols, quoted spans deleted first: `evaluate_execution_approval_policy`,
     `execution_approval_policy_summary` and `ExecutionApprovalPolicy` must each be 0.
  G5 THE FOUR MEASUREMENTS OF A DELETION ROUND, at C4.
     (a) RATCHETS: `python3 -B -m pytest tests/orchestration/test_import_reachability.py
         tests/orchestration/test_cluster_deletion_map.py
         tests/orchestration/test_cluster_deletion_order.py tests/docs/
         tests/cli/test_advertised_commands.py tests/cli/test_cli_ux.py
         tests/cli/test_worker_facade_cmd.py tests/cli/test_product_spine.py
         tests/orchestration/test_development_artifact_boundary.py -q` → exit 0.
     (b) THE SHIPPED READERS, through `apps.cli.command_catalog` and `apps.cli.commands`, never
         by grep: `len(_BASE_CATALOG)` 282 → 276, `len(collect_all_handlers())` 282 → 276,
         `len(GROUPS)` 52 → 51, duplicate command ids 0. All six deleted ids ABSENT from both
         readers and `approval` absent from `GROUPS`, printed one per line. AND THE SURVIVAL
         CHECK THIS ROUND TURNS ON: `doctor` IS STILL IN `GROUPS` and `doctor.core` is PRESENT
         in both readers, as are `worker.doctor`, `worker.add`, `worker.disable` and
         `mission.run`. If `doctor.core` is absent, you have deleted a user-facing command —
         STOP and report it.
     (c) THE ORDER FILE: `.agent/f275_deletion_order.md` holds EIGHT components against nine at
         the base; its 26-line comment header is unchanged; the body equals
         `", ".join(component)` over `measured_order()`, and you REGENERATE it rather than
         editing it.
     (d) THE CANARY: `python3 -B -m pytest tests/cli/test_golden_path.py -q` → exit 0.
  G6 RUFF AND BASH. `python3 -m ruff check` over exactly the `.py` files that
     `git diff --name-only 21c90fe5..<C4>` names and that still exist at C4 → `All checks
     passed!`, exit 0. Then repo-wide `python3 -m ruff check .` at C4 AND at the base `21c90fe5`
     read in a disposable worktree: both must read `Found 26 errors.`, the ceiling
     `tests/orchestration/test_ci_budgets.py` holds. `bash -n scripts/remedy_test_fast.sh` →
     exit 0.
  G7 THE FULL SUITE, `python3 -B -m pytest tests/ -q` SERIALLY — no `-n auto` — in the PRIMARY
     CHECKOUT, exit code from the process object. The reviewer's applied dry run was FULLY GREEN
     at 18935 passed, 23 skipped and ZERO failed, so the suite must be GREEN here too; a single
     failure is a red gate and ends the round. CLOSE THE ARITHMETIC BY THE ID SET, not by a
     file-level count: take the base-side collection in a disposable worktree at `21c90fe5`, the
     tip-side at C4, and report the fall and the number of ids GAINED, which must be 0. The
     reviewer measured 18935 + 23 = 18958 collected at the tip. Report the fall you measure and
     attribute it per file; if it differs from the reviewer's, say so rather than restating it.
  G8 THE TREE. `.agent/STOP` re-read from disk: absent. `git status --porcelain`: empty.
     `git worktree list`: the primary checkout ALONE. Branch:
     `feature/f275-one-world-completion-part-three`. `git diff --name-only <C3>..<C4>` names
     EXACTLY the 16 paths of the change set — report it as a set comparison, nothing extra and
     nothing missing. Every commit C0a through C4 single-parent with its insertion count under
     500. C5's own numbers belong to the next round's ledger entry and are not claimed here.

Handback: rewrite `.agent/handoff.md` WHOLE — the state block with `SESSION 7 of feature F275 ·
round 12 · rounds so far 12`, the one-sentence context self-assessment amend0905-throughput
requires, the per-commit changed-files table, one line per gate with its real exit code, the
deviations, the item-status table over the bundle above, the open-findings count, and the next
expected action. It has NO length cap. Then push once.

BEGIN-PLAN12 — the whole new text of `.agent/plan.md`, replacing it entirely
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 12 books round 11's PASS and two prose slips, registers R-0850 and R-0851, records
DECISION F275 D6 — that F275's "Do not touch" protects the APPROVAL GATE F017 owns and not
`execution_approval_policy.py`, which F260's own Design section lists for deletion — and deletes
the SEVENTH module group: `packages/orchestration/execution_approval_policy.py`, whole, in ONE
commit. With it go its 1197-line test file, its doc page, six `approval.policy-*` commands and
the `approval` group WHOLE. `apps/cli/commands/worker_facade_cmd.py` SURVIVES and loses six of
its eleven handlers; `_cmd_doctor_core` SURVIVES and loses one diagnostic probe, so
`remedy doctor` is untouched. The command loss is registered as R-0851.

## Next Steps

1. The `external_builder_sandbox` component, which this round's regeneration makes the order
   file's first line. It is a SINGLE module, and round 11 already measured that
   `apps/cli/commands/external_builder_cmd.py` holds seven handlers driving it, so that file
   dies with it rather than losing one handler as it did in round 11.
2. The remaining components in the recorded order — every one a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 named among the ideas
   deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 74 by distinct id at this round's base `21c90fe5`; the ledger commit this
  block fixes as C2 registers two, taking it to 76. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 stays OPEN and binds every remaining deletion round: `test_advertised_commands.py`
  cannot see an advertisement whose group has been deleted, so a round that deletes a group
  WHOLE must sweep the spaced `remedy <group> <sub>` form by hand. This round swept it and
  found zero.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
END-PLAN12

BEGIN-LEDGER12 — appended to `.agent/live_review.md` after one blank-line separator
Gate: F275 R11 — the F275 round 11 entry. VERDICT PASS, booked by round 12 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, and carried from the pushed `.agent/handoff.md` at `21c90fe5`. EVERY ONE OF THE EIGHT GATES WAS RE-RUN BY THE REVIEWER ITSELF against the committed blobs; the worker's report was evidence for nothing. Range `cb89bbc3`..`21c90fe5`, seven commits C0a `fadfb7c6`, C0b `f5e95902`, C1 `390f908d`, C2 `8ec836ca`, C3 `75a1fa1f`, C4 `eed65ba1` and C5 `21c90fe5`, each parent read from `git log --format=%p`, per-commit insertions 396, 375, 28, 24, 49, 21 and 263, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own scratchpad original and both committed copies are 47959 bytes at `bce4e44492d94253bf84fbb8d190d827a31f85da50039b39e6e5e8af46f8398c` and compare BYTE-EQUAL, so the chain reaches the emitted bytes, which §3 item 37 rules the digest-only form cannot. G2: `.agent/plan.md` byte-identical to PLAN11 at 3029 bytes, 49 lines against the cap of 50, with both mandated headings. G3, over THREE appends rather than two: `.agent/live_review.md` 569448 to 586275, growth 16827 = 1 + 16826; `.agent/prose_slips.md` 177821 to 181173, growth 3352 = 1 + 3351; `.agent/decisions.md` 958331 to 962212, growth 3881 = 1 + 3880. For each, the byte reader `post == pre + newline + slice` held with the joining byte read back as a newline; N was COUNTED from the slice by the reviewer's own reader as 5, 7 and 7, ordered equality held over the WHOLE appended region with a per-unit sha256 printed for all nineteen units on both sides; and all three negative controls — flipped IN MEMORY inside the FIRST appended paragraph, per §3 item 36 — were REJECTED by BOTH readers, with every tracked file re-read from disk afterwards and byte-equal to its committed post-blob. `^Gate: ` 32 to 33; `^Gate: F275 R10 `, `^Note: F275 R11 `, `^- R-0847 — `, `^- R-0848 — `, `^- R-0849 — ` and `^## DECISION F275 D5 ` exactly 1 each; THE OPEN SET 71 TO 74 BY DISTINCT ID against registrations 75 to 78 and resolutions 4 to 4. G4: all 22 whole-file removals absent from `git ls-tree` at C4 over 4585 tracked files, and the whole-word sweep for the four module names over the 1704 tracked files outside `.agent/` and `.data/` printed IN FULL — FOUR remaining lines, every one a must-not-touch spec file, three in `docs/roadmap/features/T2_F260.md` and one in `T2_F272.md`, and ZERO outside `docs/roadmap/features/`. All four zero-gated symbols read 0. G5: the ratchets, `tests/docs/` and the advertisement guard 317 passed at exit 0; the canary 42 passed; through the SHIPPED readers `_BASE_CATALOG` and `collect_all_handlers()` both fell 296 to 282 and `GROUPS` 56 to 52, with all 14 deleted ids ABSENT from both and all five named survivors PRESENT, and zero duplicate ids; the regenerated order file holds NINE components against ten, its 26-line header sha256 unchanged at `aff913e6…`, and the file compares EQUAL to a fresh regeneration from the live import graph. G6: ruff `All checks passed!` over the 13 edited Python files still existing at C4, and repo-wide `Found 26 errors.` at BOTH the base — read in a disposable worktree, never by writing to the primary checkout — and the tip; `bash -n` exit 0. G7: THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 19050 passed, 23 skipped and ZERO failed, and the arithmetic closes BY THE ID SET: 19164 ids at the base against 19005 at C4, a fall of EXACTLY 159 with ZERO gained, attributed 118 across the eight deleted test files, 32 in `tests/test_grouped_cli.py` — which parametrises over the catalog and which no file-level reading predicts — and 9 across the five surgically edited files. G8: `.agent/STOP` absent, porcelain empty, ONE worktree, branch correct, and `75a1fa1f..eed65ba1` naming the 49 paths in an EXACT SET MATCH, nothing extra and nothing missing. WHAT THE ROUND ACHIEVED: the sixth module group and the second strongly connected COMPONENT — `builder_routing`, `candidate_quality`, `local_candidate_generator` and `model_route_tournament`, 3388 module lines — in ONE commit at 21 insertions against 6393 deletions over 49 paths, taking four handler files, 14 catalog entries, FOUR whole command groups, nine test files and five doc pages with them. THE ROUND'S REAL WORTH IS THAT ITS SCOPE WAS ESTABLISHED BY EXECUTION: the map session 6 handed forward named 37 paths, two dying doc pages and nineteen edited files, and the reviewer's applied dry run measured 49, FIVE dying pages and twenty-seven edited files, because two of the five pages carry their dying subject only in their FILENAME and in the spaced commands they advertise. SEVEN DEVIATIONS WERE DECLARED AND ALL SEVEN ARE SUSTAINED. The load-bearing one is the AMENDED C4: the worker's first C4 went RED on G4 because its own explanatory comment QUOTED the module name in backticks, and G4's sweep clause — unlike its own zero-gate clause one sentence later — did not strip quoted spans; the worker rewrote the comment and amended rather than adding a seventh commit, since constraint 8 orders C4 to be one commit and G4 through G8 are all worded "at C4". THE AMEND IS NOT A GUARDRAIL G2 VIOLATION and the reviewer rules so explicitly: `4a257571` was local, unpushed, unreviewed and one minute old, it never reached the remote, it remains reachable in the reflog, and the push that followed was a fast-forward — G2 protects SHARED history, which is the same reading `.agent/decisions.md` already records for an unstage. The two numstat deviations are the reviewer's own block text: `apps/cli/command_catalog.py` was predicted 0/205 and measured 0/206 and `docs/system/worker-registry-route-policy-v0.md` 0/5 against 0/6, both because the reviewer's dry-run script left a blank line at a section seam that the worker correctly removed to match the file's own convention. NO FINDING IS RESOLVED BY THIS GATE.

- R-0850 — Low, A PRIVATE TEST HELPER LEFT BEHIND BY THE ROUND 11 DELETION IS NOW REFERENCED BY NOTHING, AND NO LINTER CAN SEE IT. Raised by the reviewer at the F275 round 11 gate, from the worker's own declared observation rather than from a gate, because no gate this round ordered would find it. THE MEASUREMENT, taken at `21c90fe5`: `_job_with_repo` is defined at `tests/orchestration/test_token_economy_integration.py` line 14 and occurs exactly once in that file and nowhere else under `tests/`, `packages/` or `apps/`. Its only callers were the members of `class TestRoutingIntegration`, which round 11 deleted whole because they drove `builder_routing`. A same-named helper at `tests/orchestration/test_token_economy.py` line 23 is a DIFFERENT module-level function with eight live callers and is not affected; the two were checked apart rather than assumed distinct. WHY RUFF DOES NOT CATCH IT: `F401` covers an unused IMPORT and there is no rule in this repository's selected set — `E`, `F`, `W`, `I`, `UP` — that flags an unreferenced module-level function definition, so the repo-wide count stayed at its ceiling of 26 with the dead code present. WHY IT IS LOW: nothing is wrong at runtime, no test asserts a falsehood, and the whole cost is a reader meeting a fixture-shaped helper that no test uses and having to prove that for themselves. WHY IT IS AN ID AT ALL RATHER THAN A PROSE SLIP: it is wrong state on disk under `tests/`, which operator amendment amend0827-process-diet rule 2 makes the boundary, and it is the same class as R-0841 — residue a deletion leaves in a file it edits but does not delete — which was registered, resolved, and whose fix clause produced the section-comment sweep that has since caught orphan banners in three rounds. THE FIX CLAUSE, binding on the next round whose change set already contains `tests/orchestration/test_token_economy_integration.py`: delete `_job_with_repo` and any import it alone needs, in that round's own commit, and do not open a round for it — AGENTS.md Scope Control forbids the "while I'm here" edit, and this finding exists so the deletion is scheduled rather than opportunistic. If no later round touches that file, it is discharged by the round that drafts DECISION F260 D3, which visits every file the cluster deletion has edited.

- R-0851 — Medium, DELETING `execution_approval_policy` REMOVES SIX COMMANDS AND THE WHOLE `approval` GROUP, AND NO SURVIVING COMMAND SETS OR EVALUATES AN EXECUTION-APPROVAL POLICY. Raised by the reviewer while authoring F275 round 12, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherits the idea. THE MEASUREMENT, taken at `21c90fe5` by an APPLIED dry run of the whole deletion in a disposable worktree, through the SHIPPED readers rather than by grep: `len(_BASE_CATALOG)` and `len(collect_all_handlers())` both fall 282 to 276 and `len(GROUPS)` falls 52 to 51. The six ids are `approval.policy-list`, `approval.policy-show`, `approval.policy-enable`, `approval.policy-disable`, `approval.policy-evaluate` and `approval.policy-grant` — the whole of the `approval` group, which loses its `GroupDef` too. WHAT A USER LOSES: the named-policy registry that decided whether a managed builder execution could proceed without a human, the per-policy enable and disable switches with their real-provider confirmation, the dry-run evaluation of a session against a template, and the grant that recorded a policy-authorised approval. WHAT IS EXPLICITLY NOT LOST, and this is why the severity is Medium rather than High: THE HUMAN APPROVAL GATE IS UNTOUCHED. `patch approve`, `do continue` and the approval-required truth the cockpit reads all survive, and F275's own "Do not touch" protects exactly that gate — DECISION F275 D6, recorded in the same round, is the ruling that the protected gate is F017's and not this prototype module, on the evidence that F260's Design section lists `execution_approval_policy.py` by name in the cluster deletion list. A managed execution that used to be auto-approved by policy now needs the human, which is the SAFER direction and never the more permissive one. WHICH FEATURE INHERITS THE IDEA, as RULE 3 requires and without rebuilding anything: the approval gate F017 owns takes policy-authorised approval, the same inheritor R-0845 named for the self-repair proposal queue; and the execution templates the policy evaluated against belong to `managed_builder_execution`, which is component line 3 of `.agent/f275_deletion_order.md` and dies in a later round of this same feature. THE FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that paragraph names all six ids and the `approval` group among the ideas DELETED rather than inherited, names F017 as the inheritor of policy-authorised approval, and records that Remedy deliberately ships without an automated execution-approval policy until F017 provides one. A stub, a shim, an alias or a compatibility reader is forbidden by AGENTS.md Scope Control by name, and this finding is not resolved by providing one.
END-LEDGER12

BEGIN-SLIPS12 — appended to `.agent/prose_slips.md` after one blank-line separator
2026-09-09 · F275 R12 · The round 11 block's G4 ordered a whole-word module sweep and a symbol zero-gate one sentence apart, and required backtick-quoted spans to be stripped for the SECOND but not the FIRST. The worker's own explanatory comment in `packages/orchestration/worker_registry.py` quoted a dying module name, the sweep went red on it, and the round paid an amended C4 to reword a comment that was correct. A quoted token is not a used token in EITHER reading, and the round 12 block orders the strip for both.

2026-09-09 · F275 R12 · The round 11 block predicted `apps/cli/command_catalog.py` at 0/205 and `docs/system/worker-registry-route-policy-v0.md` at 0/5, and the worker measured 0/206 and 0/6. Both differences are one blank line at a section seam that the reviewer's dry-run script left behind and the worker correctly removed to match each file's own convention. The block's totals were 21 insertions and 6391 deletions against a measured 21 and 6393; the insertions matched exactly and 47 of the 49 per-file numstats matched exactly.

2026-09-09 · F275 R12 · The round 12 block exceeds the sixty-line guidance `docs/roadmap/features/T2_F275.md` gives a deletion-round block, for the same reason round 11's did: the round books a verdict, two registrations and a DECISION beside the deletion, and the spec-per-path list is what keeps a worker from having to re-derive a boundary the reviewer has already executed. The size is declared in the block rather than left for the worker to discover.
END-SLIPS12

BEGIN-DECISION12 — appended to `.agent/decisions.md` after one blank-line separator
## DECISION F275 D6 — the "approval gate" F275's Do-not-touch protects is F017's HUMAN gate, not `execution_approval_policy.py`, which F260's Design lists for deletion (2026-09-09)

Ruled by the reviewer while authoring F275 round 12, under docs/agents/planner_reviewer_prompt.md
§4 item 7, which routes a ruling to a loud, persisted, reversible decision rather than to a
question the operator is never asked. Reverse it by deleting this section, which puts
`execution_approval_policy.py` back under the Do-not-touch clause and stops the cluster deletion
at component line 1 of `.agent/f275_deletion_order.md`.

THE APPARENT CONTRADICTION, stated plainly because it is the whole reason this decision exists.
`docs/roadmap/features/T2_F275.md`'s "Do not touch" section says: "Everything F272's and F274's
'Do not touch' sections name, unchanged: the scope-fence builtin deny list (F017), the approval
gate, STATUS semantics." That clause is inherited unchanged from `T2_F272.md`, which inherited it
unchanged from `T2_F260.md` line 433. And `T2_F260.md` line 345 — in the Design section's cluster
module list, thirty lines earlier in the same file — names `execution_approval_policy.py` among
the modules to be deleted. Read naively, one feature file both protects a module and schedules
it for deletion.

THE READING, and the evidence for it. The two clauses are about DIFFERENT things. "The approval
gate" is the human-in-the-loop mechanism F017 owns: `patch approve`, `do continue`, and the
`approval_required` truth the cockpit and the run record carry. `execution_approval_policy.py` is
a prototype POLICY layer that could authorise a managed builder execution WITHOUT that human, and
it is a cluster module by F260's own enumeration. Three measurements support the reading and were
taken rather than assumed. FIRST, `T2_F260.md` line 345 lists the module by name in the deletion
list, and the same file's Do-not-touch closes with "No module outside the lists above is deleted"
— which makes the LISTS the authority on what is deleted and the approval-gate clause a statement
about a mechanism, not about a file. SECOND, the six commands that die are `user_facing=False` in
`apps/cli/command_catalog.py`, while `patch approve` and `do continue` survive untouched by this
round's change set. THIRD, `.agent/live_review.md` already uses "the approval gate" in exactly
this sense: R-0845's own text routes the self-repair proposal queue "to the approval gate F017
owns", written five rounds before this question arose and by a different round's authoring.

CHOSEN: `execution_approval_policy.py` is deleted with its group, its tests and its doc page, and
the Do-not-touch clause is read as protecting F017's human gate, which this round does not touch.
The deletion makes Remedy STRICTLY MORE conservative — an execution that a policy could once
auto-approve now requires the human — so even a wrong reading here fails safe. The capability
loss is registered as R-0851 in the same round rather than mitigated.

ALTERNATIVES CONSIDERED AND REJECTED. (a) Treat the clause as protecting the module and stop the
deletion here — rejected because it stops F275 at its first single-module component on a reading
that contradicts F260's own deletion list, and operator amendment amend0908-f275-finish permits
an early close only when a module group is genuinely undeletable under T001's three rules, which
this one is not. (b) Ask the operator — rejected because
docs/agents/planner_reviewer_prompt.md §2 forbids handing the operator a ruling request and §4
item 7 requires a loud, persisted, reversible decision instead; this section is that decision and
any later relay is the veto. (c) Delete the module but keep the six commands as thin wrappers —
rejected on AGENTS.md Scope Control, which forbids a stub, a shim, an alias or a compatibility
reader by name.

CONSEQUENCE, stated plainly. Remedy has no automated execution-approval policy after this round,
and `remedy approval` disappears as a command group. Anything that wants an execution approved
goes through the human gate. `remedy doctor` is deliberately NOT affected: `_cmd_doctor_core`
reached this module only through a string-keyed `_try_import` diagnostic probe, that probe line
goes, and the command keeps working — a fact the round measures through the shipped readers
rather than asserting. Nothing on disk becomes inconsistent under the reversal above, because the
module and its tests are recoverable from git and no later commit depends on their absence.
END-DECISION12
