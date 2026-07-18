# Context — current state (Steps 11961-12160)

## Round 22 (current) — F012 final gate-and-snapshot closure

Review of `remedy-review-20260718-103941-READY_FOR_REVIEW.zip` (Evidence job `5bd1eb8fa7ed4601`)
returned 5 gate-and-snapshot findings; F012 stays `[~]`. Fixed as one bounded block: READY_FOR_REVIEW
is now bound to the complete packaged gate verdict matrix (a BLOCKED gate can never ride inside a
READY package); the manifest and the archive consume ONE immutable staged byte map with the gate
bytes bound into the plan (a post-manifest mutation blocks); the strict snapshot inventory is
production-enforced as an exact Plan bijection; the ArchivePlan is the sole bundle-policy owner (the
shell drops its sensitive exclusions, so an unchanged `.env` gets an EXCLUDE_SAFE_CONTEXT record and
a FIFO a BLOCK_UNSUPPORTED record); and the complete F012/F010/F011 acceptance regression is
recorded. Five new suites (34 tests) prove it. See `.agent/plan.md` for the finding table and
`.agent/live_review.md` for the verification summary.

## Round 21 — F012 final root-identity closure

Review of `remedy-review-20260718-010345-READY_FOR_REVIEW.zip` (Evidence job `0ffc34687764446b`)
returned 10 final root-identity findings; F012 stays `[~]`. Fixed as one small block: every packaged
identity is an exact raw-byte identity (`SHA256` of the exact packaged bytes) over ONE immutable
staged byte map used for both decode and package (a mutation between the two blocks); the manifest
names only members that exist; a declared zero-file subject still needs a strict Proof; one
ArchivePlan disposition owns every path (EXCLUDE_SAFE_CONTEXT / BLOCK_UNSUPPORTED, nothing silently
disappears); the final status comes from the verified build model, not a disk reread; ContentProof
accepts only `{"1.1.0"}`; and the snapshot inventory is validated and narrowly claimed. Nine new
suites (33 tests) plus a real end-to-end prove it. See `.agent/plan.md` for the finding table and
`.agent/live_review.md` for the verification summary.

## Round 20 — F012 root-of-trust closure

Review of `remedy-review-20260717-234531-READY_FOR_REVIEW.zip` (Evidence job `0706eae436294f93`)
returned 10 root-of-trust findings; F012 stays `[~]`. Fixed as one bounded block: the review package
is now a directed hash chain over a SINGLE staged byte source. Evidence is snapshotted to an
immutable private staging dir first (anchored, no-follow, hashed, bounded) and nothing reads the
original again; a strict `ContentProofV1` is the one authority and must equal the final-verifier,
change-provenance and attestable-subject sets (`.agent` forced non-authoritative); every archive
member carries an expected hash; the chain `plan → expectation → manifest` never self-hashes and is
built from immutable bytes; one bundle policy covers unchanged context; the ReviewFile matrix is
complete; and limits apply during the snapshot walk. Nine new suites (52 tests) prove it. See
`.agent/plan.md` for the finding table and `.agent/live_review.md` for the verification summary.

## Round 19 — F012 closure block

Review of `remedy-review-20260717-210512-READY_FOR_REVIEW.zip` (Evidence job `384f2db9a1bc430e`)
returned 12 findings in the file-to-archive boundary; F012 stays `[~]`. All fixed as one coherent
block: authority is now ONE explicit Content-Proof set (18 files; `.agent/` state is
operator-context, non-authoritative), bundle safety is ONE pre-read policy, the typed plan and its
verification report are packaged as verified members, file modes are captured and bound to bytes,
reads are stable/no-follow (repository AND evidence), the ReviewSubject schema is coherent, the
loader fails closed, and the archive is bounded. Nine new suites (60 tests) prove it; the base
`980ec10` has 26 pre-existing failures, unchanged by this block. See `.agent/plan.md` for the
reproduction table and `.agent/live_review.md` for the verification summary.

## Where the product is

- F001–F006 complete and merged. **F007 (Runtime harness) externally ACCEPTED** and merged
  into `main` (PR #129, merge `61e5b4a`); it is `[x]` in `docs/roadmap/STATUS.md`.
- **F010 (Automatic failure post-mortems) is ACCEPTED and `[x]`** — external verdict
  `PASS_WITH_RISKS — ACCEPTED` (2026-07-14), Evidence job `01363c70e13046e2`, package
  `remedy-review-20260714-135557-READY_FOR_REVIEW.zip`.
  - `packages/orchestration/failure_postmortem.py` — `FailureClass`, `FailureSignals`, the
    pure `classify()`, `PostmortemV1` and the atomic exactly-once writer.
  - `packages/orchestration/failure_stats.py` + `remedy stats failures` — file-based
    aggregation with an honest coverage line. No database.
  - Wiring: one post-mortem per finally-failed logical provider call (recovered retries
    write nothing), one rollup per terminally failed task, and one **job-scope** record for
    a job that failed before any task ran (worktree lock/conflict during workspace
    acquisition). Streamed call records are collected from the job stream tree and exported
    canonically under `task_runs/<task>/call_postmortems/`.
  - A post-mortem that cannot be written is durable (`postmortem_error` in the run JSON,
    `postmortem_integrity.json` in the export) and **blocks** the final verifier.
  - `runtime_probe_failed` is classifier-only: no production path emits it today.
  - `provider_timeouts.is_timeout_error()` / `is_nonzero_exit_error()` are now THE shared
    predicates; the retry path and the classifier both import them. Retry policy unchanged.
  - Config `postmortem.llm_summary` defaults **false**; v1 makes zero provider calls.

## Boundaries

- `budget_exhausted` (F018) is still a reserved class: classifiable, wired to nothing.
- **F011 (Kill switch) is ACCEPTED and `[x]`** — external verdict `PASS_WITH_RISKS —
  ACCEPTED` (2026-07-14), Evidence job `49955e41c49f41bc`, package
  `remedy-review-20260714-223538-READY_FOR_REVIEW.zip`, 0 open findings.
  `packages/orchestration/safe_points.py` is the control protocol
  (`control/jobs/<id>/stop.json`, archived on consume); the safe points live in `run_job`
  (before ANY work, including workspace acquisition) and `run_pingpong`; the job gains the
  additive `stopped` state; each consumed request leaves one `job_stopped` event and one
  `stopped` post-mortem under `evidence/stop_postmortems/<request_id>/`.
  `remedy job stop <id> [--status]`.
- **`packages/common/secure_fs.py` is the ONE implementation of the containment rules**
  (directory-FD anchoring, no-follow stat + open/fstat identity comparison, mode-bit
  writability, fail-closed). F010's post-mortem writer and F011's control area both call it —
  a hardening fix cannot land in one and miss the other.
- F011's stop finalization is a durable transaction: archive → post-mortem → event →
  STOPPED → persist → and only then remove the pending request, which is the commit record.
- **F012 round 16** closed the last trust gaps the Evidence layer still had — and a public
  command it had quietly broken. `do job-flow` died with `NameError: timeout_sec is not defined`
  (69 of its 168 tests red) while every gate reported PASS, because the suite that catches it was
  in neither the changed set nor the authoritative CLI command; a changed source file now requires
  its known regression suite to have run GREEN. A published manifest could claim a task was
  `skipped` while recording that its work was applied — both facts stored since round 12, never
  compared — so one closed truth table now binds them. The packager stopped trusting the Evidence
  job's account of itself: the ReviewSubject and every commit-chain field (`subject`,
  `changed_files`, `chain_v` included) are recomputed, and every commit ships the canonical patch
  bytes its hash names so a ZIP-only reviewer needs no repository. Dirty paths are typed with
  `lstat` and never followed (a symlink used to put an OUTSIDE file's bytes in the proof while the
  ZIP omitted the link), and the review base travels explicitly — the process CWD was an
  authorization token that silently discarded intentional declarations.
- **F012 round 17** made the last ten trust-chain checks exact — task truth by episode, and
  every file record typed end to end into the archive. A completed published manifest accepted an
  `executed` task recorded as pending/running/failed/blocked (the shared validator took the
  episode status and phase and never read them); a completed run's terminal STATUS could be
  rewritten by a later prior-episode record; the committed+dirty file union dropped `kind` and
  `link_target`, turning a dirty symlink back into a regular file; the content-proof check
  followed symlinks and hashed an outside target's bytes; committed symlinks were typed as regular
  files; dirty deletions carried no tombstone and dirty renames lost their old path; `do job-flow`
  never forwarded the review base, so a committed branch exported empty; `review_subject.json` was
  not a strict schema; the ZIP was built with `find | zip -@` and dropped a newline filename; and
  containment used a raw string prefix, so `/root/repo-evil` passed for `/root/repo`. All closed:
  `_allowed_statuses_for` and the frozen prior status, `merge_review_file_state`, git-mode kinds,
  a no-follow `lstat` content check, git-blob tombstones, base forwarding, a strict schema, a
  NUL-safe `review_zip.py` builder with exact post-build membership, and component containment.
- **F012 round 18** made the whole file-to-archive boundary one typed transaction. The package
  was built from two disagreeing sources — the typed ReviewSubject and an independent `find -type
  f` list that skips symlinks — so a safe authoritative symlink was ABSENT from the archive while
  both proofs said PASS. One `ArchivePlanV1` now gives every review file exactly one disposition
  (member, tombstone, or block — a policy-excluded change blocks rather than vanishing); the ZIP
  builder preserves each member's real unix type and mode (an executable was flattened to 0644)
  and the post-build verifier checks them (a regular entry could pass as a symlink); every content
  read goes through `secure_fs.read_verified_file_at`, an atomically no-follow anchored reader (a
  regular file swapped to an external symlink mid-read was followed and outside bytes hashed); the
  ReviewSubject schema is exact down to each commit and each file's kind and mode (an injected
  `EXTRA_SECRET` commit field and `base_kind: SECRET-/home/alice` were accepted); the packager
  recomputes the COMPLETE file record; and the real `make_review_zip.sh` is tested end to end.
- **F012 (Deterministic runs) is BUILT and `[~]`** on `feature/f012-deterministic-runs`,
  hardened **fifteen times**. Round 15 closed the last way earlier work could be denied. Round 14
  froze a run's ledger, so a later episode could no longer REWRITE work it admitted to — but it
  could still OMIT the ledger entirely and record an applied task as `skipped`, and the whole
  chain accepted it, because the finality rule had no second ledger to compare. The omission WAS
  the erasure. A task's history is now monotonic across the chain: a task that reached
  applied/passed is bound to `prior_episode` with the same run and the same frozen ledger forever;
  a skipped task stays skipped (`_block_job` decides it and the resume loop never revisits it);
  and a task stopped before completion is DELIBERATELY left free to start a new run, because that
  is exactly F011's resume. The terminal set is the committed contract's, not an invention — F011
  says an applied task is "never rolled back" and `run_job` proves it. Call-ref numbers now have
  exactly ONE text form (`int()` had made `round-01`, `round-001` and `round-000001` three names
  for one call, and `attempt-00` an index-0 call that cannot exist), with one shared formatter and
  canonicality decided by reconstruction. The review subject is a typed, VERIFIED object: an
  invalid base used to be silently ignored (producing a smaller review than asked for, with no
  error) and a non-ancestor base pulled another branch's files in — both now raise, base/head are
  full SHAs recorded in `review_subject.json`, deletions carry tombstones, renames carry both
  paths, and the commit chain is a machine-verifiable artifact rather than prose in a handoff.
  Previously hardened fourteen times. Round 14 closed the last ledger trust-chain gaps. A COMPLETE
  TERMINAL ledger is now FINAL: round 13 compared only the entry prefix, so a later episode could
  extend a run that had already published itself finished (`completed`, `complete=true`, one call)
  and republish it as `failed` with two — the contradiction lived in the header a prefix rule
  cannot see. The whole ledger object is frozen; a later episode repeats it byte-for-byte or not
  at all, and later work uses a NEW run id, which is what production already does
  (`PingPongResult.run_id` is a fresh `uuid4` per execution — proven on a real stop/resume where
  the finished run's ledger repeats with an identical sha256 while the resumed work gets a new
  run). The ledger SET is now exactly the expectation set: a fabricated `GHOST` ledger belonging
  to no JobInput task, no expectation and no call was accepted by typed validation, the writer,
  the loader AND the verified tree, because every check walked from the ledgers outward instead of
  asking whether the ledgers were the ones the record explains. Ledger refs are collision-free
  (`{task}-{run}.json` was ambiguous — `("a-b","c")` and `("a","b-c")` both produced
  `a-b-c.json`, and the anchored reader silently dropped one declaration; the ref is now the
  sha256 of an unambiguous identity encoding). And a call ref must now match a CLOSED canonical
  grammar — `calls//builder`, `calls/./builder`, `calls/builder/` and `home/alice` all passed the
  old "not dangerous" rule, and none of them names a call. **This round also introduced local
  checkpoint commits**: the reviewed state is committed before the next round starts and each
  block lands as it goes green, so `remedy integrity check` passes `relevant_untracked` for the
  first time. Local history is not acceptance — push/PR/merge still wait for the external verdict.
  Previously hardened thirteen times. Round 13 made the Run Call Ledger MEAN something: a published
  reference's ledger must be COMPLETE (it was written and never read); its `terminal_state` is
  strictly decoded from the RUN's own `final_status` through a CLOSED map instead of being
  inferred from the surrounding task (a run can pass while its task ends blocked on a post-run
  gate, and an unknown status silently became "stopped"); each entry must agree with its call on
  every replay-material field INCLUDING `ok`; the recorded ORDER must be the manifest's order
  (F140 serves stream N for call N by it, and a swap left the ledger contiguous and valid); and a
  run's history is CONTINUOUS across episodes — a later ledger must be an exact extension of the
  one an earlier episode established, so no prior call can be invented ("ghost-prior" validated),
  altered, reordered or dropped. That last rule lives in `_validate_episode_graph`, the one place
  the whole chain is in hand. Workspace containment is now decided LEXICALLY before anything is
  opened: `root/sub/../../outside` used to walk out one level per `..` and report the outside
  repository's HEAD as `status=ok`. And `.agent/*.md` are operator state under ONE policy — the
  attested union now uses the same predicate every authoritative view already used, which is what
  made the round-12 package non-authoritative.
  Previously hardened twelve times (12 + 6 + 6 + 14 + 14 + 12 + 16 + 16 + 14 + 11 + 13 + the current 11
  external findings).
  Round 12 closed LEDGER TRUST, IMMUTABILITY and the last workspace-inspection gaps. Every run's
  finalized calls are now published as a CANONICAL LEDGER ARTIFACT
  (`run_manifests/<episode>/call_ledgers/<task>-<run>.json`, strict schema, canonical bytes, in
  the exact allowlist, ref+sha bound from the expectation, verified by loader/recovery/export),
  with a strict bijection to the manifest's calls — a stored reference could previously drop a
  call, restate its counts, invent a 64-hex hash and validate, because none of those bytes were
  in the verified tree. Published episodes are IMMUTABLE: `_settle_existing_artifacts` is gone, a
  missing or altered member is corruption (verified, never recreated), and only the derived
  Root/Index are ever rewritten. An exact retry of a NON-LATEST episode is a no-op — the writer no
  longer excludes the candidate before validating the chain, which used to make an ep1 retry
  report "ep2 references unknown prior ep1". The task lifecycle is one record carrying the task's
  status at finalization AND its dispatch state, so a contradictory JobPlan is reported with both
  facts intact instead of being tidied away (with F011's mid-flight stop, `pending` + a run, kept
  legitimate). A pre-work stop on a RESUMED job carries proven `prior_episode` tasks. Workspace
  containment now stays BOUND through the inspection (a held fd + `/proc/self/fd/N` cwd; a rename
  + symlink swap previously walked the check into an outside repository and read its HEAD), every
  configured git helper is neutralized (`core.fsmonitor` executed during a "read-only" check), the
  workspace has ONE canonical identity format (a 40-hex git tree and a 64-hex content digest had
  been sharing one field, so an identical workspace read as drift), and coverage now reports CALL
  and INPUT dimensions separately — `same_inputs=true` requires both complete.
  Round 11 closed CROSS-EPISODE CONCURRENCY and the LIFECYCLE/WORKSPACE truth gaps. Every append
  for one job now runs under ONE per-job append claim (an `flock` on
  `.run_manifest_control/append.lock`, outside the canonical namespace, held from preflight to
  postcondition and released by the kernel on exception or process death) — the atomic rename only
  serialized writers sharing an episode NAME, so two writers with different ids could each decide
  they were ordinal N+1 and both succeed. Readers never take the lock. One shared
  `load_verified_canonical_chain_for_write()` now validates the COMPLETE existing chain on EVERY
  writer path, including the idempotent retry (which previously returned success over a chain
  whose prior artifact had been tampered with). A lost same-episode race verifies the winner's
  WHOLE tree — a winner with our manifest and no `calls/` is a conflict, never converged onto, and
  never repaired. After publication the chain is RELOADED and revalidated, and the projections
  accept only a typed `VerifiedCanonicalChain`. The `CallExpectation` lifecycle is now an exact
  closed matrix derived from `run_job`'s real completion rule and F011's stop semantics, so
  `completed + planning_only`, `planned + worked`, `completed + not_dispatched` and
  `completed + dispatched_no_calls` can no longer be published; the proof names its run, seals the
  run's finalized-call ledger and states EXACT counts (`expected_min_calls` is gone). A worked
  snapshot must carry every material identity with no silent empty string — an unobtainable value
  is the explicit `unavailable` marker WITH a reason — plus a typed
  `episode_start_workspace_identity`. And `--check-manifest` is strictly read-only and contained:
  it resolves the workspace through `worktrees_root_for()` with anchored no-follow traversal
  (refusing a symlinked PARENT, which previously walked the check into an outside repository) and
  compares the plumbing-only `worktree_identity()` digest, writing no git object, index, ref or
  file — where the old `write_tree_for_path` check grew the object database on every run.
  Round 10 closed the PUBLICATION MODEL and the ZERO-CALL PROOF. An append now validates the
  COMPLETE existing chain before publishing anything: every episode strict-decoded with canonical
  bytes, EVERY prior episode's call artifacts verified, ownership/unique ordinals/contiguity/exact
  history checked, and the candidate required to extend it exactly (ordinal N+1, previous ==
  latest, priors == every prior in order). Episodes are published from a PRIVATE staging directory
  outside the canonical namespace with ONE atomic rename, so a losing writer leaves nothing inside
  the winner's episode, identical writers converge, different writers conflict, cleanup can only
  ever remove the writer's own staging name, and a crash leftover is invisible to every reader,
  allowlist and export. The lost artifact create-race is now VERIFIED rather than ignored
  (identical bytes converge; different bytes are a `ManifestConflictError`). A call may be
  excluded as prior history only when its episode is a KNOWN member of the canonical chain with a
  strictly lower ordinal that this episode actually lists — and an excluded prior call still
  counts toward its run's sequence, because per-run numbering spans episodes. Zero calls is
  "complete" only when the episode's own embedded `CallExpectationV1` proves zero were expected;
  the contract's genuine cases (pre-work stop, planning-only, all-skipped) stay valid while a task
  that ran and lost its calls is exit 1. Every call is bound to the IMMUTABLE embedded job-input
  definition, and a JobPlan/snapshot task divergence blocks finalization. There is now ONE exact
  JobInput validator behind `is_ok()`, the strict decoder and every other boundary, and
  Builder/Reviewer/Repair provider+model agreement is exact with symmetric absence semantics.
  Round 9 closed the TERMINAL REFERENCE + WRITER-PATH gaps. A manifest is now validated in one
  of three explicit modes: PREPUBLICATION (shape), PUBLISHED_REFERENCE (a stored terminal record
  — coverage MUST be complete, no problems, every call bound to its hash-verified artifact) and
  CURRENT_CANDIDATE (reconstructed from live state — MAY be incomplete, and then must carry a
  bounded problem). That distinction IS the exit-1-vs-exit-5 line, and it lives in the canonical
  loader and the writer rather than in a second Evidence-only rule: `write_run_manifest` refuses
  to publish an incomplete terminal record and `load_latest_manifest_verified` refuses to read
  one back. Zero calls is complete only when the JobPlan proves zero calls were expected. The
  Index is now CANONICAL RAW BYTES at every reader (`raw == canonical_index_bytes(decode(raw))`,
  size limit before decode, exact schema, no unknown fields), and the append RECONSTRUCTS the
  index from the canonical episode chain instead of preserving old data. The idempotent and
  concurrent-create writer reads are strict (`_decode_existing_episode`: anchored, byte-limited,
  strict decode, exact canonical bytes, published-reference validation → exact match is
  idempotent success, anything else is a `ManifestConflictError`), and one shared invariant
  matrix proves that EVERY writer/recovery success (first write, idempotent retry,
  concurrent-create, Stop retry, mirror repair, index repair, second-episode append) leaves a
  tree the canonical loader reads immediately. Persisted Call lineage is VERIFIED, never
  normalized: the stored sequence is the call's position within its OWN RUN (the real data
  model), the manifest's job-wide contiguous order is DERIVED, and a tampered sequence is
  reported rather than renumbered. The JobInputDefinition is complete (required identity hashes,
  isolation mode from `JobPlan`'s real vocabulary, typed tasks, the exact execution block), and
  redundant facts must AGREE (job file hash; role provider; pinned role model). KEYS are
  validated, not only values, and `PYTHONHASHSEED` has a bounded vocabulary. Standard JSON only,
  both directions (`allow_nan=False`; `parse_constant` rejects `NaN`/`Infinity`; invalid UTF-8 →
  bounded `ManifestError`). Every PRESENT manifest tree is validated even for an unmarked legacy
  job — the marker changes ABSENCE semantics only.
  Round 8 settled the IDENTITY MODEL and made the strict layer universal: F012 now separates
  (1) RECORD/PROVENANCE identity (`provenance_projection`/`record_sha256` — job/episode/run/call
  ids, status, stop id, ordinal, timestamps, artifact refs), (2) LOGICAL INPUT identity
  (`logical_input_projection`/`logical_input_sha256` — ONLY material inputs; two separate
  executions of the same inputs hash the SAME), and (3) OUTCOME/lifecycle (never an input).
  Calls diff through the stable logical key `(task_id, sequence, role, round, kind)`. The strict
  decoder is now the ONLY untrusted entry (permissive `from_json` renamed `from_trusted_json`
  and banned from disk paths by a guard test; persisted run records and JobPlan snapshots
  strict-decode). InputSnapshot / JobInputDefinitionV1 / PreparedCallInput are EXACT recursive
  schemas (closing the unknown-field canary bypass), with an ExecutionConfig lockstep guard.
  `prompt_len_bytes` is bound into the transport fingerprint; `is_ok()` validates the nested
  input (wrapper-only is `wrapper_shape_is_valid()`); every stored member must satisfy
  `raw bytes == canonical_bytes(strict_decode(bytes))` with duplicate-key rejection and a
  byte-for-byte mirror==latest-episode rule; the writer strict-round-trips and enforces
  aggregate limits before publishing; no name-based trust prechecks remain. Round 7 closed the external trust boundary: ONE strict raw-JSON decoder layer
  (`packages/orchestration/manifest_schema.py` — no Boolean/integer coercion, no silent
  defaults, bounded, unknown fields refused, F4); the InputSnapshot validator now enforces its
  own claims (required worktree fields, redundant-fact agreement, secret/path safety reusing the
  established redactor + F007 path scrubber, F5); `job_input_sha256` is BOUND to the embedded
  definition (F6) and the call fingerprint is BOUND to its recomputed PreparedCallInput (F7);
  published calls always carry canonical hash-bound artifacts (F8), identities are strict/
  path-safe (F9), coverage is a closed enum (F10); ONE uniform size-limit contract shared by
  writer/reader/export (F11); recovery is CONTAINED by its trusted root (F3); the typed CLI
  loader and the verified-tree builder never throw on corrupt disk state and use no name-based
  prechecks (F1/F2/F16); a missing/symlinked resumable workspace is incomplete (F12); terminal
  JobPlan metadata is required (F13); the episode allowlist rejects extras (F14); the stream
  flags are mutually exclusive (F15). Round 6
  closed the public-CLI + recovery + export gaps: the public CLI (`do job-run/resume/flow`)
  preserves the omission sentinel through ONE shared `RunInvocation` structure (F1/F2, tri-state
  `--stream-evidence`/`--no-stream-evidence`, `--max-tasks`/`--timeout-sec`/`--max-output-chars`
  default `None`); the derived mirror/index are RECOVERABLE from the immutable episodes
  (`load_episode_record_for_recovery` + `rebuild_manifest_mirror_and_index_from_canonical_episodes`,
  transaction model documented — immutable episode = source of truth) so a partial publication
  converges on retry (F3/F4); the export is VALIDATE-BEFORE-COPY via `build_verified_manifest_tree`
  (undeclared/oversized/secret never enters the bundle, F5); the synthetic legacy snapshot
  fallback is GONE (F6); a complete strict schema (`validate_run_manifest` + `validate_input_snapshot`:
  UTC-aware created_at, 64-hex shas, safe stop id, unique/REMEDY_* env, no abs paths, F7); complete
  TERMINAL JobPlan/index/latest agreement (F8); the worktree collector folds all I/O failures into
  typed incomplete + always closes the root FD (F9); a typed CLI canonical load with no name-based
  precheck (F10); the rerun check recomputes a resumable workspace's CURRENT tree (F11); the F012
  scope carries no stray F001/F003 files (F12). Round 5
  wired the mechanisms through the real lifecycle: a failed mandatory snapshot HARD-BLOCKS
  before any provider call (F1) — a failed episode-start-workspace-tree capture is itself a
  snapshot failure (F12); the runner EXECUTES the resolved invocation controls, not product
  defaults (F2), with omission-sentinel (`None`) resolution (F3); the full
  `EpisodeInputSnapshotV1` wrapper is EMBEDDED in the manifest (F4); a stopped manifest, its
  snapshot and its calls share ONE episode id with the stop request id as separate metadata
  (F5); one strict `validate_episode_input_snapshot` everywhere (F6); the untracked reader
  detects same-size in-place mutation via mtime_ns/ctime_ns (F7); episode history is the exact
  ascending predecessor chain (F8); the JobPlan↔index cross-check is complete (F9); ordinal +
  predecessor derive from the verified canonical index (F10); no name-based trust ops before
  secure writes (F11); real runtime/manifest consistency + snapshot-lifecycle tests (F13). Core
  modules:
  `packages/orchestration/call_identity.py` (PreparedCallInput fingerprint + CallIdentity),
  `run_manifest.py` (RunManifestV1 + episode model + InputSnapshot + coverage +
  build_current_candidate + diff), wired into `pingpong_provider`, `pingpong_loop`
  (`_finalize_call` + `shared_call_id`), `pingpong_job`, `job_evidence` + `final_verifier`,
  `remedy job rerun --check-manifest` (exit 0/4/5). Round 4 added: typed episode-owned
  `EpisodeInputSnapshotV1` with MANDATORY blocking capture (no terminal re-probe, F1/F11);
  F2 invocation controls (timeout_sec/profile, max_output_chars, stream_evidence, max_tasks)
  persisted + hashed; FD-verified untracked reader closing the lstat→open race (F3); typed
  `WorktreeIdentity.dirty` tri-state (F4); non-time `episode_ordinal` + `previous_episode_id`
  with rollback detection (F5) and prior-episode DAG validation (F6);
  `validate_episode_artifacts_anchored` (F7); fully anchored export via
  `read_manifest_tree_bytes_anchored` (F8); `load_episode_manifest_verified` on every
  production trust read (F9); F010 records against the exact finalized context (F10);
  git-independent review-ZIP tests (F12); JobPlan/index episode cross-check (F13); one
  table-driven material-field proof (F14). Not accepted, not committed.
- F008, F009, F017, F018 and F146 are NOT started. F017 is the next unchecked feature after F012.
- F011's accepted v1 boundaries: no SIGKILL/stale-RUNNING recovery, no deep checkpoints, no
  OS-signal stop path, no signal handler/thread/daemon, no database.
- No database, no new dependency, no provider call, no Docker anywhere in F010.
- F010's accepted residual risk: the post-mortem writer does not resist a **same-UID**
  process that renames an already-opened private evidence directory (that adversary can
  edit the evidence directly anyway). Everything else — traversal, pre-existing symlinks,
  inode substitution, ineffective `O_NOFOLLOW`, check/open races — is refused. See
  `docs/roadmap/features/T0_F010.md`.
