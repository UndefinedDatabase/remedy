── STEP R9/15 — F083 CI self-check — RECORD R8 FAIL, REPAIR THE RUFF RED, PROMOTE CHECKLIST ITEM 11 ──

Goal:
  Clear the one RED gate R8 ended on and pay the debt R-0461 booked. The ruff
  failure is a defect in MY authored slice, not in the worker's conduct: one blank
  line where the repo's `I` rules want two. Fix it, record the R8 FAIL with its two
  findings, and perform the §3 promotion R-0460 asserted and R-0461 assigned to
  this round — so the claim stops being false on disk.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r9.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — RECORD-R8 appended at EOF, ONE commit, one body:
       gate line, blank line, the two findings.
  C2   `.agent/live_review.md` — the STEPS pair, ONE commit. This round became a
       repair round, so the map shifts by one and closure moves to R15.
  C3   `apps/cli/commands/ci_cmd.py` — the BLANK pair, ONE commit.
  C4   `docs/agents/planner_reviewer_prompt.md` — OPENER and ITEM11, ONE commit.
  C5   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C6   `.agent/handoff.md`, the handback, alone.

BASE: 4406f1c1. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 4406f1c1. If it does NOT, stop and hand off.

TRANSPORT: the scratchpad original of THIS block is at
`.remedy-wt/.cache/f083-r9/f083-r9.md`, which `.gitignore` drops. C0a is a byte
COPY of it — do not retype, reflow or strip anything. `cp` is denied in this
session class: copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`.

SLICE CONVENTION (R-0437, and now §3 item 11 which C4 lands): every slice body
below is the lines between its markers INCLUDING the trailing newline of its last
line, and every shape is declared UNDER THAT CONVENTION. The authored units are,
listed and NOT counted: RECORD-R8, STEPS, BLANK, OPENER, ITEM11, PLAN.

PAIR SHAPES, stated at authoring time (§4.9) and verified on these bytes:
  · STEPS, BLANK and OPENER are REWRITEs — FROM and TO are disjoint — each proved
    by FROM 0x and TO 1x over the whole file.
  · ITEM11 is APPEND-shaped: its TO literally CONTAINS its FROM as the LAST line,
    so "FROM 0x" is UNSATISFIABLE and is NOT ordered. Its property is FROM 1x
    before AND after, TO 0x before and 1x after.
  · PLAN is a WHOLE FILE, proved by byte equality.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r9.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
     `apps/cli/commands/ci_cmd.py`, `docs/agents/planner_reviewer_prompt.md`.
     Nothing else. `packages/`, `tests/` and `docs/roadmap/` stay EMPTY in the
     range diff — no test changes this round, so `tests/docs/` is not a gate.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. Do NOT run `ruff --fix`: the repair
     is the BLANK slice, applied as text, so the diff shows the intended change
     and nothing a formatter chose on its own.
  3. Commit strictly in the C-order above. Push after C6. Create NO pull request.
     This round adds NO worktree; `git worktree list` is one line throughout.
  4. Env-var assignment (all three forms), `cp`, `$?` inside `$(...)` and process
     substitution are denied in this session class. Capture real exit codes as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and use `python3` scripts written to
     `.remedy-wt/.cache/f083-r9/` for all counting, hashing and byte comparison.

--- BEGIN SLICE RECORD-R8 --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice. The blank line INSIDE this slice, between the gate line and the first finding, is part of it.)
Gate: R8 — FAIL, on ONE red gate out of seventeen, with every other gate green and re-run by the reviewer at the round's head. The red is gate 8, ruff, and it is the REVIEWER's defect in the authored CI-CMD slice rather than any act of the worker's: `python3 -m ruff check` over the four files gives `I001 Import block is un-sorted or un-formatted` at `apps/cli/commands/ci_cmd.py:15`, exit 1, because one blank line separates the import block from `def repo_root_for_ci` where `pyproject.toml`'s `select = ["E", "F", "W", "I", "UP"]` requires two. The worker isolated it correctly — the same command over the other three files alone exits 0, so the failure is the new slice's own bytes — applied the slice byte-verbatim as constraint 2 demands, declined to repair it, declared it, and ended the round under G8. That is exactly the conduct this repository asks for, and the round is charged to the reviewer. Everything else the round produced is sound and was re-derived independently: TRANSPORT three-way byte-equal at sha256 3b7d8cfb756bc950df49c605cdc99dc36971d9ea568ace4b9e70601afd129713, 29275 bytes, 400 lines, equal to the block's declared footer; C1's prefix property holds with the tail byte-equal to `b"\n" + RECORD-R7`; `apps/cli/commands/ci_cmd.py`, `tests/cli/test_ci_cmd.py` and `.agent/plan.md` each byte-equal their slices as whole files; both catalog pairs landed append-shaped with `"ci": GroupDef`, `command_id="ci.run"` and `command_id="integrity.check"` each exactly 1, and `ci_cmd` and `bench_cmd` each exactly 2 in `__init__.py`. The seam WORKS rather than merely parses: `tests/cli/test_ci_cmd.py` collects 6 and passes 6 at exit 0, including the subprocess test that really launches a stage argv through `scripts/remedy_pytest_runner.py`; the integrity gate reports passed true, fail_count 0, check_count 5 and `handlers=338`, exactly one more than the 337 measured at BASE, which is the proof the handler is reachable and not merely written; `packages/` is untouched in the range diff; the canary is 42 passed and the dashboard contract 70 passed, both exit 0. The open set is 90 registered, 4 `Done:`, 0 `Landed:`, open 86, max R-0462, no duplicate id. Insertions 400 · 341 · 5 · 76 · 16 · 2 · 75 · 9 · 152, none over 500. The four catalog suites report 601 passed at exit 0 against the 593 the block bracketed as its BASE reading: the reviewer accounted for the delta rather than accepting it, and `--collect-only` names exactly 8 new ids, all of them `test_grouped_cli.py` parametrisations over the new `ci` group — 593 + 8 = 601, fully explained, nothing dropped. The worker also declared a genuine conflict between two live rules and asked to be overruled if wrong: AGENTS.md "If Blocked" step 2 orders the exact blocker into `.agent/plan.md`, while the block's gate ordered `.agent/plan.md` to byte-equal a PLAN slice that names no blocker. It obeyed the byte-equality and put the blocker at the top of `.agent/handoff.md`. The reviewer RULES THAT CORRECT and the ruling is not a finding against either side: a whole-file slice is reviewer-authored text a worker may not edit, the handback is the channel the template already mandates for a blocker, and a worker that had instead written prose into `.agent/plan.md` would have broken the one gate that proves the file was not tampered with. The obligation the conflict really exposes belongs to the REVIEWER, and it is discharged in this block: when a round can end blocked, the PLAN slice the NEXT block authors states the blocker, which is why this round's PLAN names the ruff failure and the repair in its Current Step. Both findings below are the reviewer's.

- R-0463 — Medium, A DRY RUN THAT COULD NOT FAIL THE WAY THE REAL GATE FAILS, AND SO SHIPPED A RED SLICE. The authored CI-CMD slice reached the worker with a ruff violation in it. The proximate cause is mechanical: an earlier trim pass over the block deleted a `_ROOT_DEPTH` constant that had sat between the imports and the first `def`, and the deletion took one of the two blank lines with it. The real cause is the verification. Before delegating, the reviewer DID lint the applied slice and DID read `All checks passed!` at exit 0 — under `python3 -m ruff check --no-respect-gitignore --isolated --line-length 120 --target-version py310`. `--isolated` discards `pyproject.toml`, and with it the `select = ["E", "F", "W", "I", "UP"]` line that turns the `I` (isort) rules on at all; ruff's default selection is `E` and `F` only, so `I001` was not merely unreported, it was never evaluated. The probe was green because it was blind, which is the R-0337 class — a probe whose import path or config differs from the gate's proves nothing about the gate — recurring in a new medium, configuration rather than module resolution. It is Medium and not Low because the failure mode is silent and general: every future authored code slice checked this way would pass the reviewer and fail the worker, and the round it costs is a full delegate-and-review cycle. Standing rule, binding the reviewer from here: a dry run executes the gate's EXACT command line, from the repository root, with the repository's own configuration — no `--isolated`, no substituted flags, no convenient variant — or it is not evidence and is not reported as if it were. This block does NOT place that rule in §3: C3 lands item 11 and nothing else, and asserting a promotion this change set does not order is the R-0461 defect itself. R10 owns it as checklist item 12, and this paragraph is the text item 12 carries. OPEN.
- R-0464 — Low, A GATE OVER A PARAMETRISED SUITE QUOTED A COLLECTED COUNT AS ITS BASELINE. R8's gate 10 ordered the four catalog suites and bracketed "[BASE: 593 passed, exit 0 — a red here is this round's doing]". The suites are parametrised per catalog GROUP — `test_grouped_cli.py` alone generates eight ids for every group — so a round whose whole purpose is to ADD a group necessarily moves that number, and 601 was the correct, green result. Nothing broke, because the gate ordered the worker to REPORT the count rather than to match 593, and the worker reported 601, refused to treat the delta as either error or nuisance, and accounted for all eight ids by collection. But the bracketed figure still framed 593 as the expected reading and cost the worker a disproof it could not complete — it could not re-run the suites at BASE, no worktree being permitted that round, so it had to hand the question back unresolved. This is the R-0336 family, whose rule is to gate the PROPERTY and never a serialized count. Low: no false verdict was reached and the reviewer confirmed the delta at the gate. Refinement of that rule, binding the reviewer from here: when a gate names a collected count at all, it first establishes whether the suite is parametrised over anything the round CHANGES, and if it is, the gate states the expected DELTA and its cause — "adding one group adds eight ids" — instead of a bare baseline that the round is designed to invalidate. OPEN.
--- END SLICE RECORD-R8 ---

--- BEGIN SLICE STEPS-FROM --- (the REWRITE pair's FROM, C2; five whole contiguous lines INSIDE the existing Steps paragraph of .agent/live_review.md, occurring exactly once. The line that follows it in the file — the one beginning `closure. Each round marks` — is NOT part of this pair and is not touched.)
R9 T001 the per-stage selection tests over a fixture tree and the parallelism
measurement D2.5 defers → R10 T002 the determinism and budget stages plus the
guard-test wiring → R11 T002 the seeded-failure test per stage → R12 T003 the
hosted workflow files, the docs and the runtime budget written from measured
data → R13 the integration gate → R14
--- END SLICE STEPS-FROM ---

--- BEGIN SLICE STEPS-TO --- (the REWRITE pair's TO, C2; replaces STEPS-FROM in place, six whole lines, the rest of the paragraph untouched)
R9 the R8 record, the ruff repair and checklist item 11 → R10 T001 the
per-stage selection tests over a fixture tree, the parallelism measurement D2.5
defers, and checklist item 12 → R11 T002 the determinism and budget stages plus
the guard-test wiring → R12 T002 the seeded-failure test per stage → R13 T003
the hosted workflow files, the docs and the runtime budget written from measured
data → R14 the integration gate → R15
--- END SLICE STEPS-TO ---

--- BEGIN SLICE BLANK-FROM --- (the REWRITE pair's FROM, C3; three whole contiguous lines occurring exactly once in apps/cli/commands/ci_cmd.py)
from typing import Any

def repo_root_for_ci() -> Path:
--- END SLICE BLANK-FROM ---

--- BEGIN SLICE BLANK-TO --- (the REWRITE pair's TO, C3; replaces BLANK-FROM in place, four whole lines — the same three with a second blank line between the imports and the def, which is what ruff's I001 is asking for)
from typing import Any


def repo_root_for_ci() -> Path:
--- END SLICE BLANK-TO ---

--- BEGIN SLICE OPENER-FROM --- (the REWRITE pair's FROM, C4; one whole line occurring exactly once in docs/agents/planner_reviewer_prompt.md)
  ten checks mechanically, on the FINAL bytes, after the last edit, before any
--- END SLICE OPENER-FROM ---

--- BEGIN SLICE OPENER-TO --- (the REWRITE pair's TO, C4; replaces OPENER-FROM in place, one whole line. The list gains item 11 in the same commit, so the numeral and the enumeration agree at every commit boundary.)
  eleven checks mechanically, on the FINAL bytes, after the last edit, before any
--- END SLICE OPENER-TO ---

--- BEGIN SLICE ITEM11-FROM --- (the APPEND-shaped pair's FROM, C4; one whole line occurring exactly once in docs/agents/planner_reviewer_prompt.md — the "Why this is on disk" line that closes the checklist)
  Why this is on disk and not a habit: item 2 has recurred six times across
--- END SLICE ITEM11-FROM ---

--- BEGIN SLICE ITEM11-TO --- (the APPEND-shaped pair's TO, C4; replaces ITEM11-FROM in place. It CONTAINS the FROM line unchanged as its LAST line, so item 11 is inserted immediately after item 10 and before the closing paragraph.)
  11. **A convention paragraph names its units and states NO count of them.**
      Findings R-0460 and R-0461. A block's slice-convention paragraph LISTS its
      authored units and gives no numeral for them, and any sentence that both
      enumerates and denies enumerating is a defect of the block regardless of
      which half is true. Item 1 counts the block's LINES mechanically, which is
      a measurement; this one forbids a hand-counted numeral about the block's
      own parts, which is a recollection — the distinction the R-0402, R-0404,
      R-0436 and R-0441 family kept losing. The rule binds finding text too: a
      finding may state that a rule IS in this checklist only when the SAME block
      orders the edit that puts it here, and otherwise it names the round that
      will. R-0460 asserted its own promotion into this list while the block
      carrying it fixed a change set with no `docs/` path in it, so the sentence
      was false on disk the moment it was written and stayed false for a round
      (R-0461). This item is that promotion, finally performed.
  Why this is on disk and not a habit: item 2 has recurred six times across
--- END SLICE ITEM11-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C5)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0465. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0464 registered on this branch, of which
R-0456 to R-0459 are resolved. `.agent/live_review.md` is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R9 records the R8 FAIL, registers R-0463 and R-0464, repairs the ruff I001 the
reviewer's own CI-CMD slice shipped, and performs the §3 promotion R-0460 claimed
and R-0461 assigned here — the convention-paragraph rule becomes item 11 of the
pre-emission checklist. The CLI seam itself landed in R8 and is not re-opened.

## Next Steps
1. R10 adds the per-stage selection tests over a fixture tree that pin each
   stage's marker expression against files whose markers are known, and promotes
   R-0463's dry-run rule into §3 as checklist item 12.

## Risks
- `fast` still rests on a single 391.8 s reading, and the inventory showed it is
  inverted with respect to cost. Until that is measured under `-n auto`, no
  runtime budget can be written from measured data.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C6.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 4406f1c1.
 3. TRANSPORT, bytes read in Python: sha256, bytes and lines of
    `.remedy-wt/.cache/f083-r9/f083-r9.md`, `.agent/authored/f083-r9.md` and
    `.agent/last_block.md`; whether all three are EQUAL; whether the measured line
    count equals this block's declared footer.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` equals `b"\n" + RECORD-R8`, that slice extracted from the
    COMMITTED `.agent/authored/f083-r9.md` by its markers. Report the numstat;
    its deletion column must be 0.
 5. C2 STEPS REWRITE over the whole `.agent/live_review.md` at C2:
    STEPS-FROM 0x, STEPS-TO 1x. Then, each wholly on ONE line of the TO so no
    count is defeated by a line break: `R9 the R8 record` 1,
    `R14 the integration gate` 1, `R13 the integration gate` 0. Report the
    numstat.
 6. C3 BLANK REWRITE over the whole `apps/cli/commands/ci_cmd.py` at C3:
    BLANK-FROM 0x, BLANK-TO 1x. Report the numstat.
 7. THE RED GATE IS GREEN — this is the round's reason to exist. Run the R8 gate
    unchanged and from the repository root, with NO `--isolated` and NO other
    flag, so it reads `pyproject.toml` exactly as R8's did (R-0463):
    `python3 -m ruff check apps/cli/commands/ci_cmd.py apps/cli/command_catalog.py
    apps/cli/commands/__init__.py tests/cli/test_ci_cmd.py` — report the REAL exit
    code and the full output. It exited 1 with `I001` at BASE; report what you get.
 8. C4 PAIRS over the whole `docs/agents/planner_reviewer_prompt.md` at C4, and
    note that the two shapes DIFFER: OPENER-FROM 0x and OPENER-TO 1x (a REWRITE),
    while ITEM11-FROM must be 1x BEFORE and 1x AFTER and ITEM11-TO 0x before and
    1x after (an APPEND). Report all six counts. Then over the file at C3, the
    numerals and the enumeration must agree: `  11. **A convention paragraph`
    exactly 1, `  10. **The open-finding set` exactly 1, `  12. **` exactly 0,
    `eleven checks mechanically` exactly 1, `ten checks mechanically` exactly 0.
    Report the numstat.
 9. THE SEAM STILL WORKS: `python3 -m pytest tests/cli/test_ci_cmd.py -q` —
    report collected count and exit code [BASE: 6 collected, 6 passed, exit 0].
10. THE CATALOG STILL AGREES WITH ITSELF, all four paths confirmed on disk first
    (R-0438), in ONE run: `python3 -m pytest tests/test_command_catalog.py
    tests/cli/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_cli_ux.py
    -q` — report collected count and exit code. This round adds NO catalog group,
    so the parametrised count should not move from the 601 measured at BASE
    (R-0464); report what you MEASURE either way.
11. VERIFICATION, each run separately, exit code from the process (R-0438), each
    via `python3 -m pytest <path> -q`: `tests/ui_server/test_dashboard_contract.py`
    [70, 0]; `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0].
12. NOTHING ELSE MOVED: `git diff --name-only 4406f1c1..HEAD -- packages/ tests/
    apps/cli/command_catalog.py` must print NOTHING. Report it as a measured list.
13. INTEGRITY GATE, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every check's status, and the
    `handler_import` message [BASE: handlers=338; this round adds no handler].
14. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` and
    `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max id,
    next free id, any duplicate. Reviewer measured 90 / 4 / 0, max R-0462, at BASE
    and expects 92 / 4 / 0, max R-0464, open 88. Report what you MEASURE.
15. C5 PLAN byte-equals the PLAN slice as a whole file — report sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line, and the
    number of numbered items under `## Next Steps`.
16. CHANGE SET, measured BEFORE the handoff is written into C6, so it lists seven
    paths with `.agent/handoff.md` the seventh and last: `git diff --name-only
    4406f1c1..HEAD`. Report the list and its count.
17. Insertions (`+` column only) for C0a through C5 — report each; none over 500.
    C0b is a verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt; report it
    anyway. C6's own count cannot exist inside C6 (R-0149): final message.

The push result, the post-C6 clean-tree reading and the open-PR list postdate C5,
so per R-0449 and R-0452 they are NOT ordered into that file: run `git push -u
origin feature/f083-ci-self-check` after C6, create no PR, report all three in your
final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as C6
— feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and gate, open findings with
max and next free id, and the next action, R10 as the plan states it. C6 cannot
table its own SHA (R-0371, R-0149); say so rather than inventing one. If it
exceeds a cap, name BOTH the line and token caps (R-0462). Fortschritt, verbatim:

Fortschritt: 34 % (F083 beansprucht · R1 bis R7 PASS, R8 FAIL auf einem roten ruff-Gate und hier repariert · Stage-Tabelle, Stage-Runner und die `remedy ci` CLI-Naht als Code gelandet, mit einem Test der wirklich einen Stage-Argv durch den Runner startet · noch keine hosted workflows, keine Determinismus- oder Budget-Stage) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 250 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
