# F033 — Hunk-level diff approval · ROUND 15 · THE WRITE DOOR, AND R-0744

SESSION 4 of feature F033. Round 15, rounds so far 15.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R15`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline. Every APPEND
   slice is joined to its file as: the base blob, then one newline, then the
   slice, and the result ends in exactly one newline. Take a slice as the bytes
   from the end of its `<<<SLICE` marker line up to and INCLUDING the newline
   that ends its last content line.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON IS A SPEC, NOT A SLICE. You write the code and the tests from the
   description. Names, signatures and the behaviours the SPEC fixes are binding;
   structure, comment wording and test names are yours. If the SPEC is
   impossible, STOP and say so rather than inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>`. NEVER write a base
   blob over a tracked file.
9. Purge `__pycache__` or use `python3 -B` whenever a mutation must reach a test.
10. Byte OFFSETS and byte SPANS are measured on BYTES, never on a decoded string.
11. IF A GATE AND A SPEC PARAGRAPH DISAGREE, the GATE is load-bearing: satisfy it,
    satisfy the SPEC's INTENT around it, and declare the disagreement.

## Base

BASE is `fa963c4e2fbe50a1d5cc2abb309b17dec764d99a`, the round 14 handback commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 14 PASSED WITH RISKS and C2 books that verdict, resolves R-0743 and
registers R-0744.

R-0743 IS GENUINELY FIXED and the reviewer proved it by the COLOUR CHANGE rather
than by reading the test: the precedence mutation that came back GREEN at
`55c365d6` comes back RED at `eec2cd4a`, at exit 1 and 1 failed, naming
`test_the_index_record_beats_the_cwd_relative_fallback`.

R-0744 IS YOUR OWN DEVIATION D3, PROMOTED TO A FINDING BECAUSE IT HAS PRODUCT
EFFECT, and you were right to declare it rather than fix it past the SPEC. The
reviewer reproduced it end to end through the SHIPPED handler at `fa963c4e`: one
job, one evidence directory, one index record, driven twice. With the FULL
lowercase UUID the command exits 0 and records. With the SHORT HEX PREFIX — which
`resolve_job_id` resolves to that same job, and which exists precisely so an
operator need not type a UUID — the command exits 1 with `no_diff_available` and
records nothing. An UPPERCASE full UUID fails the same way. The operator is told
"The attempt's diff is not available to decide over" while the diff is sitting in
the directory the index names. That is the misreport
`HUNK_RECORD_REFUSAL_NO_DIFF` was minted to PREVENT, arriving through the id
instead of through the artifact. THE REVIEWER ALSO MEASURED THAT THE SUITE IS
BLIND TO IT: applying the one-line fix inside a disposable worktree left all
eleven tests in `tests/cli/test_patch_cmd.py` GREEN, so the fix needs a test that
DISCRIMINATES or the same defect returns silently.

NOW THE DOOR. Every piece behind it is built and pinned. What remains is exposure
and dispatch, and it is the most guard-dense change in this feature, so the
guards are named here rather than discovered. MEASURED AT BASE:

- `apps/cli/command_catalog.py` holds `UI_EXPOSED_COMMANDS` as a frozenset of
  exactly `job.stop` and `decision.resolve`, and
  `TestUiExposedCommands.test_the_set_holds_exactly_the_two_ruled_ids` in
  `tests/ui_server/test_command_channel.py` asserts that list by EQUALITY. Its
  NAME also states the count, so the name moves with the assertion.
- `TestCommandDoorImportGuard` holds THREE equality-shaped guards over the door:
  `DOOR_METHODS`, a tuple of the handler methods whose AST is walked;
  `ALLOWED_IMPORTS`, a frozenset of every `(module, name)` those methods may
  import; and `FORBIDDEN_MODULES`, which they may never import from. A new
  dispatch method that is not in `DOOR_METHODS` is NOT SCANNED AT ALL, and a new
  import not in `ALLOWED_IMPORTS` turns the branch tip RED. Both are widened in
  the SAME commit as the code, C4.
- `_door_imports` walks `_RemedyHandler`'s named methods and collects DIRECT
  imports only. That is exactly why DECISION F033 D4 built the recorder to drag
  no applicator behind it, and why `packages.orchestration.hunk_apply` joins
  `FORBIDDEN_MODULES` in that same commit: the guard must forbid by NAME the one
  import that would defeat it by SUBSTANCE.
- `_handle_command_submission` dispatches by an `if payload["command"] == ...`
  clause per id and ends in DECISION F009 D22's 501 guard for an exposed id no
  clause matches. `payload["args"]` is an untyped object by DECISION F009 D14, so
  every field is read with `.get` and degrades rather than raising.
- `hunk_approval._normalise_rejection` ALREADY accepts a rejection as a mapping
  with `id` or `hunk_id` plus `reason` — which is the wire form
  `docs/roadmap/features/T5_F033.md` writes as `rejected[{id, reason}]`. So the
  door passes `args.rejected` STRAIGHT THROUGH and validates nothing itself.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 14 verdict, the R-0743 resolution and the R-0744 registration
  into `.agent/live_review.md`
- C3 the R-0744 fix and the tests that DISCRIMINATE it
- C4 the door: the exposed set, the three widened guards and the dispatch —
  ONE commit, because each half without the other ships a red branch tip
- C5 the door's behaviour tests
- C6 the handback

You write NO `Done:` paragraph — `Done:` is the reviewer's word. Mark the R-0744
fix with a single line `Landed: R-0744 — <one line: what changed, which commit>`
appended in C3, and nothing else.

## Change set — these paths and nothing else

    .agent/authored/f033-r15.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    apps/cli/commands/patch.py
    tests/cli/test_patch_cmd.py
    apps/cli/command_catalog.py
    packages/orchestration/ui_server.py
    tests/ui_server/test_command_channel.py
    tests/ui_server/test_command_dispatch.py
    .agent/handoff.md

NEW FILES, named rather than counted: `.agent/authored/f033-r15.md`. This round
does NOT touch `packages/orchestration/hunk_decision_record.py`,
`packages/orchestration/hunk_ledger.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_apply.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/diff_view_source.py`,
`packages/orchestration/diff_parser.py`,
`packages/orchestration/evidence_index.py`, `apps/cli/grouped.py`,
`tests/orchestration/test_evidence_index.py`, `tests/test_command_catalog.py` or
`docs/roadmap/STATUS.md`. THE WHOLE HUNK LAYER IS PROVABLY UNTOUCHED and G8
measures it. `.agent/context.md` and `.agent/prose_slips.md` are deliberately NOT
touched: this round has no reviewer prose slip to record.

## SPEC — `apps/cli/commands/patch.py`, the R-0744 fix

ONE line changes. In `_cmd_approve_hunks`, the evidence directory is resolved
from the RESOLVED job id and not from the operator's raw argument:

    evidence_dir = evidence_index.resolve_job_evidence_dir(str(job_id))

`job_id` is the `UUID` that `resolve_job_id(job_id_str)` returned on the line
above, so `str(job_id)` is the canonical lowercase hyphenated form the index
file is named with. This fixes BOTH halves of the defect at once — the short hex
prefix and the uppercase UUID — because both differ from the canonical form only
in ways `UUID` normalises. Put the one-line WHY directly above it, naming the
finding: the operator's argument may be a prefix, and the index is keyed by the
full id.

Change NOTHING else in this file.

## SPEC — `tests/cli/test_patch_cmd.py`, the tests that discriminate it

An EDIT that ADDS. Every existing test stays untouched.

The reviewer measured that all eleven existing tests stay GREEN when the fix is
applied, so they do not reach this defect at all. Add tests that DO, each
building a job whose evidence directory really resolves under the FULL id and
then naming that job the other way:

- by SHORT HEX PREFIX — the same prefix `resolve_job_id` resolves to that job —
  records exactly as the full id does, and `save_job` really persisted it;
- by UPPERCASE full UUID — likewise.

Each must FAIL if the argument reverts to `job_id_str`, and G7 mutation (i)
is the proof. Assert the RECORDED state, not merely the exit code: a test that
only checks exit 0 would pass against a handler that recorded under the wrong
key.

## SPEC — `apps/cli/command_catalog.py`

`UI_EXPOSED_COMMANDS` gains `"patch.approve-hunks"` and nothing else changes.
Keep the frozenset literal's existing shape. The comment above it, if any, is
updated only if it states a count.

## SPEC — `tests/ui_server/test_command_channel.py`

An EDIT that WIDENS three guards and one test name, in the SAME commit as the
door code. Nothing else in this file changes.

1. `TestUiExposedCommands.test_the_set_holds_exactly_the_two_ruled_ids` asserts
   the three ruled ids in sorted order. ITS NAME STATES THE COUNT, so rename it
   so the name and the assertion cannot drift apart — a name carrying a stale
   numeral is the half nobody re-reads.
2. `DOOR_METHODS` gains `"_dispatch_approve_hunks"`. Without this the new method
   is not scanned by the import guard AT ALL, which is the worst way for a guard
   to fail.
3. `ALLOWED_IMPORTS` gains one entry per `(module, name)` the new method really
   imports, each with a trailing comment naming F033 D4 the way its neighbours
   name their own decisions. Do not add an entry the code does not import: the
   guard is an EQUALITY over what the AST finds.
4. `FORBIDDEN_MODULES` gains `"packages.orchestration.hunk_apply"`. WHY it
   belongs here even though nothing imports it: `_door_imports` collects DIRECT
   imports only, so a later edit importing the applier into a door method would
   otherwise pass a guard whose whole purpose is to keep the applier out of an
   HTTP handler. DECISION F033 D4 is the rule; this line is what enforces it.
   Its comment says so.

## SPEC — `packages/orchestration/ui_server.py`, the dispatch

An EDIT that ADDS one module-level constant, one dispatch clause and one method.

`HUNK_APPROVE_COMMAND_ID = "patch.approve-hunks"` sits beside
`JOB_STOP_COMMAND_ID` and `DECISION_RESOLVE_COMMAND_ID`, in their idiom.

`_dispatch_approve_hunks(self, job, payload) -> dict[str, Any] | None` records
one hunk decision and PERSISTS it. In order:

1. `args = payload.get("args")`, then `args if isinstance(args, dict) else {}` —
   DECISION F009 D14 types `args` as an object and never types what is inside it,
   so every field below degrades instead of raising.
2. `task_run = args.get("task_run")`, kept only when it is a `str` and otherwise
   None; None selects the job-level scope.
3. `approved = args.get("approved")` and `rejected = args.get("rejected")`, each
   kept only when it is a `list` and otherwise the empty list. They are passed
   STRAIGHT THROUGH: `decide_hunk_approval` is total on any input at all and
   already accepts the `{id, reason}` wire form, so a second validation here
   would give one fault two names.
4. Resolve the directory with `resolve_job_evidence_dir(str(job.id))` — the
   CANONICAL id, for the reason R-0744 records — and build the envelope with
   `build_diff_view(evidence_dir, task_id=task_run)`.
5. `record_hunk_decision_from_view`, with `task_id` the envelope's `task_id` when
   that is not None and `DIFF_SCOPE_JOB` otherwise, and `attempt` the envelope's
   `source` — the same envelope-derived key the CLI door composes, so one
   decision has ONE key whichever door records it. `now` is
   `datetime.now(timezone.utc)`.
6. A `HunkApprovalRefusal` returns None. The caller answers that 409 and audits
   it `rejected_state`, exactly as `_dispatch_decision_resolve`'s None does.
   THE REFUSAL'S CODE AND MESSAGE ARE DELIBERATELY NOT RETURNED THROUGH THIS
   DOOR: every message this handler emits goes through `_safe_error`, and both
   existing 409s answer with a fixed generic constant. The operator who needs the
   detail has the CLI door, which is not a network boundary. This is DECISION
   F009 D18 and D22 applied unchanged, not a new rule — say so in the docstring
   and mint no new DECISION number.
7. Otherwise `save_job(job)` and return the accepted body. BOTH are the effect,
   exactly as DECISION F009 D21 rules for `decision.resolve`: the decision is
   durable only once `save_job` returns, so a raise from either is D18 clause
   four's `rejected_effect`. Build the body in the shape the two existing
   dispatch methods build theirs, carrying the attempt key and the approved,
   rejected and pending counts derived from the ledger. REPORT the body's final
   key set in the handback.

The dispatch clause in `_handle_command_submission` sits beside the other two and
copies `decision.resolve`'s structure exactly, including its `except (OSError,
RuntimeError, ValueError, TypeError)` arm auditing `rejected_effect` and
answering 500, its None arm auditing `rejected_state` and answering 409, and its
accepted arm's ORDER — the effect, then the `accepted` audit line, then the
publication, then the event, then the 200. A new 409 message constant beside the
existing ones is fine and preferred over reusing the decision one, whose wording
names decisions.

## SPEC — `tests/ui_server/test_command_dispatch.py`

An EDIT that ADDS. Every existing test stays untouched.

Add tests for: an exposed, well-formed submission records the decision on the job
and `save_job` really persisted it, proved by loading the job back; the response
is 200 and its body carries the attempt key and the three counts; a decision the
core refuses answers 409, audits `rejected_state` and writes NOTHING to
`job.metadata`; an attempt whose evidence directory does not resolve takes the
same 409 path rather than a 500, because a named absence is not a failure; and
the `rejected[{id, reason}]` wire form really reaches the recorder with its
reason VERBATIM. Follow the file's existing idiom for standing the server up and
posting a command; do not invent a second one.

## The slices

<<<SLICE PLANF033R15
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 4 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | done | round 12 |
| one evidence-directory resolver for viewer and doors | done | round 13 |
| the CLI command and its handler | done | round 14 |
| R-0744, the CLI door's job-id resolution | open | this round |
| the write door's exposure and dispatch | open | this round |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. R-0744: the CLI handler resolves the evidence directory from the RESOLVED job
   id, so a short prefix or an uppercase UUID stops being reported as a missing
   diff. The eleven existing tests are blind to it, so the fix ships with tests
   that discriminate.
2. The write door, in ONE commit with its guards. `UI_EXPOSED_COMMANDS` gains the
   id; `DOOR_METHODS`, `ALLOWED_IMPORTS` and `FORBIDDEN_MODULES` in
   `tests/ui_server/test_command_channel.py` are EQUALITY guards that must widen
   with it, and `packages.orchestration.hunk_apply` joins the forbidden set so
   DECISION F033 D4's mistake cannot be made silently later.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report line derived from the ledger, and partial state rendered truthfully in
   viewer, node and report. R-0738 is T003's to repair.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has been allowed a `docs/` path yet.

## Risks
- The door's import guard is an EQUALITY guard: a new import reddens the branch
  tip unless it is ruled in the same commit.
<<<END PLANF033R15

<<<SLICE RECORDF033R15
Gate: F033 R14 — THE CLI COMMAND AND ITS HANDLER. THE ROUND PASSED WITH RISKS. Every gate was re-executed by the reviewer at `fa963c4e` from scripts of its own, and every ordered reading reproduced; the risk is R-0744 below, which is a REAL defect in the shipped handler and is registered rather than waived. TRANSPORT: the C0a blob is 33129 bytes at sha256 `9c373cd2…c322ca`, EQUAL to the reviewer's own scratchpad original, with ONE blob id across `.agent/authored/f033-r14.md` and `.agent/last_block.md` at C0b. THE RECORD APPEND at `096b8539` reconstructs 1517848 plus one newline plus 7219 to 1525068, the committed blob exactly, base a byte PREFIX, N COUNTED at 2, the last two blank-line units equal to the slice's paragraphs IN ORDER, and a negative control at byte 1520431 — proved to lie inside the FIRST appended paragraph, whose span the reviewer computed independently as 1517849 to 1523013 — rejected by BOTH readers. THE LEDGER walked at three commits: registered 303 to 304 with the ADDED id exactly `R-0743`; `Done:` 48 lines over 46 distinct UNMOVED throughout, correctly, because only the reviewer resolves; `Landed:` 15 at BASE and at C2 and 16 at C5, the added line matching `^Landed: R-0743 — ` exactly once and appearing at C5 rather than C2, which is where the fix landed; `Gate:` 130 to 131 with `^Gate: F033 R13 — ` exactly 1; `DECISION F033 D` 4 UNMOVED; and the open set 257 to 258. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to its slice at 2479 bytes over 46 lines, under the 50-line cap; `.agent/prose_slips.md` reconstructs 23793 plus one newline plus 472 to 24266, with the round 13 slip line going 0 to 1 and `- R-` lines 0. THE CATALOG: `ruff` exits 0; the entry reads `patch`, `approve-hunks`, `approval_gate`, `supports_json` True, and `may_mutate_repo` and `requires_permission` BOTH False, which is DECISION F033 D4 stated in the one table the UI reads capability from; its args are `job_id`, `--task-run`, `--approve-hunk`, `--reject-hunk` and `--json`, with the two hunk options repeatable; the `patch` group goes 6 to 7 with the equality guard widened in the SAME commit; `CATALOG` and `collect_all_handlers()` go 340 and 340 to 341 and 341 with ZERO handler-less ids at both ends; and `sorted(UI_EXPOSED_COMMANDS)` is still exactly `decision.resolve` and `job.stop`, so the write door was NOT opened this round. R-0743 IS RESOLVED BY COLOUR CHANGE, not by reading the test: the reviewer re-ran the precedence mutation in its own disposable worktree with its own anchor, and where it came back GREEN at 32 passed when the finding was raised, it comes back RED at exit 1 and 1 failed at `eec2cd4a`, naming exactly `test_the_index_record_beats_the_cwd_relative_fallback`. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, every REAL exit 0: `test_patch_cmd.py` 11, `test_evidence_index.py` 33, `test_command_catalog.py` 18, `cli/test_command_catalog.py` 23, `test_command_channel.py` 106, `test_grouped_cli.py` 511 — UNMOVED, as predicted from its parametrizing over GROUPS rather than commands — and the canary 42. THE STRUCTURE: seven single-parent commits over the range ending at C5, of 449, 302, 16, 4, 2, 152 and 308 insertions, every one under 500; the path set EQUALS the declared change set in BOTH directions; `git ls-files .remedy-wt` 0; and ALL TWELVE do-not-touch paths byte-identical by blob id, including `packages/orchestration/evidence_index.py`, so the claim that R-0743's repair is a TEST and touches no production code is a measurement. THE WORKER DECLARED FIVE DEVIATIONS AND EVERY ONE IS HONEST; D3 is the one that became a finding, and declaring it rather than fixing past the SPEC is exactly the required behaviour.

Done: R-0743 — RESOLVED at `eec2cd4a`, verified by the reviewer re-running the mutation the finding's FIX clause asked for rather than by reading the assertion. `tests/orchestration/test_evidence_index.py` gains ONE test, `test_the_index_record_beats_the_cwd_relative_fallback`, taking the file from 32 to 33 with no existing test moved, and it is the first case in that suite to construct BOTH sources at once — an index record naming an existing directory AND a real `remedy-job-evidence-<job_id>` directory in the CWD — which is the only state in which precedence is observable at all. THE PROOF IS THE COLOUR CHANGE: moving the relative-fallback branch above the `try` in `packages/orchestration/evidence_index.py`, inside the reviewer's own disposable worktree and with the anchor asserted unique, came back GREEN at 32 passed when the finding was raised and comes back RED at exit 1 and 1 failed, naming exactly that test, at `eec2cd4a`. `packages/orchestration/evidence_index.py` is byte-identical at the round 14 base and at that commit, so the repair really is a test and the behaviour on disk was already correct, which is what the finding claimed. This resolution reaches the precedence rule of this ONE function; the R-0671 class it belongs to — an honesty rule a module states and no test pins — is not discharged by it anywhere else in the repository.

- R-0744 — Medium, THE CLI DOOR RESOLVES THE EVIDENCE DIRECTORY FROM THE OPERATOR'S RAW ARGUMENT, SO A SHORT JOB-ID PREFIX IS REPORTED AS A MISSING DIFF. Raised by the reviewer at the F033 R14 gate, from the worker's own declared deviation D3, and promoted to a finding rather than a prose slip because the defect is on disk under `apps/` and an operator meets it. `_cmd_approve_hunks` in `apps/cli/commands/patch.py` at `fa963c4e` resolves `job_id = resolve_job_id(job_id_str)` and then calls `evidence_index.resolve_job_evidence_dir(job_id_str)` — the RAW argument — while the index is keyed by the canonical full id. MEASURED end to end through the shipped handler, on one job with one evidence directory and one index record, driven twice: with the full lowercase UUID it exits 0 and records; with the short hex prefix that `resolve_job_id` resolves to THAT SAME JOB it exits 1, records nothing, and prints `no_diff_available` — "The attempt's diff is not available to decide over" — for a diff that is present in the directory the index names. An UPPERCASE full UUID, likewise accepted by `resolve_job_id`, fails identically. The prefix form is not exotic: `resolve_job_id` exists to support it and every other handler in this file takes it. This is the misreport `HUNK_RECORD_REFUSAL_NO_DIFF` was minted to prevent, arriving through the id rather than through the artifact — a fault in what the operator asked for coming back as a fault in what the system could show. It is Medium and not High because the command REFUSES rather than recording under a wrong key, so no bad state reaches the job and the failure is loud. THE SUITE IS BLIND TO IT: the reviewer applied the fix inside a disposable worktree at `eec2cd4a` and all eleven tests in `tests/cli/test_patch_cmd.py` stayed GREEN at exit 0, so no existing test discriminates the two forms. FIX: call `resolve_job_evidence_dir(str(job_id))` with the RESOLVED `UUID`, which normalises both the prefix and the case at once, and ship tests naming a job by short prefix and by uppercase UUID that assert the decision was RECORDED, not merely that the exit code was 0. The reviewer's SPEC for round 14 named the raw argument, so the worker applying it literally and declaring the consequence was correct; the error is the reviewer's and the repair is this finding.
<<<END RECORDF033R15

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C5, so the handback at C6 can quote all of them; C6's own numbers are NOT
ordered here.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C6,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r15.md` and of `.remedy-wt/f033-r15-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r15.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1526301 bytes, plus one newline plus RECORDF033R15 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R15 — report
  it — and compare the LAST N blank-line units of the C2 blob against the
  slice's paragraphs IN ORDER. NEGATIVE CONTROL at a BYTE offset your script
  PROVES lies inside the FIRST appended paragraph, whose span you compute in
  BYTES per convention 10 and report; BOTH readers must reject it.
- **G4 THE LEDGER at C2 and at C3.** At BASE, at C2 and at C3 count
  `^- R-\d+ — ` with distinct ids, `^Done: R-\d+ — ` lines with distinct ids,
  `^Landed: R-`, `^Gate: F\d+ R\d+ — ` and `^DECISION F033 D\d+ — `; report the
  open set at all three. Ordered: registered 304 to 305 at C2 with the ADDED id
  exactly `R-0744`; `Done:` 48 lines over 46 distinct to 49 over 47 with the
  ADDED resolved id exactly `R-0743`, and the `Landed: R-0743` line STILL
  PRESENT beside its new `Done:` paragraph, as this append-only record requires;
  `Landed:` 16 at BASE and C2 and 17 at C3, the added line matching
  `^Landed: R-0744 — `; `Gate:` 131 to 132 with `^Gate: F033 R14 — ` exactly 1;
  `DECISION F033 D` 4 UNMOVED — this round mints no new DECISION; and the open
  set 258 at BASE and 258 at C2, unchanged because one id is added and one is
  resolved. Report that equality explicitly rather than inferring it.
- **G5 THE PLAN.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R15 — report
  its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets.
- **G6 THE DOOR'S GUARDS at C4.** (a) `ruff check` over
  `packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
  `apps/cli/commands/patch.py` and the three touched test files exits 0 — report
  the summary line. (b) Report `sorted(UI_EXPOSED_COMMANDS)` at BASE and at C4;
  it must gain exactly `patch.approve-hunks` and nothing else, and every member
  must resolve through `get_command`. (c) Report `DOOR_METHODS` at BASE and at
  C4, and prove `_dispatch_approve_hunks` is a real method of `_RemedyHandler` at
  C4 by AST — a name in that tuple that no method answers to makes the guard scan
  nothing. (d) Run `_door_imports` YOURSELF over the C4 source with the C4
  `DOOR_METHODS` and report the FULL set it collects, the set difference against
  `ALLOWED_IMPORTS` in BOTH directions — which must be empty both ways — and the
  intersection with `FORBIDDEN_MODULES`, which must be empty. (e) Report
  `FORBIDDEN_MODULES` at BASE and at C4; it must gain exactly
  `packages.orchestration.hunk_apply`. (f) Report the module-level command-id
  constants and their values.
- **G7 THE MUTATION RED-PROOFS at C5.** In a DISPOSABLE `git worktree` at C5,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy. FIRST the UNMUTATED CONTROLS — REAL
  exit 0 with counts — over `tests/cli/test_patch_cmd.py` (11 at BASE),
  `tests/ui_server/test_command_dispatch.py` (7 at BASE) and
  `tests/ui_server/test_command_channel.py` (106 at BASE). Then, one at a time,
  reverting fully between each, asserting the anchor is UNIQUE inside the named
  FILE before replacing it, and reporting the REAL exit code, the failure count
  and the NAME of each failing test:
  (i) in `apps/cli/commands/patch.py`, revert the R-0744 fix to `job_id_str` —
      this is R-0744's proof and it MUST go red, where at `fa963c4e` it was green;
  (ii) in `packages/orchestration/ui_server.py`, drop `save_job` from
      `_dispatch_approve_hunks`, so the effect is not persisted;
  (iii) in `packages/orchestration/ui_server.py`, return the accepted body
      instead of None when the recorder refuses;
  (iv) in `apps/cli/command_catalog.py`, remove `patch.approve-hunks` from
      `UI_EXPOSED_COMMANDS`.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/cli/test_patch_cmd.py` (11 at BASE),
  `tests/ui_server/test_command_dispatch.py` (7 at BASE),
  `tests/ui_server/test_command_channel.py` (106 at BASE),
  `tests/test_command_catalog.py` (18 at BASE),
  `tests/orchestration/test_evidence_index.py` (33 at BASE),
  `tests/orchestration/test_hunk_decision_record.py` (15 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C5`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. Report the range's path set against
  the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `apps/cli/commands/patch.py`,
  `packages/orchestration/ui_server.py` and `apps/cli/command_catalog.py`: each
  0, against `.agent/authored/f033-r15.md` as a non-zero control whose count you
  report. `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C5, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 4,
round 15, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Write external actions as command plus outcome. Quote
`_dispatch_approve_hunks`'s final signature, the accepted body's key set, the
full `_door_imports` set from G6(d), and the test names you wrote with the
property each pins.

Carry SESSION 4 forward and name the next session's first actions in this order:
read `.agent/STOP` from disk, then run the Open PR Gate, then book this round's
verdict and resolve R-0744, then the plan's step 3. No length cap. Write no
verdict on your own work.
