OUTCOME: pending
── STEP R1 — R0154 micro-round (docs-only, pre-F050) ────────────────
Goal:        Codify the R-0154 closure-ordering lesson in
             docs/roadmap/STATUS_closure_protocol.md (v4); merge the
             F252 closure PR first via the Open PR Gate.
Bundle:      Gate #161 · branch · authored texts (save + verify +
             apply) · docs gate + canary · one commit · PR (open,
             not merged).
Change:      docs/roadmap/STATUS_closure_protocol.md (FULL REPLACE),
             .agent/live_review.md, .agent/plan.md,
             .agent/authored/r0154-r1-{1,2,3}.md,
             .agent/last_block.md. Nothing else.
Constraints: AGENTS.md. Authored texts verbatim: save, sha256-verify
             against the BEGIN markers BEFORE any apply; mismatch =
             STOP + refusal record in .agent/last_block.md, apply
             nothing. Worker never writes ## Verdicts. The
             micro-round PR is NOT merged this round.
Done when:   Gate green (python3 -m pytest tests/docs/ -q + canary
             pytest tests/cli/test_golden_path.py -q, both exit 0;
             F252 baseline was 292 / 42 passed), cmp proofs exit 0,
             commit pushed, PR open.
Handback:    Completion report + rewrite .agent/handoff.md
             (changed-files table, sha256 + cmp proofs, raw gate
             transcripts, PR number).

PROCEDURE — STOP at the first red verification (AGENTS.md
If-Blocked); hand back the raw output.

1. Open PR Gate (AGENTS.md):
   gh pr list --state open --json number,headRefName,baseRefName,isDraft
   Expected: exactly one open PR — #161, head
   feature/f252-standing-red-paydown, base main, not draft. Then:
   gh pr merge 161 --merge --delete-branch
   git checkout main && git pull --ff-only
   Any other gate state (count != 1, draft, wrong base/head, merge
   failure) → STOP, hand back the raw output.
2. git checkout -b feature/r0154-closure-ordering
3. .agent/last_block.md guard: line 1 "OUTCOME: pending", then THIS
   block verbatim; flip to "OUTCOME: executed" at round end.
4. Save the three authored texts below VERBATIM (bytes between the
   BEGIN/END markers, including the final newline) to
   .agent/authored/r0154-r1-1.md, r0154-r1-2.md, r0154-r1-3.md.
   sha256sum of each file MUST equal its BEGIN marker before step 5.
5. Apply by copy (never retype):
   cp .agent/authored/r0154-r1-1.md docs/roadmap/STATUS_closure_protocol.md
   cp .agent/authored/r0154-r1-2.md .agent/live_review.md
   cp .agent/authored/r0154-r1-3.md .agent/plan.md
   cmp each target against its authored file → exit 0, all three.
6. Gate: python3 -m pytest tests/docs/ -q  AND canary:
   python3 -m pytest tests/cli/test_golden_path.py -q
   Both exit 0. Raw transcripts (command, exit code, tail) into the
   handback.
7. ONE commit of everything above:
   "docs(closure): codify the R-0154 ordering lesson — closure protocol v4"
   Push.
8. PR per AGENTS.md: title
   "R0154 micro-round — closure protocol v4 (ordering lesson)";
   body: what/why (operator-ordered pre-F050: persist the R-0154
   lesson — README capability sync in the SAME commit as the STATUS
   [x] edit; closure commit touches exactly STATUS.md, README.md,
   .agent/), changed-files table, gate results, verdict: pending R1
   review. Do NOT merge.
9. Handback per the Handback line above.

TRANSPORT NOTE (worker, R1): authored text 1 arrived hard-wrapped —
the step-4 STATUS template line was split after "· package". Rejoining
the two fragments with a single space reproduces the authored bytes
exactly (sha256 d2b67cb5… verified before any apply). The copy embedded
below is the sha256-verified form, so it re-verifies as-is. Texts 2 and
3 matched on first save. No other deviation.

--- BEGIN r0154-r1-1 sha256=d2b67cb5d12254aa9ed7253287eae8aa6a8895c83b000d7746b41c45df0545f9 ---
# STATUS.md Closure Protocol (v4)

> The only path from `[~]` to `[x]`. Reviewer (Window 1) authors; worker
> (Window 2) executes and commits. Grammar reference: ROADMAP.md Part C and
> the accepted F017/F018/F146 lines — the living precedent.

## Preconditions — ALL must hold; any failure aborts closure
1. Every step has a PASS round; every R-XXXX finding is Resolved or listed
   as a documented Medium/Low risk. Latest live_review verdict is PASS or
   PASS WITH RISKS — never PENDING/FAIL.
2. Full relevant suite green — verified by the reviewer running it where it
   has execution; otherwise via raw transcripts (command, exit code, real
   output) plus one reviewer-chosen spot-check. Never a summary.
   A dedicated integration-gate round (full suite, `pytest -n auto`, raw
   output) must have PASSed before closure; this precondition re-confirms it
   (planner_reviewer_prompt.md §3 verification tiers).
3. `remedy integrity check --json` → PASS; no relevant untracked files.
4. Feature file's Built State section is current.
5. Working tree clean, branch pushed, worker idle.

## Algorithm
1. **Evidence job (worker).** Final evidence run, fresh job id, feature-
   scoped (`feature_id=<fxxx>`). Record: `Evidence job <job_id>`.
   Canonical producer: `packages.orchestration.job_evidence.
   create_manual_completion_bundle(review_feature_id=<fxxx>, ...)` — it
   emits the full closed-schema gate set (final_verifier_report,
   fresh_evidence, artifact_contract, change_provenance, manifest_
   integrity, postmortem_integrity, commit_execution, runtime_integration).
   `write_runtime_integration_gate` alone is NOT a bundle and packages as
   BLOCKED_EVIDENCE.
   Packaging-deadlock rule: a High finding about closure packaging blocks
   `remedy integrity check` (high_blockers_open) and thereby the zip
   itself. The reviewer therefore attaches a CONDITIONAL resolution to
   such findings at authoring time — a mechanically checkable predicate
   (e.g. "Resolved when the complete bundle with all listed gates exists
   on disk at the current head") that the worker applies verbatim once the
   predicate holds — so persist → fix → resolve → package fits ONE relay.
   Producer pitfalls that block packaging: verification_runs
   entries need a sha256-hex output_hash, valid VerificationTests
   totals, and the full-length base_commit SHA — abbreviated or
   missing values surface only at zip time.
2. **Review zip (worker) — MANDATORY, fresh, never skipped.** Build via the
   canonical sequence below. Verify committed_review_subject spans
   BASE..HEAD and the zip import check passes. Record `package <filename>`
   and `SHA-256 <hash>`. **A failing zip build is a closure BLOCKER** —
   fix or go `[!]`; never close without the package.
   Docs-only features without a runtime evidence job close with an honest
   NO_EVIDENCE package (code-only snapshot); the STATUS line then omits the
   Evidence-job segment and records the NO_EVIDENCE package + SHA-256.
   Build order: the closure zip is the LAST action after ALL commits
   including the final .agent/ state and handoff rewrite; a package built
   from a dirty tree is invalid. The zip attempt's outcome — package +
   SHA-256, or the raw error — is recorded in the handoff BEFORE handback,
   always.
3. **Runtime actuals (reviewer; observed only).** Rounds, wall clock,
   models, tokens/cost where the ledger has them; `not-measured` beats a
   guess. → PR description + final report.
4. **STATUS line (reviewer authors, worker applies verbatim).** Template:
   `[x] <Fxxx> — <Name> (<T-slices> complete; accepted <YYYY-MM-DD> · live review <PASS|PASS_WITH_RISKS> — ACCEPTED[ · external verdict <V> — ACCEPTED] · Evidence job <job_id> · package <zip filename> · SHA-256 <hash> · accepted HEAD <full sha>)`
   `accepted HEAD` = the reviewed head the verdict and zip cover (manifest
   committed_review_subject.head_commit). External-verdict segment only
   when an external round happened. Touch no other line.
5. **Final commit + PR (worker).** STATUS edit is the last commit on the
   branch (Rule A4). Ordering (R-0154, F252 lesson): the README
   capability sync lands in the SAME commit as the STATUS `[x]` edit —
   README and STATUS may never disagree in any committed state (the
   ledger cross-check pin). The closure commit touches exactly
   docs/roadmap/STATUS.md, README.md and the final .agent/ state
   (incl. handoff.md rewrite) — nothing else; the feature file's Built
   State is already current from an earlier commit (precondition 4).
   Then the AGENTS.md PR workflow; description carries what/why, key
   decisions, how to review, changed-files table, latest verdict,
   open-findings count, runtime actuals.
   The closure handback includes grep proof that every piece of
   reviewer-authored applied text (STATUS line, resolution
   entries) is byte-identical to the authored paste block.
6. **Merge — deferred to the next feature.** The closure PR is NOT merged
   in this session. It merges at the next feature's start via the Open PR
   Gate on Window 1's instruction; the gap is the operator's manual-review
   window. The operator may merge manually at any time instead.
7. **End Window 1** with the feature-done banner. Next feature → fresh
   session; Rule A5 selects it.

## Canonical zip build sequence
Explicit evidence selection is mandatory. Deprecated root-dir auto-selection
(mtime-based `remedy-job-evidence-*` scanning) is disabled — the script
hard-errors if legacy dirs exist and no `--evidence-dir` or `--job-id` is
given.

```bash
# 1. Ensure tree is clean and branch is pushed.
git status          # must be clean
git push

# 2. Build with explicit evidence dir (preferred):
bash scripts/make_review_zip.sh --evidence-dir <path-to-evidence-dir>

# Or by indexed job id:
bash scripts/make_review_zip.sh --job-id <job-id>

# 3. Without evidence (code-only snapshot, e.g. docs-only features):
bash scripts/make_review_zip.sh
```

**Stale `review_archive_plan.json`:** The pipeline automatically deletes any
plan copied from evidence staging before generating a fresh one. No manual
step needed — `build_review_zip.py` always writes a new plan with current
SHA-256 hashes.

**Output:** The script prints the final zip filename and SHA-256. Record both
in the STATUS line (`package <filename>` and `SHA-256 <hash>`).

**Evidence-dir commit ordering:** the evidence dir is committed
AFTER the READY zip exists, never before. A pre-committed
evidence dir puts evidence files into the base..HEAD review
subject and the package builds BLOCKED_EVIDENCE ("evidence is
not authoritative") — F147 attempt-2 lesson.

## Failure honesty
If any precondition fails, the feature does NOT close. In order: another
repair round; `[!] <Fxxx> — <name> (blocked: <reason>)` authored by the
reviewer, committed by the worker; or an explicit operator decision in
.agent/decisions.md. Pretending completion is the one unforgivable failure
mode (AGENTS.md If-Blocked; P1 verify-before-claiming).
--- END r0154-r1-1 ---

--- BEGIN r0154-r1-2 sha256=e3066d09858a8687175f8ec0477a18ef549f9380d3d4aabaf72aff8dfb541f34 ---
# Live Review — R0154 micro-round (closure-ordering codification)

> Docs-only micro-round ordered by the operator before F050: persist
> the R-0154 ordering lesson from the F252 closure into
> docs/roadmap/STATUS_closure_protocol.md. Reviewer: Window 1.

## Steps
- R1: replace docs/roadmap/STATUS_closure_protocol.md with the
  authored v4 text (step 5 now pins the R-0154 ordering: README
  capability sync in the SAME commit as the STATUS `[x]` edit; the
  closure commit touches exactly STATUS.md, README.md and the final
  .agent/ state). Gate: tests/docs + canary. In progress.

## Findings
(none yet — IDs continue monotonically from R-0154; next free: R-0155)

## Verdicts
(pending R1)
--- END r0154-r1-2 ---

--- BEGIN r0154-r1-3 sha256=f87463160259b1b1cfedf89a593fcf10eb37502827d4892ab70a31cffaeb7046 ---
# Plan — R0154 micro-round (docs-only), then F050

## Goal
Persist the R-0154 ordering lesson from the F252 closure into
docs/roadmap/STATUS_closure_protocol.md (v4): the README capability
sync lands in the SAME commit as the STATUS `[x]` edit, and the
closure commit touches exactly docs/roadmap/STATUS.md, README.md and
the final .agent/ state — nothing else. Merge the micro-round PR,
then proceed to F050 per Rule A5.

## Next Steps
- R1: apply the authored protocol v4 text, gate with
  `python3 -m pytest tests/docs/ -q` + the golden-path canary,
  commit, push, open the PR.
- After the reviewer's PASS: merge the micro-round PR (operator
  pre-authorized), then bootstrap F050 — DAG scheduling.
--- END r0154-r1-3 ---
