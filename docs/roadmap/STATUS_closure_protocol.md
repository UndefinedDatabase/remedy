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
   Two more, from the F051 BLOCKED_EVIDENCE attempt (both caught by
   the packaging validator — catch them at authoring time instead):
   (a) verification records must carry non-empty test node ids with
   `len(node_ids) == selected` (run `--collect-only` for real ids);
   (b) `test_files` entries are files, never directories (expand
   `tests/docs/` to the actual file paths).
   A third, from the F052 BLOCKED_EVIDENCE attempt (caught by the
   packaging validator, fixed at authoring time): (c) the
   VerificationTests `run_id` must match `^vr-\d{4,}$`
   (`build_review_manifest._VT_RUN_ID_RE`) — a rejected
   VerificationTests document yields `vt_passed = None`, which
   fails the final-verifier confirmation.
   A fourth, from the F080 R4 attempt (94 rejected node ids, packaged
   BLOCKED_EVIDENCE): (d) a verification record can NEVER carry a
   FULL-SUITE node-id list. `len(node_ids) == selected` forbids
   filtering, and the packaging metadata scan correctly rejects the
   redaction-torture parametrizations whose ids embed fake secrets and
   absolute paths by design. The working shape: record the clean
   SCOPED suites in the bundle and let the full-suite proof ride in
   the committed integration-gate evidence and the reviewer's own
   re-run. The package still covers the accepted HEAD, and nothing
   green is claimed that was not run.
2. **Review zip (worker) — MANDATORY, fresh, never skipped.** Build via the
   canonical sequence below. Verify committed_review_subject spans
   BASE..HEAD and the zip import check passes. Record `package <filename>`
   and `SHA-256 <hash>`. **A failing zip build is a closure BLOCKER** —
   fix or go `[!]`; never close without the package.
   Docs-only features without a runtime evidence job close with an honest
   NO_EVIDENCE package (code-only snapshot); the STATUS line then omits the
   Evidence-job segment and records the NO_EVIDENCE package + SHA-256.
   Build order (wording aligned with accepted F252/F050 practice,
   2026-07-30; evidence-dir rule per DECISION 2026-08-01): the zip is
   built from a clean tree after all CONTENT commits — the reviewed
   head the manifest records as accepted HEAD. The final closure
   commit (STATUS/README/final .agent state) follows the READY zip;
   the evidence dir itself is NEVER committed (see "Evidence dir is
   not committed" below). A package built from a
   dirty tree is invalid. The zip attempt's outcome — package +
   SHA-256, or the raw error — is recorded in the handoff BEFORE
   handback, always.
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

## Closure-candidate findings

Operator ruling 2026-07-30 (F050→amend0730 precedent): findings
raised DURING a closure review are recorded in the closure brief as
CANDIDATES only — no R-id is spent, nothing is registered in the
already-final live_review. The NEXT session's first reviewed round
then either registers each candidate (spending the next free ID) or
resolves it inline as a DECISION per planner_reviewer_prompt.md §4
item 7. This keeps the ledger monotonic across the session boundary
and keeps the operator-facing narrative in agreement with the disk.

Disk vehicle (operator ruling 2026-08-01, F056-candidate loss): at
closure, any candidate findings are ALSO written to
`.agent/candidates.md` — one entry each: description, source
feature, date — inside the closure commit. `.agent/**` is already
within the closure commit's allowed path set, so the R-0154
exact-paths rule is unchanged. The chat brief keeps listing
candidates as before, but the FILE, not the brief, is the carrier
of record: a brief-only candidate is exactly what the F056 closure
lost. The Window-1 session bootstrap reads `.agent/candidates.md`;
if it is non-empty, the FIRST reviewed round registers each entry
(next free ID) or resolves it inline as a §4.7 DECISION, and
empties the file in that same round. A non-empty candidates file at
feature-claim time is itself a block condition
(planner_reviewer_prompt.md §1).

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

**Evidence dir is not committed (DECISION 2026-08-01, settling the
F056 closure candidate "evidence-protocol drift"):** `.gitignore`
excludes `remedy-job-evidence-*/`, and the F050–F061 closures
committed no evidence dir. The durable pointer is the package name +
SHA-256 + evidence job id in the STATUS line — exactly what every
closure since F050 records. Keep the dir outside the review subject
(session scratch is fine): a pre-committed evidence dir puts
evidence files into the base..HEAD review subject and the package
builds BLOCKED_EVIDENCE ("evidence is not authoritative") — F147
attempt-2 lesson.

## Failure honesty
If any precondition fails, the feature does NOT close. In order: another
repair round; `[!] <Fxxx> — <name> (blocked: <reason>)` authored by the
reviewer, committed by the worker; or an explicit operator decision in
.agent/decisions.md. Pretending completion is the one unforgivable failure
mode (AGENTS.md If-Blocked; P1 verify-before-claiming).
