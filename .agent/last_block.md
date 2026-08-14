── STEP CLOSURE-PREP / R19 — F077 Autonomy watchdog ──────────
Goal:        Put R18's verdict on the record, resolve R-0398 against the source,
             register R-0400 and R-0401, repair the ist-doc span the R-0398 fix
             got wrong, and add the Built State section that closure
             precondition 4 requires.

Bundle:      C0a save this block; C0b mirror it to last_block; C1 record +
             count mirrors + DOCFIX2; C2 Built State; C3 handback.

Change:      exactly these seven paths and nothing else —
             C0a  .agent/authored/f077-r19.md          (new, verbatim block)
             C0b  .agent/last_block.md                 (whole-file mirror)
             C1   .agent/live_review.md                (1 rewrite + 8 appended lines)
                  .agent/plan.md                       (whole-file replacement)
                  .agent/context.md                    (1-line rewrite pair)
                  docs/system/autonomy-watchdog-v1.md  (3-line rewrite pair)
             C2   docs/roadmap/features/T2_F077.md     (append one section)
             C3   .agent/handoff.md                    (whole-file rewrite)

Constraints: No product file changes — nothing under packages/, apps/ or tests/.
             No docs/README.md change, no docs/roadmap/STATUS.md change, no
             README.md change: closure owns those and it is not this round.
             `.agent/plan.md` must stay under 50 lines (AGENTS.md); the PLAN
             slice is 45 and is applied byte for byte, never trimmed.
             `.agent/context.md` and the ist-doc must keep their current line
             counts — both pairs are equal-line rewrites.
             C1 lands the two registrations AND every count they invalidate in
             ONE commit (finding R-0395).
             Report every measured number RAW. If a gate value does not come
             out as this block predicts, report the contradiction and do NOT
             alter any file to make a gate pass.

── C1 slices ─────────────────────────────────────────────────

(1) REWRITE in `.agent/live_review.md`: replace the single line that currently
    reads `Landed: R-0398 — ...` with the LANDED-TO-DONE slice below. The FROM
    is the whole of that one line; after the edit the string `Landed: R-0398`
    appears 0 times in the file.

<<<BEGIN LANDED-TO-DONE>>>
Done: R-0398 — `docs/system/autonomy-watchdog-v1.md` now reads "ten call sites", and the reviewer verified the corrected COUNT against the source rather than against the fix: `grep -n '_record(' packages/orchestration/orchestrator_loop.py` returns twelve matches, of which line 916 is a nested definition inside another function and line 1036 is `run_mission`'s own nested definition, leaving calls at 1064, 1119, 1180, 1191, 1203, 1210, 1253, 1267, 1293 and 1296 — ten, every one inside `run_mission`, whose `def` is at 936 and whose last body line is the `return build_boundary_handoff(result, root)` at 1304. The sentence the count sits in is unchanged in substance and remains true. What this resolution does NOT cover is the parenthetical span the repair added alongside the count: that is wrong in the other direction and is registered separately as R-0401, so the record shows the count fixed and the new defect raised instead of one absorbing the other.
<<<END LANDED-TO-DONE>>>

(2) APPEND to the END of `.agent/live_review.md`, in exactly this order: one
    blank line, the GATE-R18 slice, one blank line, the FINDING-R400 slice, one
    blank line, the FINDING-R401 slice, one blank line, the LANDED-R401 slice.
    That is 8 added lines and the file goes from 140 to 148 lines.

<<<BEGIN GATE-R18>>>
Gate: R18 — PASS, with one new finding and one carried repair. Verification tier: round gate plus the docs gate plus the state-file contract readers plus the canary; no suite claim is made in this paragraph, because R16 carries this branch's integration-gate entry and nothing since has touched product code. Fourteen of the fifteen ordered gates were re-run by a NEW session against the disk and every one of the fourteen reproduces: the tree is clean and `git worktree list` is one line; `.agent/authored/f077-r18.md` and `.agent/last_block.md` are byte-identical at shared sha256 `1ed498ee3e78a2fda99a15d9aaa5e1634284baee0003d0ad66841455b75476b6`, 214 lines each; `^Gate: R17 — ` 1, `^- R-0398 — ` 1, `^- R-0399 — ` 1 and `^Landed: ` 2; the open set recomputed mechanically from the record is 34 registered paragraphs minus 4 `Done:` lines = 30 open, no duplicate id, next free `R-0400`; `wc -l` gives `.agent/plan.md` 44, `.agent/context.md` 100 and the ist-doc 216; the PLAN whole-file replacement is byte-equal to its slice at sha256 `39fe5fda66084ba4c8e67b094ee95599161d2605a177b62fea2cffceae832a3f`, and both equal-line rewrites read FROM 0x and TO 1x; `eleven call sites` 0 and `ten call sites` 1 in the ist-doc; `tests/docs/` 295 passed; the canary 42 passed; `.agent/STOP` ABSENT; `git diff --check 1c56b295..HEAD` silent; per-commit insertions 362 and 30 with the handback's 60, none over 500; the range is exactly the seven ordered paths; and `origin/feature/f077-autonomy-watchdog` sits at the same `386ef7b5` as the branch. Transport is proven disk to disk against the COMMITTED authored file, not against a retype: the four applied record slices at authored lines 121, 125, 129 and 133 are byte-identical to record lines 134, 136, 138 and 140, and all four of the handback's own sha256 values — `24d3704c…`, `4c5f8bec…`, `fcbbd921…` and `98c43700…` — recompute exactly. The round's substance is the R17 gate record and the R-0398 repair, and the reviewer audited the repair against the SOURCE rather than reading it for plausibility: `_record` genuinely has ten call sites in `run_mission`, so the corrected count is true. The worker's three declared deviations are each correct behaviour — the denied-tool substitutions kept every proof byte-exact, the gate-5 plan value really does contradict the disk at the base commit and was reported rather than reconciled, and the 89-line handoff carries its DECISION D15 cause with no section dropped. The one gate that does NOT reproduce is gate 9's DESELECTED figure, registered as R-0400; its PASSED figure, which is the value that gates anything, reproduces exactly. What this gate does NOT say: it makes no claim about the ist-doc's new parenthetical span, which is wrong and is registered as R-0401.
<<<END GATE-R18>>>

<<<BEGIN FINDING-R400>>>
- R-0400 — Low — the state-file contract readers' DESELECTED count does not reproduce, and this branch's own integration-gate entry already contradicts it. The gates for R15, R16, R17 and R18 each record `216 passed, 16671 deselected` for the selection `-k "dashboard_contract or resource_safety or test_runner"`. Re-run at `386ef7b5` that same selection measures `216 passed, 16701 deselected`, and `python3 -m pytest -q --collect-only` measures `16917 tests collected` on two consecutive invocations. So 216 + 16701 = 16917 is internally consistent while 216 + 16671 = 16887 is thirty short, and the `Gate: R16` paragraph in this very file carries the number that settles it: its full-suite run measured `16898 passed, 19 skipped`, which is 16917 collected. The reviewer re-ran the full suite itself at `386ef7b5` and measured `16898 passed, 19 skipped in 143.68s` at exit 0, reproducing that total a third time. The last commit on this branch to touch `tests/` is `826fb5a3`, which is R15's work, so no change after R15 can explain a moving total. The reviewer did NOT determine why the earlier runs collected thirty fewer, and no cause is attributed here: there is no conditional-collection hook in the suite (`collect_ignore`, `allow_module_level`, `importorskip` all return nothing), `pyproject.toml` sets no `testpaths` or `norecursedirs`, and the gitignored `.remedy-wt/` scratch directory is not collected. This is Low because nothing green turns red: `216 passed` reproduces at every gate that reported it, and a deselected count gates nothing on its own. The consequence is narrower and real — three gates on this branch used deselected DELTAS as corroboration for a test-count claim ("+13 equals the 13 tests this round adds", "+10 for the 10 tests added"), and that arithmetic rests on a base number that is not currently reproducible. From here, a deselected count is reported as a raw measurement only, and the corroborating arithmetic for a test-count claim uses the passed count and `--collect-only`, both of which reproduce. OPEN.
<<<END FINDING-R400>>>

<<<BEGIN FINDING-R401>>>
- R-0401 — Low — the parenthetical that R-0398's repair added to `docs/system/autonomy-watchdog-v1.md` states a span that is not `run_mission`, and it still does not state the exclusion that produced the original off-by-one. The doc now reads "`_record` has ten call sites in `run_mission` (lines 936 to 1341)". `run_mission`'s `def` is at 936, but its last body line is the `return build_boundary_handoff(result, root)` at 1304; lines 1307 to 1338 are module-level constants — `IN_FLIGHT_JOB_STATES`, `BLOCKED_COMPLETIONS_BEFORE_ESCALATION`, `RETRYABLE_FAILURE_CLASSES` and `BOUNDARY_FAILURES_BEFORE_ESCALATION` — and 1341 is `def _is_retryable`, the next top-level definition. The count is unaffected, because the ten calls all sit between 1064 and 1296, which is why this is Low and not a correctness finding against the sentence. The defect is that the parenthetical was added for exactly one purpose — R-0398's own prescription, "a doc that states such a count states the span it counted over so a later reader can reproduce it" — and as written it does not serve it: a reader who counts `_record(` over 936 to 1341 finds ELEVEN occurrences, the same eleven that produced the original error, because the span given is wrong in one direction and the nested definition at 1036 is still not mentioned in the other. A repair that reproduces the defect's own failure mode for its next reader has not landed the lesson, only the number. It is registered rather than folded into R-0398's resolution so the record shows a repair being audited and found short, instead of a reviewer accepting its own prescription as met because a number changed. The fix is the DOCFIX2 rewrite in this same commit: the span becomes 936 to 1304 and the sentence names the nested definition it excludes. OPEN.
<<<END FINDING-R401>>>

<<<BEGIN LANDED-R401>>>
Landed: R-0401 — `docs/system/autonomy-watchdog-v1.md` now reads "ten call sites in `run_mission` (lines 936 to 1304, counting calls and not the nested definition at 1036)"; the DOCFIX2 rewrite pair, applied in this round's C1 alongside the finding that registers it.
<<<END LANDED-R401>>>

(3) REWRITE in `docs/system/autonomy-watchdog-v1.md` — DOCFIX2. FROM is these
    three consecutive lines exactly as they stand on disk:

<<<BEGIN DOCFIX2-FROM>>>
1341), and the executed move's entry and the blocked-completion escalation's
entry already fire in one pass at one number. The ledger's ordering is FILE order,
never a sort on this field.
<<<END DOCFIX2-FROM>>>

    TO is these three lines:

<<<BEGIN DOCFIX2-TO>>>
1304, counting calls and not the nested definition at 1036), and the executed
move's entry and the blocked-completion escalation's entry already fire in one
pass at one number. The ledger's ordering is FILE order, never a sort on it.
<<<END DOCFIX2-TO>>>

    Three lines to three lines, so the file stays at 216 lines. After the edit
    the FROM's first line `1341), and the executed move's entry and the` appears
    0 times and the TO's first line appears exactly 1 time.

(4) REWRITE in `.agent/context.md` — CONTEXTCOUNT. FROM is this one line:

<<<BEGIN CONTEXTCOUNT-FROM>>>
findings at the session close: THIRTY, next free id R-0400.
<<<END CONTEXTCOUNT-FROM>>>

    TO is this one line:

<<<BEGIN CONTEXTCOUNT-TO>>>
findings at R19: THIRTY-ONE, next free id R-0402.
<<<END CONTEXTCOUNT-TO>>>

    One line to one line, so `.agent/context.md` stays at 100 lines.

(5) WHOLE-FILE replacement of `.agent/plan.md` with the PLAN slice — 45 lines,
    applied byte for byte, nothing trimmed and nothing added:

<<<BEGIN PLAN>>>
# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0402.
Open findings: THIRTY-ONE — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368,
R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394, R-0395,
R-0396, R-0397, R-0399, R-0400, R-0401 — recomputed from `.agent/live_review.md`
at R19: 36 registered, 5 resolved (R-0383, R-0384, R-0388, R-0390, R-0398), no
duplicate id. R-0401's fix has LANDED but is not resolved; only a reviewer sets
`Done:`.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R19 — closure preparation. The R18 verdict is on the record, R-0398 is resolved
against the source, R-0400 and R-0401 are registered, the ist-doc's `_record`
span is repaired, and `docs/roadmap/features/T2_F077.md` now carries the Built
State section that closure precondition 4 requires. The other preconditions
already hold: the reviewer re-ran the full suite itself at `386ef7b5` and
measured 16898 passed, 19 skipped, exit 0.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: the evidence job, a
   FRESH review zip (a zip failure is a closure blocker), then the closure
   commit — STATUS `[x]`, the README count and tier sync in that SAME commit
   (R-0154, and tests/docs pins the count), and the final `.agent/` state —
   last on the branch, then the PR, which is NOT merged this session.
2. The next feature after F077 in STATUS order is F082 — Self-benchmark.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8).
- R14 shipped `mission resume` at exactly that scope, and DECISION F077 D12
  does not address the re-trip; no round yet owns it.
- Thirty-one open findings is the largest carry any feature has held.
- R-0396's amendment target, docs/agents/integration_gate.md, is outside this
  feature's change set, so every future gate reproduces the eight phantom
  ui_server base failures until some feature owns that doc.
<<<END PLAN>>>

── C2 slice ──────────────────────────────────────────────────

APPEND the BUILTSTATE slice to the END of `docs/roadmap/features/T2_F077.md`,
preceded by exactly one blank line. Touch no other line of that file. The file
currently ends with the `## Do not touch` section.

<<<BEGIN BUILTSTATE>>>
## Built State
- **T001 — the three evaluators, `packages/orchestration/watchdog.py`:** `Trip`
  is a frozen dataclass carrying exactly `kind`, `what`, `since_iteration` and
  `numbers` plus `to_json`, so the evidence triple cannot drift its keys between
  the evaluator that builds it and the caller that reports it. The three kinds
  are `TRIP_NO_PROGRESS`, `TRIP_BURN_ANOMALY` and `TRIP_GOAL_DRIFT`, with one
  pure evaluator each — `evaluate_no_progress`, `evaluate_burn_anomaly` and
  `evaluate_goal_drift` — and `evaluate_ledger` runs all three over one ledger
  in that fixed order, dropping non-trips. Thresholds live in config, not in
  code: `WatchdogThresholds` is resolved by `watchdog_thresholds_from_config`,
  the ONE function in the module that reaches outside, over the four keys
  `watchdog.no_progress_repeats` (3), `watchdog.burn_window` (3),
  `watchdog.burn_min_samples` (5) and `watchdog.burn_multiplier` (3.0). The burn
  tripwire is inert while `len(measured) < min_samples + window`, which is the
  "missions too young for a baseline" default this file's A9 section asks for.
  At T001 the module was import-only. Tests: `tests/orchestration/test_watchdog.py`,
  one firing and one near-miss fixture per tripwire.
- **T002 — pause, decision, dedup and the ledger entry, same module:**
  `act_on_trips` is the ONE writing function, and its docstring enumerates
  exactly what it writes: the mission STATUS once per call and only `active` →
  `paused`; one escalation record per unsuppressed trip on the job the mission
  last linked, deduped on `watchdog_decision_marker(kind)` so a class already
  awaiting an answer raises nothing further; and one `MOVE_WATCHDOG_TRIPPED`
  ledger entry per trip, whatever the decision outcome was. It returns one
  `TripAction` per trip, whose `decision_id`, `suppressed` and `note` let a
  reader tell suppression from an attachment failure. An empty trip list writes
  nothing at all. `watchdog_pass` is the loop seam: `run_mission` in
  `packages/orchestration/orchestrator_loop.py` imports it INSIDE its body and
  calls it once per iteration, so a trip on iteration k pauses before k+1
  dispatches, and the observing iteration's number is handed down rather than
  re-derived (DECISION F077 D6). The ledger's `iteration` field is an
  ATTRIBUTION, not a unique key (DECISION F077 D11).
- **T003 — the manual audit CLI and the report surface:** `evaluate_mission` is
  the read-only twin of `watchdog_pass` — same verdict over the same ledger, and
  not one write — and it backs `remedy mission watchdog <id>`
  (`_cmd_mission_watchdog`, registered `read_only`). `remedy mission resume <id>`
  (registered `write_metadata`) returns a paused mission to active through the
  same `_cmd_mission_set_status` body as `achieve`, `abandon` and `pause`.
  `latest_trips_from_ledger` reconstructs recorded trips out of a ledger,
  last-wins per kind in FILE order, and `_cmd_mission_show` leads a paused
  mission's report with the trip — placed in the command rather than in
  `render_mission_chain` so the renderer never imports `mission_state` and the
  import cycle the watchdog's in-body imports avoid is not built elsewhere.
  Tests: `tests/cli/test_mission_cmd.py`, `tests/orchestration/test_mission_e2e.py`.
- **Independence is pinned by a test, not by prose:** `evaluate_mission` writes
  nothing at all — no `set_mission_status`, no decision, no `save_job`, no ledger
  append, directly or through a callee — which is this file's Acceptance
  state-diff criterion. Built-state doc: `docs/system/autonomy-watchdog-v1.md`.
- **Known limit, deliberately not fixed here:** a mission resumed after its
  watchdog decision is answered still carries the tripping run in its ledger and
  trips again, for all three tripwires, so `mission resume` buys exactly one
  iteration. DECISION F077 D12 does not address the re-trip and no round owns it.
<<<END BUILTSTATE>>>

Done when:   Every gate below is EXECUTED and its REAL value recorded in the
             handback. Report values raw; a contradiction is reported, never
             reconciled by editing a file.

  1.  `git status --porcelain` is empty at the start of the round, after each
      commit, and at handback; `git worktree list` is exactly one line.
  2.  `.agent/STOP` is ABSENT — read it from disk at the start of the round and
      again at handback, and report both readings.
  3.  `.agent/authored/f077-r19.md` and `.agent/last_block.md` are byte-identical;
      report the shared sha256 and the line count of each.
  4.  In `.agent/live_review.md`: `grep -c '^Gate: R18 — '` is 1;
      `grep -c '^- R-0400 — '` is 1; `grep -c '^- R-0401 — '` is 1;
      `grep -c '^Done: R-0398 — '` is 1; `grep -c '^Landed: R-0398'` is 0;
      `grep -c '^Landed: '` is 2.
  5.  Open set recomputed MECHANICALLY from `.agent/live_review.md`, not carried
      from this block: `grep -c '^- R-[0-9]\+ — '` is 36, `grep -c '^Done: R-[0-9]\+ — '`
      is 5, so 31 are open; report that no id appears twice and that the next
      free id is R-0402.
  6.  `wc -l`: `.agent/live_review.md` 148, `.agent/plan.md` 45,
      `.agent/context.md` 100, `docs/system/autonomy-watchdog-v1.md` 216.
  7.  Pair application by shape. DOCFIX2 is a REWRITE: after C1 the FROM's first
      line appears 0x and the TO's first line appears 1x in the ist-doc.
      CONTEXTCOUNT is a REWRITE: FROM 0x, TO 1x in `.agent/context.md`. PLAN is a
      whole-file replacement: report the sha256 of `.agent/plan.md` and the
      sha256 of the PLAN slice extracted from the committed authored file, and
      state that they are EQUAL.
  8.  `grep -c '^## Built State' docs/roadmap/features/T2_F077.md` is 1, and the
      BUILTSTATE slice is the last content of that file.
  9.  `python3 -m pytest tests/docs/ -q` — record the count and exit code. This
      round changes a `docs/roadmap/**` file, so this gate is mandatory.
  10. `python3 -m pytest -q -k "dashboard_contract or resource_safety or test_runner"`
      — record the PASSED count and the DESELECTED count exactly as printed. Do
      not adjust either toward any number in this block or any earlier gate;
      finding R-0400 exists because that figure has not been reproducing.
  11. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  12. `python3 -m apps.cli.main integrity check --json` — record `passed`,
      `fail_count`, `check_count` and the `high_blockers_open` status.
  13. `git diff --check 386ef7b5..HEAD` produces no output.
  14. Per-commit insertions from `git show --numstat` for every commit this
      round; none may exceed 500. Report each number.
  15. `git diff --name-only 386ef7b5..HEAD` is exactly the seven ordered paths.
  16. Transport, disk to disk: for EACH of the seven slices (LANDED-TO-DONE,
      GATE-R18, FINDING-R400, FINDING-R401, LANDED-R401, DOCFIX2-TO,
      CONTEXTCOUNT-TO, BUILTSTATE, PLAN), extract it from the COMMITTED
      `.agent/authored/f077-r19.md` by its markers and compare it byte for byte
      against the region it was applied to. Report the sha256 of both sides for
      each and state that they are EQUAL. Nothing is retyped; no marker line
      reaches any target file.
  17. `git push -u origin feature/f077-autonomy-watchdog`, and the remote head
      equals the local head.

Handback:    Rewrite `.agent/handoff.md` completely (never append) per AGENTS.md
             and docs/agents/handback_template.md: feature and round, branch,
             base SHA `386ef7b5`, a per-commit table with paths and +/-, an
             item-status table covering C0a, C0b, C1, C2 and C3 with every item
             present exactly once, the verification table with every measured
             value from the gates above, the transport proofs, open-findings
             count, declared deviations, and the next expected action. Cap is 60
             lines; if the mandated content genuinely does not fit, exceed it and
             carry a "Deviations, declared" line naming the actual line count and
             the specific mandated content that caused the overage (DECISION
             D15). Never drop a section to meet the cap.
──────────────────────────────────────────────────────────────
