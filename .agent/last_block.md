STEP F110 REPAIR / ROUND 11 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 3, ROUND 11

Goal
  THE REPAIR ROUND. Round 10's verdict is FAIL: its production work is correct
  and stays, but the branch tip ships a RED suite and a committed test file
  fails ruff. Register both, fix both, and get the tip green. This round adds NO
  feature behaviour - the promotion-evidence configuration work is the NEXT
  round and is deliberately not bundled here, so the red tip is cleared by a
  change set a reader can check in one sitting.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r11.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN11 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  FINDINGS PERSIST FIRST, own commit: append RECORD10, FINDING787 and
      FINDING788 to .agent/live_review.md and SLIPS11 to .agent/prose_slips.md
  C3  FIX R-0787: the config stub and the discriminator that replaces it
  C4  FIX R-0788: the import block
  C5  append LANDED787 and LANDED788 to .agent/live_review.md
  C6  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r11.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - .agent/live_review.md (C2 and C5) -
  .agent/prose_slips.md (C2) -
  tests/orchestration/test_orchestrator_model_routing.py (C3) -
  tests/orchestration/test_config.py (C4) - .agent/handoff.md (C6)
  NO FILE UNDER packages/ OR apps/ IS EDITED THIS ROUND. Round 10's production
  code is CORRECT and stays exactly as it is; both defects are in test files.

BASE for this round is 0d025469. Every byte, count, citation and measurement
below was taken there by the reviewer.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r11.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round registers findings, so item
     23 binds. C2 is the FIRST commit that touches the ledger, before any fix -
     docs/agents/planner_reviewer_prompt.md §4 item 4.
  3. C3 precedes C4 precedes C5. Do not reorder.
  4. Newline conventions, MEASURED at 0d025469 - re-measured at THIS round's
     base, never carried forward. .agent/live_review.md is 2196008 bytes and
     ends WITHOUT a trailing newline; each append is the two bytes newline
     newline then the slice, and the file must still end without one AFTER BOTH
     appends. .agent/prose_slips.md is 58680 bytes, same shape, same two-byte
     append. .agent/plan.md is 2011 bytes and ends WITH one. Where an extractor
     yields a trailing newline the target does not take, the TARGET wins.
     .agent/decisions.md IS NOT TOUCHED this round.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
     THIS IS NOT A CONTRADICTION WITH R-0788: you fix the import ORDER the
     finding states, and the reviewer confirms it with ruff at the gate.
  6. THE WORKER NEVER WRITES A `Done:` PARAGRAPH. C5 appends `Landed:` lines
     only. `Done:` is reserved for reviewer-authored text and is written at the
     NEXT gate - docs/agents/planner_reviewer_prompt.md §4 item 4. A
     worker-authored `Done:` is itself a finding, however honestly hedged.
  7. ROUND 10'S PRODUCTION BEHAVIOUR IS NOT REVISED. Do not "fix" the stub by
     changing what role_config or config reads. The production code asks for
     `model_routing.task_class_tiers` because SPEC (e) and (g) of round 10
     require it, the reviewer verified that behaviour is correct at 0d025469,
     and the defect is that a TEST DOUBLE refuses a legitimate reader.
  8. Read .agent/STOP from disk before the first commit and again before C6.
  9. Destructive verification runs ONLY inside a disposable git worktree, never
     in the primary checkout. Purge __pycache__ before every run, use python3
     -B, remove the worktree BY ITS EXACT PATH when done, and prune.

SPEC - C3, tests/orchestration/test_orchestrator_model_routing.py
  This is a SPEC, not a slice: write it in this file's own idiom. The reviewer
  applied this exact change in a disposable worktree at 0d025469 and measured
  the suite at 20 passed, exit 0, up from 19 at the round 9 base and from
  1 failed / 18 passed at 0d025469.

  (a) THE KEY BECOMES A NAMED CONSTANT. Add a module-level constant holding
      "orchestrator.model" and use it in the stub, so the one key the operator
      override lives at is spelled once.
  (b) THE STUB ANSWERS OTHER KEYS INSTEAD OF REFUSING THEM. `_FakeConfig.get`
      returns the configured value for that key and None for every other key,
      and RECORDS every key it was asked for on the instance. None is the right
      answer for the F110 routing table: it means "no per-project overrides",
      which is exactly the state these tests intend.
  (c) THE PROOF THE REFUSAL CARRIED IS KEPT, AS A POSITIVE TEST. The assertion
      that is removed proved WHICH key was read, by refusing every other one.
      Replace it with a test that reads the recorded keys and asserts the
      operator-override key is among them. `_patch_config` must therefore build
      ONE instance and RETURN it, rather than constructing a fresh one per call
      inside the lambda, or nothing can inspect what was asked.
  (d) THE DOCSTRING SAYS WHY, not just what: the stub refused every other key,
      and that stopped being right when the fall-through path gained a SECOND
      legitimate reader. A reader who wonders why a test double is permissive
      must find that sentence here.
  (e) NO OTHER TEST IN THIS FILE IS EDITED, and none is renamed, deleted or
      skipped. The count must RISE by the one test (c) adds and by nothing else.
      THE REVIEWER MEASURED WHY ONLY ONE TEST WAS RED: the other fall-through
      cases also patch `resolve_role_config` itself, so they never reach the
      real one, and `test_the_fall_through_answer_is_a_non_empty_string` is the
      only case that does.

SPEC - C4, tests/orchestration/test_config.py
  (f) THE IMPORT BLOCK IS SORTED as ruff's isort orders it. Measured at
      0d025469 with `ruff check --fix`, the ONLY change is that
      `_TABLE_VALUED_KEYS` moves to the TOP of the
      `from packages.orchestration.config import (...)` list, above
      `ConfigKeySpec`. Nothing else in the file changes, no import is added and
      none is removed. Apply that one move.

Done when - SEVEN GATES, each run and its real exit code recorded
  G1 TRANSPORT. sha256sum .agent/authored/f110-r11.md .agent/last_block.md -
     ONE digest twice. Report wc -l of the authored file. Per
     docs/agents/planner_reviewer_prompt.md item 37 this proves the saved copy
     and its mirror agree and claims nothing about the emitted bytes.
  G2 THE PLAN. cmp the PLAN11 extraction against .agent/plan.md - exit 0.
     Report wc -l (must be under 50) and grep -c for '^## Goal' and
     '^## Next Steps' (1 each).
  G3 THE C2 LEDGER APPEND, full forensics. RECORD10, FINDING787 and FINDING788
     are ONE append in ONE commit, joined in that order by the file's own
     paragraph separator. State the arithmetic 2196008 + 2 + len(the joined
     text) against the real size after C2; show the pre-C2 content is an exact
     byte PREFIX; show the file still ends WITHOUT a newline. SECOND READER: a
     script COUNTS N from the appended text, then compares the LAST N
     blank-line units of the whole file against its N paragraphs IN ORDER.
     NEGATIVE CONTROL: flip one byte inside the FIRST appended paragraph and
     show the second reader REJECTS it. Report the count of lines matching the
     RECORD10 header EXACTLY AS THE SLICE SPELLS IT - the separator after "R10"
     is U+2014 EM DASH, not a hyphen; copy the string from the extracted slice
     rather than retyping it - before C2 (expect 0) and after C2 (expect 1).
  G4 THE C5 LEDGER APPEND AND .agent/prose_slips.md. For C5: the same byte
     arithmetic against the size after C2, the C2 content an exact PREFIX, and
     the file STILL ending without a newline - this is the second append to one
     file in one round, so state both sizes and show the second builds on the
     first. For .agent/prose_slips.md a BYTE-EQUALITY check only, per the gate
     budget: final bytes == 58680 + 2 newlines + SLIPS11, base an exact prefix.
     Report grep -c '^Landed: R-0787 — ' and '^Landed: R-0788 — ' after C5
     (1 each) and confirm grep -c '^Done: R-0787' and '^Done: R-0788' are BOTH
     0 - constraint 6 measured rather than asserted.
  G5 THE FIX, MEASURED AND RUN. git show --numstat for C3 and C4, per path.
     ast.parse over both real files. QUOTE EVERY DELETED LINE VERBATIM and name
     its region. Then run the previously-red suite:
       python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
     Report its exit code and count AT C4 - it must be exit 0. Report the same
     command's reading at the BASE 0d025469, taken in a disposable worktree, so
     the repair is shown against the failure it repairs; the reviewer measured
     1 failed, 18 passed there. Also print the keys the stub RECORDED during one
     fall-through call, so the new discriminator is shown working rather than
     asserted.
  G6 THE RED PROOF for the discriminator (c) adds, in a disposable worktree at
     C4, never cd-ed into, __pycache__ purged, python3 -B, module __file__
     printed from inside it. Control first, with its count and exit code. Then
     ONE mutation: make resolve_orchestrator_model stop reading the operator
     override key - replace the get_config().get(...) call's result with None -
     and report the exit code, the failure count and the FULL LIST of red test
     ids. PRINT ONE RAW pytest "FAILED ..." line beside your parsed set and
     confirm they agree; the node id is the SECOND whitespace-separated token,
     and both the worker and the reviewer mis-parsed this in round 9. The new
     discriminator MUST be among the red ids - if it is not, the test proves
     nothing and that is a STOP. Read git status --porcelain ON THE PRIMARY
     CHECKOUT immediately after the mutation. Revert with
     git checkout -- <exact path> INSIDE the worktree and return to the
     control's count.
  G7 THE SUITES, each its own invocation, run serially, all exit 0. The counts
     in brackets are what the reviewer measured at 0d025469; report yours beside
     them and explain any difference. Only the first two may move.
       pytest tests/orchestration/test_orchestrator_model_routing.py -q
         (1 failed / 18 passed at base - MUST become exit 0, and report the
          number YOU measure rather than targeting one this block names)
       pytest tests/orchestration/test_config.py -q                  (74)
       pytest tests/orchestration/test_role_config.py -q             (92)
       pytest tests/orchestration/test_model_routing.py -q           (391 passed,
         3 skipped)
       pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q   (68)
       pytest tests/docs/ -q                                         (295)
       pytest tests/cli/test_golden_path.py -q                       (42 - canary)
  G8 THE TREE, THE COMMITS AND THE SWEEP. git status --porcelain empty
     immediately before C6 is staged. git ls-files .remedy-wt returns nothing.
     No worktree of this round's making survives. Report
     git diff --stat 0d025469..<C5> -- packages/ apps/ docs/ - it MUST BE
     EMPTY, which is the change-set constraint MEASURED rather than asserted.
     Report the per-commit INSERTION count, the + column only, for every commit
     BEFORE the handback commit, cell by cell against the handback's own
     ## Commits table, and confirm each is under the AGENTS.md 500-insertion
     cap. The handback commit's own numbers go in neither place.

Handback - rewrite .agent/handoff.md per docs/agents/handback_template.md
  It carries: SESSION 3 of F110, round 11, rounds so far 11; the state block
  with the Fortschritt line; the item-status table with every SPEC item, both
  findings and every gate exactly once; the per-commit changed-files tables; one
  line per gate with its real result; the authored-text proofs; the deviations;
  the next step. NO length cap applies (AGENTS.md amend0827 rule 3). Report the
  two STOP readings. State the OPEN FINDING COUNT after this round's two
  registrations, derived mechanically from .agent/live_review.md - every
  '^- R-\d+ — ' paragraph minus every '^Done: R-\d+ — ' line - and note that
  both new ids stay OPEN because only reviewer-authored text resolves them.

<<<BEGIN PLAN11>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 11, session 3 — THE REPAIR ROUND. Round 10 was gated FAIL: its
production work is correct and stays, but the branch tip ships a red suite
and a committed test file fails ruff. `R-0787` (High) is a config test
double that asserted an exact key and so refused the second, legitimate
reader the F110 wiring added; `R-0788` (Low) is an unsorted import block.
Both are registered, then fixed, and no file under `packages/` or `apps/`
is touched.

## Next Steps

- The promotion-evidence round: the evidence map is read from configuration
  too, so a documented benchmark run can license a cheaper tier — the last
  unbuilt clause of T003.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- A test double that is too permissive stops proving anything, so the
  refusal `R-0787` removes is replaced by a positive test that reads the
  keys the stub recorded, and that test is red-proofed.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN11>>>

<<<BEGIN RECORD10>>>
Gate: F110 R10 — the round 10 entry. VERDICT FAIL, over the range `a1368633..e1da68d8` plus the handback commit `0d025469`. `LAST_REVIEWED_SHA` does NOT advance and stays `a1368633`. THE FAILURE IS NARROW AND THE ROUND'S PRODUCTION WORK IS CORRECT: two defects, both in TEST files, registered this round as `R-0787` (High — the branch tip ships a red suite) and `R-0788` (Low — a committed test file fails `ruff I001`). Nothing under `packages/` is wrong and nothing there is reverted. THE TRANSPORT PROOF REACHED THE REVIEWER'S OWN BYTES: the worker copied the block with `shutil.copyfile` from the reviewer's scratch original, so `cmp` between that original and the committed `.agent/authored/f110-r10.md` exits 0, and one digest `9af2d6cef398ae7fe766cf0a23ee1c4d9901b190c67508620740ec229bed1dae` at 32214 bytes covers the original, the saved copy at `9eb79b10` and the mirror at `b9d32e3d`. The block is 395 lines against the reviewer's own projection of 395, under the §3 item 1 cap of 400. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE and every size matched the pre-emission projection exactly: `.agent/plan.md` equals PLAN10 plus the one trailing newline the target's convention adds, at 44 lines; `.agent/live_review.md` is 2190200 + 2 + 5806 = 2196008; `.agent/prose_slips.md` is 58680; `.agent/decisions.md` is 738004 = 734845 + 1 + 3157 + 1. THE CONFIGURED BEHAVIOUR WAS RUN BY THE REVIEWER, NOT READ, and it is exactly what DECISION F110 D5 rules: with nothing configured the effective table IS the shipped table and `teacher` routes `summarize` at `cheap` with `seed_mapping`; with a LEGAL override re-tiering `summarize` to `mid` the same call routes `mid` with `per_project_override` and no warning; with an ILLEGAL override demoting `mission` to `cheap` the `orchestrator` call still routes `top` with `seed_mapping`, one `UserWarning` names the config key and both violated rules — `orchestration_below_top_tier` and `promotion_without_evidence` — and `provider`, `model` and `effort` come back unchanged, so a refused table does not become a config-resolution fault; and a MALFORMED value that is a bare string is reported by `validate_config` as "expected table, got str" while routing falls back to the shipped table. DEVIATION D2 IS CORRECT AND LOAD-BEARING, not scope creep: the non-`Mapping` guard the block did not order is exactly what keeps that last case from raising inside `resolve_role_config`. THE TABLE-VALUED KEY MECHANISM IS SOUND: `_TABLE_VALUED_KEYS` is derived from the registry by `value_type is dict` rather than hand-listed, so a second table key needs no second edit, and a configured table produces ZERO "Unknown key" diagnostics where the unmodified flattener would have produced one per entry. C5 is 368 insertions against ZERO deletions and C6 is 27 against zero, so constraint 8 is MEASURED: no existing test was edited. `git diff --stat a1368633..e1da68d8` over `packages/` and `apps/` with the two edited files excluded is EMPTY, and over `docs/` lists exactly the one documentation file. The per-commit insertion counts match the handback's Commits table cell by cell — 395, 315, 15, 63, 85, 85, 368, 27 — every one under the AGENTS.md cap; `0d025469` is 586 insertions against 395 deletions, a full-file rewrite of a single `.agent/**` state file and exempt under DECISION F104 D1. WHAT THE ROUND'S OWN GATES CAUGHT AND WHAT THEY DID NOT: G7 named `test_orchestrator_model_routing.py` in its unmoved group, so the block's own gate list DID catch `R-0787`, and the worker correctly refused to edit the test or bend production to the stub and reported it as a blocked item — that is the round behaving exactly as it should once the defect existed. `R-0788` no gate could catch, because constraint 5 forbids the worker to run ruff and reserves linting to the reviewer, which is where it was found. The worker's deviations D1 through D5 are all accepted; D3 declares that its own second reader failed on its first run and reports the wrong first reading rather than replacing it, which is round 9's SLIPS10 lesson applied one round later by the party that had just been told it. The tree is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's making survives, `.agent/candidates.md` is untouched and still EMPTY, `R-0767` stays OPEN, and the branch is pushed at `0d025469` with no pull request open.
<<<END RECORD10>>>

<<<BEGIN FINDING787>>>
- R-0787 — High, THE BRANCH TIP SHIPS A RED SUITE: A CONFIG TEST DOUBLE ASSERTED AN EXACT KEY AND SO REFUSED THE SECOND, LEGITIMATE READER THE F110 WIRING ADDED. Registered by the reviewer at the F110 R11 gate, against the reviewer's own round 10 block. MEASURED independently at `0d025469`: `python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q` reads exit 1 at 1 failed, 18 passed, and the same command in a disposable worktree at the round 10 base `a1368633` reads exit 0 at 19 passed — so the round introduced it. THE MECHANISM: `_FakeConfig.get` in that file carries `assert key == "orchestrator.model", f"unexpected config key {key!r}"`, a refusal that PROVED which key `resolve_orchestrator_model` read. Round 10's C4 made `resolve_role_config` read a SECOND key, `model_routing.task_class_tiers`, on the fall-through path, and `resolve_orchestrator_model` falls through to `resolve_role_config("orchestrator")` when the operator override is unset — so the stub refuses a reader that is entirely correct. EXACTLY ONE TEST IS RED and the reason is worth recording: every other fall-through case also patches `resolve_role_config` itself, so only `TestTheAnswerIsAlwaysUsable::test_the_fall_through_answer_is_a_non_empty_string` reaches the real function. THIS IS THE R-0697 CLASS — a guard the block never named, turning the branch tip red — arriving through a TEST DOUBLE rather than through an equality guard, and the reviewer's checklist item 34 sweep missed it because that sweep reads the tests that IMPORT or COUNT over an edited file and this file does neither: it stubs a DEPENDENCY of a function in an edited file. FIX: keep the proof and drop the refusal. `_FakeConfig.get` answers the configured value for the operator-override key, answers None for every other key — None being the correct "no per-project overrides" answer for the routing table — and RECORDS the keys it was asked for, and a new test asserts the operator-override key is among them. `_patch_config` returns the one instance it builds so the recording can be read. Production code is NOT changed: it asks for that key because round 10's SPEC requires it, and the reviewer verified that behaviour is correct at `0d025469`.
<<<END FINDING787>>>

<<<BEGIN FINDING788>>>
- R-0788 — Low, A COMMITTED TEST FILE'S IMPORT BLOCK FAILS `ruff I001`. Registered by the reviewer at the F110 R11 gate, against the reviewer's own round 10 block. MEASURED at `0d025469`: `python3 -m ruff check tests/orchestration/test_config.py` reports `I001 Import block is un-sorted or un-formatted` and nothing else, and `ruff check --fix` produces exactly one change — `_TABLE_VALUED_KEYS` moves to the TOP of the `from packages.orchestration.config import (...)` list, above `ConfigKeySpec`, because ruff's isort orders that name before the CamelCase ones. NO GATE COULD HAVE CAUGHT THIS ON THE WORKER'S SIDE: the round 10 block's constraint 5 forbids the worker to run ruff and reserves linting to the reviewer, which is where it was found; this is the arrangement working, not failing. Severity is Low and stated as measured: `.github/workflows/ci.yml` contains no ruff invocation, so nothing in continuous integration goes red for it, and the cost is confined to `scripts/remedy_lint.sh` and to any reader who lints the file. FIX: apply that one move and nothing else — no import is added, none is removed, and no other line of the file changes.
<<<END FINDING788>>>

<<<BEGIN SLIPS11>>>
2026-09-03 · F110 R10 · The reviewer's checklist item 34 sweep for the round 10 block read the guards on every test file that IMPORTS or COUNTS over the two edited production files, and missed `tests/orchestration/test_orchestrator_model_routing.py`, which does neither — it patches `packages.orchestration.config.get_config` with a stub that REFUSES any key but `orchestrator.model`, and so broke when `resolve_role_config` gained a second, legitimate config read. The reviewer's own DECISION D4 measurement had even listed `role_config.py`'s `resolve_orchestrator_model` among the call sites, so the file was one hop from being read. Registered as `R-0787` because the branch tip went red; recorded here as the AUTHORING lesson the id does not carry. THE LESSON: item 34's "read the tests that already guard that file" extends to tests that STUB A DEPENDENCY of an edited function — a monkeypatched double is a guard on the call path even though it names neither the edited file nor its symbols, and `rg -l '<basename>' tests/` cannot find it. Search for the patched TARGET (`get_config`, `resolve_role_config`) as well as for the edited file's own name. Reviewer block-authoring slip; no second R-id spent for the lesson (amend0827-process-diet rule 2).
<<<END SLIPS11>>>

<<<BEGIN LANDED787>>>
Landed: R-0787 — the config test double now answers None for keys other than the operator override and records every key it was asked for, and a new test asserts the override key is among them; `tests/orchestration/test_orchestrator_model_routing.py`, commit C3 of F110 R11.
<<<END LANDED787>>>

<<<BEGIN LANDED788>>>
Landed: R-0788 — `_TABLE_VALUED_KEYS` moved to the top of the config import list, the single change `ruff check --fix` produces; `tests/orchestration/test_config.py`, commit C4 of F110 R11.
<<<END LANDED788>>>
