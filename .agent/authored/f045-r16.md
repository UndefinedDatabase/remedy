── STEP CLOSURE — F045 · ROUND 16 ────────────────────────────────────
Goal:        Close F045. Persist the R15 verdict, make the feature file's
             Built State current, record DECISION F045 D8, run the closure
             preconditions, build the evidence bundle and a FRESH review zip,
             then land the STATUS and README edits as the LAST commit and open
             the PR. The PR is NOT merged in this session.

Bundle:      C0a save this block · C0b point last_block at it · C1 the R15
             verdict · C2 the Built State · C3 DECISION D8 · ITEM 4
             preconditions · ITEM 5 evidence job · ITEM 6 the zip · C4 the
             closure commit · ITEM 8 the PR.

Change:      Exactly these files, nothing beyond them:
             - `.agent/authored/f045-r16.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1)
             - `docs/roadmap/features/T2_F045.md` (C2, APPEND only)
             - `.agent/decisions.md` (C3, APPEND only)
             - `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md`,
               `.agent/plan.md`, `.agent/handoff.md` (C4)
             NO production code. NO test files. If closure reveals a defect
             needing a code change, that fix is its OWN reviewer-gated round —
             report it and STOP, do not fix it here.

Insertion budget: C1 adds 2 lines. C2 and C3 are docs appends, each well under
the 500-insertion cap. C0a/C0b are single `.agent/**` state files, cap-EXEMPT
by DECISION F104 D1. C4 is two small rewrites plus three edited lines.

Staging: EXPLICIT PATHS ONLY. Never `git add -A`. Push after every commit.

── C0a / C0b ─────────────────────────────────────────────────────────
Write `.agent/authored/f045-r16.md`; commit alone.
  Subject: `chore(f045): save the R16 closure block verbatim`
Copy it to `.agent/last_block.md`, byte-identical; commit alone.
  Subject: `chore(f045): point last_block at the R16 block`

── C1 — the R15 verdict, findings persist FIRST ───────────────────────
File: `.agent/live_review.md`. APPEND at the very END, preceded by exactly one
blank line. Change nothing above it. ONE physical line — do not re-wrap.

REVIEWER-AUTHORED. Apply byte for byte from your saved copy. Do not edit or
shorten it. Never write a `Done:` paragraph of your own
(planner_reviewer_prompt.md §4.4). If you think it is wrong, STOP and report.

>>> GATE-R15 >>>
Gate: R15 — PASS. Every value re-measured by the reviewer against the disk, not against the handback. `cmp .agent/authored/f045-r15.md .agent/last_block.md` exit 0. The open set was RECOMPUTED from the record per pre-emission checklist item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — and is exactly three: R-0350, R-0354, R-0358, all Low, next free id R-0359. C1's numstat for `.agent/live_review.md` is `2 0`, and FINDING-358 was extracted from the committed `.agent/authored/f045-r15.md` between its own markers and found byte-identical in the file, so the application was disk-to-disk rather than a retype. The F045 surface re-run by the reviewer gives `123 passed` and the canary `tests/cli/test_golden_path.py` gives `42 passed`. THE INTEGRATION GATE: `comm -13` (branch-only failures) is EMPTY, which is the only sense in which that gate defines green (docs/agents/integration_gate.md step 3). The five failures common to both sides were reproduced independently by the reviewer at HEAD — `tests/orchestration/test_role_conventions.py`, all five raising `PromptSegmentError: prompt segment 'reviewer_conventions' is over its token cap: 954 tokens estimated, cap 800` — and they are NOT chargeable to F045: `role_conventions.py` maps that segment to `docs/agents/reviewer_conventions.md`, a file `git diff main..HEAD` shows this branch never touched, and `git diff 705feeb1..HEAD` shows byte-identical to its state at F115's accepted HEAD, whose ancestor `a85e82f5` (2026-08-12) is where the document grew past the cap. F115 therefore closed over these same five ids; the condition is a property of `main`, not of this branch. The `comm -23` attribution stands as recorded: six `tests/ui_server/test_live_state.py::TestUIServerIntegration` ids, each captured stderr naming `apps/ui/dist`, each passing serially at the merge base, and a second full base run whose FAILED list is `cmp`-identical to the branch's. Tree state at the verdict: `git status --porcelain` empty, `git worktree list` one line, `git branch --list 'tmp/*'` empty, `gh pr list --state open` `[]`. R15 changed no production code and no test file, and the round declared its own overage honestly rather than dropping a mandated section.
<<< GATE-R15 <<<

Commit C1 ALONE. Subject: `docs(f045): record the R15 verdict`
Gates: `grep -c "^Gate: R15 — PASS" .agent/live_review.md` → 1 ·
       `grep -c "^## Steps" .agent/live_review.md` → 1 ·
       `git show --numstat HEAD -- .agent/live_review.md` → `2 0`

── C2 — the feature file's Built State ────────────────────────────────
File: `docs/roadmap/features/T2_F045.md`. APPEND the section below to the very
END of the file, preceded by exactly one blank line. Change nothing above it.

This is an APPEND-shaped addition: the file currently has no `## Built State`
heading, so every line below is new.

STOP-ON-FALSE-CLAIM: every claim below was verified by the reviewer against the
source before emission. VERIFY THEM AGAIN before committing. If ANY claim does
not hold on disk, do NOT "improve" it — STOP and report which one and what the
disk says. A Built State section records NAMES, FILES and LITERAL VALUES only;
it deliberately says nothing about what a command PRINTS (F115 finding R-0343
cost four closure rounds to that exact class).

>>> BUILT-STATE >>>
## Built State — what F045 actually shipped (2026-08-14)

Three modules and one report field. Built and reviewed on branch
`feature/f045-loop-definitions` over rounds R1–R16.

**Spec + validation** (`packages/orchestration/loop_spec.py`): loops are a
TOP-LEVEL `[[loop]]` array of tables in `remedy.toml` — `LOOP_TABLE_KEY` is
`"loop"` (DECISION F045 D1) — never under `[remedy]`. The models
`LoopTrigger`, `LoopScope`, `LoopAction`, `LoopBudgets`, `LoopStopRules` and
`LoopSpec` all derive from `structured_base._Strict`, whose
`model_config = ConfigDict(extra="forbid")` IS the feature's "unknown fields
rejected" requirement — there is no separate key check. `LoopSpecError` carries
`loop_name` and `field` beside its message, so a caller can group errors
without re-parsing message text. Two loaders exist on purpose:
`load_loop_specs` raises on the FIRST error, which is what a listing wants,
while `validate_loop_specs` never raises and returns EVERY message in file
order, which is what a check wants. `LOOP_TEMPLATE_VARS` is
`frozenset({"project", "date"})`; any other `{placeholder}` fails VALIDATION
rather than surfacing as a runtime error. `LoopBudgets`' five field names are
spelled exactly as the keys of `budget_resolution._CONFIG_KEYS`
(`max_total_tokens`, `max_provider_calls`, `max_wall_clock_minutes`,
`max_cost_usd`, `deadline`) so the resolver needs no translation layer, and
`deadline` is validated by `datetime.fromisoformat` plus a REQUIRED `tzinfo`
(DECISION F045 D2 — the contract is mirrored, not imported).

**Materialization** (`packages/orchestration/loop_run.py`): `run_loop` is the
ONE dispatch point and routes on `action.kind`; `loop_to_job` remains exactly
the job-kind path. Provenance is two metadata keys —
`LOOP_REF_METADATA_KEY` (`"loop_ref"`) and `LOOP_UNATTENDED_METADATA_KEY`
(`"loop_unattended"`) — and DECISION F045 D5 puts them on the JOB, never on the
`Mission` record; the mission stays reachable from that same job through
`metadata["mission_id"]`. `LoopRunOutcome` carries `job`, `mission_id` and
`notice`. `root` isolates the WHOLE firing — job store, mission record and
job-to-mission link all land under it (findings R-0351 and R-0352, which is
what that threading exists for). `last_run_for_loop` reads the store through
`storage.list_jobs_safe`, which already sorts by `created_at` descending, so
the FIRST match is the most recent — no `max()` and no re-sort.

APPROVAL SEMANTICS, the load-bearing part: BOTH action paths stop at PLANNED.
Nothing in this module executes a task, approves a plan or implies `--yes`, and
`LoopSpec.unattended` is RECORDED in metadata for audit while changing nothing
about the job's state.

**CLI** (`apps/cli/commands/loop_cmd.py`; catalog ids `loop.list`,
`loop.validate` and `loop.run` in `apps/cli/command_catalog.py`): the handlers
are `_cmd_loop_list`, `_cmd_loop_validate` and `_cmd_loop_run`. Exit codes
reuse the existing table rather than inventing one — `EXIT_ERROR` 1,
`EXIT_USAGE` 2, `EXIT_NO_PROJECT` 3. `NEVER_RAN` is `"never"` and `INERT_MARK`
is `"inert"`. The listing carries its OWN legend, `INERT_TRIGGER_LEGEND` =
`"cannot fire until the scheduler exists; run such a loop manually"`, and
deliberately does NOT reuse `loop_spec.INERT_TRIGGER_NOTICE`
(`"scheduler not yet available; ran on demand"`), because that sentence reports
a RUN and a listing runs nothing — finding R-0355, pinned negatively so the
defect cannot drift back. DECISION F045 D7 — `--yes` skips the confirmation
prompt and approves NOTHING else.

**Report** (`packages/orchestration/run_report.py`): `ReportSources.loop_ref`
defaults to `""`, and `_header_lines` appends its `- Loop:` line only when that
value is non-empty, which is why every pre-F045 golden stays byte-identical.
`collect_report_sources` reads it through `LOOP_REF_METADATA_KEY` rather than a
string literal, so the report and the materializer cannot drift apart.

Deliberately NOT built, and the code says so rather than pretending otherwise:
there is no scheduler, no watcher and no repetition. `schedule` and `event`
triggers PARSE and VALIDATE but are inert — `INERT_TRIGGER_KINDS` and the
`LoopSpec.is_inert` property — and a loop with such a trigger still
materializes on demand. There is no `--config` option on any of the three
commands, because a second way to name the file would be a second config
location in all but name.

Cover: `tests/orchestration/test_loop_spec.py`,
`tests/orchestration/test_loop_run.py`, `tests/cli/test_loop_cmd.py` and
`tests/orchestration/test_run_report.py` — 123 node ids collected together.
<<< BUILT-STATE <<<

Commit C2 alone. Subject: `docs(f045): record the Built State of loop definitions`
Gates: `python3 -m pytest tests/docs/ -q` → report the count; the branch has
been holding 294 and it MUST NOT regress ·
`grep -c "^## Built State — what F045 actually shipped (2026-08-14)$" docs/roadmap/features/T2_F045.md` → 1

── C3 — DECISION F045 D8 ─────────────────────────────────────────────
File: `.agent/decisions.md`. APPEND at the very END, preceded by exactly one
blank line. Change nothing above it. Apply byte for byte.

>>> DECISION-D8 >>>
## DECISION F045 D8 (2026-08-14) — closure precondition 2 is met by the integration gate's own definition of green, not by a zero on the suite's failure counter

WHAT was decided. `docs/roadmap/STATUS_closure_protocol.md` precondition 2
requires the "full relevant suite green". At F045's closure the full suite ends
`5 failed, 16769 passed, 19 skipped`, exit 1. F045 closes anyway, with the five
named in the STATUS verdict as PASS_WITH_RISKS and recorded here, because the
word doing the work in that precondition is RELEVANT and the five are not.

WHY this reading and not the other. `docs/agents/integration_gate.md` step 3
defines the gate's question as `comm -13 base_failed.txt branch_failed.txt` —
the failures the BRANCH introduces — and step 4 makes only "a reproducible
branch-only failure coupled to feature code" a blocker. F045's `comm -13` is
EMPTY. The five ids are `tests/orchestration/test_role_conventions.py`
parametrizations raising `PromptSegmentError: prompt segment
'reviewer_conventions' is over its token cap: 954 tokens estimated, cap 800`.
`packages/orchestration/role_conventions.py` maps that segment to
`docs/agents/reviewer_conventions.md`; `git diff main..HEAD` shows this branch
never touched that file, and the document is byte-identical to its state at
F115's accepted HEAD `705feeb19c871db6313828d76ad4e1d9e0cc4d58`, whose ancestor
`a85e82f5` (2026-08-12) is the merge that grew it past the cap. So F115 closed
over these same five ids, on the same condition, and the condition belongs to
`main` rather than to any feature branch.

The alternative — read precondition 2 as a literal zero on the failure counter
— was rejected because it makes closure depend on a defect no feature branch
may repair. AGENTS.md forbids mixing an unrelated fix into a feature branch
("Never mix unrelated features or fixes in the same branch", "no while-I'm-here
edits"), so F045 cannot lawfully fix `reviewer_conventions.md`. Under the
literal reading, EVERY feature would be blocked by a document none of them
touch, and the roadmap would stall on an unrelated file — a deadlock the
protocol's own "Failure honesty" section never contemplates, since it lists
repair, `[!]`, or an operator decision, and the repair is out of scope by rule.

CONSEQUENCE. The over-cap document is recorded as a closure CANDIDATE in
`.agent/candidates.md` rather than as an F045 finding (no R-id is spent — the
protocol's "Closure-candidate findings" rule), so the next feature's first
reviewed round must register or resolve it. It deserves its own branch: the
segment is 154 tokens over an 800-token cap, and trimming a reviewer-facing
conventions document is a content decision, not a mechanical one.

HOW TO REVERSE. Delete this decision and treat precondition 2 as a literal
zero. Doing so requires fixing `docs/agents/reviewer_conventions.md` first, in
its own branch, because otherwise nothing can close at all — which is precisely
the outcome this decision exists to avoid.
<<< DECISION-D8 <<<

Commit C3 alone. Subject: `docs(f045): record the closure precondition ruling`
Gate: `grep -c "^## DECISION F045 D8 " .agent/decisions.md` → 1

── ITEM 4 — preconditions (no commit unless a file changes) ──────────
Run and record RAW output + exit code for each:
  `python3 -m apps.cli.main integrity check --json`   → must be `"passed": true`
  `git status --porcelain`                            → must be EMPTY
  `git rev-list --left-right --count origin/feature/f045-loop-definitions...HEAD`
  `git worktree list`                                 → exactly one line
If integrity check is not passed, STOP and hand back with the raw output. Do
not work around it.

NOTE on the `remedy` CLI: bare `remedy …` invocations are denied in this
environment. `python3 -m apps.cli.main …` is the same entry point and is what
the reviewer used. If the module form also fails, record the raw error and say
so — do not silently substitute a third path.

── ITEM 5 — the evidence job ─────────────────────────────────────────
Use the canonical producer, never a bare gate writer:
`packages.orchestration.job_evidence.create_manual_completion_bundle(
     review_feature_id="f045", ...)`.

  - Write the evidence directory under `.remedy-wt/` (gitignored) so it NEVER
    enters the base..HEAD review subject. A pre-committed evidence dir packages
    as BLOCKED_EVIDENCE.
  - `base_commit` is the FULL 40-char merge base:
    `cb3ef34fddbf0efa5799d8de93cb2d8e66566d20`
  - Record the evidence job id. Use `f045-closure` as the job id, matching the
    F103/F104/F105/F107/F111/F115 precedent in `docs/roadmap/STATUS.md`.

Heed EVERY producer pitfall in `docs/roadmap/STATUS_closure_protocol.md` — they
surface only at zip time:
  (a) `verification_runs` entries need a sha256-hex `output_hash`, valid
      `VerificationTests` totals, and the FULL-LENGTH `base_commit`.
  (b) verification records need non-empty node ids with
      `len(node_ids) == selected` — get REAL ids with `--collect-only`.
  (c) `test_files` entries are FILES, never directories.
  (d) the `VerificationTests` `run_id` must match `^vr-\d{4,}$`.
  (e) NEVER put a full-suite node-id list in a verification record.

Record the CLEAN SCOPED suites and nothing else:
  `tests/orchestration/test_loop_spec.py`
  `tests/orchestration/test_loop_run.py`
  `tests/cli/test_loop_cmd.py`
  `tests/orchestration/test_run_report.py`
Together they collect 123 node ids (reviewer-verified) and the reviewer scanned
them for absolute paths and secret-like strings and found none. Do NOT include
`tests/ui_server/**`, `tests/orchestration/test_role_conventions.py`, or any
redaction-torture parametrization. The full-suite proof rides in the committed
`.agent/gate_f045_r15/` evidence and in the reviewer's own re-run.

── ITEM 6 — the review zip: MANDATORY, FRESH, from a CLEAN tree ──────
In this order:
  1. `git status --porcelain` → must be EMPTY. If it is not, STOP.
  2. `git push`
  3. Record the FULL 40-char HEAD sha. This is `accepted HEAD` — the head the
     zip and the verdict cover, i.e. AFTER C3 and BEFORE the closure commit.
  4. `bash scripts/make_review_zip.sh --evidence-dir <the .remedy-wt evidence dir>`
Verify `committed_review_subject` spans BASE..HEAD and the zip import check
passes. Record the package filename and its SHA-256.
If the build FAILS: record the raw error VERBATIM in the handoff, author no
`[x]` line, STOP, hand back. A failing zip is a closure BLOCKER.

── C4 — the closure commit, LAST on the branch ───────────────────────
It touches EXACTLY `docs/roadmap/STATUS.md`, `README.md` and final `.agent/`
state — nothing else (Rule A4, R-0154).

(a) `docs/roadmap/STATUS.md` — REWRITE this single line, touching no other.
    The FROM matches exactly once (reviewer-verified).
FROM:
- [~] F045 — Loop definitions
TO (fill ONLY the four angle-bracket slots from ITEMs 5 and 6):
- [x] F045 — Loop definitions (T001–T003 complete; accepted 2026-08-14 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job <EVIDENCE_JOB_ID> · package <ZIP_FILENAME> · SHA-256 <ZIP_SHA256> · accepted HEAD <FULL_40_CHAR_HEAD_SHA>)

(b) `README.md`, SAME commit — exactly two REWRITE pairs. Each FROM matches
    exactly once (reviewer-verified). If either FROM does not match byte for
    byte, STOP and report the actual line rather than guessing.
FROM: 45 of 255 registered items accepted. Next: F045 (Loop definitions).
TO:   46 of 255 registered items accepted. Next: F057 (Rate-limit-aware scheduler).
FROM: | 2 | Minimal Self-Build Runtime | 6 | 14 |
TO:   | 2 | Minimal Self-Build Runtime | 8 | 14 |

    The tier row goes 6 → 8, NOT 6 → 7, and this is deliberate. The table's
    rule is the feature file's tier prefix: counting `- [x] F<id>` lines in
    STATUS.md whose `docs/roadmap/features/T<n>_F<id>.md` exists reproduces
    EVERY total in that table (16, 22, 14, 26, 16, 29, 16, 15, 12, 12, 12, 10,
    9, 8, 10, 10, 10, 8). By that rule Tier 2 already stands at SEVEN accepted
    — F103, F104, F105, F107, F111, F115 and F254 — while the README says 6,
    because the F111 closure commit `98a49b5c` incremented the count line and
    left the tier row alone (every other Tier 2 closure incremented it:
    `8eb93954` 0→1, `64228c05` 1→2, `ef9d4ae0` 2→3, `76fb0191` 3→4,
    `3c017c4e` 4→5, `57a24947` 5→6). F045 makes it eight. No test pins this
    cell, which is why the drift survived. DECLARE this correction explicitly
    in the handoff and the PR description as a pre-existing off-by-one that
    F045's mandated README sync necessarily corrects — do not bury it.
    VERIFY the derivation yourself before committing; if your count disagrees
    with 8, STOP and report your numbers rather than writing either value.

(c) `.agent/candidates.md` — REPLACE the `(empty — …)` line with the two
    candidate entries below, keeping the file's existing header block and its
    blockquote intact. Apply byte for byte.

>>> CANDIDATES >>>
- The reviewer-conventions document is over its prompt-segment token cap, and
  `main` is red because of it. `docs/agents/reviewer_conventions.md` estimates
  954 tokens against a cap of 800, so `prompt_segments` raises
  `PromptSegmentError` and five `tests/orchestration/test_role_conventions.py`
  ids fail on `main` itself. Present since `a85e82f5` (2026-08-12); F115 and
  F045 both closed over it under DECISION F045 D8. No feature branch may fix it
  without mixing an unrelated fix (AGENTS.md), so it needs its own branch:
  trimming ~154 tokens from a reviewer-facing conventions document is a content
  decision. · source F045 · 2026-08-14
- The README tier table is unpinned and silently drifted. No test in
  `tests/docs/` counts the `Done` column of the `## Status` table, while the
  accepted-count line beside it IS pinned by
  `test_the_readme_accepted_count_equals_the_status_count`. The Tier 2 cell
  therefore sat at 6 while the ledger said 7 from the F111 closure
  (`98a49b5c`, 2026-08-13) until F045's closure corrected it to 8. A pin
  deriving each row from the feature files' tier prefixes would have caught it
  the same day. · source F045 · 2026-08-14
<<< CANDIDATES <<<

(d) Rewrite `.agent/plan.md` — UNDER 50 lines, keeping `## Goal` and
    `## Next Steps` — to the CLOSED state: F045 closed, the PR number, the
    accepted HEAD, open findings THREE (R-0350, R-0354, R-0358), all Low and
    carried as documented risks, next free id R-0359, and the next action being
    the Open PR Gate at the next feature's start. End with, verbatim:
Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrationsgate ✅ · Closure ✅) — gemessen

(e) Update `.agent/context.md` ONLY if it is now stale. If you touch it,
    validate the draft against EVERY test that reads it — run
    `rg -ln 'context.md' tests/` and satisfy all of them together: the
    dashboard contract wants the substring "Steps" and "## Active Branch" with
    a `feature/` slug, `test_test_runner.py` wants a roadmap F-id, and
    `tests/regression/test_resource_safety.py` wants "resource" or "pytest"
    (finding R-0162 — the first repair fixed one reader and tripped another).

(f) Rewrite `.agent/handoff.md` as the closure handback per
    `docs/agents/handback_template.md`. Cap 60 lines; if MANDATED content
    genuinely does not fit, exceed it with a "Deviations, declared" line naming
    the actual count and the mandated content that caused it. NEVER drop a
    section. Last line repeats the plan's Fortschritt verbatim.

BEFORE committing C4 run BOTH, and they must be green IN THE SAME COMMIT as the
edits:
  `python3 -m pytest tests/docs/ -q`                    (the README/STATUS count
     pair is pinned by `test_the_readme_accepted_count_equals_the_status_count`
     in `tests/docs/test_docs_consistency.py`, which counts `^- \[x\] F\d{3} — `
     lines in STATUS.md and pins the README's N to it)
  `python3 -m pytest tests/cli/test_golden_path.py -q`  (the canary)
Commit subject: `docs(f045): close F045 in the roadmap ledger`

── ITEM 8 — the PR ───────────────────────────────────────────────────
`git push`, then `gh pr create` per the AGENTS.md PR workflow. Base `main`,
head `feature/f045-loop-definitions`. The description carries: what changed and
why; key decisions (F045 D1 through D8, naming D8's closure ruling explicitly);
how to review; a changed-files table; the latest verdict (R15 PASS; feature
PASS_WITH_RISKS); the open-findings count (3 — R-0350, R-0354, R-0358, all Low,
named); the declared README tier-row correction from (b); and runtime actuals —
rounds, wall clock, models, tokens — with `not-measured` wherever the ledger has
no number, NEVER a guess.
Do NOT merge it. It merges at the next feature's start via the Open PR Gate.
Commit subjects and the PR title must never contain a leading-slash token, an
absolute path, or a secret-like string — the metadata scanner rejects them and
blocks closure.

── Constraints ───────────────────────────────────────────────────────
- AGENTS.md is highest authority. Self-review loop before EVERY commit.
- Explicit-path staging only. Never `git add -A`. Push after every commit.
- Never work on main. Never force-push. Never merge. Never rewrite history.
- The closure commit is the LAST commit on the branch. Nothing after it but
  the PR.
- NO production code, NO test files. A needed fix is a STOP and a report.
- Authored texts (GATE-R15, BUILT-STATE, DECISION-D8, CANDIDATES, the STATUS
  and README pairs) are applied byte for byte from your saved copy. No trailing
  whitespace anywhere. Verify with a Python scan (`l != l.rstrip()`), and say
  which command you actually ran if `grep -rn ' $'` is denied.
- Never write a `Done:` paragraph; use `Landed: R-XXXX — <one line>`.
- If ANY precondition, the evidence job, or the zip fails: STOP, record the raw
  output, hand back. Do NOT author a `[x]` line for a feature that did not meet
  its preconditions. Pretending completion is the one unforgivable failure mode.

── Done when ─────────────────────────────────────────────────────────
Record the command, the exit code and the REAL output for every one.

  (a) `cmp .agent/authored/f045-r16.md .agent/last_block.md` → exit 0
  (b) C1's three gates
  (c) C2's `tests/docs/` count (≥ 294, no regression) and its grep → 1
  (d) C3's grep → 1
  (e) `python3 -m apps.cli.main integrity check --json` → `"passed": true`
  (f) evidence job id · zip filename · zip SHA-256 · accepted HEAD (40 chars)
  (g) `tests/docs/` and the canary, both green, in the closure commit
  (h) `grep -c "^- \[x\] F045 — " docs/roadmap/STATUS.md` → 1 AND
      `grep -c "^- \[~\] F045" docs/roadmap/STATUS.md` → 0
  (i) `grep -c "46 of 255 registered items accepted" README.md` → 1 AND
      `grep -c "| 2 | Minimal Self-Build Runtime | 8 | 14 |" README.md` → 1
  (j) the open set, recomputed from the record after C1:
      python3 - <<'EOF'
      import re
      lines=open('.agent/live_review.md').read().splitlines()
      reg=[m.group(1) for l in lines if (m:=re.match(r'^- (R-\d+) — ',l))]
      done=[m.group(1) for l in lines if (m:=re.match(r'^Done: (R-\d+) — ',l))]
      print("OPEN",sorted(set(reg)-set(done)))
      EOF
      → must print exactly: OPEN ['R-0350', 'R-0354', 'R-0358']
  (k) `git status --porcelain` at the end → REPORTED VERBATIM, must be EMPTY
  (l) `git worktree list` → exactly one line
  (m) `git log --oneline c6b0aeb7..HEAD` → REPORTED
  (n) the PR URL

Handback:    completion report plus the rewritten `.agent/handoff.md`. Include
             the per-commit table, all raw output, the item-status table (C0a,
             C0b, C1, C2, C3, ITEM 4, ITEM 5, ITEM 6, C4, ITEM 8 — each exactly
             once, `done`/`skipped`/`deviated` with a reason), and grep proof
             that the applied STATUS line, the applied GATE-R15 entry, the
             Built State heading, DECISION D8 and the candidate entries are
             byte-identical to the authored text. The closure VERDICT is the
             reviewer's, not yours.
──────────────────────────────────────────────────────────────────────
