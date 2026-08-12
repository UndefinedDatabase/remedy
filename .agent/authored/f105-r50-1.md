── STEP closure-prep — F105 R50 ──────────────────────────────
Goal:        Resolve R-0269, record the R49 gate and the residual risks F105
             closes on, then build the two closure artifacts — the evidence
             bundle and a FRESH review zip — WITHOUT closing the feature.
Bundle:      C1 save block · C2 mirror · C3 the gate, the resolution and the
             risk register · C4 integrity check · C5 evidence job · C6 review
             zip · C7 plan, handoff, push.
Change:      .agent/authored/f105-r50-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md.
             NOTHING else. No production code, no tests, no docs, no STATUS.md,
             no README.md, no PR. The evidence dir and the zip are BUILT but
             NOT committed.
Constraints: The feature does NOT close this round. PR #189 blocks the closure
             PR and only the operator can resolve it. No merge, no `main`, no
             force-push.
Done when:   R-0269 reads Resolved, the risk register is on disk, and both
             artifacts have a recorded outcome — a package name plus SHA-256,
             or a raw error. Either is a valid result; a missing record is not.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────

C1 — write this ENTIRE block to `.agent/authored/f105-r50-1.md` byte for byte,
  commit it ALONE.
C2 — `cp` it over `.agent/last_block.md`, commit alone, `cmp` silent.

C3 — .agent/live_review.md. ONE pair, PAIR_DONE, and it is a REWRITE: the
  worker's `Landed:` line is REPLACED by the reviewer's resolution text. The
  TO does not contain the FROM. No ID advance: R50 registers no finding, so
  the next free ID stays R-0270.

<<<PAIR_DONE_FROM>>>
  Landed: R-0269 — the note now states what the directional guard proves and what it cannot catch, one paragraph in the measurement section of docs/system/cache-optimal-prompt-ordering-v1.md, in this round C4 commit.
<<<END_PAIR_DONE_FROM>>>

<<<PAIR_DONE_TO>>>
  Done: R-0269 — RESOLVED at R49 C4 (a8b6f66e). The note now carries, in its
  measurement section, both halves of the truth: the directional guard proves a
  REGRESSION property — composition never orders a role's prompt worse than the
  hand-written original — and does NOT prove that the registry sorts, since
  forcing every segment to one rank leaves `plan` at exactly its own
  `before_prefix` of 227 with the assertion still passing, while reversing the
  sort key does fail five of six roles. It names the T003 goldens' rank
  assertions as the proof of the sort. Verified by the reviewer against the
  committed diff, not the report: the paragraph's numbers match the reviewer's
  own R48 worktree probe exactly, and both cited test names
  (`test_manifest_names_and_ranks`, `test_manifest_ranks_are_non_decreasing`)
  were confirmed to exist in the goldens. The durable doc now carries what only
  a rewritten handoff carried before, which was the whole finding.
- Reviewer gate on R49 (2026-08-12): PASS — and this is the INTEGRATION GATE
  entry for F105, the one entry permitted to claim the full suite.
  Range `9c80cf59..5786967b` = seven commits, exactly the fifteen paths the
  block named, no production code and no test module among them. Insertions per
  commit 209, 181, 69, 15, 268, 149 and 14, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r49-1.block.md`, the
  committed `.agent/authored/f105-r49-1.md` and `.agent/last_block.md` all
  three hash to
  `2a191709a351799e814c69fb3754d8206660e08cb26c36d922903859336efba4`
  at 209 lines; both `cmp` runs silent.
  Stray reconcile over C3: 69 added, 1 removed, 0 stray. PAIR_ID measured as a
  REWRITE, the ID line reading R-0270 1x and R-0269 0x; PAIR_LR measured
  CONTAINS-FROM, FROM 1x before and 1x after.
  THE FULL SUITE WAS RE-RUN BY THIS REVIEWER, not taken from the handback:
  `python3 -m pytest -n auto -q` on the branch returns
  `16462 passed, 19 skipped in 114.17s`, exit 0 — the same 16462/19/0 the
  worker recorded at 99s, reproduced independently. Zero failures on the
  branch, so `comm -13` is empty by construction and no branch-only id exists
  to attribute. There is no BLOCKER.
  The seven base-only ids are all
  `tests/ui_server/test_live_state.py::TestUIServerIntegration::*` and all
  belong to the R-0221 environment class. The attribution is the strongest this
  branch has produced: the failure text names the cause (`Server did not start
  in time`, stderr `ERROR: React UI not built.`), the predicate was MEASURED
  rather than assumed (base dist 08:54:33 against newest base src 08:55:15 —
  stale by construction, because `cp -a` preserves the dist mtime while
  `git worktree add` stamps the sources fresh), and each of the seven passes on
  a serial re-run at the merge base once R-0221's own test rebuilds dist there.
  The reviewer confirmed `_frontend_is_stale()` reads exactly that predicate.
  The parity claim was proved by CONTENT, not by trusting the env var: one
  aggregate `apps/ui/dist` hash across all four readings, and the primary's
  dist mtime unmoved, so nothing wrote through into the primary checkout. The
  base worktree ran on the throwaway branch `tmp/base-gate` per DECISION D3,
  and was removed, pruned and deleted with proof.
  Membership of the class differs from F104 R7's six ids; the worker's reading
  — xdist scheduling deciding which ids run before the mid-run rebuild, not a
  growing defect — is consistent with all three methods existing at base. Flake
  debt is NOT growing: zero branch-only failures this gate, against an alarm
  threshold of ten.
  Both declared deviations are ACCEPTED and both are self-reference limits, not
  scope changes: a `Landed:` line committed with its own fix cannot name a
  later SHA, and a gate row counting insertions per commit cannot count the
  commit that writes it (C6b, the R47 C3b shape already accepted).
  `LAST_REVIEWED_SHA` advances 9c80cf59 -> 5786967b.
- Residual risks F105 closes on. Seven findings stay OPEN, every one Low or
  Medium, none inside F105's own change set, none blocking acceptance — the
  "listed as a documented Medium/Low risk" branch of
  STATUS_closure_protocol.md precondition 1. No High finding is open, so the
  `high_blockers_open` condition does not apply.
  - R-0221 (Low) — the UI auto-build test rebuilds `apps/ui/dist` mid-suite and
    costs every integration gate phantom base-only failures; exactly seven at
    the R49 gate, all attributed. Not F105's code; routed to the F252
    flake-debt class.
  - R-0239 (Low) — a reviewer-authored gate citation named a path that does not
    exist. The worker caught it, ran the real path and declared the correction,
    so nothing was skipped and no number is wrong. It stays open as the record
    of the citation-accuracy lesson, not as outstanding work.
  - R-0247 (Low) — a reviewer-authored finding cited a line count of 101 where
    the file was 100. The substance was untouched and the finding's own subject
    was fixed. Same class as R-0239, same reason for staying open.
  - R-0262 (Low) — `plan_job_llm` composes its prompt OUTSIDE the `try` that
    turns a provider failure into a renderable result, so a raising composer
    escapes the function. Pre-existing, real, and deliberately outside F105's
    change set: F105 moved composition, it did not own error handling.
  - R-0265 (Medium) — a provider that reports usage but no cache field leaves a
    measured-looking `0` the ledger cannot distinguish from a real zero.
    Documented in `docs/system/cache-optimal-prompt-ordering-v1.md` rather than
    worked around; the fix belongs to the actuals producer.
  - R-0266 (Medium) — the ledger's `role` is a hardcoded `builder` in
    production data, so a per-role split of production rows is one bucket.
    `remedy stats cache` prints that limit in its own output instead of burying
    it. The fix is a producer change, out of scope here.
  - R-0268 (Low) — a `.agent/STOP` file carries no provenance. Belongs to the
    self-drive protocol, not to prompt composition.
- R50: closure PREPARATION, not closure. The resolution above, this risk
  register, the integrity check, the evidence bundle and a fresh review zip.
  The STATUS line, the README sync and the closure PR are deliberately NOT in
  this round: PR #189 is open from a non-`feature/*` branch, which the
  AGENTS.md Open PR Gate makes stop-and-report, and only the operator can
  resolve it. F105 stays `[~]`.
<<<END_PAIR_DONE_TO>>>

C4 — integrity check. Run `remedy integrity check --json`; if `remedy` is not
  on PATH in this sandbox, use the identical module entry point (the R48/R49
  precedent is `python3 -m apps.cli.grouped ...`) and SAY which form you used.
  Record the raw JSON verdict and every non-PASS check by name. This is closure
  precondition 3. Do not fix anything it reports in this round — record it.

C5 — evidence job, per STATUS_closure_protocol.md step 1. READ the producer
  before calling it:
  `packages.orchestration.job_evidence.create_manual_completion_bundle`, called
  with `review_feature_id="f105"`. Read its real signature and honour it; do
  not guess arguments. `write_runtime_integration_gate` alone is NOT a bundle
  and packages as BLOCKED_EVIDENCE — use the canonical producer.
  Build the evidence directory UNDER `.remedy-wt/`, never inside the review
  subject, and do NOT commit it. Record the job id.
  The protocol lists the producer pitfalls that surface only at zip time —
  sha256-hex `output_hash`, valid VerificationTests totals, full-length base
  commit SHA, non-empty node ids with `len(node_ids) == selected`, `test_files`
  as files not directories, `run_id` matching `^vr-\d{4,}$`, and NEVER a
  full-suite node-id list. Read that section and honour it. Record the clean
  SCOPED suites; the full-suite proof rides in the committed R49 gate evidence
  and the reviewer's own re-run.

C6 — review zip, per the protocol's "Canonical zip build sequence". The tree
  must be clean and the branch pushed BEFORE building. Explicit evidence
  selection is mandatory:
  `bash scripts/make_review_zip.sh --evidence-dir <the C5 dir>`
  Verify `committed_review_subject` spans BASE..HEAD and that the zip import
  check passes. Record the package filename and its SHA-256.
  A FAILING zip build is a closure BLOCKER, not something to route around:
  record the raw error, state plainly that closure is blocked on it, and hand
  back. Do not fall back to a no-evidence package to produce something.

C7 — plan and handoff.
  Rewrite `.agent/plan.md` (UNDER 50 lines, keeping `## Goal` and
  `## Next Steps`). It must state: `LAST_REVIEWED_SHA` is 5786967b with R49
  GATED PASS and the INTEGRATION GATE PASSED (16462 passed, 0 failed, 0
  branch-only); T001-T004 all DONE; R-0269 Resolved and seven residual risks
  registered; the real outcome of the integrity check, the evidence job and the
  zip; and that F105 remains `[~]`, NOT closed. Next Steps: the operator
  resolves PR #189, then ONE closure round writes the STATUS `[x]` line and the
  README capability sync in the SAME commit (R-0154), commits it LAST on the
  branch, and creates the closure PR.
  Then rewrite `.agent/handoff.md` (UNDER 60 lines, or over with a DECISION D15
  "Deviations, declared" line naming the real count and the mandated content
  that caused it). Feature and round, branch, this round's SHAs, changed-files
  table, item-status table for C1-C7, the gates below with real exit codes, the
  open-findings count, and the next expected action. It MUST record the
  integrity verdict, the evidence job id, and the package name + SHA-256 or the
  raw failure — every artifact-build attempt appears with its status, including
  failed attempts with blocking reasons (AGENTS.md handoff.md rules).
  Commit C7, push the branch, create NO pull request.

Gates — real exit codes, never the word "green"
  A  sha256sum + cmp across the scratch block file, `.agent/authored/f105-r50-1.md`
     and `.agent/last_block.md`: all three equal, both cmp silent.
  B  wc -l the authored file against the cap of 400.
  C  PAIR_DONE is a REWRITE: measure FROM 1x before and 0x after, and each
     TO-ONLY added line exactly 1x AMONG THE LINES C3's OWN DIFF ADDS.
  D  Stray reconcile for C3: every ADDED line appears in the authored file.
     Report added, removed and stray counts.
  E  grep -c '^<<<' over live_review.md, plan.md and handoff.md — all 0.
  F  grep -c '^## Steps' .agent/live_review.md — exactly 1. The file gains no
     new `##` heading this round; the risk register is a bullet inside Steps.
  G  python3 -m pytest tests/docs/ -q
  H  Canary: python3 -m pytest tests/cli/test_golden_path.py -q
  I  `git status --porcelain` empty and `git worktree list` shows the primary
     ALONE. Prove the evidence dir and the zip are NOT tracked:
     `git status --porcelain --ignored | grep -c remedy-job-evidence` and a
     `git ls-files` check that neither artifact is committed.
  J  insertions per commit under 500; `git diff --name-only 5786967b..HEAD` is
     exactly the five `.agent/` paths named above — no STATUS.md, no README.md,
     no docs, no tests, no production code.
