# F083 R27 — pre-closure content round

SPLIT round. It lands the last CONTENT this feature owes before closure: the
feature file's Built State section, which closure precondition 4 requires and
which the closure commit's own path set forbids it from writing. It also writes
down the R26 integration-gate verdict and both registers and FIXES the reviewer
gate defect that round exposed.

Base: `git rev-parse HEAD` MUST print ceb46a23 before the first commit. If it does
not, stop and report — every gate below is measured against that base.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The slices carried here are
named CHECKLIST, BUILTSTATE, RECORD-R26 and PLAN. CHECKLIST is the only FROM/TO
pair; BUILTSTATE and RECORD-R26 are EOF-APPENDs and PLAN is a whole-file
replacement. Extract every one of them programmatically from the COMMITTED
`.agent/authored/f083-r27.md` by their markers — never by retyping.

CHECKLIST's pair shape, declared and verified rather than asserted: its TO
literally CONTAINS its FROM, so it is an APPEND in the §4.9 sense even though the
new text is inserted BEFORE the anchor line. The FROM therefore still occurs
exactly once after the replacement, inside the TO. Gate 4 checks it that way.

Shell note, so a guard does not eat a gate: this session rejects `$( )`, `${...}`
and shell loops by form. Route anything of that shape through `python3 - <<'PY'`
and read every exit code from the process object, never from `$?`.

--- BEGIN SLICE CHECKLIST --- (FROM/TO pair, docs/agents/planner_reviewer_prompt.md, C1)
FROM:
  Why this is on disk and not a habit: item 2 has recurred six times across
TO:
  14. **A per-commit gate names the commits it can honestly reach.** Finding
      R-0489. A gate that orders a value PER COMMIT over a range ending in the
      handback commit is unmeetable for that last commit: its own insertion count
      cannot exist while its text is being written, so an honest worker writes
      "and this commit's own" beside a sentence that then miscounts the range.
      Order the per-commit numbers for the commits BEFORE the handback commit,
      and order the handback commit's own numbers in the ROUND REPORT, which is
      written after that commit exists. Item 13 governs the ORDER the block
      imposes on the worker's runs; this one governs which commits a per-commit
      gate can reach at all, which no ordering check surfaces because the gate's
      sequence is fine and only its RANGE is wrong. The R26 instance: gate 19
      covered a six-commit range, so the handback reported five insertion counts
      and called the range "five single-parent commits" while HEAD held six.
  Why this is on disk and not a habit: item 2 has recurred six times across
--- END SLICE CHECKLIST ---
--- BEGIN SLICE BUILTSTATE --- (EOF-APPEND to docs/roadmap/features/T2_F083.md, C2)

## Built State — what F083 delivered

Accepted at the R26 integration gate on branch `feature/f083-ci-self-check`.
Three new modules under `packages/orchestration/`, one CLI module, one hosted
workflow file and one system document; every module carries its own test file.

- `packages/orchestration/ci_stages.py` — the stage table as DATA and nothing
  else. `CI_STAGES` holds `fast`, `standard`, `ui`, `smoke`, `budgets` and
  `excluded`, each with its marker expression, the reason it exists and its own
  `timeout_sec`. The module RUNS NOTHING at import, so reading the table can
  never start a test run, and `pytest_argv_for_stage` renders the argv a caller
  hands to the runner. The selections are MEASURED: the marker selections were
  collected against the whole suite and their union covered it with nothing
  outside.
- `packages/orchestration/ci_run.py` — the runner. Every stage goes through
  `scripts/remedy_pytest_runner.py` AS A SUBPROCESS, because that script owns the
  process-group isolation, the 512 KiB output caps, the `REMEDY_PYTEST_TIMEOUT_SEC`
  budget and exit code 124 for a timeout; shelling out to bare `pytest` would lose
  all four. `run_ci_stage` never raises on a red stage, so every selected stage
  runs and `ci_exit_code` reports the sum. Remedy deliberately does NOT retry a
  failing stage — quarantine is an explicit marker change in a reviewed diff,
  because retries hide rot.
- `packages/orchestration/ci_budgets.py` — the ceilings the `budgets` stage
  checks, with `parse_ruff_error_count` and `check_lint_ceiling`.
  `LINT_ERROR_CEILING` is 26 and is a RATCHET: DECISION F083 D5 freezes the
  existing lint debt rather than fixing it inside a feature that does not
  otherwise touch those files, so the debt stays visible and cannot grow.
- `apps/cli/commands/ci_cmd.py` — the `remedy ci` seam and the summary table.
  `remedy ci run` runs every stage in table order; `--stage NAME` runs exactly
  one. A stage carrying `runs_in_ci=False` is REPORTED as skipped together with
  the command that runs it by hand, never silently dropped, so the coverage claim
  stays honest.
- `.github/workflows/ci.yml` — a THIN WRAPPER that names no stage and selects no
  tests of its own: it installs the Python and UI toolchains and then calls
  `remedy ci run` once. Its 90-minute job cap sits ABOVE the 3900 seconds the
  stage budgets sum to, so a slow stage dies at ITS OWN budget and names itself
  in the summary instead of the job being killed first and naming no stage.
- `docs/system/ci-self-check-v1.md` — the stage table, the measured runtime
  budgets and the exclusions, every claim pinned to a stage collection.

DECISION F083 D4: `determinism` is deliberately NOT a stage of its own. The
manifest suite's node ids already sit wholly inside what `standard` selects, so a
determinism stage would either re-run them or force `standard` to be narrowed,
and narrowing it is a marker-semantics change this file's Do-not-touch forbids.

DECISION F083 D6: the UI toolchain is a PRECONDITION of the `ui` stage rather
than a part of it. `test_typescript_compiles` and the Vite probes in
`tests/runtimes/test_apps_ui_probe.py` skip when the toolchain is absent, which
is why the hosted workflow installs it before the run — otherwise the Acceptance
line would be met by a skip instead of by a compile.

Integration gate, R26: the branch run reported `17047 passed, 19 skipped` and the
merge-base run `16988 passed, 19 skipped`, both at exit 0, with 0 branch-only and
0 base-only failures and nothing left unattributed. Evidence sits in
`.agent/gate_f083_r26/`.

NOT measured: hosted wall time. The first hosted run is that measurement.
--- END SLICE BUILTSTATE ---
--- BEGIN SLICE RECORD-R26 --- (EOF-APPEND to .agent/live_review.md, C3)

Gate: R26 — PASS. This was the integration gate, and it is green in both directions. TRANSPORT, against the reviewer's OWN original bytes and NOT by digest fallback (§4.9): the block was emitted to `.remedy-wt/f083-r26.md` and COPIED rather than retyped, and the committed `.agent/authored/f083-r26.md` and `.agent/last_block.md` are byte-IDENTICAL to that original, all three at sha256 461cc40b451538c67da83a4fcc000056736d3a86a715cc0e9d7bdd2bd885fe29 over 17873 bytes and 224 lines, under the 400-line cap. C1 is a pure append and was proved so: `.agent/live_review.md` goes 305119 B to 308606 B, the former prefixes the latter, the 3487-byte tail byte-EQUALS the RECORD-R25 slice extracted from the committed authored file by its markers, `git show --numstat` is `2 0`, and the file's count of transport marker LINES is 0 at base and 0 at HEAD while the bare substring count is 4 at both. THE GATE ITSELF REPRODUCES AT THE REVIEWER'S OWN HAND. The reviewer re-ran the full branch suite itself from the repository root at ceb46a23 and got `17047 passed, 19 skipped in 111.66s` at exit 0 with 0 `FAILED` and 0 `ERROR` lines, which equals the worker's `17047 passed, 19 skipped in 126.08s` reading; both raw logs still carry the sha256, byte count and line count their committed `full_log_provenance.txt` records — 6c34205a…1ad8 over 19129 B and 242 lines for the branch run, 10761be9…83dd over 19049 B and 241 lines for the base run — and the reviewer re-derived BOTH failure lists out of those raw logs rather than trusting the committed ones, getting 0 and 0, so `comm -13` and `comm -23` are empty and the two committed comm files are correctly empty. The base run is the control and the branch-only conclusion does not depend on it: a branch run with zero `FAILED` lines makes the branch-only set empty against ANY base. Parity was independently corroborated rather than accepted: the reviewer recomputed the composite digest of the PRIMARY checkout's `apps/ui/dist` and got 5876f488eab879fcfe1fae4cfb7329e63246c0aff9dd57a203b56d8f15b69d44, which equals BOTH the BEFORE and the AFTER readings the committed `dist_hashes.txt` carries — so the copy was faithful and `REMEDY_UI_NO_AUTO_BUILD=1` held across the base run. The freshness step this block added over the F082 R21 procedure earned its place: R21 copied a content-correct but STALE `dist`, the UI server refused to start, and that gate paid eight base-only failures for per-id attribution; R26 re-stamped the copied `dist` newer than the worktree's `src` and took zero. The remaining gates reproduce: the canary is `42 passed` at exit 0; ruff is `Found 26 errors.` with `[*] 25 fixable` at exit 1 and the only path C3 changed before HEAD is `.agent/handoff.md`, so the reading is invariant across the commit it was taken at; the open set recomputes to 116 registered, 12 resolved, 0 landed and 104 open, max R-0488 and next free R-0489, 0 duplicate ids, 0 resolutions naming an unregistered id, R-0488 resolved and R-0482 and R-0487 still open, with 0 open findings above Medium — 36 Medium and 68 Low; `.agent/plan.md` byte-EQUALS its PLAN slice at sha256 8cd8b2e201f28bc30eb5b67714b00a6f73788c617b734a63bf8ece2f75265840 over 2085 bytes and 37 lines; the range gate prints nothing; the change set is exactly 14 paths, every one under `.agent/`; the evidence directory holds its nine `.txt` members with 0 `.log` files among 3533 tracked paths; the worktree was removed and `tmp/base-gate` deleted; and the history is six single-parent commits chained to 6a413eb7 with a reflog showing only `commit:` entries. Collection arithmetic cross-checks in three places: 17047 + 19 = 17066, which equals the reviewer's own `--collect-only` count, and 16988 + 19 = 17007, which equals what F082's own integration gate collected at the commit that is now main's tip — so the 59-test difference is exactly this feature's additions. The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed exactly, six commits, none added, dropped or reordered. All four declared deviations are honest and none is a defect. The tooling substitution deserves naming: this session denies `cp`, so the parity copies ran through `shutil.copytree(..., symlinks=True)`, and the worker measured the PROPERTY the block ordered — both paths are real directories with 0 symbolic links at them — rather than reporting the tool. That is the correct reading of a gate that names a property, and `symlinks=True` is the right flag here because it preserves `node_modules`' internal RELATIVE links inside the copy instead of following them, while the prohibition the gate exists for is the DIRECTORY-level symlink that would let a build write THROUGH into the primary checkout; the unchanged dist digest is the evidence that no such write happened.

- R-0489 — Low, A GATE ORDERED A PER-COMMIT NUMBER FOR THE COMMIT THAT WOULD CARRY THE ANSWER, SO THE HANDBACK'S SENTENCE ABOUT ITS OWN RANGE IS FALSE AT HEAD BY CONSTRUCTION. Gate 19 of the R26 block ordered "per-commit insertions from `git show --numstat`, reported per commit" over a range whose last commit is C4, the handback commit itself. C4's own numstat cannot exist while C4's text is being written, so the worker honestly wrote "224, 158, 2, 108, 9 and C4's own" and, in the same cell, "five single-parent commits chained to 6a413eb7" — true of the five commits that existed as it wrote, false of the six-commit range that same sentence names. Nothing measured was wrong and nothing green was claimed that was not run: the reviewer measured all six itself at 224, 158, 2, 108, 9 and 80, and the history is linear with no amend, rebase or reset. The defect is the reviewer's GATE, not the round, and it is the R-0371 class — ordering a value that cannot exist when the text is written — landing in the one place `docs/agents/handback_template.md` already documents as self-referential (R-0149, which the R26 handback's own commit table cites). Low and not Medium: the only false thing is a count of commits in a range, and the correct numbers sit beside it.
Done: R-0489 — resolved in the same round that registered it, and the fix is a rule on disk rather than a sentence in a record. C1 of this round added item 14 to the pre-emission block checklist in `docs/agents/planner_reviewer_prompt.md`: a per-commit gate orders the numbers for the commits BEFORE the handback commit and orders the handback commit's own numbers in the round report, which is written after that commit exists. This round's own gate 16 is written that way and is the worked example. Registering and resolving in one round is the R-0460/R-0461 precedent applied deliberately: a finding may assert its own promotion into that checklist only when the SAME block orders the edit that performs it, and this block does, in a commit that lands BEFORE the record claiming it.
--- END SLICE RECORD-R26 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C4)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. `.agent/live_review.md` is the source of truth for the open set and for
the next free finding id; this file repeats neither.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R26 is closed PASS: the integration gate ran the full suite on the branch and at
the merge base and found 0 branch-only and 0 base-only failures. R27 records that
verdict, registers and resolves R-0489, and lands the feature file's Built State
section — the last content this feature owes, and a closure precondition the
closure commit's own path set cannot satisfy itself. T001, T002 and T003 are
COMPLETE.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: the evidence job, then a
   FRESH review zip from a clean tree, then the STATUS line and the README
   capability sync in ONE commit, then the PR. The zip's package name and
   SHA-256 do not exist until the worker builds it, so the STATUS line is
   authored as a template with named slots and gated on its GRAMMAR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the toolchain-dependent tests.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- Closure packaging has a documented history of BLOCKED_EVIDENCE traps. The
  closure block names each one it must clear rather than discovering them at zip
  time.
- R-0482 (a live `NameError` on a guard's refusal path) and R-0487
  (`docs/README.md` is never link-checked) are both frozen here and belong to a
  paydown branch: each is a code- or test-content fix this feature may not make.
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C0a** saves this block verbatim to `.agent/authored/f083-r27.md` by COPYING
`.remedy-wt/f083-r27.md`, never by retyping. **C0b** mirrors the COMMITTED copy
over `.agent/last_block.md`.

**C1** applies CHECKLIST to `docs/agents/planner_reviewer_prompt.md`, the only
file in that commit.

**C2** applies BUILTSTATE as an EOF-append to
`docs/roadmap/features/T2_F083.md`, the only file in that commit.

**C3** applies RECORD-R26 as an EOF-append to `.agent/live_review.md`, the only
file in that commit.

**C4** applies PLAN. **C5** rewrites `.agent/handoff.md`.

The ordered sequence is exactly C0a, C0b, C1, C2, C3, C4, C5 — seven commits, no
gaps and no spare numbers. C1 lands BEFORE C3 on purpose: C3's record states that
the checklist rule is on disk, and that sentence must be true when it is written.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created and none is merged. No worktree is added or removed this round.
2. `.agent/live_review.md` is APPENDED to once, at C3. No committed text in it is
   edited; write no resolution and no `Landed:` line beyond the RECORD-R26 slice.
3. No marker line reaches any target file. Every slice is extracted from the
   COMMITTED `.agent/authored/f083-r27.md` by its markers.
4. `docs/roadmap/STATUS.md` is NOT touched this round. The `[~]`→`[x]` edit
   belongs to the closure commit and to no other. `README.md` is not touched
   either. Gate 13 proves both.
5. NOTHING under `packages/`, `apps/`, `scripts/`, `tests/` or `.github/` is
   modified. Gate 12 proves it. The 26 ruff errors are NOT fixed and the lint
   ceiling is NOT raised.
6. CHECKLIST is a pair whose TO CONTAINS its FROM. Apply it by replacing the ONE
   occurrence of the FROM with the TO; do not hand-insert the new item. After the
   replacement the FROM still occurs exactly once, inside the TO — that is the
   expected reading, not a failure.
7. If any gate is red, stop at that gate, record its real output verbatim, and
   hand back. Do not widen the change set to route around it.
8. Your handback's Deviations section states explicitly whether the ordered
   commit sequence was followed, per `docs/agents/handback_template.md`.

## Done when — every command run as its own unpiped process, each exit code read
## from that process, the working directory named for every one of them

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit and
   before C5. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS ceb46a23.
3. `.agent/authored/f083-r27.md` and `.agent/last_block.md` byte-equal as
   COMMITTED blobs, and both byte-equal `.remedy-wt/f083-r27.md`; report the
   sha256, byte count and line count shared by all three.
4. CHECKLIST at C1, scoped to `docs/agents/planner_reviewer_prompt.md` alone:
   report the FROM's occurrence count BEFORE the replacement (must be exactly 1),
   the TO's occurrence count AFTER (must be exactly 1), and the FROM's count
   AFTER (must be exactly 1, inside the TO). Report also that the file contains 0
   marker lines and 0 bare `FROM:`/`TO:` label lines.
5. BUILTSTATE at C2: the pre content of `docs/roadmap/features/T2_F083.md`
   PREFIXES the post content, the tail byte-EQUALS the BUILTSTATE slice as
   extracted from the committed authored file by its markers, and
   `git show --numstat` has deletion column 0. Report also that `## Built State`
   occurs 0 times BEFORE and exactly 1 time AFTER, and that the file holds 0
   marker lines.
6. RECORD-R26 at C3: the pre content of `.agent/live_review.md` PREFIXES the post
   content, the tail byte-EQUALS the RECORD-R26 slice as extracted the same way,
   and `git show --numstat` has deletion column 0. Report the file's count of
   transport BEGIN-marker LINES at base and at HEAD; they must be equal.
7. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   unchecked-box lines.
8. `python3 -m pytest tests/docs/ -q` — the docs-round gate, required because this
   round's change set includes `docs/roadmap/**`. Report the passed count and the
   exit code.
9. `python3 -m pytest tests/cli/test_golden_path.py -q` — the canary. Report the
   passed count and the exit code.
10. `python3 -m pytest tests/orchestration/test_ci_stages.py
    tests/orchestration/test_ci_workflow.py tests/cli/test_ci_cmd.py -q` — the
    stage-table, workflow-guard and CLI-seam suites, which are the tests that
    would notice if the Built State text described a shape the code does not
    have. Report the passed count and the exit code.
11. `python3 -m ruff check .` — report the `Found N errors.` line and the exit
    code. Take this reading AT C4 and name the commit; C4 and not C5, because C5
    writes the handback that carries the reading.
12. `git diff --name-only ceb46a23..HEAD -- packages/ apps/ scripts/ tests/
    .github/` prints NOTHING. Report that it printed nothing.
13. `git diff --name-only ceb46a23..HEAD -- docs/` lists EXACTLY
    `docs/agents/planner_reviewer_prompt.md` and
    `docs/roadmap/features/T2_F083.md`. Report the list, and report separately
    that `docs/roadmap/STATUS.md` and `README.md` are each absent from
    `git diff --name-only ceb46a23..HEAD`.
14. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line and every
    `^Landed: R-\d+ — ` line; report registered, resolved, landed and open, the
    maximum id, the next free id, and that no id repeats and no resolution names
    an unregistered id. R-0489 must appear BOTH registered and resolved, and
    R-0482 and R-0487 must appear still open. Report the values measured; this
    block predicts none of them.
15. The change set: `git diff --name-only ceb46a23..HEAD` lists exactly
    `.agent/authored/f083-r27.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`,
    `docs/agents/planner_reviewer_prompt.md` and
    `docs/roadmap/features/T2_F083.md`. Report the list and that nothing else is
    in it.
16. Per-commit insertions from `git show --numstat`, for C0a, C0b, C1, C2, C3 and
    C4 — the six commits that exist before the handback commit is written — none
    exceeding 500. C5's own insertion count goes in the ROUND REPORT instead of
    the handoff, because a commit cannot measure itself; report it there. Report
    also that the history is linear with no amend, rebase or reset, naming the
    number of commits the range holds at the time you read it.

## Handback

Completion report plus a rewritten `.agent/handoff.md` per
`docs/agents/handback_template.md`: feature and round, branch, the commit table,
the item-status table with every ordered item above appearing exactly once, the
real verification results, the open-findings count, and the next expected action.
The handoff's Next section names, in order: read `.agent/STOP` from disk, run the
AGENTS.md Open PR Gate, then the closure round per
`docs/roadmap/STATUS_closure_protocol.md`.

Fortschritt: 97 % (F083 beansprucht · R1 bis R7, R9 bis R21, R23 bis R26 PASS, R8 und R22 FAIL — beide in der Folgerunde repariert · T001, T002 und T003 fertig · das Integration Gate ist durch: Branch und Merge-Base beide grün, 0 branch-only und 0 base-only Failures, vom Reviewer selbst nachgefahren · diese Runde liefert die Built-State-Sektion, die die Closure als Vorbedingung verlangt, und schliesst R-0489 · danach bleibt nur die Closure selbst: Evidence-Job, frische Review-Zip, STATUS-Zeile plus README-Sync, PR · R-0482 und R-0487 sind bewusst auf einen eigenen Paydown-Branch geroutet · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
