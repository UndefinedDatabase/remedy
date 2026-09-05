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
6. EXACTLY ONE SELF-USE ITEM IS CONSUMED BY THIS CLOSE (F257). The first
   pending item in `scripts/self_use_queue.json` — the one
   `packages.orchestration.self_use_queue.next_self_use_item` answers — has
   been planned through `packages.orchestration.self_use_job` and RUN
   through `packages.orchestration.self_use_runner.run_next_self_use_item`
   (F258 T002) to the normal approval gate like any other job — never
   promoted — and its `consumed_by` set to this
   feature's id in the closure commit. Before that: every string
   `packages.orchestration.self_use_findings.describe_self_use_run_defects`
   returns for the run's own `JobPlan` (F258 T003) is registered as a normal
   R-id finding in `.agent/live_review.md` under the standard rules (red-proof
   required for a repair) before the close, and the closure paragraph names
   every finding raised and whether it was repaired; an empty tuple means
   nothing to register, not that nothing was checked. If the queue holds NO
   pending item,
   the session calls
   `packages.orchestration.self_use_generator.generate_and_append_if_empty`
   FIRST (F258 T001) — its Tier 1 (the oldest open Low/Medium finding in
   `.agent/live_review.md`) supplies one in practice, since the ledger rarely
   runs dry. Only once THAT also answers `None` is the track truly
   exhausted, not blocked: record `self-use NONE (queue exhausted)` in the
   handback and close normally, because a genuinely empty queue with no
   eligible source asks the operator to curate more rather than stopping a
   feature. Why this is a
   precondition and not an intention: "Remedy is used on Remedy" rots the
   moment it depends on someone remembering to do it, which is DECISION F257
   D2's CONSEQUENCE clause in as many words.

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
   DECISION amend0827 D1 (2026-08-27): record the package's ARCHIVED PATH
   beside its name and hash — the absolute directory the package was moved
   to, or the literal `NOT ARCHIVED` when it was left where it was built.
   The round that builds the package is the only actor that knows the
   answer, and without it no later session can tell whether the operator's
   review window is still open or whether the archive is simply somewhere it
   is not allowed to look. Reverse by dropping the field.
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
   `[x] <Fxxx> — <Name> (<T-slices> complete; accepted <YYYY-MM-DD> · live review <PASS|PASS_WITH_RISKS> — ACCEPTED[ · external verdict <V> — ACCEPTED] · Evidence job <job_id> · package <zip filename> · SHA-256 <hash> · package path <absolute dir|NOT ARCHIVED> · accepted HEAD <full sha>)`
   The `package path` segment is DECISION amend0827 D1's; it is the DURABLE
   carrier of the archived location, because `.agent/handoff.md` is rewritten
   at every handback and keeps nothing.
   `accepted HEAD` = the reviewed head the verdict and zip cover (manifest
   committed_review_subject.head_commit). External-verdict segment only
   when an external round happened. Touch no other line.
5. **Final commit + PR (worker).** STATUS edit is the last commit on the
   branch (Rule A4), with ONE permitted successor — see DECISION amend0827 D2
   under "Closure-candidate findings": a commit whose path set is exactly
   `.agent/candidates.md`, carrying a candidate the closure GATE raised, may
   follow it and is declared in the handback. Ordering (R-0154, F252 lesson): the README
   capability sync lands in the SAME commit as the STATUS `[x]` edit —
   README and STATUS may never disagree in any committed state (the
   ledger cross-check pin). The closure commit touches exactly
   docs/roadmap/STATUS.md, README.md, scripts/self_use_queue.json (the one
   `consumed_by` edit precondition 6 requires) and the final .agent/ state
   (incl. handoff.md rewrite) — nothing else; the feature file's Built
   State is already current from an earlier commit (precondition 4).
   Then the AGENTS.md PR workflow; description carries what/why, key
   decisions, how to review, changed-files table, latest verdict,
   open-findings count, runtime actuals.
   The closure handback includes grep proof that every piece of
   reviewer-authored applied text (STATUS line, resolution
   entries) is byte-identical to the authored paste block.
   Operator amendment amend0905-throughput (2026-09-05) — LEDGER ROTATION
   IS A STEP OF THIS SEQUENCE. After the verdict bookings and BEFORE the
   STATUS `[x]` flip, the worker runs `python3 scripts/rotate_live_review.py`
   as its OWN commit (paths: `.agent/live_review.md` and
   `.agent/live_review_archive.md` only). It moves, byte-verbatim, every
   `Gate:` record of a `[x]` feature and every resolved finding pair into
   the append-only archive, verifies each moved record's sha256 before and
   after and refuses on mismatch, keeps the open-findings count identical,
   and prints the old and new ledger sizes, which the handback records. The
   next block's byte-append arithmetic re-baselines on the post-rotation
   length; the archive is read only on demand, by id, never at session
   start. Reverse by deleting this paragraph.
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

DECISION amend0827 D2 (2026-08-27), the carrier for a candidate raised at the
CLOSURE GATE: a reviewer gating the closure commit itself has, under the two
rules above, no file left to write to — the disk vehicle wants the candidate
"inside the closure commit" and Rule A4's rendering makes that commit the last
on the branch. A `.agent/candidates.md`-ONLY COMMIT AFTER THE CLOSURE COMMIT IS
THEREFORE EXPLICITLY PERMITTED. Its path set is exactly that one file, it is
declared as such in the handback, and it is not a deviation to be argued case by
case. Rule A4 as stated in `docs/roadmap/ROADMAP.md` asks only that "STATUS.md
[is] updated in the same PR", which such a commit does not disturb, and the
R-0154 pin the rendering protects is README/STATUS agreement, which it cannot
touch. The rejected alternative was to move the closure gate BEFORE the closure
commit; that would leave the STATUS flip and the README sync as the one change
nobody gates, trading a recording gap for a verification gap. Reverse by
deleting this paragraph.

Operator amendment amend0827-process-diet (2026-08-27), rule 1 — the closure
sequence is the ONE exception to the ban on pure bookkeeping rounds. Registering
or resolving these candidates, and the verdict bookkeeping the closure needs, may
occupy rounds of their own here and only here.

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
