You are the WORKER for F103 R7 (SPLIT round): CLOSURE PART 1 — Built State, the load-bearing full-suite confirmation run, the evidence job and a FRESH review zip, per docs/roadmap/STATUS_closure_protocol.md.

Read these before acting, from disk, not from memory: AGENTS.md (highest authority), docs/roadmap/STATUS_closure_protocol.md, docs/agents/worker_conventions.md, docs/agents/handback_template.md, .agent/plan.md, .agent/live_review.md, .agent/handoff.md.

You are the ONLY writer this round. The reviewer is read-only and will re-run every verification command itself before any verdict. A summary is not evidence — record real commands, real exit codes, real output.

The STATUS `[x]` line and the README sync are NOT written this round. The reviewer authors them from the values your handback reports; R8 applies them. Do not create a PR.

If anything goes red: STOP per AGENTS.md If-Blocked, commit only the valid completed portion, and hand back with the RAW output. A failing zip build is a closure BLOCKER — do not work around it, do not retry blind.

── STEP closure-1/2 — F103 ────────────────────────────────────
Goal:        Persist the R7/R8 closure split, land the Built State
             section, satisfy the closure preconditions, run the
             load-bearing full-suite confirmation, and produce the
             evidence job plus the fresh review zip.
Bundle:      1 state commits · 2 Built State · 3 preconditions ·
             4 full-suite confirmation · 5 evidence job ·
             6 review zip · 7 handback
Change:      .agent/** state files and
             docs/roadmap/features/T2_F103.md (APPEND) ONLY.
             No STATUS.md, no README.md, no source, no tests.
Constraints: The evidence dir is gitignored and OUTSIDE the review
             subject; it is NEVER committed (a committed dir turns
             the package BLOCKED_EVIDENCE — F147 attempt-2 lesson).
             Commits under 500 lines each. Never force-push. Never
             work on main. `git add -A` is forbidden — stage exact
             paths.
Done when:   Integrity check PASS, full suite green at the content
             HEAD, bundle complete, zip import check green, package
             filename + SHA-256 recorded.
Handback:    Completion report + rewrite .agent/handoff.md (see 7).
───────────────────────────────────────────────────────────────

1. STATE COMMITS (persist FIRST)
   Three authored texts follow at the bottom, delimited by BEGIN/END
   markers. The authored bytes are everything BETWEEN the marker
   lines, including the final newline; the marker lines are never
   content.
   a. COMMIT A: this entire prompt saved verbatim to
      .agent/last_block.md (own commit), message
      "chore(f103): save the R7 closure block".
   b. Save the three texts to .agent/authored/f103-r7-1.md,
      .agent/authored/f103-r7-2.md, .agent/authored/f103-r7-3.md.
      Verify each with `sha256sum` against its BEGIN-marker hash.
      Any mismatch → STOP, hand back naming the block and BOTH
      hashes; apply nothing.
      COMMIT B: exactly those three files, message
      "chore(f103): save the R7 authored texts".
   c. Apply f103-r7-1 to .agent/live_review.md as TWO FROM→TO
      replacement pairs. BOTH pairs are REWRITES (the TO does not
      contain the FROM), so for each pair report, FROM BEFORE any
      edit: FROM count 1x, TO count 0x; and AFTER the edit: FROM 0x,
      TO 1x. Each FROM string is a unique whole line in the file
      (verified by the reviewer: line 42 and line 425).
      Apply f103-r7-2 to .agent/plan.md as a COMPLETE replacement,
      by `cp .agent/authored/f103-r7-2.md .agent/plan.md`, then
      prove it with `cmp .agent/authored/f103-r7-2.md .agent/plan.md`
      and record the exit code.
      COMMIT C: exactly .agent/live_review.md and .agent/plan.md,
      message "chore(f103): split closure into R7 and R8 and set the
      closure plan".

2. BUILT STATE (content commit — closure precondition 4)
   docs/roadmap/features/T2_F103.md currently ends with the line
   "already the primary key, so no schema migration is needed."
   followed by one newline. Apply f103-r7-3 as a pure APPEND to the
   end of that file — the authored text BEGINS with a blank line, so
   append it exactly as-is with no added or removed blank lines.
   Prove the append shape: the file's byte count before + the
   authored file's byte count == the byte count after, and
   `tail -c <N>` of the result is byte-identical to the authored
   file (any equivalent disk-to-disk proof is fine — record the
   command and its exit code).
   COMMIT D: exactly docs/roadmap/features/T2_F103.md, message
   "docs(f103): Built State — ledger store, live mirror, cost CLI".
   GATES for this docs-round change (planner_reviewer_prompt.md §3
   item 5), both must exit 0:
     python3 -m pytest tests/docs/ -q
     python3 -m pytest tests/cli/test_golden_path.py -q
   Red → STOP and hand back the raw output.

3. PRECONDITIONS (closure protocol head)
   a. `python3 -m apps.cli.grouped integrity check --json` — record
      the RAW json. Must be `"passed": true`. Not PASS → STOP.
      (The `remedy` console script is blocked by this session's
      permission policy; the module entry point is the same code.)
   b. `git status --porcelain` → empty.
      `git ls-files --others --exclude-standard` → no relevant
      untracked files.
   c. `git push` — the branch must be up to date, because the zip
      records committed state.

4. FULL-SUITE CONFIRMATION RUN (closure protocol precondition 2)
   THIS IS LOAD-BEARING, NOT A FORMALITY. R6 landed production code
   in packages/orchestration/job_evidence.py AFTER the R5 integration
   gate, so this is the ONLY full-suite evidence covering the
   live-mirror wiring. Run it at the content HEAD from step 2:
     python3 -m pytest -n auto -q
   Record the command, the full tail (counts line), the exit code and
   the wall clock. Any failure → STOP and hand back the raw failing
   ids; a regression here is a normal repair round, not something to
   route around. Note for context: the R5 gate measured 16121 passed
   / 19 skipped on this branch.

5. EVIDENCE JOB (closure protocol algorithm step 1)
   Produce the final bundle with the canonical producer,
   `packages.orchestration.job_evidence.create_manual_completion_bundle`,
   called with `review_feature_id="f103"` and `job_id="f103-closure"`
   (the F080/F254 naming precedent), writing into a NEW evidence dir
   named `remedy-job-evidence-f103-closure/` at the repository root —
   that glob is already in .gitignore (line 226), so the dir is
   outside the review subject and must never be committed.
   `write_runtime_integration_gate` alone is NOT a bundle.
   Values:
   - repo_root: the repository root.
   - base_commit: the FULL sha
     c1c0fbcbfb6b8ddb0d6fd30cb4bf8459b334a05d (the merge base with
     main). Full length, never abbreviated.
   - head_commit: the FULL sha of the content HEAD after COMMIT D.
   - job_title / step_range: name F103 and the round range R1-R7.
   Honour every named producer pitfall AT AUTHORING TIME. Each
   `verification_runs` entry uses the fields
   run_id, command, exit_code, passed, failed, test_files,
   stdout_summary, head_sha, output_hash, selected, deselected,
   skipped, node_ids, duration_seconds, and must satisfy:
   - `run_id` matches `^vr-\d{4,}$`;
   - `output_hash` is bare sha256 HEX;
   - `test_files` entries are FILES, never directories;
   - `node_ids` are REAL ids taken from `--collect-only -q`, with
     `len(node_ids) == selected`;
   - exit_code 0 and failed 0 (the producer refuses otherwise).
   Record the SCOPED suites only — recommended:
   tests/orchestration/test_token_ledger.py and
   tests/cli/test_stats_cost.py (115 together at the reviewer's own
   run). Do NOT put a full-suite node-id list in a verification
   record: `len(node_ids) == selected` forbids filtering and the
   packaging metadata scan rejects the redaction-torture ids by
   design (F080 R4, 94 rejected ids, packaged BLOCKED_EVIDENCE). The
   full-suite proof rides in step 4's transcript and the reviewer's
   own re-run, which is the working shape.
   Record the producer invocation and its full stdout, including the
   returned summary dict and the final verdict.

6. REVIEW ZIP (closure protocol algorithm step 2 — MANDATORY, FRESH)
   From a CLEAN tree at the content HEAD (a package built from a
   dirty tree is invalid):
     bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f103-closure
   Verify that committed_review_subject spans
   c1c0fbcbfb6b8ddb0d6fd30cb4bf8459b334a05d..<content HEAD> and that
   the zip import check passes. Record the printed package filename
   and SHA-256 EXACTLY — they go verbatim into the STATUS line the
   reviewer authors. A zip failure is a closure BLOCKER: STOP, hand
   back the raw error.

7. HANDBACK
   Re-run the canary if any commit followed step 2. Final
   `git status --porcelain` → empty, and the evidence dir must still
   be untracked-and-ignored (`git status --porcelain` must not list
   it). Rewrite .agent/handoff.md as the LAST commit, message
   "chore(f103): rewrite handoff for the R7 handback", and push.
   The handoff carries:
   - feature + round, branch, the per-commit changed-files table;
   - the transport proofs: the three sha256 verifications, the two
     pair counts before and after, the `cmp` exit code for plan.md,
     and the append proof for the feature file;
   - the verification table with REAL exit codes: docs gate, canary,
     integrity check, the FULL-SUITE confirmation (counts + wall
     clock), the producer run, the zip build tail;
   - the four values the reviewer needs, VERBATIM, one per line:
     evidence job id · package filename · SHA-256 · content HEAD
     (the full sha at handback; if the handoff commit moves HEAD,
     state BOTH the content HEAD and the final HEAD);
   - the item-status table (AGENTS.md), every bundle item 1-7
     exactly once, with `done` / `skipped` / `deviated` and a reason;
   - open findings count (0) and the next expected action (R8);
   - any deviation, DECLARED, with its cause. The stated-cause
     overage clause applies: never drop a mandated section to meet
     the line cap.
   NO STATUS.md edit. NO README.md edit. NO PR. Those are R8.

AUTHORED TEXTS

<<<BEGIN AUTHORED f103-r7-1
sha256=aeb26d7dd909d3860cfc83e6fe7172fe4b5d1c7368b33e4ed1d2676c77b10201>>>
PAIR 1 — REWRITE
FROM:
- R7: closure per docs/roadmap/STATUS_closure_protocol.md.
TO:
- R7: closure part 1 per docs/roadmap/STATUS_closure_protocol.md — the
  Built State section, the load-bearing full-suite confirmation run,
  the evidence job and the FRESH review zip. Closure runs in TWO relays
  because the STATUS line quotes the evidence job id, the package name
  and its SHA-256, and the reviewer can only author that line once
  those values exist (F079 R4/R5 and F254 R11/R12 precedent).
- R8: closure part 2 — the reviewer-authored STATUS `[~]`->`[x]` line
  and the README capability sync in the SAME commit (R-0154), last on
  the branch (Rule A4), then `gh pr create`; the PR is NOT merged by
  the session that creates it.

PAIR 2 — REWRITE
FROM:
- R7: pending — closure, next session.
TO:
- R7: in flight — closure part 1. Awaiting the handback with the
  evidence job id, the package filename, its SHA-256 and the content
  HEAD the zip records as the accepted head.
- R8: pending — closure part 2.
<<<END AUTHORED f103-r7-1>>>

<<<BEGIN AUTHORED f103-r7-2
sha256=db2f23b12b432b87af6e95c148ad322b642bd4d2e3084f94b0a05a2d2dd3e44d>>>
# Plan — F103 Token ledger (SQLite)

Branch: feature/f103-token-ledger · claimed `[~]` in
docs/roadmap/STATUS.md. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
R1-R6 PASSed; LAST_REVIEWED_SHA 7f32dae9. Open findings 0; next free
ID R-0222. R-0221 is carried in `.agent/candidates.md`. No PR exists.

## Goal
Close F103 per docs/roadmap/STATUS_closure_protocol.md. The substance
is built and gated: T001 schema plus the never-fail writer, T002 the
call site with backfill and a content-comparing reconcile, T003 the
cost aggregation with `remedy stats cost`, `backfill-ledger` and
`verify-ledger`, the R5 integration gate, and R6's live mirror at the
task-run evidence seam so a real job yields rows. Closure records what
was built on the feature file and packages the accepted head.

## Current Step
R7 — closure part 1: the Built State section on
docs/roadmap/features/T2_F103.md (a CONTENT commit, before the zip),
the closure preconditions, the LOAD-BEARING full-suite confirmation
run, the evidence job through `create_manual_completion_bundle` with
`review_feature_id="f103"` into a gitignored dir outside the review
subject, and a FRESH review zip from that clean content head. The
handback carries the job id, the package filename, its SHA-256 and the
content HEAD; the reviewer authors the STATUS line from those values
and never from a guess.

## Next Steps
- R8 — closure part 2: apply the authored STATUS `[~]`->`[x]` line and
  the README ledger sync in the SAME commit (R-0154), keep R-0221 in
  `.agent/candidates.md` as the next feature's block condition, write
  the final `.agent` state, commit LAST on the branch (Rule A4), push,
  `gh pr create`. That PR merges at the next feature's Open PR Gate,
  which is the operator's manual-review window.

## Risks
- The full-suite confirmation is LOAD-BEARING, not a formality: R6
  landed production code AFTER the R5 gate, so it is the only
  full-suite evidence over the live-mirror wiring. A regression there
  is a normal repair round, never a closure workaround.
- Packaging pitfalls named in the protocol must be met at authoring
  time: sha256-hex output_hash, FULL-length base_commit, real node ids
  with `len(node_ids) == selected`, `test_files` are files and never
  directories, `run_id` matching `^vr-\d{4,}$`, and NEVER a full-suite
  node-id list.
- The evidence dir stays OUTSIDE the review subject and is never
  committed — a committed one packages BLOCKED_EVIDENCE.
- A failing zip build is a closure BLOCKER: stop, hand back the raw
  error, do not work around it.
<<<END AUTHORED f103-r7-2>>>

<<<BEGIN AUTHORED f103-r7-3
sha256=e17ddc6d8f54df1252b4143169442c5a0c77d17174138a20fe8a480fb3246c5b>>>

## Built State (accepted 2026-08-08, R1–R6)

Built and reviewed on branch feature/f103-token-ledger:

- **Store & writer** (packages/orchestration/token_ledger.py, T001):
  `SCHEMA_VERSION = 1` recorded in a `meta` row, migrations as numbered
  steps rather than an if-ladder. One database per project at
  `token_ledger_path_for(project_id)` =
  `<data_root>/projects/<uuid>/ledger.sqlite` (`LEDGER_FILENAME`);
  `open_ledger` sets `PRAGMA journal_mode=WAL` plus a busy timeout and
  migrates on open. Table `calls` is keyed by `call_id` and carries the
  three covering indexes the Design names (job_id; ts_utc; role+model).
  `record_call` NEVER fails the run: any failure returns False and
  increments the counter `ledger_miss_count()` reads, so a miss is
  counted rather than silently dropped. The module docstring carries the
  mandated sentence verbatim — "The file evidence remains the source of
  truth and the database is a mirror." Python's bundled `sqlite3` only:
  no ORM, no new dependency. This is the FIRST and so far ONLY use of
  SQLite in Remedy, and the docstring says so where a reader would look.
- **Row granularity** (DECISION D16): a row is one FINALIZED TASK RUN,
  its key `call_id_for_task_run(job_id, task_id)` = `"<job_id>:<task_id>"`.
  No per-HTTP-request record exists on disk, and synthesising one would
  fabricate ids, timestamps and a usage split no file records — the F075
  tokens-unmeasured lesson. Remedy deliberately does not do that.
- **Data layer** (T002): `call_record_from_evidence` derives a row from
  `task_runs/<task_id>/provider_evidence.json` through `token_truth`'s
  own canonical aliases — imported, never re-parsed, so the feature adds
  no second capture path. `backfill_ledger` scans an evidence tree, is
  idempotent by `call_id`, and its counters satisfy
  `scanned == recorded + skipped + failed` on every path.
  `verify_ledger` compares CONTENT, not presence (finding R-0219): it
  re-derives each row from its own evidence through the same builder the
  live hook uses and reports field-level mismatches in `drifted_rows`.
- **Live mirror** (packages/orchestration/job_evidence.py, R6, finding
  R-0220): `_resolve_job_ledger_project_id` resolves the target ONCE per
  export, read-only, and `export_job_evidence` threads it and the job id
  through `_write_task_run_evidence` into the writer's keyword-only
  `ledger_*` opt-in. A real job therefore yields its task runs as rows
  with nobody passing a `ledger_*` argument by hand, which is what makes
  the acceptance criterion true of the built system rather than of a test
  that armed the hook itself. An absent `repo_path` returns None instead
  of letting `Path("")` become the process CWD, so evidence export can
  never escape into the wrong project.
- **Queries & CLI** (T003): `query_cost` and `merge_cost_reports` bucket
  by role, model or day and aggregate read-only across projects;
  `apps/cli/commands/stats_ledger_cmd.py` adds `stats.cost`,
  `stats.backfill-ledger` and `stats.verify-ledger` to the existing
  `stats` group, in human and `--json` output, every figure labelled with
  its basis (`provider_reported` | `price_table` | `unknown`; nothing in
  Remedy writes `price_table`, so cost stays NULL rather than inventing a
  price). P6 holds in code, not only in prose: there is no `COALESCE` in
  the queries, so a sum over all-unmeasured rows stays NULL and never
  renders as a measured zero, while COUNTS use `COUNT` because 0 is their
  honest empty value. Reads open with `mode=rw` plus
  `PRAGMA query_only=1`, which refuses to create a database and rejects
  every write at the driver without leaving `-wal`/`-shm` sidecars beside
  a ledger it merely read.
- **Measured cost** (finding R-0218): the mirror costs a median
  **+1.386 ms per finalized task run** at `write_evidence_bundle`
  (0.587 ms inert vs 1.973 ms active), independently reproduced by the
  reviewer at +1.395 ms with a row count of 330/330. The Goal's "without
  slowing it perceptibly" criterion is therefore met with a number rather
  than a claim, on a path whose sibling work is a provider call measured
  in seconds.
- **Tests**: tests/orchestration/test_token_ledger.py and
  tests/cli/test_stats_cost.py — 115 together. Integration gate (R5):
  16121 passed, 19 skipped, zero branch-only failures, re-run
  independently by the reviewer.
<<<END AUTHORED f103-r7-3>>>
