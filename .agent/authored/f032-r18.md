STEP CLOSURE 1 OF 2 / F032 — ROUND R18 — Built State, the evidence bundle, the zip

BASE. This block is authored against `12f28a424be48fc41602383e8844f694e408553d`,
the tip of `feature/f032-evidence-triple` and the handback of R17, measured with
`git rev-parse HEAD` rather than copied from a short form. Every reading below
was taken there by the reviewer unless another SHA is named.

FRAME CONVENTION. Every rule line in this block is exactly ten hyphens, and no
other line is a run of one repeated character. Nothing in the frame is
appliable: the appliable bytes are the slices, each proved against its own
target by its own gate.

----------

GOAL

Take F032 to the edge of closure. Book the R17 integration-gate verdict and the
one finding it produced, make the feature file's Built State section current —
it does not exist yet, and precondition 4 of the closure protocol requires it —
then run the evidence job and build the FRESH review zip that precondition 2
and step 2 make mandatory. The STATUS flip, the README sync and the pull request
are R19's, not this round's.

----------

WHAT THE REVIEWER READ AND MEASURED BEFORE ORDERING ANY OF THIS

(a) `docs/roadmap/STATUS_closure_protocol.md` preconditions, checked one by one
    against disk. Precondition 2 HOLDS: R17's integration gate passed and the
    reviewer re-ran the full suite itself at `12f28a42`, `python3 -m pytest -n
    auto -q` exit 0 at `17982 passed, 20 skipped in 117.52s`, matching the
    worker's own `17982 passed, 20 skipped` exactly. Precondition 4 FAILS
    TODAY: `grep -n "Built State" docs/roadmap/features/T5_F032.md` returns
    nothing, so that section must be written this round, which is what S3 does.
    Precondition 5 holds: tree clean, branch pushed, remote tip equal.
(b) PRECONDITION 3 CANNOT BE RUN AS WRITTEN AND HAS A DOCUMENTED SUBSTITUTE.
    `remedy integrity check --json` is refused by this session's command guard
    for the reviewer and for every subagent alike. The closure protocol's own
    canonical route is the MODULE rather than the CLI, and that is the route
    S5 takes; report the refusal verbatim if the CLI is attempted, and never
    report a PASS that was not produced.
(c) THE PROVEN PIPELINE IS ON DISK AND IS NOT REWRITTEN HERE.
    `.agent/authored/f031-r68.md` is the block that built F031's closure bundle
    and zip, and its `EVIDENCESCRIPT` slice runs from line 303 to line 445 of
    that file. It carries, already solved, every packaging pitfall this feature
    would otherwise rediscover: node ids from `--collect-only` and never from a
    `-v` log; `len(node_ids) == selected` with nothing deselected; `test_files`
    as real files and sorted; a `run_id` matching `^vr-\d{4,}$`; the
    full-length base SHA; `output_hash` as sha256 over `stdout_summary`
    exactly; the twice-scrubbed `stdout_summary` tail on a whole-line boundary;
    and a `_unsafe_text` scan of every packaged string with a red control,
    run BEFORE the bundle is written so a rejection is a red there rather than
    a BLOCKED_EVIDENCE zip later. S4 ADAPTS that script; it does not replace it.
(d) THE FOUR SCOPED SUITES F032 SHOULD RECORD, each measured by the reviewer at
    `12f28a42` with `python3 -m pytest <path> -q` and with `--collect-only`,
    and each scanned with `scripts/build_review_manifest._unsafe_text`:
    `tests/orchestration/test_decision_evidence.py` 134 passed;
    `tests/orchestration/test_decision_inbox.py` 35 passed;
    `tests/ui_contracts/test_decision_answer_wiring.py` 55 passed;
    `tests/ui_server/test_decisions_endpoint.py` 4 passed. All four: exit 0, 0
    failed, 0 skipped, 0 deselected, collected id count EQUAL to selected, and
    ZERO ids rejected by `_unsafe_text`, whose red control on a fabricated
    absolute path returned True. A FULL-SUITE node-id list is never recorded —
    the protocol's pitfall (d) — so the full-suite proof rides in R17's
    committed gate evidence and the reviewer's own re-run.
(e) `packages/orchestration/job_evidence.py:2895` is
    `create_manual_completion_bundle`, whose keyword parameters are
    `repo_root`, `base_commit`, `job_id`, `job_title`, `step_range`,
    `prior_job_ids`, `verification_runs`, `timestamp`, `generated_at`,
    `head_commit`, `task_partition`, `num_tasks`, `note_prefix` and
    `review_feature_id`. That is the canonical producer the protocol names;
    `write_runtime_integration_gate` alone is NOT a bundle and packages as
    BLOCKED_EVIDENCE.
(f) `git merge-base HEAD main` is
    `a399a3304f9d962cd920c251488c40c486b35fdc`, the branch's cut point and the
    `base_commit` the bundle records.
(g) `.agent/live_review.md` at the base: 274 paragraphs matching `^- R-\d+ — `,
    24 lines matching `^Done: R-\d+ — `, so the OPEN SET is 250 and the maximum
    id is `R-0713`. This round registers exactly one finding, so the next free
    id is `R-0714` and the open set becomes 251.
(h) THE OPEN SET WAS SEARCHED FOR R-0714's DEFECT BEFORE THE ID WAS MINTED, as
    the pre-emission checklist requires. Eleven open findings mention the
    auto-build or the dist rewrite; the two that come closest are R-0445, the
    copy-preserves-mtime defect that makes the base worktree's build stale, and
    R-0565, the parity check that compares content hashes and is blind to a
    byte-identical rebuild. BOTH ARE ABOUT THE PROCEDURE IN
    `docs/agents/integration_gate.md`. Neither names a TEST, neither names
    `tests/ui_server/test_dashboard_contract.py`, and neither observes that the
    flag the procedure sets is popped from inside the suite. R-0714 is a
    distinct defect in a distinct file with a distinct repair, and its text
    says so rather than leaving a later reader to wonder.
(i) R-0445's OWN SYMPTOM DID NOT RECUR AT R17, and the reason is worth
    recording: that finding predicts eight `tests/ui_server/test_live_state.py`
    base failures on every gate run, and R17's base run had two failures,
    neither of them from that file. The R17 block's S4 stamped
    `dist/index.html`'s mtime to NOW inside the base worktree, which is exactly
    the one-line procedure repair R-0445 asks for, and it worked.

----------

BUNDLE

C0a  save this block verbatim to `.agent/authored/f032-r18.md`
C0b  mirror the same bytes over `.agent/last_block.md`
C1   `.agent/plan.md`, slice PLANF032R18 applied whole
C2   `.agent/live_review.md` slices LEDGER18 and FINDING714 appended in that
     order, and `.agent/prose_slips.md` slice SLIP18 appended
C3   `docs/roadmap/features/T5_F032.md`, slice BUILTSTATE appended
C4   the handback

C3 IS THE ACCEPTED HEAD. The evidence job and the zip run AFTER C3 and BEFORE
C4, from a clean tree, so the manifest's `committed_review_subject` spans the
merge base to C3. C4 records their outcome and changes no content.

CHANGE SET. Exactly these paths, and nothing else is created, edited or
deleted: `.agent/authored/f032-r18.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`,
`docs/roadmap/features/T5_F032.md`, `.agent/handoff.md`. THE EVIDENCE
DIRECTORY IS NEVER COMMITTED and neither is the zip: both live under
`.remedy-wt/`, which is gitignored, and a committed evidence dir puts evidence
files into the review subject and packages BLOCKED_EVIDENCE.

----------

CONSTRAINTS

1.  A slice is applied BYTE FOR BYTE. It is never retyped from memory, never
    reflowed, never trimmed and never corrected — if a slice looks wrong, apply
    it as given and say so in the handback's deviations.
2.  SLICE CONVENTION. A slice begins at the line after `<<<SLICE NAME>>>` and
    ends at the line before `<<<END NAME>>>`. The slice's bytes are those lines
    including the newline that ends the last of them. Extract them
    PROGRAMMATICALLY from the committed C0a blob — `git show
    <C0a>:.agent/authored/f032-r18.md` — never by retyping from this prompt.
    PLANF032R18 REPLACES `.agent/plan.md` whole. LEDGER18, FINDING714, SLIP18
    and BUILTSTATE are APPENDS: the target's existing bytes, then exactly one
    newline, then the slice. LEDGER18 and FINDING714 go into ONE commit in that
    order, each as its own append.
3.  The script S4 orders is ADAPTED PRODUCTION-SHAPED CODE, not a slice. Copy
    the `EVIDENCESCRIPT` body out of the committed
    `.agent/authored/f031-r68.md` programmatically, change ONLY the constants
    S4 names, and report a diff of what you changed. Do not retype it.
4.  The commits happen in the order the Bundle lists. C1 is the first
    substantive commit, so `.agent/plan.md` is current before anything else is
    committed.
5.  Every commit passes the AGENTS.md self-review loop and the Commit Gate, and
    the tree is clean after each. Commit subjects carry no leading-slash token,
    no absolute path and no secret-like string.
6.  Push after C4: `git push -u origin feature/f032-evidence-triple`. CREATE NO
    PULL REQUEST, FLIP NO STATUS LINE, TOUCH NO README. Those are R19's and
    doing them here would put the closure commit before its own gate.
7.  Read `.agent/STOP` from disk twice — once before C0a and once before C4 —
    and report the exact command output both times. If it EXISTS at either
    reading, stop, write the handback, and end.
8.  Where a command's exit code is needed and this session's shell refuses
    `$?`, chain `&& echo <MARKER>` and report whether the marker printed. Never
    report an exit code that was not observed.
9.  A FAILING ZIP BUILD IS A CLOSURE BLOCKER, NOT A THING TO WORK AROUND. If
    the package does not build READY, record the RAW error verbatim in the
    handback, leave the branch as it is, and end the round. Never report a
    package that was not produced, and never turn a blocked attempt into a
    success report.
10. Run no `npm`, `npx`, `node` or `vite`. The frontend is current and no item
    below needs a build; if something you are about to run would invoke them,
    stop and report.

----------

SPEC — what this round produces

S1. THE RECORD MOVES FIRST. C2 appends LEDGER18, then FINDING714, to
    `.agent/live_review.md`, and SLIP18 to `.agent/prose_slips.md`.

S2. NOTHING IS RESOLVED THAT WAS NOT FIXED. This round registers `R-0714` and
    resolves nothing, so `^Done: R-\d+ — ` does not move and the open set goes
    from 250 to 251.

S3. THE FEATURE FILE GAINS ITS BUILT STATE SECTION, slice BUILTSTATE, appended
    at C3. That is closure precondition 4 and it must land in a commit of its
    own BEFORE the zip is built, because the zip's accepted HEAD is C3 and the
    protocol requires the Built State to be current from an earlier commit than
    the closure commit R19 will make.

S4. THE EVIDENCE BUNDLE, after C3, from a clean tree. Take the `EVIDENCESCRIPT`
    body from the committed `.agent/authored/f031-r68.md` and change ONLY these
    constants, reporting each old and new value:
      - the docstring and `EVIDENCE_DIR`, to
        `.remedy-wt/f032_closure_evidence/remedy-job-evidence-f032-closure`;
      - `BASE`, to `a399a3304f9d962cd920c251488c40c486b35fdc`, the full 40-char
        merge base reading (f) names, which the script's own `assert len(BASE)
        == 40` re-checks;
      - the `runs` list, to the four suites and counts reading (d) measured,
        keyed `vr-0001` through `vr-0004` in that order;
      - `job_id` to `f032-closure`, `job_title` to a sentence naming F032,
        `step_range` to `T001-T003`, `prior_job_ids` to `["f031-closure"]`,
        `note_prefix` to name the F032 closure, and `review_feature_id` to
        `f032`.
    Everything else — `_tail`, `mkrun`, the `_unsafe_text` scan with its red
    control, the `output_hash` preimage check — is kept AS IT IS, because each
    line of it is a packaging pitfall already paid for. Report the script's
    full stdout, including the per-run selected/node-id/deselected counts, the
    scan's rejected count and its red control, and the `OUTPUT_HASH` lines.

S5. INTEGRITY, BY THE ROUTE THAT EXISTS. Precondition 3 asks for `remedy
    integrity check --json`. If the CLI is refused, reach the same check
    through its Python module from the repository root and report the real
    result either way, naming which route produced it. Report also that there
    are no relevant untracked files: `git status --porcelain` is 0 lines and
    `git ls-files .remedy-wt` is 0 lines.

S6. THE REVIEW ZIP, MANDATORY AND FRESH, from a clean tree at C3:
    `bash scripts/make_review_zip.sh --evidence-dir <the EVIDENCE_DIR of S4>`.
    Report the command, its exit code, the printed package filename and its
    SHA-256, and confirm the manifest's `committed_review_subject` spans the
    merge base to C3. Then report the package's ARCHIVED PATH — the absolute
    directory it was moved to, or the literal `NOT ARCHIVED` when it was left
    where it was built. That field is DECISION amend0827 D1's and R19's STATUS
    line cannot be authored without it.

S7. NOTHING ELSE CHANGES. No STATUS line, no README, no pull request, no
    production code, and no file under `packages/`, `apps/` or `tests/`.

S8. THE SPEC AND THE BUNDLE AGREE. S1 and S2 are C2, S3 is C3, S4 to S6 run
    between C3 and C4 and are REPORTED in C4. Nothing in this SPEC is performed
    by a commit the Bundle does not list.

----------

SLICES

<<<SLICE PLANF032R18>>>
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D8.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
T001, T002 and T003 are COMPLETE and the integration gate PASSED at R17: the
branch's full suite is exit 0 at 17982 passed, the branch-only failure set is
empty, and both base-only ids pass serially at the merge base and on the
branch. R18 is closure part one — the R17 verdict and the one finding the gate
produced, the feature file's Built State section that closure precondition 4
requires and that does not exist yet, then the evidence job and the FRESH
review zip. The STATUS flip, the README sync and the pull request are R19's.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R17 verdict, R-0714 and the reviewer's slip | ordered | the record is touched first |
| C3 the feature file's Built State | ordered | precondition 4; the accepted HEAD |
| C4 the handback | ordered | records the bundle and the package |

## Next Steps
1. R19, closure part two: the authored STATUS line and the README capability
   sync in ONE commit, last on the branch, then the pull request — which is NOT
   merged in this session, per the closure protocol's step 6.

## Risks
- A failing zip build is a closure BLOCKER, not a thing to route around. The
  raw error goes in the handback and the branch is left as it is.
- Closure precondition 3 names a CLI this session's guard refuses. The check is
  reached through its Python module instead and the route used is named, so no
  PASS is reported that was not produced.
<<<END PLANF032R18>>>

<<<SLICE LEDGER18>>>
Gate: F032 R16 and R17 — THE INTEGRATION GATE PASSED, and this entry is the only place in this record that may carry a full-suite claim for F032. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `12f28a42`. THE CENTRAL READING IS THE REVIEWER'S OWN AND NOT THE WORKER'S: `python3 -m pytest -n auto -q` from the repository root, exit 0, `17982 passed, 20 skipped in 117.52s`, against the worker's independently recorded `17982 passed, 20 skipped in 179.96s` — the same pass and skip counts from two separate runs, and no `FAILED` line in either. THE BRANCH-ONLY FAILURE SET IS EMPTY, so no id is a blocker and nothing this feature wrote broke anything the merge base had working. TWO BASE-ONLY IDS EXIST AND BOTH ARE ATTRIBUTED BY DIRECT EVIDENCE, as the VOID parity claim requires: `tests/orchestration/test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogicalIdentity::test_different_execution_identities_same_logical_hash`, which re-ran serially to exit 0 at the base AND on the branch and whose cause is the mid-run rewrite of the base worktree's `apps/ui/dist`; and `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`, whose `pgrep -f` predicate is machine-wide, which recorded `returncode=0, stdout='2351843'` under parallel load and which also re-ran serially to exit 0 in both checkouts. Neither file is touched by this branch: `git diff --stat a399a330..1fa2b3df -- tests/orchestration/ tests/cli/` lists exactly one path, `tests/orchestration/test_decision_evidence.py`, the file F032 ADDS. THE PARITY CLAIM IS VOID AND THE GATE SAID SO RATHER THAN HIDING IT. All three files under the base worktree's `apps/ui/dist` carry mtime `02:57:08`, inside the base run window `02:55:51` to `02:58:15`, and the vite content-hash asset names changed from the copied-in pair to a different pair, so a real build ran inside the worktree. THAT THE GATE SAW THIS AT ALL IS THE ROUND'S BEST WORK: the block ordered the EVENT measured rather than the outcome, per finding R-0444, and a content digest alone would have reported parity intact — which is precisely finding R-0565's prediction, now demonstrated a second time. The worker additionally measured the same window on the BRANCH side, which the block did not order, and reported that the primary checkout's `dist` was rewritten too with its asset NAMES unchanged, a byte-identical rebuild; reporting the unordered half rather than the ordered half alone is the right instinct and is recorded here as such. THE CAUSE IS NOW KNOWN AND IS REGISTERED SEPARATELY AS `R-0714`. FINDING R-0445's OWN SYMPTOM DID NOT RECUR: it predicts eight `tests/ui_server/test_live_state.py` base failures on every gate run, and there were none, because the R17 block's S4 stamped `dist/index.html`'s mtime to NOW inside the base worktree — the one-line procedure repair that finding asks for, applied and shown to work. R16 IS BOOKED IN THIS SAME ENTRY BECAUSE IT WAS THE SAME GATE, ATTEMPTED AND HONESTLY ABANDONED: its session was refused `npm run build` in every form, it declined both available substitutes on the ground that each would make the gate green about something it had not tested, it started neither suite and deliberately created no gate-named evidence directory with no run behind it. Everything R16 committed was re-verified and correct, and the reviewer — whose session was NOT refused the build — ran `npm run build` itself before R17, `vite v6.4.2`, 986 modules, 1.35s, into the gitignored `apps/ui/dist` with `git status --porcelain` still 0 lines, so no tracked file changed and nothing reviewable was authored by the reviewer. R17's own S1 then measured the result independently and reported the asset filenames, which matched. THE RECORD MOVED EXACTLY AS ORDERED ACROSS BOTH ROUNDS: transport proved from digests the reviewer held BEFORE delegating, `5b3d7191…` for R16 and `413f9456…` for R17, each equal across the scratch original, the saved copy and the mirror, the two committed paths one blob in each round; the plans byte-equal to their slices with the trailing-newline negative controls `False`; the appends byte-identical with the base a byte PREFIX, `1101489 + 1 + 6398 = 1107888` and `2328 + 1 + 604 = 2933` at R16 and `1107888 + 1 + 4656 = 1112545` at R17; the open set unmoved at 250 with maximum `R-0713` at both gates; and `^Gate: F\d+ R\d+ — ` gaining exactly `F032 R15` and then `F032 R16`. NOTHING ELSE MOVED: `git diff --stat c1e20833..8c42bad2 -- packages/ apps/ tests/ docs/` EMPTY, both path residues empty, `git ls-files .remedy-wt` 0 lines, `git worktree list` one line, `git branch --list "tmp/*"` empty after `tmp/base-gate` was deleted, the remote tip equal to the local tip and the Open PR Gate `[]`. ONE DEFECT IN THE R17 BLOCK WAS THE REVIEWER'S AND IS RECORDED IN `.agent/prose_slips.md`: its base SHA was written out to 40 characters after only the first eight were measured, and the resulting string names no object. NO BLOCK CONDITION AROSE IN EITHER ROUND: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER18>>>

<<<SLICE FINDING714>>>
- R-0714 — Medium, A TEST RUNS A REAL FRONTEND BUILD FROM INSIDE THE SUITE AND ASSERTS A TAUTOLOGY, WHICH MAKES THE INTEGRATION GATE'S ONLY NEUTRALISATION LEVER UNENFORCEABLE. Raised by the reviewer at the F032 R17 gate; the worker found and named the mechanism in `full_log_provenance.txt` and minted no id, correctly, because the block ordered none. `tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_runs_by_default` copies the environment, does `env.pop("REMEDY_UI_NO_AUTO_BUILD", None)`, and calls the UNPATCHED `_auto_build_frontend()` inside `patch.dict(os.environ, env, clear=True)`. `packages/orchestration/ui_server.py` returns early only when that variable equals the string `"1"`, and its next guard is `if not (ui_root / "package.json").is_file()` where `ui_root` is resolved from `Path(__file__).resolve().parent.parent.parent`, NOT from the working directory — so `package.json` always resolves, the early return never fires, and the test really runs `npm install` when `node_modules` is older than `package.json` and then `npm run build`. THE TEST'S OWN DOCSTRING STATES THE OPPOSITE — "Returns None because package.json path doesn't match test env, but it tried" — and that sentence is false of every run. THE ASSERTION CANNOT FAIL: it is `assert result is None or isinstance(result, Path)` over a function annotated `-> Path | None`, so every possible execution satisfies it, including one where npm is missing, the install fails, or the build errors out. It is a blind gate over production code in the sense operator amendment amend0827 rule 2 reserves an id for. THE EFFECT IS MEASURED, NOT INFERRED. At F032 R17 the base worktree's `apps/ui/dist` was rewritten inside the base run window — all three files at `Fri Aug 28 02:57:08 2026` inside `02:55:51` to `02:58:15`, with the vite content-hash asset names changing — while `REMEDY_UI_NO_AUTO_BUILD=1` was set in that run's environment, which is exactly the flag this test pops. The primary checkout's `dist` was rewritten inside the branch run window too. That mid-run rewrite is the mechanism finding R-0176 records, and it caused the base-only failure of `tests/orchestration/test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogicalIdentity::test_different_execution_identities_same_logical_hash`, which passes serially at both the merge base and the branch. MEDIUM AND NOT HIGH because it produces no false GREEN: the branch run was exit 0 with no FAILED line, and every base-only id was attributed by direct evidence as the protocol's alternative route allows. NOT LOW because `REMEDY_UI_NO_AUTO_BUILD=1` is the ONE lever `docs/agents/integration_gate.md` step 3 has for neutralising the auto-build, this test makes it unenforceable for any full-suite run on any feature, and it silently spends an npm install and an npm build inside every such run. THIS IS NOT A DUPLICATE, and the neighbours are named so a later reader does not re-litigate it: R-0445 is the copy-preserves-mtime defect that leaves the base worktree's build older than its sources, and R-0565 is the parity check that compares content digests and is blind to a byte-identical rebuild. Both are defects of the PROCEDURE in `docs/agents/integration_gate.md`; neither names a test, neither names this file, and neither observes that the flag the procedure sets is discarded from inside the suite it is protecting. R-0445 additionally predicts a symptom that did NOT occur at R17, which is further evidence the two are separate. COUNTER-MEASURE: patch the SEAM rather than the environment. `_auto_build_frontend` reaches npm through `exec_guard.run_guarded_runtime_build_command` as a module attribute precisely so a test can patch it, and the sibling `test_no_npm_when_disabled` in the same class already patches `subprocess.run` for the same purpose. The test should assert that the seam WAS CALLED with the expected argv, which is the behaviour its name claims, instead of asserting that a union-typed return value is a member of its own union. The docstring is corrected in the same edit. OPEN.
<<<END FINDING714>>>

<<<SLICE SLIP18>>>
- 2026-08-28 · F032 R17 · The block's BASE paragraph wrote the base commit as
  `c1e208334cd8c7c0cef0a0ae3e5a1e63a4dc65d5` after measuring only the leading
  eight characters, so thirty-two of the forty were invented and the string
  names no git object; the real tip was
  `c1e20833405fc3a5a8f3b50729046578dbc97329`. The worker resolved the intent
  from the short form the gates quote, ran against the real tip and declared
  the discrepancy. Nothing on disk under `packages/`, `apps/`, `tests/` or
  `docs/` was wrong, so no id was spent. Measure a SHA in full or write only
  the short form that was measured.
<<<END SLIP18>>>

<<<SLICE BUILTSTATE>>>
## Built State (F032, 2026-08-28)

What exists on disk at the close of F032, so a later reader need not
reconstruct it from the roadmap's future tense.

**The Python surface.** `packages/orchestration/decision_evidence.py` carries
`DecisionEvidenceRef`, `DecisionOptionOutcome`, `DecisionEvidenceTriple`,
`DECISION_EVIDENCE_REF_KINDS`, `NO_MATERIAL_DOWNSIDE`, `UNKEYED_OPTION`,
`BOILERPLATE_PHRASES`, the two `DECISION_EVIDENCE_STATUS_*` markers,
`TRIPLE_REQUIRED_TYPES`, `evidence_triple_problems`,
`export_decision_evidence`, `DecisionEvidenceError` and the emit gate
`enforce_decision_evidence`. Its tests are
`tests/orchestration/test_decision_evidence.py`, including the canary producer
whose missing field the gate refuses.

**Where the gate sits.** At the DERIVATION point, inside
`packages/orchestration/decision_queue.py::list_decisions`, per amendment A1 —
there is no enqueue seam and no decision store. All eight producing decision
types carry real triples and all eight are listed in `TRIPLE_REQUIRED_TYPES`;
the only members of `DECISION_TYPES` outside it are `worker_approval` and
`revert_missing`, which have no producer at all.

**The browser.** `apps/ui/src/api/decisionCard.ts` projects the triple onto the
card model — `evidenceRefs`, `evidenceNote`, and each answer's own
`expectedOutcome` and `downside`, matched to its option — and enforces §17 of
the design reference in that layer: a ref's `label` is scrubbed and is the only
field a renderer may show, `evidence_status` becomes prose and never reaches
the model. `apps/ui/src/components/panels/DecisionInboxCard.tsx` renders the
receipts strip, the honest note and each answer's stakes, and takes an OPTIONAL
`onOpenEvidence` handler under which a receipt becomes a control. Its rules are
in `RightLivePanel.module.css`; its guards are
`tests/ui_contracts/test_decision_answer_wiring.py`.

**What F032 deliberately did NOT build.** No provenance resolver and no
staleness badge — amendment A2 routes those to F066. No evidence panel and no
navigation behind the receipt chips — amendment A7 and DECISION F032 D8 route
those to F023, whose T003 owns the EvidencePanel; F032 ships the entry point
and F023 wires it. No options list was grown for a producer that did not
already have one, per amendment A3.
<<<END BUILTSTATE>>>

----------

DONE WHEN — the gates, in this order

Every gate is EXECUTED and its real output recorded. "Green" as a word is a
finding. Each gate runs at a commit strictly earlier than C4, so the handback
can quote all of them; C4's own numbers are not gated and are not owed.

G1 HYGIENE, BASE, SENTINEL. `git rev-parse HEAD` before C0a — REPORT it and
   confirm it equals the base this block names, in full. `git rev-parse
   --abbrev-ref HEAD` is `feature/f032-evidence-triple`. `git status
   --porcelain | wc -l` is `0` after each of C0a, C0b, C1, C2 and C3. `ls -la
   .agent/STOP` before C0a and again before C4 — report the exact output of
   both.

G2 TRANSPORT. One digest comparison, disk to disk. Report `sha256sum` over the
   reviewer's gitignored scratch original `.remedy-wt/f032-r18.md`, over
   `.agent/authored/f032-r18.md` at C0a and over `.agent/last_block.md` at C0b —
   all three equal — plus the git blob id of the two committed paths, which must
   be one blob. That chain covers the original, the copy and the mirror, and
   makes no claim about any prompt's bytes.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob. Report the content
   line count of EACH slice region found and how many regions there were, the
   block's TOTAL line count, and PROSE as TOTAL minus the content total. PROSE
   must be under 400 and TOTAL under 490.

G4 THE PLAN, at C1. `.agent/plan.md` is byte-equal to slice PLANF032R18
   extracted from the committed C0a blob — report `True`. NEGATIVE CONTROL: the
   same comparison with the slice's trailing newline removed — report `False`.
   Report `wc -l`, which must be under 50, and the counts of `^## Goal$` and
   `^## Next Steps$`, one each.

G5 THE APPENDS, at C2 and C3, each read with `git show <base-sha>:<path>` so no
   tracked file is ever overwritten to get a baseline. For EACH of
   `.agent/live_review.md` (which takes LEDGER18 then FINDING714),
   `.agent/prose_slips.md` and `docs/roadmap/features/T5_F032.md`: READER (a),
   byte identity against the pre-commit bytes plus one newline plus the slice
   or slices in order — report `True`, the arithmetic, and that the pre-commit
   blob is a byte PREFIX. READER (b), structural — count N, the paragraphs the
   appended slices contribute, and compare the LAST N blank-line units of the
   post-commit file against those paragraphs IN ORDER; report N and the result.
   NEGATIVE CONTROL for each: flip one byte IN MEMORY inside the FIRST appended
   paragraph and report that BOTH readers reject it. Then report, before and
   after C2, the counts of `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `, `^Done: R-\d+
   — ` and `^Landed: R-`, the size of the open set, the maximum id, and the
   lists of gate keys and ids ADDED. The reviewer measured the open set at 250
   and the maximum at `R-0713`; this round registers exactly `R-0714` and
   resolves nothing, so the open set must read 251 and the maximum `R-0714`.

G6 THE EVIDENCE BUNDLE, after C3. Report the constant-by-constant diff S4
   requires between the F031 script and the adapted one; the adapted script's
   FULL stdout, untruncated, including every per-run line, the `SCAN rejected
   strings` count with its red control, and every `OUTPUT_HASH` line; and the
   absolute `EVIDENCE_DIR`. Report `git status --porcelain | wc -l` afterwards,
   which must still be `0` because the evidence directory is gitignored.

G7 INTEGRITY AND THE ZIP, after G6 and from a clean tree at C3. Report S5's
   integrity result and WHICH ROUTE produced it, quoting any refusal verbatim.
   Then report the zip command, its exit code, the printed package filename,
   its SHA-256, the manifest's `committed_review_subject` head and base, and
   the package's ARCHIVED PATH or the literal `NOT ARCHIVED`. If the build does
   not produce a READY package, report the RAW error and stop under constraint
   9.

G8 CANARY, DOCS, STRUCTURE AND THE PR GATE, at C3. FIRST the two suite
   obligations every round of this shape owes, both run BEFORE the evidence
   bundle so the accepted HEAD is gated by them: `python3 -m pytest
   tests/cli/test_golden_path.py -q`, the canary every handback runs, and
   `python3 -m pytest tests/docs/ -q`, owed because this round's change set
   includes `docs/roadmap/`. Report each command's exit code and pass line; the
   reviewer measured `295 passed` for the docs suite at `a4a24663` and orders
   the growth reported rather than predicted. THEN the structural readings.
   Report `git diff --name-only
   12f28a424be48fc41602383e8844f694e408553d..<C3>`, which is exactly the Change
   set less `.agent/handoff.md` — report BOTH residues. Report `git diff --stat
   12f28a424be48fc41602383e8844f694e408553d..<C3> -- packages/ apps/ tests/`,
   which must be EMPTY, and that `docs/roadmap/STATUS.md` and `README.md` are
   untouched. Report the insertion count of every commit from C0a through C3,
   each single-parent and each under 500, compared cell by cell against the
   `+/-` column of the handback's `## Commits` table. Report `^<<<SLICE ` and
   `^<<<END ` counts in every written file against a CONTROL over the committed
   C0a blob. Report `git ls-files .remedy-wt`, `git worktree list`, `git branch
   --list "tmp/*"`, and `gh pr list --state open --json
   number,headRefName,baseRefName,isDraft`.

----------

HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has no
length cap; it is valid when its mandated sections are present. It carries: the
feature and round, the SESSION NUMBER — this is SESSION 4 of F032, whose rounds
so far are R1 to R5 in session 1, R6 to R9 in session 2, R10 to R14 in session
3, and R15 through R18 in this one — the branch, the base and every commit SHA,
a per-commit changed-files table with the `+/-` column, ONE LINE PER GATE G1 to
G8 carrying its real readings, the item-status table covering C0a to C4 and S1
to S8 with every item present exactly once, the open-findings count, the
deviations and assumptions, and the next expected action.

IT ADDITIONALLY CARRIES A `## Closure artifacts` SECTION, because R19 cannot
author the STATUS line without it and `.agent/handoff.md` is the only channel
that survives this round: the evidence job id, the absolute EVIDENCE_DIR, the
package filename, its SHA-256, the package's archived path or `NOT ARCHIVED`,
the accepted HEAD in full, and the integrity route and result. State plainly
that no pull request was created, no STATUS line was flipped and nothing was
merged.

WRITE THIS FILE ONCE. `.agent/handoff.md` is rewritten in full every round and
is not an append-only record, so if a sentence in it turns out to be false, the
repair is a deviation line in the NEXT round's handback and NEVER a commit of
its own — that clause is carried here from the F032 R12 entry of
`.agent/live_review.md`, which labelled it binding on the next block ordering a
handback. Measure every numeral before writing it, and state no count you did
not count.
