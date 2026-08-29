# Handoff — F033 Hunk-level diff approval · round 15

## Session

SESSION 4 of feature F033 · round 15 · rounds so far 15

## Range

Review of `fa963c4e2fbe50a1d5cc2abb309b17dec764d99a`..`HEAD` (BASE is the round 14
handback commit, on branch `feature/f033-hunk-approval-v2`).

## Commits

### 46beed78 docs(f033): save the round 15 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r15.md | +439 / -0 | C0a — the reviewer's block, copied byte for byte with `shutil.copyfile`. NEW FILE. |

### 31bdb60d docs(f033): mirror the round 15 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +291 / -301 | C0b — the same bytes, so both paths hold ONE blob id (G2). |

### 5e5ba592 docs(f033): open round 15 in the plan
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +17 / -18 | C1 — byte-equal to slice PLANF033R15. |

### bd83cedb docs(f033): book the round 14 verdict, resolve R-0743 and register R-0744
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6 / -0 | C2 — slice RECORDF033R15 appended: the R14 gate paragraph, the `Done: R-0743` resolution and the `- R-0744` registration. |

### 54b569cb fix(f033): resolve the evidence dir from the resolved job id
| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/commands/patch.py | +3 / -1 | C3 — R-0744's one-line fix, `resolve_job_evidence_dir(str(job_id))`, plus the WHY comment naming the finding. |
| tests/cli/test_patch_cmd.py | +75 / -4 | C3 — the two tests that DISCRIMINATE the prefix and uppercase forms, one docstring bullet, and `_job()`'s optional id (deviation D2). |
| .agent/live_review.md | +2 / -0 | C3 — the single `Landed: R-0744 — …` line the block orders, and nothing else. |

### ff9e8e35 feat(f033): open the write door for hunk approval
| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/command_catalog.py | +1 / -0 | C4 — `UI_EXPOSED_COMMANDS` gains `patch.approve-hunks`. |
| packages/orchestration/ui_server.py | +120 / -2 | C4 — `HUNK_APPROVE_COMMAND_ID`, `COMMAND_HUNK_DECISION_STATE_MESSAGE`, the dispatch clause and `_dispatch_approve_hunks`. |
| tests/ui_server/test_command_channel.py | +36 / -10 | C4 — the three widened guards, the renamed exposed-set test, and the fifth widening deviation D1 names. |

### e24d3b44 test(f033): pin the write door's hunk decision effects
| Path | +/- | Reason |
|------|-----|--------|
| tests/ui_server/test_command_dispatch.py | +189 / -0 | C5 — `TestApproveHunksDispatchEffects`, five tests. |

### C6 docs(f033): hand back the round 15 write door
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C6 — this file. A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/g7-f033-r15 e24d3b44`
  — exit 0, "Preparing worktree (detached HEAD e24d3b44)". Created for the G7 mutations
  and used for nothing else.
- `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/g7-f033-r15` then
  `git worktree prune` — removed BY EXACT PATH; `git worktree list` is back to the
  primary checkout alone and `git status --porcelain` is empty.
- `git push -u origin feature/f033-hunk-approval-v2` — the round's FINAL action, run
  immediately after C6. Its outcome cannot be recorded in the file it pushes (the
  write-once rule forbids a second handoff commit), so it is reported in the round
  report instead; a reader auditing it runs
  `git log origin/feature/f033-hunk-approval-v2 -1` and expects the C6 sha.
- No `gh` command, no PR create/edit/merge, no force-push, no history rewrite, no branch
  deletion.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a (`No such file or
directory`) and again before C6 (same) — absent both times. `git status --porcelain`
empty after every one of the seven commits before C6. Branch
`feature/f033-hunk-approval-v2` throughout (`git rev-parse --abbrev-ref HEAD`). No
force-push, no rewrite, no branch deletion; `git rev-parse feature/f033-hunk-approval`
is still `ed04081283081f237d96147da39a07fca0b1ccad`.

**G2 TRANSPORT — PASS.** `46beed78:.agent/authored/f033-r15.md` is 32348 bytes at sha256
`92c6e6c8fb819492e05020373597f833d68729e3d30f9bf7965a83ca809de170`;
`.remedy-wt/f033-r15-block.md` is 32348 bytes at the same sha256; EQUAL, compared as
bytes. `git rev-parse 31bdb60d:.agent/authored/f033-r15.md` and
`git rev-parse 31bdb60d:.agent/last_block.md` both print
`9ef8597a4a5a0ad38622ee804b71cdc7b64db615` — ONE blob id.

**G3 THE RECORD APPEND at C2 — PASS.** (a) BASE blob 1526301 bytes (the ordered value);
slice 7431 bytes; C2 blob 1533733; 1526301 + 1 + 7431 = 1533733 and
`base + b"\n" + slice == C2` byte for byte; BASE is a byte PREFIX of C2; C2 ends in
exactly one newline. (b) N COUNTED by the script = 3. The LAST 3 blank-line units of the
C2 blob equal the slice's three paragraphs IN ORDER: 3720 vs 3720 (`Gate: F033 R14 —`),
1375 vs 1375 (`Done: R-0743 —`), 2331 vs 2331 (`- R-0744 —`). NEGATIVE CONTROL: the
first appended paragraph's BYTE span, computed on bytes, is 1526302 to 1530022 and
`C2[1526302:1530022]` really is that paragraph; the control offset 1528162 is proved to
lie inside it (1526302 ≤ 1528162 < 1530022). The reconstruction reader rejects it (the
slice does not start there) and the paragraph reader rejects it (it is not a paragraph
boundary) — BOTH readers reject.

**G4 THE LEDGER at C2 and C3 — PASS.**

| reading | BASE `fa963c4e` | C2 `bd83cedb` | C3 `54b569cb` |
|---|---|---|---|
| `^- R-\d+ — ` lines / distinct ids | 304 / 304 | 305 / 305 | 305 / 305 |
| `^Done: R-\d+ — ` lines / distinct ids | 48 / 46 | 49 / 47 | 49 / 47 |
| `^Landed: R-` | 16 | 16 | 17 |
| `^Gate: F\d+ R\d+ — ` | 131 | 132 | 132 |
| `^DECISION F033 D\d+ — ` | 4 | 4 | 4 |
| open set (registered − resolved) | 258 | 258 | 258 |

Registered 304 → 305 at C2 with the ADDED id exactly `R-0744`. `Done:` 48 lines over 46
distinct → 49 over 47 with the ADDED resolved id exactly `R-0743`, and the
`Landed: R-0743` line is STILL PRESENT beside its new `Done:` paragraph
(`^Landed: R-0743 — ` counts 1 at BASE, at C2 and at C3). `Landed:` 16 at BASE and 16 at
C2 and 17 at C3, the added line matching `^Landed: R-0744 — ` exactly once. `Gate:`
131 → 132 with `^Gate: F033 R14 — ` exactly 1. `DECISION F033 D` 4 UNMOVED at all three —
this round minted no DECISION. THE OPEN SET IS 258 AT BASE AND 258 AT C2, stated as an
explicit equality rather than inferred: one id was added and one was resolved.

**G5 THE PLAN — PASS.** `.agent/plan.md` at C1 is 2422 bytes over 45 lines — under the
50-line cap AGENTS.md sets — and byte-EQUAL to slice PLANF033R15 (`c1 == slice` is True).

**G6 THE DOOR'S GUARDS at C4 — PASS.**
(a) `python3 -m ruff check` over `packages/orchestration/ui_server.py`,
`apps/cli/command_catalog.py`, `apps/cli/commands/patch.py`,
`tests/ui_server/test_command_channel.py`, `tests/ui_server/test_command_dispatch.py`
and `tests/cli/test_patch_cmd.py` — REAL EXIT CODE 0, summary line `All checks passed!`.
(b) `sorted(UI_EXPOSED_COMMANDS)` at BASE `['decision.resolve', 'job.stop']`; at C4
`['decision.resolve', 'job.stop', 'patch.approve-hunks']`; ADDED exactly
`['patch.approve-hunks']`, REMOVED `[]`. Every member resolves through `get_command`:
`decision.resolve → decision.resolve`, `job.stop → job.stop`,
`patch.approve-hunks → patch.approve-hunks`.
(c) `DOOR_METHODS` at BASE is the ten names
(`_handle_command_submission`, `_dispatch_job_stop`, `_dispatch_decision_resolve`,
`_publish_command_result`, `_emit_command_accepted_event`, `_audit_attempt`,
`_command_is_ui_exposed`, `_replayed_command_result`, `_rate_limit_admits_command`,
`_read_command_payload`); at C4 the same eleven with `_dispatch_approve_hunks` inserted
after `_dispatch_decision_resolve`; ADDED exactly `['_dispatch_approve_hunks']`. By AST
over the C4 source: exactly 1 `_RemedyHandler` ClassDef, `_dispatch_approve_hunks` IS a
real `FunctionDef` member of it, and the set of `DOOR_METHODS` names no method answers
to is `[]` — so nothing in that tuple scans nothing.
(d) `_door_imports` run by this worker over the C4 `ui_server.py` with the C4
`DOOR_METHODS` collects 23 pairs:

    ('apps.cli.command_catalog', 'UI_EXPOSED_COMMANDS')
    ('datetime', 'datetime')
    ('datetime', 'timezone')
    ('packages.orchestration.command_audit', 'audit_command_attempt')
    ('packages.orchestration.command_nonce', 'lookup_nonce_result')
    ('packages.orchestration.command_nonce', 'publish_nonce_result')
    ('packages.orchestration.config', 'get_config')
    ('packages.orchestration.config', 'get_key_spec')
    ('packages.orchestration.data_paths', 'resolve_data_root')
    ('packages.orchestration.diff_view_source', 'DIFF_SCOPE_JOB')
    ('packages.orchestration.diff_view_source', 'build_diff_view')
    ('packages.orchestration.escalation', 'answer_task_decision')
    ('packages.orchestration.evidence_index', 'resolve_job_evidence_dir')
    ('packages.orchestration.flight_plan', 'open_clarification_questions')
    ('packages.orchestration.flight_plan', 'resolve_flight_plan_approval')
    ('packages.orchestration.hunk_approval', 'HunkApprovalRefusal')
    ('packages.orchestration.hunk_decision_record', 'record_hunk_decision_from_view')
    ('packages.orchestration.hunk_ledger', 'HUNK_STATE_APPROVED')
    ('packages.orchestration.hunk_ledger', 'HUNK_STATE_PENDING')
    ('packages.orchestration.hunk_ledger', 'HUNK_STATE_REJECTED')
    ('packages.orchestration.safe_points', 'request_stop')
    ('packages.orchestration.storage', 'save_job')
    ('packages.orchestration.timeline', 'append_run_event')

`found − ALLOWED_IMPORTS` is `[]` and `ALLOWED_IMPORTS − found` is `[]` — empty BOTH
ways. The intersection with `FORBIDDEN_MODULES` is `[]`.
(e) `FORBIDDEN_MODULES` at BASE is nine modules (`packages.common.secure_fs`,
`packages.orchestration.diff_repair_apply`, `packages.orchestration.exec_guard`,
`packages.orchestration.job_fulfillment`, `packages.orchestration.patch_apply`,
`packages.orchestration.source_apply`, `packages.orchestration.workspace`, `shutil`,
`subprocess`); at C4 the same nine plus `packages.orchestration.hunk_apply`. ADDED
exactly `['packages.orchestration.hunk_apply']`, REMOVED `[]`.
(f) The module-level command-id constants at C4:
`JOB_STOP_COMMAND_ID = "job.stop"`,
`DECISION_RESOLVE_COMMAND_ID = "decision.resolve"`,
`HUNK_APPROVE_COMMAND_ID = "patch.approve-hunks"`.

**G7 THE MUTATION RED-PROOFS at C5 — PASS, all four RED.** In the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/g7-f033-r15` at `e24d3b44`, never in the primary
checkout, every run `python3 -B` with `-p no:cacheprovider`. IMPORT PATH PROVED FIRST:
`packages.orchestration.ui_server.__file__`, `apps.cli.commands.patch.__file__` and
`apps.cli.command_catalog.__file__` all resolve under
`.remedy-wt/g7-f033-r15/`. Each mutation's anchor was asserted UNIQUE (count 1) inside
the named file before replacement, and each was reverted fully before the next.

UNMUTATED CONTROLS — `tests/cli/test_patch_cmd.py` REAL exit 0, 13 passed (11 at BASE,
+2 this round); `tests/ui_server/test_command_dispatch.py` REAL exit 0, 12 passed (7 at
BASE, +5 this round); `tests/ui_server/test_command_channel.py` REAL exit 0, 106 passed
(106 at BASE, unmoved).

- **(i) `apps/cli/commands/patch.py`, the R-0744 fix reverted to `job_id_str`** — RED.
  `test_patch_cmd.py` REAL exit 1, 2 failed 11 passed, naming
  `TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId::test_a_short_hex_prefix_records_exactly_as_the_full_id_does`
  and
  `TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId::test_an_uppercase_uuid_records_exactly_as_the_lowercase_one_does`.
  The other two suites stayed exit 0. THE 11 PASSED IS THE REVIEWER'S OWN MEASUREMENT
  REPRODUCED: the eleven pre-existing tests are blind to the defect, and the two new ones
  are the whole discrimination.
- **(ii) `packages/orchestration/ui_server.py`, `save_job` dropped from
  `_dispatch_approve_hunks`** — RED. `test_command_dispatch.py` REAL exit 1, 2 failed 10
  passed, naming
  `TestApproveHunksDispatchEffects::test_an_accepted_submission_records_the_decision_and_persists_it`
  and
  `TestApproveHunksDispatchEffects::test_the_rejected_wire_form_reaches_the_recorder_with_its_reason_verbatim`.
  The other two suites stayed exit 0.
- **(iii) `packages/orchestration/ui_server.py`, the accepted body returned where the
  recorder refuses** — RED, in TWO suites. `test_command_dispatch.py` REAL exit 1, 2
  failed 10 passed, naming
  `TestApproveHunksDispatchEffects::test_a_refused_decision_is_409_audited_rejected_state_and_writes_nothing`
  and
  `TestApproveHunksDispatchEffects::test_an_unresolvable_evidence_directory_takes_the_same_409_path`;
  `test_command_channel.py` REAL exit 1, 1 failed 105 passed, naming
  `TestCommandChannelDoor::test_every_exposed_command_reaches_the_answer_its_effect_gives`.
- **(iv) `apps/cli/command_catalog.py`, `patch.approve-hunks` removed from
  `UI_EXPOSED_COMMANDS`** — RED, in TWO suites. `test_command_dispatch.py` REAL exit 1, 5
  failed 7 passed, naming all five `TestApproveHunksDispatchEffects` tests;
  `test_command_channel.py` REAL exit 1, 1 failed 105 passed, naming
  `TestUiExposedCommands::test_the_set_holds_exactly_the_ruled_ids_and_no_other`.

REVERTED CONTROL — 13 / 12 / 106, all REAL exit 0, back to the unmutated readings. The
worktree was then removed by exact path and `git worktree prune` run; `git worktree list`
shows the primary checkout alone.

**G8 SUITES AND STRUCTURE — PASS.** Serially, one pytest process at a time, in the
primary checkout, each `python3 -B -m pytest -q`:

| suite | REAL exit | passed | at BASE |
|---|---|---|---|
| tests/cli/test_patch_cmd.py | 0 | 13 | 11 |
| tests/ui_server/test_command_dispatch.py | 0 | 12 | 7 |
| tests/ui_server/test_command_channel.py | 0 | 106 | 106 |
| tests/test_command_catalog.py | 0 | 18 | 18 |
| tests/orchestration/test_evidence_index.py | 0 | 33 | 33 |
| tests/orchestration/test_hunk_decision_record.py | 0 | 15 | 15 |
| tests/cli/test_golden_path.py (canary) | 0 | 42 | 42 |

`git rev-list --reverse BASE..C5` walks SEVEN commits, each with exactly ONE parent, each
under 500 INSERTIONS (the `+` column of `git diff --numstat`, never insertions plus
deletions): `46beed78` +439, `31bdb60d` +291, `5e5ba592` +17, `bd83cedb` +6, `54b569cb`
+80, `ff9e8e35` +157, `e24d3b44` +189.

PATH SET IN BOTH DIRECTIONS: the range touches 10 paths; "in range, NOT in the change
set" is `[]`; "in the change set, NOT in range" is `['.agent/handoff.md']`, which is C6
and therefore outside `BASE..C5` by construction.

DELIMITER COUNTS at C5 — `.agent/plan.md` 0/0, `apps/cli/commands/patch.py` 0/0,
`packages/orchestration/ui_server.py` 0/0, `apps/cli/command_catalog.py` 0/0 for
`<<<SLICE ` and `<<<END `; the non-zero CONTROL `.agent/authored/f033-r15.md` reads 4 and
5 (the fifth `<<<END ` is convention 2's own prose quoting `<<<END RECORDF033R15`).
`git ls-files .remedy-wt` reads 0 lines.

DO-NOT-TOUCH PATHS, byte-identical at BASE and at C5 by blob id — 14 of 14:
`packages/orchestration/hunk_decision_record.py` `0563c5a00660`;
`packages/orchestration/hunk_ledger.py` `57c00fcfde62`;
`packages/orchestration/hunk_approval.py` `25d1a8d0d08d`;
`packages/orchestration/hunk_apply.py` `195f0d223210`;
`packages/orchestration/hunk_subset_diff.py` `6c47c2083795`;
`packages/orchestration/diff_view_source.py` `30a86b1b977d`;
`packages/orchestration/diff_parser.py` `b6632f657426`;
`packages/orchestration/evidence_index.py` `4d797b53312a`;
`apps/cli/grouped.py` `c9c5265d0b87`;
`tests/orchestration/test_evidence_index.py` `4c96243ad30e`;
`tests/test_command_catalog.py` `df1e11e6946a`;
`docs/roadmap/STATUS.md` `a370be066b7a`;
`.agent/context.md` `4e3a3f2d9c3f`;
`.agent/prose_slips.md` `bcbce4fa932f`.
THE WHOLE HUNK LAYER IS PROVABLY UNTOUCHED.

## What the round shipped, in the terms the block asked to be quoted

`_dispatch_approve_hunks`'s final signature:

    def _dispatch_approve_hunks(self, job: Any,
                                payload: Any) -> dict[str, Any] | None:

The accepted body's key set is exactly six keys —
`{"command", "outcome", "attempt_key", "approved", "rejected", "pending"}` — measured by
the equality assertion in
`test_the_accepted_body_carries_the_attempt_key_and_the_three_counts`, which pins the
whole dict: `{"command": "patch.approve-hunks", "outcome": "accepted", "attempt_key":
"job:workspace.diff", "approved": 1, "rejected": 1, "pending": 1}`. The three counts come
from the LEDGER's entry states, not from the request.

The full `_door_imports` set is the 23-pair listing in G6(d) above.

Tests written, with the property each pins:

| test | property |
|---|---|
| `test_patch_cmd.py::TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId::test_a_short_hex_prefix_records_exactly_as_the_full_id_does` | R-0744, half one: a job named by the short hex prefix `resolve_job_id` resolves to THAT job records the mixed decision under `job:workspace.diff` with states `approved, rejected, pending`, read back off disk. Premise asserted first: `resolve_job_evidence_dir(str(job.id))` really is the fixture's directory and `resolve_job_id(prefix) == job.id`. |
| `…::test_an_uppercase_uuid_records_exactly_as_the_lowercase_one_does` | R-0744, half two: an UPPERCASE full UUID records identically. The job id is FIXED (`0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d`) so "the uppercase form is a different string" is a fact rather than a probability. |
| `test_command_dispatch.py::TestApproveHunksDispatchEffects::test_an_accepted_submission_records_the_decision_and_persists_it` | The effect RAN and `save_job` RETURNED — the decision is on a job RELOADED from storage, and the audit line is `accepted`. |
| `…::test_the_accepted_body_carries_the_attempt_key_and_the_three_counts` | The 200 body EQUALS the six-key dict above; a pending hunk is reported as pending. |
| `…::test_the_rejected_wire_form_reaches_the_recorder_with_its_reason_verbatim` | `rejected[{id, reason}]` — the wire form `docs/roadmap/features/T5_F033.md` writes — passes STRAIGHT THROUGH, and the reason `"  DSN=postgres://x is out of scope  "` arrives on the job with its surrounding whitespace and its own `=` intact. |
| `…::test_a_refused_decision_is_409_audited_rejected_state_and_writes_nothing` | A refusal from the core is 409 with the generic message, audited `rejected_state`, and `job.metadata` carries NO decisions key at all. The offending id does not reach the wire. |
| `…::test_an_unresolvable_evidence_directory_takes_the_same_409_path` | A NAMED ABSENCE IS NOT A FAILURE: no index record and no CWD-relative directory takes the 409 path, never 500. |
| `test_command_channel.py::TestUiExposedCommands::test_the_set_holds_exactly_the_ruled_ids_and_no_other` (renamed) | The exposed subset is exactly the three ruled ids, and the NAME no longer carries a numeral that can go stale. |
| `test_command_channel.py::TestCommandChannelDoor::test_every_exposed_command_reaches_the_answer_its_effect_gives` (widened, deviation D1) | Every exposed id dispatches, and the two 409s carry DIFFERENT messages on purpose. |

## Authored-text proofs

| authored text | applied to | result |
|---|---|---|
| the whole block | `.agent/authored/f033-r15.md` (C0a) and `.agent/last_block.md` (C0b) | disk-to-disk EQUAL to `.remedy-wt/f033-r15-block.md`: 32348 bytes, sha256 `92c6e6c8…de170`, both paths ONE blob id `9ef8597a…b615`. |
| `PLANF033R15` | `.agent/plan.md` (C1) | extracted from the COMMITTED C0a blob, byte-EQUAL, 2422 bytes / 45 lines. |
| `RECORDF033R15` | `.agent/live_review.md` (C2) | extracted from the COMMITTED C0a blob; `base + newline + slice == C2` byte for byte, 1526301 + 1 + 7431 = 1533733. |

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 `.agent/plan.md` | done | |
| C2 the R14 verdict, the R-0743 resolution, the R-0744 registration | done | |
| C3 the R-0744 fix and the discriminating tests | done | with the `Landed: R-0744` line and nothing else |
| C4 the door — exposure, three widened guards, dispatch | done | ONE commit, plus the fourth guard deviation D1 names |
| C5 the door's behaviour tests | done | five tests |
| C6 the handback | done | this file |
| R-0744 fix | done | `54b569cb`; red-proved by G7 mutation (i) |
| G1 HYGIENE | done | PASS |
| G2 TRANSPORT | done | PASS |
| G3 THE RECORD APPEND | done | PASS, N = 3, both readers reject the control |
| G4 THE LEDGER | done | PASS, every ordered number met |
| G5 THE PLAN | done | PASS, 2422 bytes / 45 lines |
| G6 THE DOOR'S GUARDS | done | PASS, (a)–(f) |
| G7 THE MUTATION RED-PROOFS | done | PASS, all four RED |
| G8 SUITES AND STRUCTURE | done | PASS, seven suites exit 0 |

## Deviations & assumptions

**D1 — a FIFTH edit to `tests/ui_server/test_command_channel.py`, which the SPEC said
would not change.** The SPEC names four edits and closes with "Nothing else in this file
changes". A fifth guard the block did not name reddens on the widened set:
`TestCommandChannelDoor::test_every_exposed_command_reaches_the_answer_its_effect_gives`
iterates `sorted(UI_EXPOSED_COMMANDS)` and branches TWO ways — `job.stop` answers 200,
"else" must answer 409 with the literal `decision is not open`. Measured with the door
code in place and that test untouched: REAL exit 1, 1 failed 105 passed,
`assert 'hunk decision was refused' == 'decision is not open'`. G8 orders that suite at a
REAL exit 0, so per convention 11 the GATE is load-bearing: the "else" arm now reads its
expected message from a per-id map `{"decision.resolve": "decision is not open",
"patch.approve-hunks": "hunk decision was refused"}`, and the docstring moves from "BOTH
exposed ids now dispatch" to "EVERY exposed id now dispatches". The change WIDENS the
guard and weakens nothing — the two 409 messages are now asserted apart, which is the
property the SPEC's own "a new 409 message constant … is preferred over reusing the
decision one, whose wording names decisions" asks for and which nothing else pinned. The
disagreement between the SPEC paragraph and the gate is DECLARED here rather than
silently resolved.

**D2 — two non-test edits to `tests/cli/test_patch_cmd.py`, whose SPEC says "An EDIT that
ADDS. Every existing test stays untouched".** No existing test's body moved — G7 mutation
(i) measures 11 passed beside the 2 new failures, which is the eleven intact. Two
supporting edits were made besides the added class: (a) the module docstring's ordered
property list gains ONE bullet for the new property, in the file's existing style and in
the position the new class occupies, because that list is what a reader trusts to
enumerate what the file pins; (b) the shared `_job()` helper gains an optional `job_id`
parameter defaulting to `uuid4()`. Reason for (b): the uppercase test asserts
`str(job.id).upper() != str(job.id)` as its premise, and `uuid4` can in principle mint an
id whose 31 free nibbles are all digits, which would make that premise a rare flake; a
FIXED id carrying hex letters makes it a fact. Both edits are additive and backward
compatible.

**D3 — the `Landed: R-0744` line names its own commit by ROLE, not by sha.** It reads "at
C3 of F033 round 15 — the commit this line lands in, whose sha the round 15 handback
names, because a commit cannot carry its own id", which is the idiom the round 14
`Landed: R-0743` line established for the same unknowable. The sha is `54b569cb`, named
here and in the commit table above.

**D4 — the G7 controls are 13 / 12 / 106, not the 11 / 7 / 106 the block quotes.** Not a
disagreement: the block's parenthesised numbers are the BASE readings, and G7 runs at C5,
where C3 has added 2 tests to `test_patch_cmd.py` and C5 has added 5 to
`test_command_dispatch.py`. Both readings are reported side by side above so neither has
to be inferred.

**Assumptions.** None beyond the block. Nothing was adjusted to force a colour: every
mutation went red on its own, and no gate came back red and was then repaired by
weakening a test — D1's widening was applied to the DOOR CODE's new behaviour, which the
SPEC ordered, not to an assertion about it.

## Next

The next session's first actions, in this order: read `.agent/STOP` from disk; run the
Open PR Gate; book this round's verdict and resolve R-0744; then the plan's step 3 —
T003, rejection reasons quoted verbatim into the next repair prompt, the report line
derived from the ledger, and partial state rendered truthfully in viewer, node and
report, with R-0738 as T003's to repair. SESSION 4 carries forward.
