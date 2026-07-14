# Plan — Steps 7161-7260 — F010 closure and integration

## Goal
Every FINAL failed provider call, task or supported run failure leaves a deterministic,
machine-readable post-mortem; `remedy stats failures` aggregates them from the filesystem.
Zero LLM calls, no database, no change to retry policy or run states.

## Current Step
**Branch `feature/f010-failure-postmortems` (from `main` @ `8bdd085`, clean).**
F010 stays `[~]` until external acceptance.

## Documentation baseline
`docs/roadmap/features/T0_F010.md` (commit `8bdd085`, "advanced docs") is the binding
contract. It agrees with this round's brief on every material point: the `FailureClass`
members, `PostmortemV1`, the pure classifier with precedence
`typed exception > terminal loop signal > error_class > retry reasons > unknown`, the
shared timeout predicate ("import or extract it, never copy the string match"), call-level
post-mortems in the per-call evidence directories, a task-level rollup in the job evidence
export area, `remedy stats failures [--since] [--job] [--json]`, config key
`postmortem.llm_summary` defaulting false, no database, and the honest coverage line for
pre-F010 runs. **No material difference to record.**

## Discovery (actual names in the current tree, verified before wiring)
1. **Builder error-class field** — `BuilderOutput.error_class` (`pingpong_provider.py:98`),
   values `"" | "parse" | "config"`.
2. **Reviewer error-class field** — `ReviewerOutput.error_class`
   (`pingpong_provider.py:693`), same value set; also `StructuredParseResult.error_class`
   (`structured_outputs.py:101`, `PARSE_ERROR_CLASS`).
3. **Terminal ping-pong status** — `PingPongResult.final_status`
   (`pingpong_loop.py:100`). Real values: `staged_review_passed`, `staged_blocked`,
   `max_rounds_reached`, `provider_unavailable`, `test_failed`, `review_failed`,
   `target_mutation_blocked`, `builder_no_changes`.
4. **Retry-reason field** — `PingPongResult.retry_reasons` (list[str], format
   `"{role}:attempt{n}:{error[:120]}"`), plus `PingPongResult.retries_used`.
5. **Provider-attempt records** — `ProviderAttempt` (`pingpong_loop.py:53`): `role`,
   `provider`, `is_retry`, `is_parse_retry`, `error`, `stream_call_id`,
   `stream_artifact_refs`.
6. **Per-call evidence directory allocator** —
   `ClaudeCliProvider._allocate_stream_call_dir()` (`pingpong_provider.py:832`):
   `<stream_evidence_dir>/round-NN/<kind>-II` with `kind ∈ {attempt, parse-retry}`, driven
   by `begin_stream_call(round, kind)`. Only allocated for `claude-cli` with stream
   evidence on.
7. **Stream call ID / artifact refs** — `provider.last_stream_call_id` and
   `last_stream_artifact_refs` (`raw_stream.jsonl`, `run_events.jsonl`), copied onto
   `BuilderOutput/ReviewerOutput.stream_call_id` / `.stream_artifact_refs`.
8. **Timeout detection used by retry** — inline in `_call_with_retry`
   (`pingpong_loop.py:1876`): `"timeout" in out.error.lower() or "TimeoutExpired" in
   out.error`. **Extracted** to `provider_timeouts.is_timeout_error()`; the retry path now
   imports it.
9. **Nonzero-exit detection used by retry** — inline: `"exited" in error.lower() or
   "nonzero" in error.lower()`. **Extracted** to `provider_timeouts.is_nonzero_exit_error()`.
10. **Worktree exceptions** — `WorktreeError` / `WorktreeLockError` /
    `WorktreeConflictError` (`worktrees.py:41-49`).
11. **Task terminal failures** — `TaskEntry.status` ∈ `TASK_FAILED ("failed")`,
    `TASK_BLOCKED ("blocked")` (`pingpong_job.py:34-40`), with `TaskEntry.final_status`,
    `.error`, `.test_passed`, `.reviewer_verdict`.
12. **Runtime-probe failure payload** — F007 `runtime probe` JSON: `ok`, `error_class`,
    `runtime_status`, `error`, `survivors` (exit 5 / 4).
13. **Evidence export root and task layout** — `data_paths.evidence_exports_dir()` →
    `<data>/evidence_exports/<job_id>/`, task artifacts under `task_runs/<task_id>/`
    (`job_evidence.py:44`).
14. **Existing `--since` semantics** — ISO-8601 timestamp string, lexicographic compare
    (`event_ledger.list_events`: `if since and le.timestamp < since`). Reused verbatim.
15. **Config-key convention** — `ConfigKeySpec(key, env_var, description, value_type,
    default)` in `_CONFIG_KEY_SPECS` (`config.py:79`).

## Design decisions
- **Logical call boundary** = `_call_with_retry()`. Its transport retries are ONE logical
  call. A post-mortem is written only at the three real terminal exits (builder failure,
  reviewer failure without a parse retry, reviewer parse-retry failure) — so a recovered
  transport retry or a recovered parse retry writes nothing.
- **Call directory**: the provider's existing per-call stream directory when it has one;
  otherwise a stable per-call directory under the run directory
  (`runs/<run_id>/calls/<role>/round-NN/<kind>`). No parallel evidence hierarchy, no
  renamed stream artifacts.
- **Task rollup**: written by the job evidence export into `task_runs/<task_id>/postmortem.json`,
  referencing the call-level post-mortems copied alongside it — so everything is in the
  bundle, in the content proofs and in the review ZIP.

## Boundaries
No F008/F009/F011/F012/F017/F018/F146. `stopped` and `budget_exhausted` are classifiable
but wired to nothing. No database, no new dependency, no provider call.

## External FINDINGS on `remedy-review-20260713-214321` (sha256 `e2ca8f15…c4d169cf`, job `b8478bb5f0174f27`)
Package formally consistent (18/18 proofs, all gates, 0 provider calls); the findings are
functional. Externally: 1 failed / 86 passed on the F010 files (the read-only writer test
under ROOT), 216 passed on the affected suites.

1. **Streamed call post-mortems lost in the export** — the collector looked only at
   `pingpong_runs/<run>/`; a streamed job writes them under
   `jobs/<job>/evidence/task_runs/<task>/streams/…`, so the rollup referenced nothing and
   stats saw nothing.
2. **Data-root exemption could disable the target-mutation guard** — `REMEDY_DATA_DIR` equal
   to the repo, or an ancestor of it, exempted every file in the tree.
3. **The real Claude timeout wording classified as `unknown`** — the provider says
   `claude CLI timed out after 600s`; the shared predicate matched neither `timeout` nor
   `TimeoutExpired`, so F001 did not retry it and F010 did not classify it.
4. **Write failures swallowed** — `postmortem_error` / `postmortem_paths` never reached the
   durable run JSON, and a failed task-postmortem export left a text file while the package
   kept clean gates.
5. **Writer containment too weak** — a symlinked destination directory was followed out of
   the evidence tree; `os.replace` publication was last-writer-wins; `os.access` lies to
   root, which is why the read-only test failed there.
6. **A real worktree lock produced no post-mortem at all** — `_acquire_job_workspace()` fails
   before any task exists, so nothing owned the failure.
7. **`runtime_probe_failed` had no production caller** — the claim was stronger than the code.
8. **Stats warnings named `postmortem.json`** (every record is called that) and the docs
   claimed an "unscanned job" metric that does not exist.

## Fixes (all in this round)
`collect_task_call_postmortems()` as the ONE collector over both layouts, canonical
`call_postmortems/<layout>/` export, rollup refs to those; strict data-root invariant (only a
data root strictly INSIDE the repo exempts, and only what is under it); the shared predicate
recognises `timed out` (profiles/counts/backoff untouched); durable `postmortem_paths`
(run-relative) + `postmortem_error` in the run JSON, `postmortem_integrity.json` in the
export and a BLOCKING final verifier; a contained, create-only (`os.link`) writer with an
unpredictable `O_EXCL`/`O_NOFOLLOW` temp file and mode-bit read-only detection; `scope="job"`
records written on workspace-acquisition failure and counted in their own scope; the
runtime-probe claim corrected to classifier-only; path-qualified stats warnings and honest
coverage wording.

## Second FINDINGS round on `remedy-review-20260713-220339` (sha256 `a89c9722…7cb61084`, job `d9b65b99ffa5498a`)
Package formally clean; six functional findings:
1. Writer created directories BEFORE containment was checked, and resolved the path before
   walking it — so an internal symlink (`root/link -> root/real`) was accepted and a rejected
   request had already created `outside/newdir`.
2. `repo/.data -> repo/src` still exempted the source tree from the target-mutation guard.
3. `JobPlan.postmortem_path` / `postmortem_error` were never serialized: a job-level write
   failure died at the persist/reload boundary and `postmortem_integrity` said `ok: true`.
4. Retry evidence was run-global: a recovered builder timeout classified an unrelated
   reviewer failure as `provider_timeout`.
5. Secrets and absolute paths reached records, `postmortem_error` and the stats histogram;
   streamed `postmortem_paths` degraded to the bare `postmortem.json`.
6. Documentation/test contract had to follow.

## Fixes
Validate-then-create writer with lexical + `lstat` component checks and a no-progress write
guard; lexical, symlink-free data-root invariant; `"postmortem": {path, error}` persisted in
`job.json` (backward compatible); `CallRetryEvidence` per logical call (run-global summary
untouched); `safe_text()` reusing `stream_evidence.redact_text` plus portable path
references, applied to every shareable field and to the stats key; unique relative
`postmortem_paths`.

## Third FINDINGS round on `remedy-review-20260713-224612` (sha256 `ebb48781…b66654d6`, job `5a778c1cab1f4cf2`)
Package formally clean (20/20 proofs, all gates, `postmortem_integrity {ok:true}`, 0 provider
calls). Externally: the three F010 files hold **149** tests (not 147 — the count was
hand-computed instead of read off pytest), the affected invocation passed 639 in 53.36s.

1. **Writer still check-then-use.** Validation used `Path` calls and then reopened by NAME:
   swapping the validated destination for a symlink immediately before `os.open()` put the
   record outside the evidence tree. `O_NOFOLLOW` on the temp file does not protect a
   symlinked PARENT.
2. **Relative / symlink-addressed data roots misclassified.** `REMEDY_DATA_DIR=remedy_data`
   (relative) and a repo addressed through a symlink both made Remedy's own post-mortem look
   like a builder mutation of the target.
3. **`file:` URIs and `label:/abs/path` were not redacted** — while F007 already had an
   accepted scrubber for exactly this boundary.
4. Docs said `scope = call | task` and the STATUS line omitted `job`; test totals were
   miscounted.

## Fixes
Directory-FD-anchored writer (names resolved once, against held descriptors; fail closed
without `O_DIRECTORY`/`O_NOFOLLOW`/`dir_fd`); identity-based, symlink-free, lexical+resolved
data-root invariant that understands relative values and symlinked repo spellings; F007's
scrubber extracted to `packages/common/path_redaction.py` and used by both `dev_server.py`
and `safe_text()`, plus a label-prefixed path rule; documentation and STATUS corrected and
pinned by a docs-consistency test.

## Fourth FINDINGS round on `remedy-review-20260714-101117` (sha256 `32931f8d…2333a35a`, job `953ec09d1b4b4403`)
Package formally clean. The architecture, wiring, aggregation, redaction and documentation
are accepted; one portability defect remains.

**External platform:** Linux 4.4, `O_DIRECTORY` and `O_NOFOLLOW` present, `dir_fd` APIs
present, `_DIR_FD_SUPPORTED == True` — and
`os.open("link", O_RDONLY|O_DIRECTORY|O_NOFOLLOW, dir_fd=root_fd)` **opens the symlink
target**. External F010 core result: **177 passed, 7 failed** (all seven the writer's
symlink-safety tests). The rest passed: 89 + 140 + 166 + 96 + 28 + 26.

1. The capability check asked whether flag CONSTANTS exist — a false positive.
2. The existing-record read also leaned on `O_NOFOLLOW`.
3. `root=None` did `mkdir(parents=True)` on an untrusted destination before anchoring.
4. Nothing reproduced the external platform deterministically.
5. The trusted root's own identity was not verified.

## Fixes
Pre-stat (`follow_symlinks=False`) → open → `fstat` identity comparison for every component,
the trusted root and the existing record; the capability check now tests the primitives the
guarantee is built from and fails closed; `root` is mandatory and `root=None` raises before
any mutation; a fixture that strips `O_NOFOLLOW` from directory opens reproduces the
external host and proves every refusal comes from our own checks.

## Next
Package Evidence and one READY_FOR_REVIEW ZIP; F010 stays `[~]`. F011 not started.
**Not externally accepted.**


## Closure (2026-07-14)

External verdict on `remedy-review-20260714-135557-READY_FOR_REVIEW.zip`
(sha256 `02b36b4d…f95ed53e`, Evidence job `01363c70e13046e2`):
**PASS_WITH_RISKS — ACCEPTED**. SHA matched, 23/23 proofs matched, no uncovered Source/Test
file, F010 core 194 passed, writer 109 passed, focused F007 redaction 26 passed, and the
seven Linux 4.4 `O_NOFOLLOW` failures are fixed.

The one remaining failure in a supporting invocation (`518 passed, 1 failed`) was the
unchanged F007 readiness test assuming Python startup takes under 1.5s. Corrected test-side
only: poll `runtime.log` for the startup marker under a finite deadline, assert the process
is alive, then call `wait_ready()`. No F007 production code changed.

F010 is `[x]`. Both residual risks (same-UID directory relocation; test-side slow-host fix)
are documented. F011 is the next unchecked feature and has NOT been started.
