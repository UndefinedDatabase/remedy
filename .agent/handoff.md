# Handback — F027 Task veto · Round 6

## Session

SESSION 1 of feature F027 · round 6 · rounds so far 6

Roughly a third of the session's context budget remained at the point this handback was
written. This round booked round 5's verdict, resolved R-1067's registration, recorded
DECISION F027 D6, fixed the guard walker's `if TYPE_CHECKING:` false reach, reviewed and
landed round 5's uncommitted draft of the write door's veto clause and its answer of a
`veto:` replan proposal, and wrote the door tests round 5 stopped short of. All five gates
(G1–G5) ran green; G6 follows below.

## Range

Review of `96cb51546..ae7d4941f` (C1 through C5, all committed). C6 (this handback) follows.

## Commits

### 94973b971 F027 R6 C1: copy round 6 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r6-block.md | +199/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r6-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f027-r6-records.diff | +49/-0 | copy of the records.diff payload |

279 insertions by `git show --numstat` — matches the block's stated expectation exactly
(block line count 199 plus 80), under the 500-line cap.

### 29b3e8567 F027 R6 C2: book round 5, resolve R-1067, record D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +29/-0 | DECISION F027 D6 appended, verbatim from records.diff |
| .agent/live_review.md | +4/-0 | round 5's Gate entry and R-1067's `Done:` paragraph appended |
| .agent/plan.md | +11/-19 | rewritten whole to the plan.md payload |

29/0 decisions.md, 4/0 live_review.md, 11/19 plan.md by `git show --numstat` — matches the
block's stated expectation exactly. `git apply --check` on records.diff → exit 0; the real
`git apply` → exit 0.

### 3742ab963 F027 R6 C3: the door vetoes a task and answers a replan proposal; the guard skips type-only imports
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/decision_inbox.py | +16/-0 | S5, from round 5's draft: `_answerable_by_decision_resolve` gains a `veto:` branch — true while a `vetoed_tasks` entry exists with no `veto_answers` entry, false on `TaskVetoError` |
| packages/orchestration/ui_server.py | +81/-0 | S4, from round 5's draft: `JOB_VETO_TASK_COMMAND_ID`; the `_read_command_payload` shape check for `task_id` and `reason`; `_handle_command_submission`'s new veto clause calling `_dispatch_veto_task`; the `veto:` branch of `_dispatch_decision_resolve` calling `veto_proposal.answer_replan_proposal` |
| tests/orchestration/test_decision_inbox.py | +37/-4 | from round 5's draft: `ANSWERABLE_DECISION_TYPES` gains `replan_proposal`; a new test proves a `veto:` card answerable while open and not answerable once answered |
| tests/ui_server/test_command_channel.py | +60/-6 | W1 (mine) plus the draft's two declared exposed-set adjustments: `_module_level_closure`/`imports_of` skips the body of an `if TYPE_CHECKING:` (or `if typing.TYPE_CHECKING:`) block per DECISION F027 D6, with a new synthetic-module test; `DOOR_METHODS` gains `_dispatch_veto_task`; `ALLOWED_IMPORTS` gains four entries (see Deviations); the door's `job.veto-task` shape-error case and `UI_EXPOSED_COMMANDS`'s literal list |

194 insertions by `git show --numstat`, under the 500-line cap. Reviewed the draft (S4, S5)
against round 5's spec word for word before staging it; found it compliant except for the
`ALLOWED_IMPORTS` count (Deviations). `ruff check` on all four files → clean.
`pytest -q tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard` → 7 passed
(includes the new walker test and the now-green transitive-forbidden test).

### 080219c12 F027 R6 C4: test the door's veto and its answer of a replan proposal
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_dispatch.py | +236/-0 | W3: `TestVetoTaskDispatchEffects` (200 with the control file and event written, three bad-reason shapes each 400 on `reason`, a missing `task_id` 400, an already-vetoed task and a finished job each 409 naming the code, audit outcomes for each) and `TestVetoProposalAnswerDispatchEffects` (accept and replan each 200, a second answer and an unknown id each 409) |

236 insertions, under the 500-line cap. `ruff check` → clean.
`pytest -q tests/ui_server/test_command_dispatch.py` → 49 passed (11 new).

### ae7d4941f F027 R6 C5: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r6-mutations.py | +208/-0 (new) | the round's mutation tool for G5 (excluded from `ruff check` by `pyproject.toml`'s `.agent/authored` exclusion, DECISION F263 D3) |

208 insertions, under the 500-line cap.

### (C6, this commit) F027 R6 C6: rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see below | this handback, rewritten whole per `docs/agents/handback_template.md` |

## External actions

`git push -u origin feature/f027-task-veto` after C6 → see G6 below for the real outcome.
No PR created or merged this round (constraint 5; none was open before this round — see the
Open PR Gate reading in G6 below). One worktree added and removed: `git worktree add
--detach .remedy-wt/f027-r6-mut ae7d4941f` for G5, then `git worktree remove --force
.remedy-wt/f027-r6-mut` and `git worktree prune` immediately after the mutation tool ran;
`git worktree list` before and after matched except for that one entry (see Verification).

## Verification

**BEFORE ANYTHING ELSE (all four readings, all passed):**
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2   (absence confirmed — continue)

$ pwd
/home/decodeux/Repos/remedy
$ git branch --show-current
feature/f027-task-veto
$ git log --oneline -1
96cb51546 F027 R5: write blocked handoff (door guard reddens on task_veto's frozen exec_guard reach)
$ git status --porcelain
 M packages/orchestration/decision_inbox.py
 M packages/orchestration/ui_server.py
 M tests/orchestration/test_decision_inbox.py
 M tests/ui_server/test_command_channel.py
$ git diff HEAD | sha256sum
bb6a81da0676e797cd7303d77b4712d58ebefefc7dccd3bcdc99c248d8d8a395  -
```
All four matched the block's step 2 exactly.

**Block bytes (step 3):** `.remedy-wt/f027-r6/block.md` → 199 lines, sha256
`968fe65d40c578492059112af5b0774556d4e7d0dcd1c4b9baa33bbb8a7c73e1` — both match the
delegation message's two readings exactly.

**Worktree list (step 4):** reported in full at round start; unchanged at handback except
for the G5 worktree added and removed (see External actions and G5 below).

**G1 TRANSPORT** — payload readings (all matched the table):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1127 | 629949b44993842d7db4b9e5451cfde25f05cc3448a0047f2564a7f1c9b0bf2c |
| records.diff | 49 | 9988 | c57e29fdb9193f4f37d6f6ce74d1bd588862a83434641bb368d2ddd1697db874 |

Copy comparisons, all byte-identical (sha256 equal on both sides):
- `git show 94973b971:.agent/authored/f027-r6-block.md` = `.remedy-wt/f027-r6/block.md`
  (`968fe65d...`)
- `git show 94973b971:.agent/authored/f027-r6-plan.md` = `.remedy-wt/f027-r6-payloads/plan.md`
  (`629949b4...`)
- `git show 94973b971:.agent/authored/f027-r6-records.diff` =
  `.remedy-wt/f027-r6-payloads/records.diff` (`c57e29fd...`)

**G2 THE RECORDS** — sha256 at `29b3e8567`, all matched the block's table exactly:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 310462 | c08e4485e54fb30c7e9580be127a908fe2887f403885128db3c5b2454658c283 | yes |
| .agent/decisions.md | 2179770 | 92559cd5450c245b21c4aedc9ae37d8ea3948e95b4ad839aa471424ff42d0a9d | yes |
| .agent/plan.md | 1127 | 629949b44993842d7db4b9e5451cfde25f05cc3448a0047f2564a7f1c9b0bf2c | yes |

`open_finding_ids` (via `scripts/rotate_live_review.py`) over the ledger's text at `29b3e8567`
→ `[]` — matches the reviewer's own reading (empty).

**G3 THE CODE:**
```
$ ruff check packages/orchestration/ui_server.py packages/orchestration/decision_inbox.py \
    tests/ui_server/test_command_channel.py tests/orchestration/test_decision_inbox.py \
    tests/ui_server/test_command_dispatch.py tests/cli/test_decision_cmd.py
All checks passed!
REAL_EXIT=0
```
`git diff -U0 96cb51546 3742ab963 -- tests/ui_server/test_command_channel.py` — reported in
full (see Deviations for the one departure from "and nothing else"): it holds the walker's
`root` parameter, its docstring note, the `is_type_checking_test` helper and the skip itself
with the DECISION F027 D6 comment (the walker's skip); the new synthetic-module test (its
test); `_dispatch_veto_task` added to `DOOR_METHODS` (the door method name); four
`ALLOWED_IMPORTS` lines each commented `# F027 D5` — `veto_task_command`,
`validate_veto_reason`, `TaskVetoRefused` and `answer_replan_proposal` (S6 names three; the
fourth is the declared deviation below); the `job.veto-task` shape-error branch in
`test_every_exposed_command_reaches_the_answer_its_effect_gives` and the `job.veto-task`
entry in `test_the_set_holds_exactly_the_ruled_ids_and_no_other`'s literal list (the two
declared exposed-set adjustments). Nothing else appears in the diff.

**G4 THE TESTS:**
```
$ pytest -q -p no:cacheprovider -rs tests/cli/test_job_veto.py tests/cli/test_job_plan_cmd.py \
    tests/cli/test_job_pause.py tests/ui_server/test_command_channel.py \
    tests/ui_server/test_command_dispatch.py tests/ui_contracts/test_steering_send_contract.py \
    tests/orchestration/test_decision_inbox.py tests/orchestration/test_veto_proposal.py \
    tests/orchestration/test_task_veto.py tests/cli/test_decision_cmd.py \
    tests/test_command_catalog.py tests/cli/test_advertised_commands.py \
    tests/cli/test_exit_codes.py tests/orchestration/test_event_names.py \
    tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py \
    tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py \
    tests/orchestration/test_block_lint.py tests/docs tests/cli/test_golden_path.py
1335 passed in 85.40s
REAL_EXIT=0
```
Zero `SKIPPED` lines (`-rs` printed no short summary section; grepping the whole output for
"skip", case-insensitive, matched nothing).

Reconciling against the reviewer's `1281 passed` (their run excluded the golden path and W3):
`1335 - 1281 = 54`. `--collect-only -q` node counts: `tests/cli/test_golden_path.py` → 42
(excluded from the reviewer's count, included in mine); the new walker test
(`test_the_walker_skips_only_a_type_checking_import`) → 1 (new this round, not in the
reviewer's carried draft); `tests/ui_server/test_command_dispatch.py`'s two new classes → 11
(W3, not yet written when the reviewer measured). `42 + 1 + 11 = 54` — every one of the 54
accounted for.

Per-file grown-node counts (`--collect-only -q`):
- `tests/ui_server/test_command_channel.py` → 110 tests collected
- `tests/ui_server/test_command_dispatch.py` → 49 tests collected
- `tests/orchestration/test_decision_inbox.py` → 47 tests collected

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"name": "handler_import", "status": "pass"}, {"name": "live_review_verdict", "status": "pass"}, {"name": "plan_consistency", "status": "pass"}, {"name": "relevant_untracked", "status": "pass"}, {"name": "repo_root_hygiene", "status": "pass"}, {"name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks `pass`.

**G5 THE RED PROOFS:**
```
$ git worktree add --detach .remedy-wt/f027-r6-mut ae7d4941f
Preparing worktree (detached HEAD ae7d4941f)
REAL_EXIT=0

$ python3 -B .agent/authored/f027-r6-mutations.py .remedy-wt/f027-r6-mut
--- control run (unmutated, before) ---
control: exit=0
206 passed in 16.85s
m1 the door's payload check lets a blank reason through to the job: exit=1 failed=3 failing_node_ids=['tests/ui_server/test_command_dispatch.py::TestVetoTaskDispatchEffects::test_a_bad_reason_is_a_400_on_reason_before_the_job_is_read[-reason_required]', 'tests/ui_server/test_command_dispatch.py::TestVetoTaskDispatchEffects::test_a_bad_reason_is_a_400_on_reason_before_the_job_is_read[sk-ant-aaaaaaaaaaaaaaaaaaaaaaaa-reason_invalid]', 'tests/ui_server/test_command_dispatch.py::TestVetoTaskDispatchEffects::test_a_bad_reason_is_a_400_on_reason_before_the_job_is_read[x*501-reason_too_long]']
m2 the door's payload check is removed for task_id: exit=1 failed=2 failing_node_ids=['tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_every_exposed_command_reaches_the_answer_its_effect_gives', 'tests/ui_server/test_command_dispatch.py::TestVetoTaskDispatchEffects::test_a_missing_task_id_is_a_400_on_task_id']
m3 the door's clause answers a refused veto with a 200: exit=1 failed=2 failing_node_ids=['tests/ui_server/test_command_dispatch.py::TestVetoTaskDispatchEffects::test_a_finished_job_is_409_naming_the_code', 'tests/ui_server/test_command_dispatch.py::TestVetoTaskDispatchEffects::test_an_already_vetoed_task_is_409_naming_the_code']
m4 the door's clause passes a fixed actor instead of the token fingerprint: exit=1 failed=1 failing_node_ids=['tests/ui_server/test_command_dispatch.py::TestVetoTaskDispatchEffects::test_accepted_veto_writes_the_control_file_and_its_event']
m5 the door's veto: branch is removed, so the answer falls to the escalation route: exit=1 failed=2 failing_node_ids=['tests/ui_server/test_command_dispatch.py::TestVetoProposalAnswerDispatchEffects::test_a_replan_is_a_200_and_creates_the_follow_up_job', 'tests/ui_server/test_command_dispatch.py::TestVetoProposalAnswerDispatchEffects::test_accepting_the_reduced_scope_is_a_200']
m6 the inbox's veto: branch reads true for an answered proposal: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_decision_inbox.py::test_veto_card_is_not_answerable_once_answered']
m7 the walker follows the body of an if TYPE_CHECKING: block again: exit=1 failed=2 failing_node_ids=['tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_reaches_only_the_accepted_forbidden_modules_transitively', 'tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_walker_skips_only_a_type_checking_import']
m8 the walker skips every if body, not only a type-only one: exit=1 failed=1 failing_node_ids=['tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_walker_skips_only_a_type_checking_import']
restored byte-identical: True (packages/orchestration/decision_inbox.py)
restored byte-identical: True (packages/orchestration/ui_server.py)
restored byte-identical: True (tests/ui_server/test_command_channel.py)
--- control run (unmutated, after) ---
control: exit=0
206 passed in 11.44s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0

$ git worktree remove --force .remedy-wt/f027-r6-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
$ git worktree list
(unchanged from round start — see step 4's reading; f027-r6-mut no longer present)
```
Every one of the 8 mutations was caught red; both control runs (before and after) were green;
all three touched files restored byte-identical.

**G6 TREE AND PUSH** — reported below, after C6, since C6 itself cannot contain these
readings.

## Authored-text proofs

Block copy: `git show 94973b971:.agent/authored/f027-r6-block.md` sha256-compared against
`.remedy-wt/f027-r6/block.md` → identical (`968fe65d...`). Plan payload copy: same comparison
against `.remedy-wt/f027-r6-payloads/plan.md` → identical (`629949b4...`). Records-diff copy:
same comparison against `.remedy-wt/f027-r6-payloads/records.diff` → identical (`c57e29fd...`).
Post-C2, the sha256 of `.agent/live_review.md`, `.agent/decisions.md` and `.agent/plan.md`
read via `git show 29b3e8567:<path> | sha256sum` all matched the block's G2 table exactly
(see Verification above for the three values). `open_finding_ids` over that same reading →
`[]`, matching the reviewer's own empty reading.

## Deviations & assumptions

**ALLOWED_IMPORTS carries four F027 D5 entries, not the three S6 names.** S6 (bound word for
word except for D6's stop-clause change) names exactly `task_veto.veto_task_command`,
`task_veto.validate_veto_reason` and `veto_proposal.answer_replan_proposal`. The draft I
reviewed and landed also imports `task_veto.TaskVetoRefused` inside `_read_command_payload`,
to catch the exception `validate_veto_reason` raises for each of its three failure codes
(`reason_required`, `reason_too_long`, `reason_invalid`) and turn it into a `_command_field_error`
on field `reason` — exactly the pattern already established for `CHAT_SEND_COMMAND_ID` two
clauses above it (`except SteeringError as exc: return None, _command_field_error("message",
str(exc))`) and for `PlanEditRefused` elsewhere in `ALLOWED_IMPORTS`. I could not remove this
fourth import: `TaskVetoRefused` subclasses plain `Exception`, not `ValueError` (unlike
`SteeringError` and `PlanEditRefused`, both `ValueError` subclasses that a bare `except
ValueError` could catch without a new import), and I am barred from editing `task_veto.py` to
change that (constraint 3's do-not-touch list). The only alternative — a bare `except
Exception` — would need a `# noqa: BLE001` mark, and `tests/test_ble001_ratchet.py`'s frozen
`MAX_EXCUSED = 290` (not in this round's tracked path set, and `pyproject.toml` isn't either)
forbids growing that count without touching two files this round may not touch. Round 5's own
blocked handback already declared this exact same fourth entry when it wrote the draft I
reviewed, for the identical reason, and no operator ruling has since changed it. I therefore
kept it, verified the code is otherwise correct and fully tested (G4, G5 both fully green
including a mutation that removing this check would let through), and report the G3 diff
exactly as run rather than editing it to look compliant: the diff carries this one line
beyond "the three import entries ... and nothing else." A reviewer ruling — widen S6's stated
three to four with a decision amendment, exactly as DECISION F027 D6 itself amended S6's stop
clause, or bump `MAX_EXCUSED` and touch `pyproject.toml` in a future round under a decision
that explicitly authorizes it — would close this permanently; I made neither call myself since
both are outside this round's authority and tracked path set.

**No other deviation.** W2 (reviewing the draft) found S4 and S5 otherwise implemented exactly
as specified; the two exposed-set adjustments round 5's handback declared stand unchanged. W1's
walker fix and its test, and W3's door tests, are new work this round, not deviations from a
draft. C1–C5 followed the block's bundle order and subject lines exactly; no commit was split,
reordered, or added beyond the block's own C1–C6.

## Next

Per the block's own order: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
6, then T003 — the strike, the reason on hover, the dimmed unreachable set with its link, the
veto affordance and the inbox card's plain-words menu on the page. Open findings: 0 (R-1067
closed this round; the ledger's open set read `[]` at C2). Operator-questions count: 5.
