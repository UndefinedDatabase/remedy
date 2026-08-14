── STEP CLOSURE / R20 — F077 Autonomy watchdog ────────────────────────
Round base — the SHA every range gate in this block measures from: c0909569

Goal:  Close F077. Record the R19 verdict, register R-0402, run the closure
       preconditions, build the evidence bundle and a FRESH review zip, then
       land the STATUS and README edits as the LAST commit on the branch and
       open the PR. The PR is NOT merged in this session. The feature file's
       Built State is already current from commit 4fa56b23, so precondition 4
       holds and this round must NOT touch the feature file again.

Bundle:  C0a save this block · C0b mirror it · C1 the R19 verdict + R-0402 +
         the counts it invalidates · ITEM 2 preconditions · ITEM 3 the evidence
         job · ITEM 4 the zip · C2 the closure commit · ITEM 6 the PR.

Change:  Exactly these files, nothing beyond them:
         - `.agent/authored/f077-r20.md` (NEW, C0a)
         - `.agent/last_block.md` (C0b)
         - `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md` (C1)
         - `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md`,
           `.agent/plan.md`, `.agent/handoff.md` (C2)
         NO production code. NO test files. NO feature file. NO docs/README.md.
         NO docs/system/**. If closure reveals a defect needing a code change,
         that fix is its OWN reviewer-gated round — report it and STOP.

Staging: EXPLICIT PATHS ONLY. Never `git add -A`. Push after EVERY commit.

── C1 — the R19 verdict and R-0402, findings persist FIRST ────────────
Three files, ONE commit (finding R-0395: a registration and every count it
invalidates land together).

(1) `.agent/live_review.md` — APPEND at the very END: one blank line, the
    GATE-R19 slice, one blank line, the FINDING-R402 slice. That is 4 added
    lines; the file goes from 148 to 152 lines. Each slice is ONE physical
    line — never re-wrap it. Change nothing above the append point.
    Never write a `Done:` paragraph of your own (planner_reviewer_prompt.md
    §4.4); nothing is resolved this round.

<<<BEGIN GATE-R19>>>
Gate: R19 — PASS. Verification tier: round gate plus the docs gate plus the state-file contract readers plus the canary; no suite claim is made here, because R16 carries this branch's integration-gate entry and R19 touched no product file, which the range confirms — `git diff --name-only 386ef7b5..HEAD` is eight paths and not one is under `packages/`, `apps/` or `tests/`. Every ordered gate was re-run by the reviewer against the disk and every one reproduces: the tree is clean and `git worktree list` is one line; `.agent/authored/f077-r19.md` and `.agent/last_block.md` are byte-identical at shared sha256 `791bf4d7d4a2949422998faeda9e766e4a465c56423365b404e8926667298ff4`, 274 lines each; `^Gate: R18 — ` 1, `^- R-0400 — ` 1, `^- R-0401 — ` 1, `^Done: R-0398 — ` 1, `^Landed: R-0398` 0 and `^Landed: ` 2; the open set recomputed mechanically from the record is 36 registered paragraphs minus 5 `Done:` lines = 31 open, no duplicate id, next free `R-0402`; `wc -l` gives the record 148, `.agent/plan.md` 45, `.agent/context.md` 100, the ist-doc 216 and the feature file 129; `git diff --check 386ef7b5..HEAD` is silent; per-commit insertions are 274, 237, 34, 53, 102 and 14, none over 500; and `origin` sits at the same `c0909569` as the branch. Transport is proven disk to disk against the COMMITTED authored file rather than against a retype: all nine slices were re-extracted by marker and each appears EXACTLY ONCE in its target — LANDED-TO-DONE, GATE-R18, FINDING-R400, FINDING-R401 and LANDED-R401 in the record, DOCFIX2-TO in the ist-doc, CONTEXTCOUNT-TO in `.agent/context.md`, BUILTSTATE as the tail of the feature file, and PLAN byte-equal to the whole of `.agent/plan.md` at sha256 `705f7de4e04c01b2a5ffa9925c151125483534f0c354071993c193cb47562e70`; both REWRITE pairs read FROM 0x and TO 1x, and zero marker lines leaked into any target. Suites re-run by the reviewer AFTER the state files were replaced: `tests/docs/` 295 passed, the canary 42 passed, the three state-file contract readers 216 passed, and `integrity check --json` passed=true fail_count=0 check_count=5 with `high_blockers_open` pass. The round's substance is the Built State section closure precondition 4 requires, and the reviewer audited it against the SOURCE before authoring it and again after application: every symbol it names exists and is spelled as the module spells it, `act_on_trips`'s enumerated writes match its docstring, `evaluate_ledger`'s fixed order and non-trip dropping match its body, and the four config defaults 3, 3, 5 and 3.0 match `packages/orchestration/config.py`. The deselected figure that R-0400 registers reproduced the reviewer's own measurement exactly — `216 passed, 16701 deselected` — which is the finding confirming itself on its first application rather than a value drifting again. The worker's declared deviations are each correct: the denied-tool substitutions kept every proof byte-exact and retyped nothing, and the 134-line handoff carries its DECISION D15 cause with no section dropped. TWO defects in this round belong to the REVIEWER and not to the worker, and both are registered as R-0402: the block said "exactly these seven paths" over an enumeration of eight and "the seven slices" over a list of nine, and the worker was right to report the contradiction rather than reconcile it — the cost was one unordered follow-up commit, `c0909569`. What this gate does NOT say: it makes no claim about the closure artifacts, which R20 produces.
<<<END GATE-R19>>>

<<<BEGIN FINDING-R402>>>
- R-0402 — Low — the R19 block twice stated a COUNT of its own enumerations and both counts were wrong, and the worker paid for it with an unordered sixth commit. The Change section read "exactly these seven paths" and then listed eight (`.agent/authored/f077-r19.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md`, `docs/system/autonomy-watchdog-v1.md`, `docs/roadmap/features/T2_F077.md`, `.agent/handoff.md`), and gate 16 read "for EACH of the seven slices" and then named nine. The SETS were right — `git diff --name-only 386ef7b5..HEAD` returns exactly those eight paths and no ninth, and all nine slices were proven — so nothing was misbuilt; only the reviewer's arithmetic over its own list was wrong, which is why this is Low. The cost was still real and lands entirely on the worker: gate 15 as written could not be satisfied, the handback had already been committed carrying the block's own "seven" verbatim, and the honest resolution took a follow-up commit that no order in the block asked for. The class is the reviewer's recurring one — a gate asserting a value the reviewer did not measure — but aimed at a new target: not the code (checklist item 8), not the target file (item 6), not the guarding tests (item 7), but the block's OWN enumerations, which is the one place the checklist never thought to look because it is the only place the reviewer fully controls. From here, a block that states the cardinality of a list it also enumerates counts that list mechanically on the final bytes, at the same moment checklist item 1 counts the block's lines, or states no number at all and lets the enumeration speak — the enumeration is the contract; the numeral adds nothing but a way to be wrong. OPEN.
<<<END FINDING-R402>>>

(2) `.agent/plan.md` — WHOLE-FILE replacement with the PLAN slice, applied byte
    for byte, nothing trimmed or added. It is under the 50-line AGENTS.md cap;
    its exact length is not stated here on purpose (R-0379) and gate 6 measures
    it.

<<<BEGIN PLAN>>>
# Plan — F077 Autonomy watchdog

Branch: feature/f077-autonomy-watchdog, cut from main after PR #199 merged.
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0403.
Open findings: THIRTY-TWO — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368,
R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394, R-0395,
R-0396, R-0397, R-0399, R-0400, R-0401, R-0402 — recomputed from
`.agent/live_review.md` at R20: 37 registered, 5 resolved (R-0383, R-0384,
R-0388, R-0390, R-0398), no duplicate id. All are Medium or Low; there are no
High or blocker findings, which is what closure precondition 1 requires.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger, postmortems and actuals, and on
no-progress repetition, a burn-rate anomaly or goal drift it PAUSES the mission
and raises one decision per trip class carrying the evidence triple. It stops;
it never repairs. Thresholds live in config, not code.

## Current Step
R20 — closure. All five preconditions hold: every round has a PASS verdict and
every finding is an open Medium or Low; the reviewer re-ran the full suite
itself and measured 16898 passed, 19 skipped at exit 0; `integrity check` is
passed=true with `high_blockers_open` clear and zero relevant untracked files;
the feature file's Built State landed at 4fa56b23; and the tree is clean with
the branch pushed. What remains is the evidence job, the FRESH review zip, the
closure commit and the PR.

## Next Steps
1. Evidence job `f077-closure`, then the review zip — a failing zip build is a
   closure BLOCKER, never a thing to work around.
2. The closure commit LAST on the branch: STATUS `[x]` and the README count and
   tier sync in the SAME commit (R-0154; tests/docs pins the count to the
   ledger), plus the final `.agent/` state. Then the PR, which is NOT merged
   this session — it merges at F082's start via the Open PR Gate.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again — the code CONFIRMS it for all
  three tripwires, so D4's verb buys exactly one iteration (inventory Q8), and
  DECISION F077 D12 does not address the re-trip.
- Thirty-two open findings is the largest carry any feature has held.
- R-0396's amendment target, docs/agents/integration_gate.md, is outside this
  feature's change set, so every future integration gate reproduces the eight
  phantom ui_server base failures until some feature owns that doc.
<<<END PLAN>>>

(3) `.agent/context.md` — ONE REWRITE pair, equal line counts, so the file
    stays at 100 lines and every reader assertion on it survives.
    FROM (one line):

<<<BEGIN CTXCOUNT-FROM>>>
findings at R19: THIRTY-ONE, next free id R-0402.
<<<END CTXCOUNT-FROM>>>

    TO (one line):

<<<BEGIN CTXCOUNT-TO>>>
findings at R20: THIRTY-TWO, next free id R-0403.
<<<END CTXCOUNT-TO>>>

Commit C1 ALONE. Subject: `docs(f077): record the R19 verdict and register R-0402`

── ITEM 2 — preconditions (no commit) ─────────────────────────────────
Run each and record the RAW output and exit code:
  `python3 -m apps.cli.main integrity check --json`  → must be `"passed": true`
  `git status --porcelain`                           → must be EMPTY
  `git worktree list`                                → exactly one line
  `python3 -m pytest -n auto -q`                     → the full suite
The full-suite baseline the reviewer measured itself at `386ef7b5` is
`16898 passed, 19 skipped`, exit 0. Report YOUR numbers raw. If they differ,
report the difference and STOP — do not reconcile.
If the integrity check is not passed, STOP and hand back with the raw output.

── ITEM 3 — the evidence job (no commit) ──────────────────────────────
Use the canonical producer, never a bare gate writer:
`packages.orchestration.job_evidence.create_manual_completion_bundle(
     review_feature_id="f077", ...)`.

  - Write the evidence directory under `.remedy-wt/` (gitignored) so it NEVER
    enters the base..HEAD review subject. A pre-committed evidence dir packages
    as BLOCKED_EVIDENCE.
  - `base_commit` is the FULL 40-char merge base, reviewer-verified with
    `git merge-base main HEAD`:
    `6227c3a26c3b3d518d9619e39931dbd4c680e3cb`
  - `job_id` is `f077-closure`, matching the F103/F104/F105/F107/F111/F115/
    F045/F057 precedent in `docs/roadmap/STATUS.md`.
  - `step_range` is `1-3` (T001-T003).

Read `tests/orchestration/test_review_manual_completion_shapes.py` and its
`_bundle` helper (around line 301) BEFORE building your run entry, rather than
inventing a shape. Heed EVERY producer pitfall in the closure protocol — they
surface only at zip time:
  (a) `verification_runs` entries need a sha256-hex `output_hash`, valid
      `VerificationTests` totals, and the FULL-LENGTH `base_commit`.
  (b) verification records need non-empty node ids with
      `len(node_ids) == selected` — get REAL ids with `--collect-only`.
  (c) `test_files` entries are FILES, never directories.
  (d) the `VerificationTests` `run_id` must match `^vr-\d{4,}$`.
  (e) NEVER put a full-suite node-id list in a verification record.

Record the CLEAN SCOPED suites and nothing else:
  `tests/orchestration/test_watchdog.py`
  `tests/orchestration/test_mission_e2e.py`
Together they collect 61 node ids and the same 61 pass — both reviewer-verified
at `c0909569` — and the reviewer scanned those ids for absolute paths and
secret-like strings and found none. Do NOT include any other test path. The
full-suite proof rides in the committed `.agent/gate_f077_r16/` evidence, in the
`Gate: R16` record entry, and in the reviewer's own re-runs.

── ITEM 4 — the review zip: MANDATORY, FRESH, from a CLEAN tree ───────
In this order:
  1. `git status --porcelain` → must be EMPTY. If not, STOP.
  2. `git push`
  3. Record the FULL 40-char HEAD sha. This is `accepted HEAD` — the head the
     zip and the verdict cover, i.e. AFTER C1 and BEFORE the closure commit.
  4. `bash scripts/make_review_zip.sh --evidence-dir <the .remedy-wt evidence dir>`
Verify `committed_review_subject` spans BASE..HEAD and the zip import check
passes. Record the package filename and its SHA-256.
If the build FAILS: record the raw error VERBATIM in the handoff, author no
`[x]` line, STOP and hand back. A failing zip is a closure BLOCKER.

── C2 — the closure commit, LAST on the branch ────────────────────────
It touches EXACTLY `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md`,
`.agent/plan.md` and `.agent/handoff.md` — nothing else (Rule A4, R-0154).
All of (a)-(e) land in ONE commit.

(a) `docs/roadmap/STATUS.md` — REWRITE this single line, touching no other.
    REWRITE-shaped pair. The FROM matches exactly once and is the file's only
    `[~]` line — both reviewer-verified at `c0909569`.
FROM (one line):

<<<BEGIN STATUS-FROM>>>
- [~] F077 — Autonomy watchdog
<<<END STATUS-FROM>>>

TO (one line; fill ONLY the three angle-bracket slots from ITEMs 3 and 4 —
change no other character):

<<<BEGIN STATUS-TO>>>
- [x] F077 — Autonomy watchdog (T001–T003 complete; accepted 2026-08-14 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f077-closure · package <ZIP_FILENAME> · SHA-256 <ZIP_SHA256> · accepted HEAD <FULL_40_CHAR_HEAD_SHA>)
<<<END STATUS-TO>>>

(b) `README.md`, SAME commit — exactly two REWRITE pairs. Each FROM matches
    exactly once (reviewer-verified). If either FROM does not match byte for
    byte, STOP and report the actual line rather than guessing.

<<<BEGIN README1-FROM>>>
47 of 255 registered items accepted. Next: F077 (Autonomy watchdog).
<<<END README1-FROM>>>

<<<BEGIN README1-TO>>>
48 of 255 registered items accepted. Next: F082 (Self-benchmark).
<<<END README1-TO>>>

<<<BEGIN README2-FROM>>>
| 2 | Minimal Self-Build Runtime | 9 | 14 |
<<<END README2-FROM>>>

<<<BEGIN README2-TO>>>
| 2 | Minimal Self-Build Runtime | 10 | 14 |
<<<END README2-TO>>>

    Both numbers are derived, not guessed, and the reviewer reproduced the
    derivation mechanically at `c0909569` before emitting this block: counting
    `- [x] F<id>` lines in STATUS.md whose `docs/roadmap/features/T<n>_F<id>.md`
    exists yields 16 / 22 / 9 for tiers 0 / 1 / 2 and 47 in total, which is
    exactly what the README says today. F077 makes both 48 and 10.
    `F082 — Self-benchmark` is the first `[ ]` line in STATUS order (Rule A5).
    VERIFY the derivation yourself before committing; if your count disagrees
    with 48 or 10, STOP and report your numbers rather than writing either
    value. `tests/docs/test_docs_consistency.py` pins the README's N to the
    STATUS `[x]` count, which is why (a) and (b) must land together.

(c) `.agent/candidates.md` — REWRITE the single `(empty — …)` paragraph into the
    CANDIDATES slice, keeping the file's header and blockquote intact.
FROM (two lines):

<<<BEGIN CAND-FROM>>>
(empty — the F057 entry was registered as finding R-0380, and the R14 verdict's
candidate on PR #199 as R-0381, both in `.agent/live_review.md` on the F077
branch, 2026-08-14.)
<<<END CAND-FROM>>>

TO:

<<<BEGIN CANDIDATES>>>
(empty — F077's closure raised no candidate. Every finding this feature
produced was registered as an R-id in `.agent/live_review.md` in the round that
found it, and the thirty-two still open are carried openly in the STATUS line's
PASS_WITH_RISKS verdict and in the closure PR, 2026-08-14.)
<<<END CANDIDATES>>>

(d) `.agent/plan.md` — FULL REPLACEMENT with the FINALPLAN slice, applied byte
    for byte. Under the 50-line cap; gate 6 measures it.

<<<BEGIN FINALPLAN>>>
# Plan — F077 Autonomy watchdog · CLOSED

Branch: feature/f077-autonomy-watchdog. F077 is `[x]` in docs/roadmap/STATUS.md
as of this commit, which is the LAST on the branch. Next free finding id:
R-0403. Open findings: THIRTY-TWO, all Medium or Low, none a blocker — the
verdict is PASS_WITH_RISKS and the ids are named in the closure PR and in
`.agent/live_review.md`, which is the source of truth.

## Goal
Continuous operation gets a tripwire independent of the thing it watches. A
watchdog reads the orchestrator loop's ledger and on no-progress repetition, a
burn-rate anomaly or goal drift it PAUSES the mission and raises one decision
per trip class carrying the evidence triple. It stops; it never repairs.
Thresholds live in config, not code. DONE: T001, T002 and T003 are built,
tested and green, the integration gate ran on the branch and at the merge base
with zero branch-only failures, and `docs/system/autonomy-watchdog-v1.md`
records the built state.

## Current Step
None. The feature is closed and the PR is open and UNMERGED by design: it
merges at the next feature's start via the AGENTS.md Open PR Gate, which is the
operator's manual-review window. The operator may merge it manually at any time.

## Next Steps
1. A NEW session, per docs/agents/self_drive_protocol.md Phase 1: rule 1
   re-reads `.agent/STOP` from disk FIRST, then rule 2 runs the Open PR Gate,
   which merges this feature's PR before any new branch exists.
2. Then Rule A5 claims the next feature in STATUS order: F082 — Self-benchmark.
3. `.agent/candidates.md` is empty, so no candidate registration is owed at that
   claim.

## Risks
- A mission resumed AFTER its watchdog decision is answered still carries the
  tripping run in its ledger and trips again for all three tripwires, so
  `mission resume` buys exactly one iteration. DECISION F077 D12 does not
  address the re-trip; it is recorded in the feature file's Built State as a
  known limit and no feature owns it yet.
- R-0396's amendment target, docs/agents/integration_gate.md, is outside this
  feature's change set, so every future integration gate reproduces the eight
  phantom ui_server base failures until some feature owns that doc.
<<<END FINALPLAN>>>

(e) `.agent/handoff.md` — rewrite as the CLOSURE handback per
    `docs/agents/handback_template.md`. Cap 60 lines; if MANDATED content
    genuinely does not fit, exceed it with a "Deviations, declared" line naming
    the actual count and the mandated content that caused it. NEVER drop a
    section. It must carry: the evidence job id, the package filename and its
    SHA-256, the accepted HEAD, the full-suite numbers you measured, the
    per-commit table, an item-status table covering C0a, C0b, C1, ITEM 2,
    ITEM 3, ITEM 4, C2 and ITEM 6 with every item present exactly once, the
    transport proofs, the open-findings count, and the PR number and URL. Name
    the next session's FIRST action explicitly: Phase 1 rule 1 of
    `docs/agents/self_drive_protocol.md` — re-read `.agent/STOP` from disk —
    BEFORE rule 2's Open PR Gate.

BEFORE committing C2 run BOTH, and they must be green IN THE SAME COMMIT as the
edits:
  `python3 -m pytest tests/docs/ -q`                    (baseline 295 passed)
  `python3 -m pytest tests/cli/test_golden_path.py -q`  (baseline 42 passed)
Commit subject: `docs(f077): close F077 in the roadmap ledger`

── ITEM 6 — the PR ────────────────────────────────────────────────────
`git push`, then `gh pr create` per the AGENTS.md PR workflow. Base `main`,
head `feature/f077-autonomy-watchdog`. The description carries: what changed and
why; key decisions (F077 D6, D7, D11 and D12 at minimum, named); how to review;
a changed-files table; the latest verdict (R19 PASS; feature PASS_WITH_RISKS);
the open-findings count (32, all Medium or Low, all named); and runtime actuals
— rounds (20), wall clock, models, tokens — with `not-measured` wherever the
ledger has no number, NEVER a guess. Do NOT merge it.
Commit subjects and the PR title must never contain a leading-slash token, an
absolute path, or a secret-like string — the metadata scanner rejects them and
blocks closure.

── Constraints ────────────────────────────────────────────────────────
- AGENTS.md is highest authority. Self-review loop before EVERY commit.
- The closure commit is the LAST commit on the branch. Nothing after it but the
  PR.
- Authored texts are applied byte for byte, extracted from the COMMITTED
  `.agent/authored/f077-r20.md`, never retyped. No trailing whitespace
  anywhere: verify with a Python scan (`l != l.rstrip()`) and say which command
  you actually ran if `grep -rn ' $'` is denied.
- No committed line may state a value that does not exist when it is written
  (R-0371): a commit never states its own SHA. Report those in the handback.
- Report every measured number RAW. A contradiction is reported, never
  reconciled by editing a file. "Green" as a word is not evidence.
- If ANY precondition, the evidence job, or the zip fails: STOP, record the raw
  output, hand back. Do NOT author a `[x]` line for a feature that did not meet
  its preconditions. Pretending completion is the one unforgivable failure mode.

── Done when ──────────────────────────────────────────────────────────
Record the command, the exit code and the REAL output for every one.
  1. `.agent/authored/f077-r20.md` and `.agent/last_block.md` are byte-identical;
     report the shared sha256 and the line count of each, which must be at or
     under 400.
  2. `.agent/STOP` is ABSENT — read from disk at the round start and at
     handback; report both readings.
  3. In `.agent/live_review.md`: `grep -c '^Gate: R19 — '` is 1;
     `grep -c '^- R-0402 — '` is 1; `grep -c '^Landed: '` is 2 and unchanged.
  4. Open set recomputed MECHANICALLY from the record, not carried from this
     block: `grep -c '^- R-[0-9]\+ — '` is 37, `grep -c '^Done: R-[0-9]\+ — '`
     is 5, so 32 are open; report that no id appears twice and that the next
     free id is R-0403.
  5. `wc -l .agent/live_review.md` is 152; `wc -l .agent/context.md` is 100.
  6. `wc -l .agent/plan.md` after C1 and again after C2 — report both; each must
     be under 50.
  7. Pair application by shape. CTXCOUNT, STATUS, README1, README2 and CAND are
     REWRITEs: after their commit each FROM appears 0x and each TO appears 1x in
     its target file. PLAN and FINALPLAN are whole-file replacements: report the
     sha256 of `.agent/plan.md` and of the slice, and state they are EQUAL.
  8. `grep -c '^- \[~\]' docs/roadmap/STATUS.md` is 0 after C2, and
     `grep -c '^- \[x\] F077 — ' docs/roadmap/STATUS.md` is 1.
  9. ITEM 2's four commands with raw output and exit codes.
  10. ITEM 3: the evidence directory path, the summary dict the producer
      returned, and confirmation that the directory is OUTSIDE the git index
      (`git status --porcelain` stays EMPTY).
  11. ITEM 4: the package filename, its SHA-256, the accepted HEAD, and that
      `committed_review_subject` spans BASE..HEAD.
  12. `python3 -m pytest tests/docs/ -q` and
      `python3 -m pytest tests/cli/test_golden_path.py -q` after C2.
  13. `python3 -m apps.cli.main integrity check --json` after C2 — report
      `passed`, `fail_count`, `check_count`, `high_blockers_open`.
  14. `git diff --check c0909569..HEAD` produces no output.
  15. Per-commit insertions from `git show --numstat` for every commit this
      round; none may exceed 500. Report each number.
  16. `git diff --name-only c0909569..HEAD` — report the paths it returns and
      confirm the set equals the enumeration in the Change section above. Report
      the count you measure; do not adopt a count from this block (finding
      R-0402).
  17. Transport, disk to disk: for EACH slice named in this block, extract it
      from the COMMITTED `.agent/authored/f077-r20.md` by its markers and
      compare byte for byte against the region it was applied to. Report the
      sha256 of both sides and state they are EQUAL. Confirm no marker line
      reached any target file. Report how many slices you proved.
  18. `git push`, remote head equals local head, and the PR number and URL.
──────────────────────────────────────────────────────────────────────
