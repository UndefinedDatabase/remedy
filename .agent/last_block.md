BEGIN BLOCK f045-r4-1
── STEP T003a/3 — F045 Loop definitions · ROUND 4 (findings, decisions, D4) ──

Goal:        Register the two R3 block defects, close the STOP re-check gap on
             disk, land DECISIONs F045 D4 and D5 with rationales the code
             supports, validate the mission action's goal template, and then
             close the four findings that were already open.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 register R-0348/R-0349 ·
             ITEM 3 C2 protocol STOP re-check · ITEM 4 C3 decisions D4+D5 ·
             ITEM 5 C4 loop_spec mission-template validation · ITEM 6 C5 its
             tests · ITEM 7 C6 the four finding resolutions · ITEM 8 C7 plan +
             handoff · ITEM 9 gates.
Change:      .agent/authored/f045-r4-1.md · .agent/last_block.md ·
             .agent/live_review.md · docs/agents/self_drive_protocol.md ·
             .agent/decisions.md · packages/orchestration/loop_spec.py ·
             tests/orchestration/test_loop_spec.py · .agent/plan.md ·
             .agent/handoff.md. Nothing else. Do NOT edit loop_run.py,
             test_loop_run.py, config.py, budget_resolution.py,
             mission_state.py, packages/core/models.py or anything under apps/.
Constraints: SPLIT round. Never work on main; never force-push; no PR this
             round; merge nothing. Do-not-touch (feature file):
             scheduling/cron, the routine library, notifications. This round
             adds NO CLI and NO dispatch — `run_loop`, `last_run_for_loop` and
             the shared job builder are R5's, deliberately deferred so this
             block stays under the reviewer's own size cap.
Insertion budget, per commit (counter-measure for R-0345): C0a ≈ block size ·
             C0b ≈ block size · C1 ≤ 12 · C2 ≤ 12 · C3 ≤ 65 · C4 ≤ 12 ·
             C5 ≤ 45 · C6 ≤ 12 · C7 ≤ 115. ITEM 1 is ordered as TWO commits
             because one commit carrying both copies of the block exceeds the
             500-insertion cap — that is not a deviation this time, it is the
             plan.
Done when:   every gate in ITEM 9 has been RUN and its real exit code and
             output recorded.
Handback:    completion report + rewrite .agent/handoff.md

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r4-1.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R4 block verbatim`
C0b: copy that same file over `.agent/last_block.md`, replacing the R3 block.
Commit subject: `chore(f045): point last_block at the R4 block`
Prove it: cmp .agent/authored/f045-r4-1.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — register the two R3 block defects ═══
File `.agent/live_review.md`. APPEND at the END of the `## Findings` section,
after R-0347's paragraph, one blank line between paragraphs. Two lines:

- R-0348 — Medium — a DECISION's rationale contradicted the module it described. The R3 block's ITEM 3 ordered DECISION F045 D5 as verbatim bytes, asserting that loop provenance on a mission "could only be added as a NEW FIELD, which moves that schema version". `packages/orchestration/mission_state.py` documents the opposite in `Mission`'s own class docstring: `mission_plan` (F069) is "ADDITIVE and OPTIONAL" and "which is why :data:`MISSION_SCHEMA_VERSION` does NOT move for it". The same ordered text told a later reader to reverse the decision by bumping that version, which `Mission.from_json` turns into `unknown mission schema version` for every record already on disk, and its field enumeration named seven fields while the dataclass has nine — `dossier_ref` and `mission_plan` were missing. The R3 worker refused to append the bytes and reported the contradiction instead of "improving" them, which was the only correct move: a block that orders verbatim text leaves the worker no repair path. The decision's CONCLUSION — provenance rides on the job — was never in doubt; only its reason was false, and a false reason in `.agent/decisions.md` is worse than no entry, because that file exists to be trusted later without re-derivation. This is pre-emission checklist item 8 (docs/agents/planner_reviewer_prompt.md §3): the reviewer read the class definition and asserted a property established in the class DOCSTRING it had not read. Counter-measure, applied from R4 on: a DECISION that states what a change to another module would COST quotes the sentence in that module which establishes the cost, or does not state the cost at all. OPEN.

- R-0349 — Medium — the block attributed a behaviour to a function that does not exist. The R3 block's ITEM 8 ordered the job's `mission` field to be set to the mission's goal and justified it as "the shape `mission_state.start_follow_up` already uses". `grep -rn "start_follow_up" --include=*.py .` returns nothing anywhere in the repository; the function that builds a mission-linked job and sets `mission=mission.goal` is `mission_state.continue_mission`, at `packages/orchestration/mission_state.py:893`. The R3 worker refused to substitute the correct name on its own authority and reported it, correctly: this is the R-0338/R-0342/R-0343 family — a document naming a symbol whose behaviour was never run — and a silent rename would have buried the reviewer's error under a plausible-looking fix. Nothing landed wrong. Counter-measure, applied from R4 on: every symbol a block cites as precedent is grepped to its own definition before emission, and the block carries the `file:line` where it was found so the worker can check the citation in one command. OPEN.

Commit subject: `docs(f045): register R-0348 and R-0349, the R3 block defects`

═══ ITEM 3 · C2 — the STOP re-check point (fixes R-0347) ═══
File `docs/agents/self_drive_protocol.md`. APPEND-shaped pair: the TO contains
the FROM verbatim and adds a paragraph after it.
FROM (exactly one line):
Each round is: author → delegate → review → verdict.
TO:
Each round is: author → delegate → review → verdict.

Before AUTHORING each round the reviewer re-reads `.agent/STOP` from disk.
Phase 0 runs once at session start, G6 binds at any point, and a sentinel that
appears mid-session is otherwise invisible until an unrelated gate trips over
it (finding R-0347). Every block's gate list therefore also keeps a
`git status --porcelain` gate, and every handoff that names the next session's
first action names Phase 1 rule 1 before rule 2.

Commit subject: `docs(agents): give the stop sentinel a re-check point`

═══ ITEM 4 · C3 — DECISIONs D4 and D5 ═══
File `.agent/decisions.md`. APPEND at the very END, preceded by one blank
line. Change nothing above it.

## DECISION F045 D4 (2026-08-13) — `action.mission` is a GOAL TEMPLATE, validated like `goal_template`

`LoopAction.mission` carries a mission's GOAL as operator-authored text, not a
mission id and not a reference to an already-stored mission. A loop that named
an id could not be versioned in the config file this feature requires: the id
does not exist until the mission is created, and it differs per machine. The
text therefore accepts the same `{project}` and `{date}` placeholders as
`action.goal_template`, and `loop_spec._semantic_errors` rejects any OTHER
placeholder at VALIDATION time, mirroring the goal_template rule directly above
it. The feature file's A9 line — "Goal templates may reference simple variables
(project slug, date); undefined variables fail validation, not runtime" — is
written about goal templates; applying it to only one of the two
operator-authored templates in the same table would be an accident, not a
design.

Alternatives considered: (a) `action.mission` names a stored mission id —
rejected, ids are per-machine runtime values and cannot live in versioned
config; (b) leave the mission text unvalidated — rejected, an undefined
placeholder would then reach run time, which A9 forbids for the sibling field.

Reverse this decision by deleting the `action.mission` branch in
`_semantic_errors` and treating the field as an opaque string.

## DECISION F045 D5 (2026-08-13) — a mission-action loop records `loop_ref` on the JOB, not on the Mission

A loop firing produces one JOB. A `Mission` is a persistent goal whose chain
GROWS: `mission_state.continue_mission` (`mission_state.py:893`) appends
follow-up jobs that have nothing to do with any loop. A `loop_ref` on the
mission record would therefore claim an entire growing chain came from one
loop, and would stop being true the first time an operator types a follow-up.
The job is the unit that actually came from the loop, evidence and reports are
job-shaped, and the feature's Acceptance line asks for `loop_ref` visible in
evidence and report. So the provenance stays on the job, under the
`LOOP_REF_METADATA_KEY` metadata key T002 established, and the mission remains
reachable from that same job through `metadata["mission_id"]` and through
`mission_state.mission_for_job`. `mission_state.py` is not touched at all.

Explicitly NOT the reason: schema cost. `Mission`'s own class docstring records
the F069 precedent — `mission_plan` is "ADDITIVE and OPTIONAL", "which is why
:data:`MISSION_SCHEMA_VERSION` does NOT move for it" — so a `loop_ref: str = ""`
field could have been added without a bump. This paragraph exists because the
first draft of this decision asserted the opposite and was refused at the R3
gate (finding R-0348). The decision rests on where provenance is TRUE, not on
what recording it elsewhere would cost.

Alternatives considered: (a) add an additive optional `loop_ref` to `Mission` —
rejected, it attributes a whole chain to one firing and edits another feature's
module from inside this branch; (b) record nothing on the mission path —
rejected, Acceptance requires `loop_ref` in evidence.

Reverse this decision by adding `loop_ref: str = ""` to `Mission` as an
additive optional field — no version bump, per the `mission_plan` precedent —
and writing it in the mission path; the job-side key stays either way, because
evidence reads the job. Do NOT reverse it by bumping
`MISSION_SCHEMA_VERSION`: `Mission.from_json` raises `unknown mission schema
version` for any value but the current one, so a bump invalidates every mission
already stored.

Commit subject: `docs(f045): record decisions D4 and D5`

═══ ITEM 5 · C4 — mission-template validation (DECISION D4) ═══
File `packages/orchestration/loop_spec.py`, function `_semantic_errors`.
APPEND-shaped pair: the TO contains the FROM verbatim.
FROM:
    if spec.action.goal_template:
        for var in _undefined_template_vars(spec.action.goal_template):
            fail(f"goal_template references undefined variable '{var}'",
                 "action.goal_template")

    return errors
TO:
    if spec.action.goal_template:
        for var in _undefined_template_vars(spec.action.goal_template):
            fail(f"goal_template references undefined variable '{var}'",
                 "action.goal_template")

    # DECISION F045 D4: action.mission is an operator-authored goal TEMPLATE
    # too, so the same placeholders fail VALIDATION here rather than surfacing
    # as a run-time error (feature file, A9).
    if spec.action.mission:
        for var in _undefined_template_vars(spec.action.mission):
            fail(f"action.mission references undefined variable '{var}'",
                 "action.mission")

    return errors

Commit subject: `feat(f045): validate the mission action's goal template`

═══ ITEM 6 · C5 — tests for D4 ═══
File `tests/orchestration/test_loop_spec.py`. APPEND two tests at the END,
reusing whatever helper the file already has for writing a `remedy.toml` under
`tmp_path`. Read the file first; do not invent a second helper.
NOTE (counter-measure for R-0344): neither assertion may match against a string
that carries a filesystem path.
 1. a mission action whose text uses BOTH `{project}` and `{date}` validates
    clean — `validate_loop_specs` returns `[]`.
 2. a mission action whose text uses `{sprint}` produces exactly one message,
    `loop '<name>': action.mission references undefined variable 'sprint'` —
    assert the whole returned list equals that single-element list, the shape
    line 115 of this file already uses.
Commit subject: `test(f045): pin the mission template validation`

═══ ITEM 7 · C6 — the four finding resolutions ═══
File `.agent/live_review.md`. Four APPEND-shaped edits: each existing finding
paragraph keeps its bytes and gains a `Done:` line directly BELOW it, one blank
line between. Change nothing else; the trailing `OPEN.` inside each paragraph
stays exactly as it is, because the `Done:` line is what marks resolution in
this repository. R-0348 and R-0349 stay OPEN and get no `Done:` line — their
counter-measures are applied by THIS block and are gated at the next round.

Below R-0344's paragraph:
Done: R-0344 — RESOLVED at the R4 gate. Verified against the disk, not the report: no assertion in `tests/orchestration/test_loop_run.py` matches a string that carries a filesystem path — its assertions read `job.user_prompt`, `job.name`, `job.project_id`, `job.metadata`, `job.budgets`, `job.state` and two `LoopRunError` messages whose text names a loop and a variable and no path. The R1 defect's own site is fixed too: `tests/orchestration/test_loop_spec.py:265` scans `reported_keys` rather than whole warning strings, and `:115` asserts the exact message `loop 'typo-carrier': unknown key 'cadence'`, which contains no path. The counter-measure is now load-bearing rather than remembered: the two tests this round adds were ordered under the same NOTE and assert whole message lists, not substrings of paths.

Below R-0345's paragraph:
Done: R-0345 — RESOLVED at the R4 gate. Verified against the disk, not the report: `git log --numstat` over the R2 range shows SIX commits at 491, 5, 59, 168, 182 and 74 insertions — every one under the AGENTS.md 500-insertion cap, and `packages/orchestration/loop_run.py` (168) landed in `6794e7f0` while `tests/orchestration/test_loop_run.py` (182) landed separately in `5d613f49`, so no commit bundled a new module with its test file. The 491-insertion block save `f99a3407` is the largest and is the one the counter-measure most nearly missed; this round's block splits its own save into two commits ahead of time rather than discovering the cap at commit time.

Below R-0346's paragraph:
Done: R-0346 — RESOLVED at the R4 gate. Verified against the disk, not the report: the DECISION headings that existed only in a module docstring now live in `.agent/decisions.md`, and this round's change set carries that file again for D4 and D5 rather than leaving them in `loop_spec.py`'s comments. The counter-measure is applied, not restated: every block since R2 that carries a DECISION has carried `.agent/decisions.md` in its change set, and the R3 block did too — it halted for a different reason.

Below R-0347's paragraph:
Done: R-0347 — RESOLVED at the R4 gate. Fixed on disk rather than in reviewer habit, which is the whole point of the finding: `docs/agents/self_drive_protocol.md` Phase 2 now orders the `.agent/STOP` re-read before each round is authored, so the sentinel has a re-check point inside the round loop instead of only in the one-shot Phase 0 probe. The gap was verified to be real before it was closed — `grep -c "re-reads" docs/agents/self_drive_protocol.md` printed 0. The reviewer performed the re-read before authoring both R3 and R4, finding the sentinel absent each time, and both blocks kept the `git status --porcelain` gate the counter-measure requires.

Commit subject: `docs(f045): resolve R-0344 to R-0347`

═══ ITEM 8 · C7 — plan and handoff ═══
Rewrite `.agent/plan.md` (AGENTS.md: under 50 lines, keeps `## Goal` and
`## Next Steps`): Current Step becomes R4 done — R-0344 to R-0347 resolved,
R-0348 and R-0349 registered, D4 and D5 landed, the mission action's template
validated; R5 = the dispatch (`run_loop`, the inert notice, the shared job
builder, `last_run_for_loop`) and R6 = the CLI. Open findings becomes 2
(R-0348, R-0349); next free finding ID R-0350. Fortschritt becomes
`Fortschritt: ~45 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung`. Keep the
first two existing Risks; replace the third with: the mission path lands in R5
and writes real mission records, so every test that touches it passes an
explicit `root`.
Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). It carries: feature + round,
branch, every commit SHA, a per-commit changed-files table, the raw results of
ITEM 9's gates, open-findings count 2, an item-status table with one row per
ITEM 1-9, the next expected action, and the Fortschritt line verbatim. The
"next expected action" section names Phase 1 rule 1 (read `.agent/STOP` from
disk) BEFORE rule 2 (the Open PR Gate) — the R-0347 counter-measure; its
absence is a finding.
Commit subject: `docs(f045): update the plan and handoff for R4`

═══ ITEM 9 · gates ═══
Run every command; record the REAL exit code and REAL output. Report counts as
OBSERVED — do not predict them and do not restate a count this block gave you.

(a) cmp .agent/authored/f045-r4-1.md .agent/last_block.md
(b) grep -c "^- R-0348 — Medium" .agent/live_review.md
(c) grep -c "^- R-0349 — Medium" .agent/live_review.md
(d) grep -c "^Done: R-" .agent/live_review.md
(e) grep -c "^## DECISION F045 D" .agent/decisions.md
(f) grep -c "re-reads" docs/agents/self_drive_protocol.md
(g) python3 -m pytest tests/orchestration/test_loop_spec.py tests/orchestration/test_loop_run.py -q
(h) python3 -m pytest tests/test_agent_tooling.py -q
(i) python3 -m pytest tests/docs/ -q
(j) python3 -m pytest tests/cli/test_golden_path.py -q      (canary)
(k) python3 -m ruff check packages/orchestration/loop_spec.py tests/orchestration/test_loop_spec.py
(l) git status --porcelain                                  → EMPTY

Gates (b)-(f) are scoped to their target FILE, never to this block or to
`.agent/authored/**`, both of which legitimately contain the same strings.

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r4-1
