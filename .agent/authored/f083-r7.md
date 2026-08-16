── STEP R7/14 — F083 CI self-check — RECORD R6, REGISTER R-0460, RESOLVE FOUR FINDINGS ──

Goal:
  Close the record R6 left open: write the R6 PASS verdict, register the one
  finding that review produced, and replace the four `Landed:` lines with the
  reviewer's `Done:` resolutions — only reviewer-authored text sets Resolved
  (§4.4). This round writes NO code. The `remedy ci` CLI seam is fully scoped and
  moves to R8, so the map is repaired in this same block (R-0455).

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r7.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R6-BLOCK appended at EOF, ONE commit.
  C2   `.agent/live_review.md` — FINDING-R460 appended at EOF, ONE commit.
  C3   `.agent/live_review.md` — the LANDED→DONE pair, ONE commit.
  C4   `.agent/live_review.md` — the STEPS pair, ONE commit.
  C5   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C6   `.agent/handoff.md`, the handback, alone.

BASE: e166b640. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals e166b640. If it does NOT, stop and hand off.

TRANSPORT: the scratchpad original of THIS block is at
`.remedy-wt/.cache/f083-r7/f083-r7.md`, which `.gitignore` drops. C0a is a byte
COPY of it — do not retype, reflow or strip anything. `cp` is denied in this
session class: copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The authored units are, listed and NOT counted
(R-0402, R-0460): GATE-R6-BLOCK, FINDING-R460, LANDED→DONE, STEPS, PLAN.

PAIR SHAPES, stated at authoring time (§4.9) and verified on these bytes, not
asserted: LANDED→DONE and STEPS are both REWRITEs — FROM and TO are disjoint —
so each is proved by FROM 0x and TO 1x over the whole file. No pair in this block
is append-shaped.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r7.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`. Nothing
     else. `apps/`, `packages/`, `tests/`, `scripts/` and `docs/` stay EMPTY in
     the range diff — this round writes no code and no test, by design.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. No slice contains an instruction
     addressed to you about the file it lands in (R-0450).
  3. C1 before C2, C2 before C3, C3 before C4. Push after C6. Create NO pull
     request. This round adds NO worktree; `git worktree list` is one line
     throughout.
  4. Env-var assignment (all three forms), `cp`, `$?` inside `$(...)` and process
     substitution are denied in this session class. Capture real exit codes as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and use `python3 - <<"PY"` heredocs —
     QUOTED delimiter — for all counting, hashing and byte comparison.

--- BEGIN SLICE GATE-R6-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R6 — PASS. Verification tier: the live-state contract reader, the two live-state readers and the canary, all re-run by the reviewer at the round's head, plus ruff, both orchestration test files, an independent re-derivation of every authored-text proof out of the committed git objects, and a direct behavioural probe of all three repairs against the committed module; no full-suite claim is made. TRANSPORT held in its strongest form: the committed `.agent/authored/f083-r6.md` byte-equals the REVIEWER'S OWN scratchpad original at `.remedy-wt/.cache/f083-r6/f083-r6.md`, three-way with `.agent/last_block.md`, all sha256 7c6acd4e1202d599bdcbff83b7e31c0e8e870f3e18a8a832ce60052450024540, 30218 bytes, 346 lines, and the measured 346 equals the block's declared footer — so no applied byte was retyped anywhere on the path. The three EOF appends each hold the prefix property from the git blobs, with tails byte-equal to `b"\n" + GATE-R5-BLOCK`, `b"\n" + FINDINGS` and `b"\n" + LANDED` and numstats `2 0`, `8 0` and `5 0`. The C3 REWRITE pair holds in both directions, FROM 0x and TO 1x, with the three ordered literals at 1, 1 and 0 and the substring the dashboard contract reads still present. C4's two files were read back OUT of fb9ddf12: every one of the ten ordered code literals sits at its ordered count, all five FROM literals gone and all five TO literals present exactly once, `lambda command, cwd:` exactly 3, every TO slice present VERBATIM, and TESTS-APPEND at the file's end preceded by exactly two blank lines. The repairs were then probed as BEHAVIOUR, not as text, because a diff that applies cleanly is not a defect that is fixed: `ci_exit_code(())` and the all-skipped tuple both return 1 where both returned 0 at 81af8a98, while green-plus-skipped stays 0 and green-plus-red stays 1 — the empty case narrowed and nothing else; the injected runner receives the repository root; and a REAL subprocess launched through `_run_via_subprocess`, with a child comparing `os.getcwd()` against the anchor, exits 0 — so the anchor survives the process boundary, which no unit test in this round shows. ruff exits 0 over both files, `test_ci_run.py` collects 8 and passes 8 at exit 0 — the 6 at BASE plus the 2 appended — the stage table is untouched at 7/7, the dashboard contract, resource safety and the integrity-gate tests are 113 passed exit 0 together, and the canary is 42 passed exit 0. C6's plan byte-equals PLAN at 32 lines with one numbered Next Step, `## Goal` and `## Next Steps` present and no `- [ ]` line. The open set at HEAD is 87 registered, 0 Done, 4 Landed, max R-0459, no duplicate id, and the four new ids are exactly the four ordered. The integrity gate reports passed true, fail_count 0, check_count 5, every named check pass. Insertions 346 · 235 · 2 · 8 · 7 · 44 · 5 · 12, with the handback's own 152 measured after the fact, none over 500. The worker declared one defect in the block's own text before the reviewer read the diff — the tenth consecutive round — and it is registered below as R-0460.
--- END SLICE GATE-R6-BLOCK ---

--- BEGIN SLICE FINDING-R460 --- (APPEND to .agent/live_review.md, C2, with exactly one blank line between the file's current last line and the first line of this slice)
- R-0460 — Low, A BLOCK'S OWN CONVENTION PARAGRAPH MISCOUNTED ITS SLICES AND DENIED STATING A COUNT IN THE SAME BREATH. Declared by the WORKER while applying the R6 block, with the disk evidence, before the reviewer read the diff. That block's SLICE CONVENTION paragraph reads "five REWRITE pairs and one end-of-file append in the two code files", while its C4 bundle line orders "all six repair pairs" and six exist: RUNNER, INJECT, CALL and EXIT in `packages/orchestration/ci_run.py`, ASSERT and LAMBDAS in `tests/orchestration/test_ci_run.py`. The same sentence ends "No numeral is stated for that list — the list IS the statement (R-0402)" while stating numerals inside it, so the paragraph contradicts the rule it cites in the act of citing it. Nothing on disk is wrong: the worker gave the C4 line precedence, applied six, altered no slice and declared the disagreement, and gate 6 was satisfiable only with all six applied — which is why the round is green. This is the R-0402 / R-0404 / R-0436 / R-0453 family, whose standing rule is count it mechanically or state NO numeral, and it is now also the R-0331 family — clause-vs-clause disagreement inside one block — landing in a paragraph written to prevent exactly this. Low: no gate, claim or byte depended on the numeral. Standing rule from here, binding the reviewer, and placed in the pre-emission checklist rather than left as finding prose (R-0452): a block's convention paragraph names its authored units and states NO count of them, and any sentence that both enumerates and denies enumerating is a defect of the block regardless of which half is true. OPEN.
--- END SLICE FINDING-R460 ---

--- BEGIN SLICE LANDED-FROM --- (the REWRITE pair's FROM, C3; four whole contiguous lines occurring exactly once in .agent/live_review.md)
Landed: R-0456 — the stage run is anchored at `repo_root` via `cwd=`, the injected runner signature carries it, and a test pins that the runner receives the root; C4.
Landed: R-0457 — `ci_exit_code` returns 1 when no stage ran, with the empty and all-skipped tuples both pinned by a test; C4.
Landed: R-0458 — the assertion that could not fail is replaced by one on the argv shape a regression can actually produce; C4.
Landed: R-0459 — `.agent/plan.md` names one future round; C6.
--- END SLICE LANDED-FROM ---

--- BEGIN SLICE DONE-TO --- (the REWRITE pair's TO, C3; replaces LANDED-FROM in place, four whole lines. Only reviewer-authored text sets Resolved, which is what this pair is.)
Done: R-0456 — the run is anchored: `_run_via_subprocess` takes the root and passes `cwd=`, the injected signature carries it, and `run_ci_stage` hands over the same `repo_root` it already used to find the script. Verified by the reviewer at e166b640 rather than read from the handback — the injected runner receives the repository root, and a REAL subprocess launched through `_run_via_subprocess`, whose child compares `os.getcwd()` against the anchor, exits 0. The anchor therefore survives the process boundary, which the unit test alone does not show. RESOLVED.
Done: R-0457 — a run in which nothing ran is red. Verified by the reviewer at e166b640 against the committed module: `ci_exit_code(())` and the all-skipped tuple both return 1 where both returned 0 at 81af8a98, while green-plus-skipped stays 0 and green-plus-red stays 1 — the repair narrowed exactly the empty case and touched no other outcome. RESOLVED.
Done: R-0458 — the guard is now a proposition a regression can violate: it measures the argv against the `["-m", "pytest"]` shape the module docstring says shelling out would lose, and the vacuous list-membership line is gone from the committed file. RESOLVED.
Done: R-0459 — `.agent/plan.md` names one future round, and the map remains the single place the full round chain is stated. RESOLVED.
--- END SLICE DONE-TO ---

--- BEGIN SLICE STEPS-FROM --- (the REWRITE pair's FROM, C4; six whole lines INSIDE the existing Steps paragraph, occurring exactly once. The line that follows it in the file — the one beginning `closure. Each round marks` — is NOT part of this pair and is not touched.)
repairs R-0456 to R-0458 and the cwd anchor → R7 T001 the `remedy ci` CLI seam
and the summary table it prints → R8 T001 the per-stage selection tests over a
fixture tree and the parallelism measurement D2.5 defers → R9 T002 the
determinism and budget stages plus the guard-test wiring → R10 T002 the
seeded-failure test per stage → R11 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R12 the integration gate → R13
--- END SLICE STEPS-FROM ---

--- BEGIN SLICE STEPS-TO --- (the REWRITE pair's TO, C4; replaces STEPS-FROM in place, seven whole lines, the rest of the paragraph untouched)
repairs R-0456 to R-0458 and the cwd anchor → R7 the R6 record and the four Done
resolutions → R8 T001 the `remedy ci` CLI seam and the summary table it prints →
R9 T001 the per-stage selection tests over a fixture tree and the parallelism
measurement D2.5 defers → R10 T002 the determinism and budget stages plus the
guard-test wiring → R11 T002 the seeded-failure test per stage → R12 T003 the
hosted workflow files, the docs and the runtime budget written from measured
data → R13 the integration gate → R14
--- END SLICE STEPS-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C5)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0461. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0460 registered on this branch, of which
R-0456 to R-0459 are resolved. `.agent/live_review.md` is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R7 closes the record R6 left open: the R6 PASS verdict, R-0460 registered, and
the four `Landed:` lines replaced by the reviewer's `Done:` resolutions, since
only reviewer-authored text sets Resolved. It writes no code, and it repairs the
map because the CLI seam moves out of this round.

## Next Steps
1. R8 makes the runner reachable: a `ci` group and `ci.run` entry in
   `apps/cli/command_catalog.py`, `apps/cli/commands/ci_cmd.py` carrying
   `COMMAND_HANDLERS` and the summary table, its wiring in
   `apps/cli/commands/__init__.py`, and `tests/cli/test_ci_cmd.py` — including
   one test that really launches a stage argv through the pytest runner script.

## Risks
- `fast` still rests on a single 391.8 s reading, and the inventory showed it is
  inverted with respect to cost. Until that is measured under `-n auto`, no
  runtime budget can be written from measured data.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C6.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals e166b640.
 3. TRANSPORT, bytes read in Python: sha256, bytes and lines of
    `.remedy-wt/.cache/f083-r7/f083-r7.md`, `.agent/authored/f083-r7.md` and
    `.agent/last_block.md`; whether all three are EQUAL; whether the measured
    line count equals this block's declared footer.
 4. C1 and C2 PREFIX PROPERTY, each over `<commit>^..<commit>`: `pre` prefixes
    `post`, and `post[len(pre):]` equals `b"\n" + <slice>`, each slice extracted
    from the COMMITTED `.agent/authored/f083-r7.md` by its markers. Report both
    numstats; each deletion column must be 0.
 5. C3 REWRITE PAIR over the whole `.agent/live_review.md` at C3: LANDED-FROM 0x,
    DONE-TO 1x. Line-anchored: `^Landed: R-` must be 0, `^Done: R-` must be 4.
    Report the C3 numstat.
 6. C4 REWRITE PAIR over the whole file at C4: STEPS-FROM 0x, STEPS-TO 1x. Then
    count these three literals, each wholly on ONE line of the TO so no count is
    defeated by a line break: `R7 the R6 record and the four Done` must be 1,
    `R13 the integration gate` must be 1, `R12 the integration gate` must be 0.
    Confirm the substring `Steps` still occurs. Report the C4 numstat.
 7. NO CODE WAS WRITTEN, which is this round's defining constraint:
    `git diff --name-only e166b640..HEAD -- apps/ packages/ tests/ scripts/ docs/`
    must print NOTHING. Report it as a measured list.
 8. THE CODE R6 LANDED STILL RUNS, untouched: `python3 -m pytest
    tests/orchestration/test_ci_run.py tests/orchestration/test_ci_stages.py -q`
    — report collected count and exit code [reviewer measured 8 and 7, both exit
    0, at BASE].
 9. VERIFICATION, each run separately, exit code from the process (R-0438):
    `tests/ui_server/test_dashboard_contract.py` [70/70, 0] — the reader of both
    files this round rewrites; `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; and the canary
    `tests/cli/test_golden_path.py` [42/42, 0], each via `python3 -m pytest <path>
    -q`. `tests/docs/` is NOT a gate: no `docs/roadmap/**` path is in the change
    set.
10. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` and
    `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max id,
    next free id, any duplicate. Reviewer measured 87 / 0 / 4 max R-0459 at BASE
    and expects 88 / 4 / 0, max R-0460, open 84. Report what you MEASURE.
11. INTEGRITY GATE, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every named check's status.
12. C5 PLAN byte-equals the PLAN slice as a whole file — report sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line, and the
    number of numbered items under `## Next Steps`.
13. CHANGE SET, measured BEFORE the handoff is written into C6, so it lists four
    paths with `.agent/handoff.md` the fifth and last: `git diff --name-only
    e166b640..HEAD`. Report the list and its count.
14. Insertions (`+` column only) for C0a through C5 — report each; none over 500.
    C0b is a verbatim single-`.agent/`-file rewrite, exempt by the AGENTS.md
    counting rule; report its number anyway. C6's own count cannot exist inside
    C6 (R-0149): report it in your final message.

The push result, the post-C6 clean-tree reading and the open-PR list postdate C6,
so per R-0449 and R-0452 they are NOT ordered into that file: run `git push -u
origin feature/f083-ci-self-check` after C6, create no PR, report all three in
your final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as C6
— feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and gate, open findings with
max and next free id, and the next action, R8's CLI seam. C6 cannot table its own
SHA (R-0371, R-0149); say so rather than inventing one. Repeat this Fortschritt
line verbatim:

Fortschritt: 25 % (F083 beansprucht · R1 bis R6 PASS · Stage-Tabelle und Stage-Runner als Code gelandet · Runner-Defekte R-0456 bis R-0458 repariert, verifiziert und aufgelöst · noch keine CLI, kein Summary, keine hosted workflows) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, end. Do not
widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 207 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
