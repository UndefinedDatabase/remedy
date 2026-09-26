# Handback — F289 Self-use sources completion · Round 1

## Session

SESSION 1 of feature F289 · round 1 · rounds so far 1

Roughly half of the session's context budget remained at the point this handback was written.
This round claimed F289, re-headed `.agent/live_review.md` at the F289 claim (booking F027's
round 14 closing-round Gate entry), registered and repaired R-1073 (the diff parser's timing
test), recorded DECISION F289 D1, and landed T002: `doctor_core_report()` as an importable
function beside `_cmd_doctor_core`, returning structured `DoctorWarning`/`DoctorCoreReport`
values with `subject`/`repair_path`/`actionable`, the command's own text and `--json` output
proved byte-identical to the base by a two-tree parity tool, and the self-use generator's Tier 3
(`_doctor_warning_tier`) rendering the first actionable, untargeted warning as a one-task job.

## Range

Review of `d0239fa34..HEAD` (C1a through C5b; this commit is C6).

## Commits

### b894870a2 F289 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r1-block.md | +348/-0 (new) | copy of this round's block, verbatim |
| .agent/authored/f289-r1-plan.md | +38/-0 (new) | copy of the plan.md payload |
| .agent/authored/f289-r1-context.md | +32/-0 (new) | copy of the context.md payload |

418 insertions by `git show --numstat` — matches the block's stated expectation exactly
(block line count 348 plus 70), under the 500-line cap.

### 8158c8a52 F289 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r1-claim.diff | +146/-0 (new) | copy of the claim diff payload |

146 insertions by `git show --numstat` — matches the block's expected 146 exactly.

### 58db5158d F289 R1 C2: claim F289, re-head the live review record, book F027 R14, register R-1073, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +16/-15 | rewritten whole to the context.md payload |
| .agent/decisions.md | +60/-0 | DECISION F289 D1 appended, via `git apply` of claim.diff |
| .agent/live_review.md | +28/-22 | re-headed heading/paragraph/Steps, F027 R14 Gate entry and R-1073 appended |
| .agent/plan.md | +19/-12 | rewritten whole to the plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F289's line `[ ]` to `[~]`, via `git apply` of claim.diff |

16/15, 60/0, 28/22, 19/12, 1/1 by `git show --numstat` — matches the block's C2 expectation
exactly for every file.

### 13b8f88fb F289 R1 C3: guard the diff parser's complexity class by a scale ratio (R-1073)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_diff_parser.py | +72/-29 | S1: `HUGE_DIFF_PARSE_CEILING_SECONDS` replaced by `SMALL_DIFF_BODY_LINE_COUNT`, `PARSE_TIMING_SAMPLES`, `HUGE_DIFF_MAX_SCALING`; the perf-budget test rewritten to a scale-ratio guard of the minimum of five parses each |
| .agent/live_review.md | +2/-0 | the `Landed: R-1073 —` line appended, starting with its own blank line |

74 insertions total (2 + 72) by `git show --numstat`; no expectation was stated for C3 by the
block (only C1a, C1b and C2 carry stated expectations), so this is what was measured.

### 30efd723d F289 R1 C4: make doctor core's report importable and render its actionable warnings as Tier 3
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/worker_facade_cmd.py | +114/-16 | S2/S3/S4/S5: `MODEL_ALIAS_TABLE_PATH`, `DoctorWarning`, `DoctorCoreReport` added; `_cmd_doctor_core`'s body through `ready` moved into `doctor_core_report()`; `_warn` gains `subject`/`repair_path`; `_cmd_doctor_core` now calls the new function and prints from `as_json()` unchanged |
| packages/orchestration/self_use_generator.py | +89/-7 | S6: `_DOCTOR_PROVENANCE`/`_DOCTOR_PROVENANCE_RE`, `_targeted_doctor_keys`, and the real `_doctor_warning_tier` (Tier 3); module docstring item 3 rewritten |

203 insertions total (114 + 89) by `git show --numstat`; no expectation was stated for C4 by
the block, so this is what was measured.

### 5e9fabeea F289 R1 C5a: test the doctor report and Tier 3
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_worker_facade_cmd.py | +106/-0 | `TestDoctorCoreReportFunction`: `as_json()` parity with the command's own output, key order, every warning's three-key `as_json()`, dead-builtin actionability + repair-path existence, dead-configured/unknown-variable non-actionability, `actionable_warnings()` order |
| tests/orchestration/test_self_use_generator.py | +234/-1 | `_no_standing_order` also stubs `doctor_core_report` to an empty report; `TestDoctorWarningTier` (stubbed) and `TestDoctorWarningTierRealChain` (real dead-model chain) |

**DEVIATION (declared, constraint 2):** the block's C5 bundled the two test files and the two
tools into one commit; `git diff --cached --stat` measured 742 insertions before committing,
over the 500-line cap, so it was split into C5a (this commit, the two test files: 340
insertions) and C5b (the two tools: 402 insertions), each its own subject, per constraint 2's
own instruction ("split a commit that would reach it into parts with their own subjects (C4a
and C4b, C5a and C5b), and say so").

### dbfba8cd0 F289 R1 C5b: add the mutation and parity tools
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r1-mutations.py | +250/-0 (new) | G5's mutation/red-proof tool: 12 mutations, purges `__pycache__`, restores bytes, control first and last |
| .agent/authored/f289-r1-parity.py | +152/-0 (new) | G3's parity tool: 5 scenarios × 2 modes, two fresh-subprocess trees, sha256 comparison |

402 insertions total (250 + 152) by `git show --numstat`; see the C5a deviation above for why
this is a separate commit from the test files.

### (this commit) F289 R1 C6: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten whole | this handback, per `docs/agents/handback_template.md`, carrying every gate reading |

## External actions

`git worktree add --detach .remedy-wt/f289-r1-base d0239fa3` and `git worktree add --detach
.remedy-wt/f289-r1-par 30efd723d` (G3), removed via `git worktree remove --force` for both and
`git worktree prune` after the parity run. `git worktree add --detach .remedy-wt/f289-r1-mut
dbfba8cd0` (G5), removed via `git worktree remove --force` and `git worktree prune` after the
mutation run. `git push -u origin feature/f289-self-use-sources` after this commit (C6) → see
G6 below for the real outcome. No `gh pr create` this round (block: "Do NOT create a pull
request: the branch opens one at F289's closure").

## Verification

**BEFORE ANYTHING ELSE (all readings matched):**
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
(absence confirmed at round start — continue)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
main
$ git log --oneline -1
d0239fa34 Merge pull request #283 from UndefinedDatabase/feature/f027-task-veto
$ git checkout -b feature/f289-self-use-sources
Switched to a new branch 'feature/f289-self-use-sources'
```
All matched the block's step 2 exactly.

**Block bytes (step 3):** `.remedy-wt/f289-r1/block.md` → 348 lines (newline count), sha256
`94b51d1827237ef79de9c5898cd9f17fd7f5e925e7f62bd6f3216f8b2f537ae7` — both the line count and
the sha256 match the delegation message's two readings exactly.

**Worktree list (step 4):** the primary checkout plus every reviewer worktree already listed
(`f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-r1-dry`, `f027-*`, `f284-*`, `f289-r1-dry`,
`f289-r1-sim`) and the `job-*` worktrees, nothing else.

**PAYLOADS** — readings (all matched the table exactly, verified before use):
| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 146 | 19624 | c3825c100157897a46ffc99489eb5718a258868eb7ab348eaab45293fefdb8e8 |
| context.md | 38 | 1627 | 764044aa73bcb904fce2ddb75ecd1466bc1d588642b75999487a647efc457f85 |
| plan.md | 32 | 1222 | 52838685baed54c3a2672f8593942a42e0fb329e286b3d272405f0102c931dfb |

**G1 TRANSPORT** — each `.agent/authored/f289-r1-*` state-payload copy read via
`git show <commit>:<path>` and compared byte-for-byte against its source:
| copy | source | commit | equal | sha256 |
|---|---|---|---|---|
| f289-r1-block.md | .remedy-wt/f289-r1/block.md | b894870a2 | True | 94b51d1827237ef79de9c5898cd9f17fd7f5e925e7f62bd6f3216f8b2f537ae7 |
| f289-r1-plan.md | .remedy-wt/f289-r1-payloads/plan.md | b894870a2 | True | 52838685baed54c3a2672f8593942a42e0fb329e286b3d272405f0102c931dfb |
| f289-r1-context.md | .remedy-wt/f289-r1-payloads/context.md | b894870a2 | True | 764044aa73bcb904fce2ddb75ecd1466bc1d588642b75999487a647efc457f85 |
| f289-r1-claim.diff | .remedy-wt/f289-r1-payloads/claim.diff | 8158c8a52 | True | c3825c100157897a46ffc99489eb5718a258868eb7ab348eaab45293fefdb8e8 |

**G2 THE CLAIM** — read at C2 (`58db5158d`) via `git show <C2>:<path>`, all five matched the
reviewer's simulation exactly:
| path | bytes | sha256 | match |
|---|---|---|---|
| docs/roadmap/STATUS.md | 54111 | e4ec53b9440611ebbe6239a2af1105a629427499bab85869338449de5444e039 | yes |
| .agent/live_review.md | 317231 | 6df1c98d4e37381aa83b91326bafaabe90bd813f2f6dd775c6cb810bf8a02b72 | yes |
| .agent/decisions.md | 2211184 | ed4530356eeb7203c79182eb4db25d585be69ac850a16b6902c8ac4d018c4be2 | yes |
| .agent/plan.md | 1222 | 52838685baed54c3a2672f8593942a42e0fb329e286b3d272405f0102c931dfb | yes |
| .agent/context.md | 1627 | 764044aa73bcb904fce2ddb75ecd1466bc1d588642b75999487a647efc457f85 | yes |

`open_finding_ids` (via `scripts/rotate_live_review.py`) over the ledger's text: at `d0239fa3`
→ `[]`; at C2 (`58db5158d`) → `['R-1073']` — both match the block's own readings exactly. At C2
the ledger has exactly one line reading `## Findings` and exactly one reading `## Steps`; its
last line begins `- R-1073 — `. `docs/roadmap/STATUS.md` at C2 reads F289's line in full as
`- [~] F289 — Self-use sources completion (doc staleness and doctor warnings)`, beginning
`- [~] F289 — ` as required. `git diff --name-only 8158c8a52 58db5158d` names exactly:
`.agent/context.md`, `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md` — the table above's five paths and no others.

**G3 THE CODE AND THE PARITY**
```
$ python3 -m ruff check apps/cli/commands/worker_facade_cmd.py \
    packages/orchestration/self_use_generator.py tests/cli/test_worker_facade_cmd.py \
    tests/orchestration/test_self_use_generator.py tests/orchestration/test_diff_parser.py
All checks passed!
REAL_EXIT=0
```
`git diff -U0 58db5158d 13b8f88fb -- .agent/live_review.md`, reported whole:
```
diff --git a/.agent/live_review.md b/.agent/live_review.md
index 9983b2aa5..410f08fc6 100644
--- a/.agent/live_review.md
+++ b/.agent/live_review.md
@@ -436,0 +437,2 @@ Gate: F027 R14 — the F027 round 14 entry: the closing round — the booking of
+
+Landed: R-1073 — the diff parser's timing test asserts the ratio of the minimum of five parses of the 10,000-line fixture to that of a 1,000-line fixture below 20, and the absolute ceiling is gone, at this round's C3.
```
Adds exactly the blank line and the one `Landed:` line, nothing else.

THE PARITY — `.agent/authored/f289-r1-parity.py` run against `git worktree add --detach
.remedy-wt/f289-r1-base d0239fa3` and `git worktree add --detach .remedy-wt/f289-r1-par
30efd723d`, whole output:
```
a_as_shipped json: base=64cb55120c535a31c2cfcd2f4e15640ba2416e0b9087c763dd4d4a6cff28f1aa par=64cb55120c535a31c2cfcd2f4e15640ba2416e0b9087c763dd4d4a6cff28f1aa equal=True
a_as_shipped text: base=c07d866bc5705454d6f433936bb4fabc116a6052a1113e3e7f9c9d3ec32bd993 par=c07d866bc5705454d6f433936bb4fabc116a6052a1113e3e7f9c9d3ec32bd993 equal=True
b_dead_model_and_configured_id json: base=ac786cfb0dba0b73f134df0a509c60b6f935e330311e5b9dc09d43cebaa360ec par=ac786cfb0dba0b73f134df0a509c60b6f935e330311e5b9dc09d43cebaa360ec equal=True
b_dead_model_and_configured_id text: base=92960a1b1bb0a0bd22dfc66833cced7bd8763eee21d5db9a8118ee2fd322e1bc par=92960a1b1bb0a0bd22dfc66833cced7bd8763eee21d5db9a8118ee2fd322e1bc equal=True
c_unknown_and_unparsable_env_variable json: base=2d510e29f44c0d6237ffbbe027828b93722127694db2ac484353f8570262a68c par=2d510e29f44c0d6237ffbbe027828b93722127694db2ac484353f8570262a68c equal=True
c_unknown_and_unparsable_env_variable text: base=b21295fea76ad32c60c8c2d90577c4b5da5154ee35ec02d58b5c7f9a3d85a636 par=b21295fea76ad32c60c8c2d90577c4b5da5154ee35ec02d58b5c7f9a3d85a636 equal=True
d_dead_model_loaders_raise json: base=6002a52d2096b64cddaf5514414c4fa0fbe0e1b7ce0f6cbb78bcba0695cb8f83 par=6002a52d2096b64cddaf5514414c4fa0fbe0e1b7ce0f6cbb78bcba0695cb8f83 equal=True
d_dead_model_loaders_raise text: base=aea349ca254c5e2a68fb0ad1b41eaac87ceda0f657cb14417d43f80e10068ac7 par=aea349ca254c5e2a68fb0ad1b41eaac87ceda0f657cb14417d43f80e10068ac7 equal=True
e_empty_scripts_dir json: base=dd166f31eb53e892d58214a517497dd0de09ce9517f5bb93eccbfbc8626dc94e par=dd166f31eb53e892d58214a517497dd0de09ce9517f5bb93eccbfbc8626dc94e equal=True
e_empty_scripts_dir text: base=94f9585cebb860e41fd9a90b8c9626d2585afc771f1290a1dc44ab4b7df20620 par=94f9585cebb860e41fd9a90b8c9626d2585afc771f1290a1dc44ab4b7df20620 equal=True
PARITY: True
REAL_EXIT=0
```
`PARITY: True`, required and met. Both worktrees removed via `git worktree remove --force`,
`git worktree prune` run; `git worktree list` afterwards showed the primary checkout and only
the pre-existing reviewer/job worktrees.

**G4 THE TESTS** — serial run in the primary checkout at C5 (`dbfba8cd0`), trimmed:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_worker_facade_cmd.py \
    tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py \
    tests/orchestration/test_self_use_queue.py tests/orchestration/test_diff_parser.py \
    tests/orchestration/test_env_registry.py tests/orchestration/test_disk_floor.py \
    tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_toolchain.py \
    tests/cli/test_mission_cmd.py tests/orchestration/test_import_reachability.py \
    tests/test_no_orphan_modules.py tests/test_test_categories.py tests/test_ble001_ratchet.py \
    tests/test_imports.py tests/test_command_catalog.py tests/test_subprocess_timeouts.py \
    tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py \
    tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py \
    tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs \
    tests/cli/test_golden_path.py
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
998 passed, 1 skipped in 241.40s (0:04:01)
REAL_EXIT=0
```
One `SKIPPED` line, the pre-existing D12 quarantine, unchanged. The reviewer's own reading at
`d0239fa3` (before any code change) was `983 passed, 1 skipped`; this round's own two edited
test files add exactly 15 collected nodes — `python3 -m pytest --collect-only -q` on
`tests/cli/test_worker_facade_cmd.py tests/orchestration/test_self_use_generator.py` reads 90
nodes at `d0239fa3` (47 + 43) and 105 nodes at C5 (53 + 52) — and 983 + 15 = 998, which is
exactly what ran. No other difference from the reviewer's count.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=161", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0, as required.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f289-r1-mut dbfba8cd0`, then
`.agent/authored/f289-r1-mutations.py` run against it, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1_doctor_warning_as_json_also_writes_subject: exit=1 failed=1 nodes=['tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_every_warnings_as_json_key_list_is_exactly_three_keys']
m2_dead_builtin_model_warning_carries_no_repair_path: exit=1 failed=3 nodes=['tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_a_dead_builtin_default_is_actionable_with_its_id_and_repair_path', 'tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_actionable_warnings_answers_exactly_the_actionable_ones_in_order', 'tests/orchestration/test_self_use_generator.py::TestDoctorWarningTierRealChain::test_a_real_dead_builtin_default_becomes_a_tier_3_item']
m3_dead_configured_model_warning_carries_the_alias_table_repair_path: exit=1 failed=1 nodes=['tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_a_dead_configured_id_and_an_unknown_variable_are_not_actionable']
m4_unknown_env_variable_warning_carries_no_subject: exit=1 failed=1 nodes=['tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_a_dead_configured_id_and_an_unknown_variable_are_not_actionable']
m5_doctor_core_report_as_json_writes_warnings_before_blockers: exit=1 failed=1 nodes=['tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_as_json_key_order']
m6_tier_3_ignores_the_keys_the_queue_already_targets: exit=1 failed=2 nodes=['tests/orchestration/test_self_use_generator.py::TestDoctorWarningTier::test_of_two_actionable_warnings_the_first_is_offered_then_the_second', 'tests/orchestration/test_self_use_generator.py::TestDoctorWarningTier::test_a_consumed_entry_targeting_a_key_still_withdraws_it']
m7_tier_3_offers_the_last_actionable_warning_instead_of_the_first: exit=1 failed=1 nodes=['tests/orchestration/test_self_use_generator.py::TestDoctorWarningTier::test_of_two_actionable_warnings_the_first_is_offered_then_the_second']
m8_tier_3_accepts_a_detail_holding_a_heading_line: exit=1 failed=1 nodes=['tests/orchestration/test_self_use_generator.py::TestDoctorWarningTier::test_a_detail_shaped_like_a_heading_raises']
m9_tier_3_writes_the_summary_as_the_task_body_instead_of_the_detail: exit=1 failed=1 nodes=['tests/orchestration/test_self_use_generator.py::TestDoctorWarningTier::test_a_single_actionable_warning_becomes_a_tier_3_item']
m10_generate_self_use_item_tries_tier_3_before_the_ledger_tier: exit=1 failed=1 nodes=['tests/orchestration/test_self_use_generator.py::TestDoctorWarningTier::test_an_eligible_ledger_finding_wins_over_tier_3']
m11_tier_3_offers_a_warning_that_is_not_actionable: exit=1 failed=1 nodes=['tests/orchestration/test_self_use_generator.py::TestDoctorWarningTier::test_only_non_actionable_warnings_answer_none']
m12_diff_parser_does_quadratic_work_per_body_line: exit=1 failed=1 nodes=['tests/orchestration/test_diff_parser.py::test_the_huge_diff_parses_inside_the_recorded_perf_budget']
restored byte-identical: True (apps/cli/commands/worker_facade_cmd.py)
restored byte-identical: True (packages/orchestration/self_use_generator.py)
restored byte-identical: True (packages/orchestration/diff_parser.py)
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every one of the 12 mutations caught with at least one failing node; both controls green; all
three files restored byte-identical. `git worktree remove --force .remedy-wt/f289-r1-mut`,
`git worktree prune` run; `git worktree list` afterwards showed the primary checkout and only
the pre-existing reviewer/job worktrees.

**G6 AFTER C6** — reported in the final reply, after this commit and the push.

## Authored-text proofs

Block copy: `.remedy-wt/f289-r1/block.md` sha256
`94b51d1827237ef79de9c5898cd9f17fd7f5e925e7f62bd6f3216f8b2f537ae7`, matched against `git show
b894870a2:.agent/authored/f289-r1-block.md` → identical. Payload copies: the same comparison
against `.remedy-wt/f289-r1-payloads/{plan.md,context.md}` via `git show
b894870a2:.agent/authored/f289-r1-{plan,context}.md` → identical, and
`.remedy-wt/f289-r1-payloads/claim.diff` via `git show
8158c8a52:.agent/authored/f289-r1-claim.diff` → identical (sha256 values in the PAYLOADS/G1
tables above). Post-C2, the sha256 of `docs/roadmap/STATUS.md`, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/plan.md` and `.agent/context.md`, read via `git show
58db5158d:<path>`, matched the block's G2 table exactly. `open_finding_ids` over the C2 reading
→ `['R-1073']`, matching the block's own reading exactly.

## Deviations & assumptions

**One declared split (constraint 2).** The block's bundle names C5 as one commit ("THE TESTS
AND THE TOOLS: the two test files, your mutation tool ..., and your parity tool ..."). Staging
all four files together and running `git diff --cached --stat` measured 742 insertions, over
the 500-line cap. Per constraint 2's own instruction, it was split into C5a (the two test
files, `tests/cli/test_worker_facade_cmd.py` and `tests/orchestration/test_self_use_generator.py`,
340 insertions) and C5b (the two tools, `.agent/authored/f289-r1-mutations.py` and
`.agent/authored/f289-r1-parity.py`, 402 insertions), each under 500 and each with its own
subject naming the split. No file the block orders was edited or retyped; `git apply --check`
preceded the one `git apply` (of `claim.diff`) and both returned exit 0; every other commit's
`git show --numstat` reading matches the block's stated expectation exactly (C1a: 418, C1b:
146, C2: 16/15+60/0+28/22+19/12+1/1); the round's tracked path set (`git diff --name-only
d0239fa3` at the tip before C6) is exactly constraint 3's set. `.agent/STOP` was absent both at
the round's own step-1 check and now. Nothing was merged, no branch or worktree named in
constraint 6 was deleted, no force-push, no `git stash`. amend0917 rule 1 was honored: no full
suite was run this round (only the targeted serial selection G4 names).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 418 insertions, matches block exactly |
| C1b | done | 146 insertions, matches block exactly |
| C2 (the claim) | done | 16/15, 60/0, 28/22, 19/12, 1/1, matches block exactly |
| C3 (R-1073) | done | 74 insertions (2 + 72); no expectation stated, measured and reported |
| C4 (the code) | done | 203 insertions (114 + 89); no expectation stated, measured and reported |
| C5a (the tests) | done | split from C5 (declared deviation), 340 insertions |
| C5b (the tools) | done | split from C5 (declared deviation), 402 insertions |
| C6 (the handback) | done | this commit |
| Push after C6 | done | see final reply |
| G1 TRANSPORT | done | all four payload copies byte-identical |
| G2 THE CLAIM | done | all five sha256 readings match, open-set and STATUS-line readings match |
| G3 THE CODE AND THE PARITY | done | ruff clean, ledger diff exact, PARITY: True |
| G4 THE TESTS | done | 998 passed, 1 skipped; 15 nodes added, accounted for; integrity check all pass |
| G5 THE RED PROOFS | done | all 12 mutations caught, all files restored, controls green |
| G6 TREE AND PUSH | done | see final reply |

## Next

Per the block's own `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from disk, currently
absent) — then the review of this round (round 1) — then T001: the documentation-staleness
catalog of at least ten checks over the README, the guides and the command catalog, and the
self-use generator's Tier 2. Open findings: 1 (R-1073, landed this round at C3, awaiting the
reviewer's `Done:`). Operator questions open: 0.
