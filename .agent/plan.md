# Plan — Steps 10361-10560 — F012 hardening round 14 (external FINDINGS)

## Round 14 binding feature discovery (files READ COMPLETELY, authoritative)

Read in full: `docs/roadmap/STATUS.md`, `T0_F004.md`, `T0_F005.md`, `T0_F010.md`, `T0_F011.md`,
`T0_F012.md`, `T0_F017.md`, `T0_F018.md`, `T0_F147.md`, `T3_F084.md`, `T7_F140.md`.
Keyword sweep over the committed feature tree for: complete ledger, terminal, run id, call ledger,
call id, stream N, artifact ref, immutable, idempotent, prior episode, replay, F012, F140.

### Binding clauses selected (and the production seam each binds)

1. **F010** — "a call the loop abandons writes exactly one `postmortem.json` — in the provider's
   existing per-call stream directory when it has one, otherwise in
   `runs/<run_id>/calls/<role>/round-NN/<kind>/`." → BINDS F4: there are TWO real call-ref
   namespaces, not one. Seam: `parse_call_ref` / `CALL_REF_NAMESPACES`.
2. **F010** — "`postmortem_paths` are unique relative references —
   `streams/<role>/round-NN/<kind>-II/postmortem.json` for streamed calls,
   `calls/<role>/round-NN/<kind>/postmortem.json` for fallback calls. Never the ambiguous bare
   basename." → BINDS F4's exact grammar, INCLUDING the streamed `-II` attempt index.
3. **F140** — "The replay provider: serves stream N for call N after verifying the outgoing
   prompt's hash matches the recorded one." → BINDS F1/F6: replay operates WITHIN one frozen Run
   Ledger; a ledger that can still grow after it says it finished has no stable N.
4. **F140 / "Do not touch"** — "Stream formats, manifest semantics, certificate members." →
   round 14 adds no manifest field and changes no stream byte; the ledger REF changes shape, and
   F012 is unmerged so no accepted record uses the old one.
5. **F012 (own Built State)** — "Prior-Episode calls stay IN the ledger — the run made them." →
   preserved: a later episode still carries the prior run's ledger, now byte-for-byte.
6. **F012 (own Built State)** — "published Evidence is immutable; a missing or altered member is
   corruption" → BINDS F1: a published terminal ledger cannot later change.
7. **F011** — the mid-flight stop leaves the task pending with a finished run → BINDS F1: the
   resume must NOT extend that run's ledger. Verified: production gives the new work a new run id.
8. **F084** — "the demo REPLAYS it through the normal storage/evidence writers" → the frozen-
   ledger rule must hold for recorded fixtures too; nothing added is execution-time-only.
9. **F017/F018/F147** — read and NOT implemented.

## Persisted sources of truth consulted

- `packages/orchestration/pingpong_loop.py` — `PingPongResult.run_id = uuid4().hex[:16]` (a FRESH
  run per execution: this is why terminal finality is safe), `shared_call_id` (the ONE identity
  F010's post-mortem writer and F012's manifest both use), `_allocate_stream_call_dir`
  (`rel_prefix = f"streams/{role}"`, `f"round-{n:02d}/{kind}-{idx:02d}"`).
- `packages/orchestration/pingpong_job.py` — `task.run_id = result.run_id` per execution.
- `packages/orchestration/manifest_schema.py` — `MAX_ID_LEN = 128` (the ref bound argument).

## Reproduced against production BEFORE fixing (all 4 findings)

| # | Reproduction | Result before |
|---|---|---|
| F1 | ep1 `completed/complete/[c1]`; ep2 same run `failed/complete/[c1,c2]` | chain ACCEPTED |
| F2 | `task_id=GHOST, run_id=ghostrun, complete=true, entries=[]` | manifest ACCEPTED |
| F3 | `("a-b","c")` and `("a","b-c")` | BOTH → `call_ledgers/a-b-c.json` |
| F4 | `calls//builder`, `calls/./builder`, `calls/builder/`, `home/alice`, `c1` | ALL accepted |

## Production behaviour proven (the rules are the product's, not inventions)

Real stop-then-resume, fake providers, zero network:

```
ep1  T001 run=f5962555  completed complete=True  2 entries
ep2  T001 run=f5962555  completed complete=True  2 entries   <- byte-identical (sha256 equal)
ep2  T002 run=9ae434c5  completed complete=True  2 entries   <- new work, NEW run id
```

Real call ids emitted by a live run: `calls/builder/round-01/attempt`,
`calls/reviewer/round-01/attempt`. Streamed form: `streams/<role>/round-NN/<kind>-II`.

## Judgement calls recorded

1. **The task-status→ledger-state rule stays narrow** (carried from round 13). Only
   `passed`/`applied` pin `completed`; production reaches `blocked`/`failed` with a SUCCESSFUL run
   via post-run gates.
2. **`_call` fixture call ids changed to the real canonical refs.** The finding required it
   ("Do not preserve synthetic test-only `c1` values"): a fixture using a shape production never
   emits cannot prove a grammar.
3. **Two round-13 tests rewritten, not deleted**: one hard-coded `c1`; one recorded honestly that
   `calls/home/alice/attempt` was accepted under the old weak rule. The closed grammar now refuses
   it (`home` is not a role), so the note is superseded rather than wrong.
4. **Pre-existing baseline debt unchanged.** `tests/cli/test_do_cmd_summary.py` and
   `tests/cli/test_product_spine.py` fail 18 tests at base `b0ba27a` itself (they require
   `docs/core-product-spine-v0.md`, removed by an earlier docs restructure). Out of scope;
   excluded from the recorded CLI command rather than hidden by a green number.

## Local commit discipline (new this round, user-authorized)

The reviewed round-13 state was verified byte-identical to the packaged content proof (81/81) and
committed as `8d186b4` BEFORE any round-14 edit, then one commit per logical block. `remedy
integrity check` now passes `relevant_untracked` for the first time in the F012 rounds, because
the work is in history instead of an 84-file dirty tree. Local history is NOT an acceptance
signal: push/PR/merge still wait for external acceptance, and F012 stays `[~]`.

---

## Superseded round-13 plan (retained for provenance)

# Plan — Steps 10161-10360 — F012 hardening round 13 (external BLOCKED_EVIDENCE + FINDINGS)

## Round 13 binding feature discovery (files READ COMPLETELY, authoritative)

Read in full: `docs/roadmap/STATUS.md`, `T0_F004.md`, `T0_F005.md`, `T0_F010.md`, `T0_F011.md`,
`T0_F012.md`, `T0_F017.md`, `T0_F018.md`, `T0_F147.md`, `T3_F084.md`, `T7_F140.md`.
Keyword sweep run over the committed feature tree for: RunCallLedger, finalized calls, call
sequence, terminal state, complete ledger, prior episode, replay, stream N, workspace containment,
trusted root, path traversal, Evidence authoritative, Content Proof, change provenance, F012.

### Binding clauses selected (and the production seam each binds)

1. **F140** — "The replay provider: serves stream N for call N after verifying the outgoing
   prompt's hash matches the recorded one." → BINDS F4: the ledger's per-run ORDER is replay
   material, so it must be verified, not merely contiguous. Seam: `validate_call_ledgers`.
2. **F140 / "Do not touch"** — "Stream formats, manifest semantics, certificate members." →
   round 13 adds no manifest field and changes no stream byte; it only validates what is there.
3. **F010** — "the requested path is checked LEXICALLY (so a link the caller asked us through is
   still visible — `resolve()` answers 'where does it point', not 'did you ask me through a
   link')." → BINDS F7. Seam: `_open_contained_workspace_fd` → `secure_fs.lexical_parts`.
4. **F010** — "The trusted root is verified the same way ... never reopened by name once its fd is
   held." + "Fail closed." → BINDS F7's defence in depth. Seam: `secure_fs.open_verified_dir`.
5. **F011** — "the anchored primitives now live once, in `packages/common/secure_fs.py`, and both
   features call them." → one canonical helper, not a local copy. Seam: `require_single_component`.
6. **F011** — the mid-flight stop ("the call in flight finishes, nothing new starts") → BINDS F2:
   `pending` + a finished run is legitimate, so the task/ledger matrix must permit it.
7. **F012 (own Built State)** — "unique contiguous call sequence, each call's job/episode
   ownership" and "Prior-Episode calls stay IN the ledger — the run made them." → BINDS F5's
   prefix/extension rule. Seam: `validate_ledger_chain` in `_validate_episode_graph`.
8. **F012 (own Built State)** — the call_id is "a path-SHAPED reference ... shared with F010" →
   BINDS F6: the ledger's rule for call_id is the committed ref rule, not a component rule.
9. **F084** — "the demo REPLAYS it through the normal storage/evidence writers" → the ledger
   contract must hold for recorded fixtures too; nothing added is execution-time-only.
10. **F017/F018/F147** — read and NOT implemented (scope fences, budgets, golden path).

## Persisted sources of truth consulted

- `packages/orchestration/pingpong_loop.py` — the RUN record and its `final_status` vocabulary
  (12 literals actually written, + `builder_no_changes` recognised by `pingpong_evidence`).
- `packages/orchestration/pingpong_job.py` — the TASK status transitions; proved that a task
  reaches `blocked` AFTER a `staged_review_passed` run (completion gate / target guard /
  workspace apply), which is why the task→ledger rule is narrow.
- `packages/common/secure_fs.py` — `lexical_parts`, `open_verified_dir`, `anchor_root`.
- `packages/orchestration/final_verifier.py` — `_OPERATIONAL_PREFIXES` / `_is_source_for_alignment`
  (the committed operator-state policy reused verbatim by the attest path).

## Reproduced against production BEFORE fixing (all 7 code findings)

| # | Reproduction | Result before |
|---|---|---|
| F1 | ledger `complete=false`, hash resealed | ACCEPTED as published reference |
| F2 | `terminal_state=failed` on an applied task | ACCEPTED |
| F3 | entry `ok=false` vs call `ok=true` | ACCEPTED |
| F4 | swap two entries' `per_run_sequence` | ACCEPTED (still contiguous) |
| F5 | `call_id=ghost-prior, episode_id=ep1` | ACCEPTED (chain-level; manifest cannot see it) |
| F6 | prior entry `call_id=/home/alice/SUPERSECRET` | ACCEPTED; `/home/alice` in canonical bytes |
| F7 | `root/sub/../../outside` | `status=ok` + the OUTSIDE repo's real HEAD |

## Recorded contract differences (findings that contradict the committed contract)

1. **F6 "no separators" for `call_id`.** Refused: production call ids are
   `calls/builder/round-01/attempt`. Verified by running it — the writer failed with "call ledger
   entry call_id 'calls/builder/round-01/attempt' is not a safe bounded component" and NO manifest
   was written. The committed rule (safe relative REF) is implemented and extracted into one
   shared `safe_call_ref()`; the finding's intent (refuse `/home/alice/SUPERSECRET`) is met.
2. **F2's implied "task status pins the run outcome".** Only `passed`/`applied` do. Production
   reaches `blocked`/`failed` with a SUCCESSFUL run via post-run gates, and F011 leaves `pending`
   with a finished run. The matrix permits those; forbidding them would refuse real records.
3. **Pre-existing baseline debt (carried forward from round 12).** `tests/cli/test_do_cmd_summary.py`
   and `tests/cli/test_product_spine.py` fail 18 tests at base `b0ba27a` itself (they require
   `docs/core-product-spine-v0.md`, removed by an earlier docs restructure). Out of scope;
   recorded, not fixed; excluded from the recorded CLI command rather than hidden by a green number.

## Bug found in my own round-13 rule (fixed before proceeding)

`validate_ledger_chain` first keyed its resolution map on `call_id` alone. A `call_id` is unique
only WITHIN a run (`calls/builder/round-01/attempt` is every task's first builder call), so
unrelated tasks collided and a REAL stop-then-resume was refused ("attributes call ... to episode
X, but it was published by Y"), leaving the chain with one episode instead of two. Keyed by
(task, run, call_id). Caught by `tests/cli/test_job_rerun_manifest.py`'s real resume test.

---

## Superseded round-12 plan (retained for provenance)

# Plan — Steps 9961-10160 — F012 hardening round 12 (external FINDINGS)

## Round 12 binding feature discovery (files READ COMPLETELY, authoritative)
- `docs/roadmap/STATUS.md` — **F012 `[~]`**, F017 `[ ]`. Unchanged.
- `T0_F012.md` — the whole contract. Clauses that decided this round:
  * "Exit codes: 0 verification complete and no drift; 4 confirmed blocking drift; 5 no blocking
    drift but coverage incomplete (`same_inputs=null`, "Input equality could not be fully
    verified.")" — the F9 two-dimension coverage rule reports into exactly this.
  * "**Immutable artifact conflict** — on an idempotent write, an existing call artifact must
    equal the canonical bytes exactly; a tampered one raises `ManifestConflictError`, and no
    root/index update follows." — F2 extends the same principle to a MISSING artifact.
  * "the immutable per-episode manifest + call artifacts are the source of truth; the root mirror
    and index are DERIVED projections" — the F10 transaction phases and the F3 no-op.
  * "An immutable `InputSnapshot` is captured at episode start (after workspace acquisition...)".
  * "`isolation_mode` from the JobPlan's real vocabulary (`worktree` | `copy`)" — the non-git /
    copy workspace case behind F9.
  * "Planning-only job (zero calls): valid manifest, empty hash list"; "a genuine zero-call
    (all-skipped) job ... stays valid and complete".
- `T0_F010.md` — create-only (`os.link`) publication: a concurrent DIFFERENT record conflicts, an
  identical one is idempotent. Postmortems not weakened.
- `T0_F011.md` — **"the call in flight finishes, nothing new starts"**; the stop finalization is a
  durable transaction; double stop requests are idempotent. This is what makes F5's pre-work
  resume normal AND what corrected the prompt's F4 rule (see below).
- `T0_F004.md` / `T0_F005.md` — raw streams referenced not duplicated; schema/parse-retry modes.
- `T0_F017.md` / `T0_F018.md` / `T0_F147.md` — not started, not implemented here.
- `T3_F084.md` — demo replays a recorded bundle through the normal writers.
- `T7_F140.md` — the replay provider "serves stream N for call N", **keyed by call
  sequence/hash** — why the F1 ledger records the run's own per-run order rather than deriving it.

Tree searched for: `F012`, `finalized calls`, `call ledger`, `zero calls`, `pre-work stop`,
`prior episode`, `immutable artifact`, `idempotent`, `input coverage`, `workspace identity`,
`read only`, `fsmonitor`, `filter process`, `copy isolation`, `non-git`, `same inputs`, `golden`,
`demo`, `replay`, `bit-exact`. `immutable artifact` and `workspace identity` appear only in
`T0_F012.md`; `non-git` also in F146/F081/F143; `same inputs` also in F079/F118; `bit-exact` in
F140. `call ledger`, `input coverage`, `fsmonitor` and `filter process` appear NOWHERE in the
committed tree — they are new vocabulary this round introduces.

## Differences between this prompt and the committed contract
1. **F4's "a task cannot be both never dispatched and the owner of a Run" is too strong as
   written.** F011's mid-flight stop legitimately leaves `pending` + a run holding the finalized
   call ("the call in flight finishes"). The first cut of the rule blocked those manifests and
   left the job `running` — caught by the F011 suite. Implemented the honest reading: the run is
   PROOF of dispatch, so the expectation may never say `skipped`/`not_dispatched` while a run
   exists; the run id is never erased; `skipped` + a run IS reported (skipping precedes dispatch).
2. **F9's "compute a strict anchored filesystem-tree content identity" for non-Git workspaces** is
   not implemented this round. `worktree_identity()` already yields a complete strict identity for
   every git worktree (including `copy`-isolation workspaces that are git worktrees). A genuinely
   non-git workspace records an explicit `unavailable` identity and therefore INCOMPLETE input
   coverage — which is the finding's own stated fallback ("If a complete filesystem identity
   cannot be obtained, record incomplete Input coverage rather than claiming determinism"). The
   preferred filesystem-identity path is NOT built; it is recorded here as the one deliberate gap.

## Round 12 persisted ledger/run/task sources used by F012
- `task_jobs/<job>/job.json` (JobPlan: task status, run_id, episode index) — MUTABLE.
- `pingpong_runs/<run>/result.json` `finalized_calls` — MUTABLE; it GENERATES the ledger at
  finalization and is never trusted afterwards.
- `jobs/<job>/evidence/run_manifests/<episode>/…` — the IMMUTABLE canonical tree: manifest, call
  artifacts, and (new) `call_ledgers/<task>-<run>.json`.

## Round 12 exact sources of truth (recorded decisions)
- **Call completeness** → the canonical `RunCallLedgerV1` artifact in the episode tree, bound by
  ref + sha256 from `TaskCallExpectationV1`, with a strict bijection to the manifest's calls.
- **Workspace identity for logical comparison** → the typed `episode_start_workspace_identity`
  (status/head/digest/dirty/problems). `episode_start_workspace_tree` is provenance only.
- **Input coverage rules** → completed/stopped/worked: every material identity real (not
  `unavailable`) and the workspace identity ok; planning-only / pre-work-stop: explicit typed
  unavailability with a reason; non-git: honest `unavailable` ⇒ INCOMPLETE input coverage,
  never `same_inputs=true`.
- **Immutability boundary** → the atomic `rename` that publishes the staged episode directory.
  Before it: nothing canonical exists, a stage may be rebuilt or discarded. After it: the
  manifest, every call artifact and every ledger are immutable — verified, never repaired — and
  only the derived Root/Index may still be (re)written.

## Round 12 findings (all fixed as one block)
F1 canonical Run Call Ledger artifact + bijection · F2 published artifacts immutable (no silent
repair) · F3 exact retry of a non-latest episode is a no-op · F4 one exact task lifecycle record
(contradictions reported, never normalized) · F5 pre-work stop with proven prior tasks · F6
held-handle workspace containment · F7 all configured git helpers neutralized · F8 one canonical
workspace identity format · F9 input coverage vs call coverage · F10 honest transaction phases ·
F11 bounded safe staging cleanup.

## Round 12 real defects reproduced against production BEFORE fixing
- F1: drop call 2, set both counts to 1, `finalized_calls_sha256="b"*64` → `validate_run_manifest`
  ACCEPTED it as a published reference.
- F2: publish, delete the call artifact, retry → SUCCESS, artifact recreated, loader green again.
- F3: ep1, ep2, exact retry of ep1 → `ManifestError: episode ep2 references unknown prior ep1`.
- F4: `skipped`/`pending` + run_id → expectation normalized, run id discarded, no problem.
- F5: pre-work stop on a resumed job with a completed prior task → validator REJECTED a normal
  resume ("`prior_episode` cannot happen in stopped/pre_work_stop").
- F6: verify → rename → symlink an outside repo → inspect → the OUTSIDE repo's HEAD was observed.
- F7: `core.fsmonitor` script RAN during `worktree_identity()`; identity said `ok`, problems `[]`.
- F8: reference `episode_start_workspace_tree` = 40-hex git tree; candidate = 64-hex content
  digest; blocking drift on an identical workspace.

# Plan — Steps 9761-9960 — F012 hardening round 11 (external FINDINGS)

## Round 11 binding feature discovery (files READ COMPLETELY, authoritative)
- `docs/roadmap/STATUS.md` — **F012 `[~]`** (built, acceptance pending); F017 `[ ]`. Unchanged.
- `T0_F012.md` — the whole contract. Clauses that decided this round:
  * "Planning-only job (zero calls): valid manifest, empty hash list." — the planning-only row of
    the F7 matrix.
  * "a genuine zero-call (all-skipped) job, which stays valid and complete" — the only zero-call
    form a COMPLETED worked episode may take.
  * "For an episode of ordinal N, `prior_episode_ids` is EXACTLY every ordinal 1..N-1 ...
    `previous_episode_id` is exactly the ordinal-(N-1) episode" — the candidate rule the F1 lock
    now makes race-safe.
  * "The latest is the MAX-ordinal episode and the root mirror mirrors it."
  * "An immutable `InputSnapshot` is captured at episode start (AFTER workspace acquisition...)"
    — why a WORKED episode must carry a workspace identity (F10).
  * "`build_current_candidate` recomputes a resumable job workspace's CURRENT tree
    (`worktrees.write_tree_for_path`)" — the round-6 design F11 replaces: that helper MUTATES the
    inspected repository. **This is the one place this round supersedes an earlier Built-State
    sentence; the doc is updated accordingly.**
  * "a MISSING workspace, a SYMLINKED workspace, or one whose tree cannot be reconstructed yields
    INCOMPLETE coverage... Only a completed job whose worktree was intentionally cleaned uses the
    documented rerun-from-recorded-target semantics" — preserved exactly, now with `absent` vs
    `escapes` distinguished.
  * exit 0/1/2/4/5 semantics; "recorded, not promised".
- `T0_F004.md` / `T0_F005.md` — raw streams referenced not duplicated; schema/parse-retry modes.
- `T0_F010.md` — "Publication is create-only (`os.link`), not `os.replace`: a concurrent DIFFERENT
  record conflicts instead of overwriting; an identical one is idempotent." The repository's
  established conflict model; F3/F5 extend exactly it. Postmortems not weakened.
- `T0_F011.md` — "the call in flight finishes, nothing new starts"; the stop finalization is a
  durable transaction; "Double stop requests are idempotent". These define the `stopped`/`worked`
  row of the F7 matrix (a stop CAN leave undispatched tasks and a task that never reached a call).
- `T0_F017.md` / `T0_F018.md` / `T0_F147.md` — not started, not implemented here.
- `T3_F084.md` — demo replays a recorded bundle through the normal writers.
- `T7_F140.md` — the replay provider "serves stream N for call N", keyed by call sequence/hash;
  why F6's per-run sequence and F9's exact per-run counts must be exact.

Tree searched for: `F012`, `episode append`, `ordinal`, `concurrent`, `idempotent`, `artifact`,
`zero calls`, `planning only`, `pre-work stop`, `call expectation`, `workspace identity`,
`check only`, `read only`, `logical input`, `provenance`, `golden`, `demo`, `replay`.
`zero calls`, `planning-only`, `call expectation`, `canonical readability` and `logical input`
appear ONLY in `T0_F012.md`; `concurrent`/`idempotent` also in F010/F011 (the create-only model);
`replay`/`golden` in F004/F084/F140.

**Difference between this prompt and the committed contract:** one, recorded above — the round-6
Built-State sentence naming `write_tree_for_path` for the rerun check. That helper runs
`git add -A` + `git write-tree`; the prompt's F11 requires a read-only check. The contract's
INTENT ("recompute the CURRENT workspace so a mutation is detected as drift") is preserved by
`worktree_identity()`, which is read-only and already the digest every other worktree uses.

## Round 11 append/publication/retry race windows (enumerated)
| # | window | before | now |
|---|---|---|---|
| 1 | two writers read the chain before either publishes (DIFFERENT episode ids, same ordinal) | both succeeded; chain had duplicate ordinal 2 | the per-job append claim serializes the whole transition |
| 2 | idempotent retry while a PRIOR episode's artifact is tampered/missing/extra | success; loader then rejected the tree | the shared full-chain validation runs on every path |
| 3 | idempotent retry while THIS episode has an undeclared artifact | success | the exact per-episode allowlist is enforced on the retry |
| 4 | lost directory rename to a winner with our manifest but no `calls/` | success | the winner's WHOLE tree is verified; incomplete → conflict |
| 5 | between publication and the projections | projections derived from a preflight-era view | the chain is reloaded and revalidated; projections take only a `VerifiedCanonicalChain` |
| 6 | lost artifact create race (staging and settlement) | Boolean checked (r10) | unchanged + noncanonical/missing/symlink now explicit |
| 7 | exception/kill while holding the claim | n/a | `flock` is released by the kernel; no stale ownership |

## Round 11 source of truth (recorded decisions)
- **Prior Episodes** → `load_verified_canonical_chain_for_write()` over the anchored, strict,
  artifact-verified episode records — never the index alone, never the JobPlan.
- **Expected Calls** → the embedded `CallExpectationV1` (exact counts + run id + ledger seal),
  decided at finalization; verification never re-consults the mutable JobPlan.
- **CallExpectation lifecycle matrix** → `_LIFECYCLE_MATRIX` in `run_manifest.py`, derived from
  `run_job`'s real completion rule (completed ⇔ every task applied/skipped; a max-tasks boundary
  PAUSES) and F011's stop semantics. Rows: planned/planning_only, stopped/pre_work_stop,
  completed/worked, stopped/worked.
- **Canonical root for resumable workspaces** → `worktrees.worktrees_root_for(repo)` =
  `<repo>/.remedy-wt`, entered with anchored no-follow traversal. The JobPlan's path is a claim
  checked against that root, never a trust root itself.

## Round 11 findings (all fixed as one block)
F1 per-job append serialization · F2 shared full-chain validation on every writer path · F3
complete-winner verification after a lost race · F4 post-publication revalidation + typed
`VerifiedCanonicalChain` · F5 complete artifact create-race handling · F6 membership always
decided · F7 exact CallExpectation lifecycle matrix · F8 expectation tasks exactly the embedded
JobInput · F9 exact call counts + run binding + ledger seal · F10 phase-aware snapshot identities
(no silent empty string) · F11 contained read-only workspace inspection · F12 one universal writer
postcondition · F13 authoritative Evidence matches the handoff.

## Round 11 real defects reproduced against production BEFORE fixing
- F1: `ep2a` and `ep2b` both published ordinal 2 (threads, both preflighting first); loader:
  `duplicate episode ordinals`, `ordinals are not 1..N contiguous: [1, 2, 2]`.
- F2: idempotent `ep2` retry over a tampered `ep1` artifact → SUCCESS; loader rejected `ep1`.
- F2: `ep1` retry with `ep1/calls/EXTRA.json` → SUCCESS; loader rejected the undeclared artifact.
- F3: a winner with an identical manifest and no `calls/` → writer SUCCESS; loader rejected it.
- F7: `completed + planning_only`, `planned + worked`, `completed + dispatched_no_calls`,
  `completed + not_dispatched`, `stopped + planning_only`, `pre_work_stop` snapshot + `worked`
  expectation — all ACCEPTED.
- F8: a ghost expectation task with an empty JobInput task list — ACCEPTED.
- F9: `expectation.run_id = WRONG-RUN` while the call's run id was real — ACCEPTED.
- F10: a completed worked manifest with `job_initial_tree=""` / `episode_start_workspace_tree=""`
  — ACCEPTED.
- F11: `write_tree_for_path` grew the git object db 8 → 12; a parent-symlink workspace escape was
  followed.

## Round 11 production defects found while fixing (real, not test artifacts)
- A **non-git target** (a real product case: `copy` isolation, and the F011 suite's own repo) has
  no tree objects, so `job_initial_tree`/`episode_start_workspace_tree` were EMPTY. The first cut
  of the F10 rule blocked those manifests, which aborted the stop finalization and left the job
  `running` — a real F011 weakening, caught by that suite. Fixed the right way: production now
  records the explicit `unavailable` marker instead of a silent empty string, and an unavailable
  identity must carry a reason.
- `git status` / `git diff` run a repository's configured CLEAN FILTER over working files, so even
  the plumbing identity could fire an arbitrary configured command from a "read-only" check. Now
  neutralized per invocation (`-c filter.X.clean=cat`).

# Plan — Steps 9561-9760 — F012 hardening round 10 (external FINDINGS)

## Round 10 binding feature discovery (files READ COMPLETELY, authoritative)
- `docs/roadmap/STATUS.md` — F001–F007/F010/F011 accepted `[x]`; **F012 `[~]`** (built, external
  acceptance pending); F008/F017 `[ ]`. Round 10 keeps F012 `[~]`.
- `T0_F012.md` (886 lines) — the whole contract. Binding clauses used this round:
  * **"Planning-only job (zero calls): valid manifest, empty hash list."** (Edge cases) — the
    contract PERMITS a planning-only zero-call reference, so F6 had to make it genuinely work
    rather than block it.
  * **"a genuine zero-call (all-skipped) job, which stays valid and complete"** (Blocking missing
    coverage) — the second permitted zero-call case.
  * "A task that should have call records but whose run record is missing, a corrupt
    finalized-call record, an empty fingerprint or an unresolved call artifact is a blocking
    manifest-integrity failure" — the F6 blocking side.
  * "For an episode of ordinal N, `prior_episode_ids` is EXACTLY every ordinal 1..N-1 in
    ascending order and `previous_episode_id` is exactly the ordinal-(N-1) episode. Skipping the
    immediate predecessor..." — the F1 candidate rule.
  * "The latest is the MAX-ordinal episode and the root mirror mirrors it" — F1/F10.
  * exit 0/1/2/4/5 semantics + "recorded, not promised".
- `T0_F004.md` — raw streams are REFERENCED, never duplicated or reformatted (untouched).
- `T0_F005.md` — the schema/parse-retry modes behind PreparedCallInput `mode` (untouched).
- `T0_F010.md` — **"Publication is create-only (`os.link`), not `os.replace`: a concurrent
  DIFFERENT record conflicts instead of overwriting; an identical one is idempotent."** This is
  the repository's established conflict model, and F3/F4 extend exactly it to artifacts and
  episode directories. Also: one postmortem per finally-failed call/task/job (not weakened).
- `T0_F011.md` — the stop finalization is a durable transaction; "Double stop requests are
  idempotent"; a manifest that cannot be written is durable and blocks. F10's matrix proves the
  Stop retry converges after EVERY publication window.
- `T0_F017.md` / `T0_F018.md` / `T0_F147.md` — not started, not implemented here.
- `T3_F084.md` — Demo replays a RECORDED bundle through the normal writers; "the bundle is the
  contract".
- `T7_F140.md` — the replay provider "serves stream N for call N", keyed by **call
  sequence/hash**. This is why F5's per-run sequence must stay exact across episodes and why F7's
  call→task binding matters: a replay indexes calls by their recorded identity.

Feature tree searched for: `F012`, `zero calls`, `planning-only`, `coverage`, `episode`,
`previous_episode`, `call sequence`, `task id`, `run id`, `artifact`, `concurrent`, `idempotent`,
`writer success`, `canonical readability`, `recovery`, `logical input`, `provenance`, `golden`,
`demo`, `replay`. `zero calls`, `planning-only`, `previous_episode`, `canonical readability` and
`logical input` appear ONLY in `T0_F012.md`; `concurrent`/`idempotent` also in F010/F011 (the
create-only model above); `replay`/`golden` in F084/F140/F004.

**Difference between this prompt and the committed contract: none material.** One clarification:
the prompt asks for "planning-only: zero Calls expected" and the contract explicitly permits a
planning-only manifest, but production could not build one (a planned job has no resolved
`execution_config`, so every `*_source` was empty and its own definition failed validation). That
is a real gap the round closed — with no execution config every value IS the product default, so
the definition now records `"default"` sources honestly and a planning-only manifest validates.

## Round 10 write/publication/recovery race windows (enumerated)
| # | window | old behaviour | now |
|---|---|---|---|
| 1 | between the artifact pre-read and its create-only write | the Boolean was ignored → success over another writer's bytes | re-read; identical converges, different → `ManifestConflictError` |
| 2 | between artifact writes and the episode-manifest claim | the loser's artifact stayed in the winner's episode | artifacts only ever exist under the private staging name |
| 3 | at the episode-manifest create | winner/loser settled, but contamination had already happened | the claim IS the atomic directory rename |
| 4 | between the episode publication and the mirror/index write | index could advance over an unvalidated chain | full chain preflight precedes publication; mirror/index derive from the canonical on-disk record |
| 5 | crash mid-publication | a half-built episode could exist under `run_manifests/` | staging lives outside the canonical namespace; leftovers are invisible to readers/exports and cleanable |
| 6 | idempotent retry over a tampered artifact | overwritten or accepted | conflict |
| 7 | concurrent identical writers | both wrote into one directory | converge on one canonical tree |

## Round 10 source of truth (recorded decisions)
- **Expected Calls** → the EMBEDDED `CallExpectationV1` in the episode record, decided at
  finalization from the JobPlan task status + the persisted run records. Verification never
  re-consults the mutable JobPlan. (Contract: zero calls is valid only for planning-only /
  all-skipped / pre-work-stop.)
- **Prior-Episode membership** → the CANONICAL chain read from the verified index
  (`read_canonical_episode_order`), passed to `_collect_calls` as
  `prior_episode_ordinals` + `prior_episode_ids` + `episode_ordinal`. Never the call's own claim.
- **Declared tasks for a Call** → `episode_snapshot.input.job_input.tasks` (immutable), never
  `job.tasks` (mutable). A divergence between them BLOCKS finalization.
- **Role providers/models** → `job_input.execution` is the definition; `snapshot.models` is the
  scalar view; they must agree, and absence is symmetric.

## Round 10 findings (all fixed as one block)
F1 append validates the complete existing canonical chain before publishing · F2 append validates
every previous Call artifact · F3 lost artifact create-races are verified (converge or conflict) ·
F4 conflict-safe staged Episode publication (no contamination, no unsafe cleanup, no undeclared
staging member in Evidence) · F5 only KNOWN, listed, strictly-earlier prior Episodes may excuse a
Call; prior Calls still count toward the stored in-run sequence · F6 self-contained
`CallExpectationV1` proof for zero-Call references · F7 every Call bound to the embedded JobInput,
and JobPlan/Snapshot task divergence blocks finalization · F8 ONE exact JobInput validator behind
`is_ok`, the strict decoder and every other boundary · F9 exact Builder/Reviewer/Repair
provider+model agreement with an exact `models` schema · F10 one universal writer-success
postcondition over 14 operations plus the failure postconditions · F11 authoritative Evidence
records every claimed test run.

## Round 10 real defects reproduced against production BEFORE fixing
- F1: `write ep1 ordinal 1` + `write ep2 ordinal 1` → second write **reported success**; the tree
  then failed with `duplicate episode ordinals`, `ordinals are not 1..N contiguous`,
  `latest is not the max-ordinal episode`.
- F2: append over a tampered ep1 artifact → **success**; the chain immediately failed artifact
  validation.
- F3: a lost artifact create race with DIFFERENT bytes → **success**; the canonical loader then
  rejected the tree.
- F4: writer A's `0001-reviewer-round02-attempt.json` was left inside writer B's episode.
- F5: a call claiming `UNKNOWN-FUTURE` was silently excluded → `coverage=complete, problems=[]`.
- F6: an `applied_to_job_workspace` task with `run_id=""` → `calls=[], coverage=complete`; same
  for a run whose `finalized_calls` was empty.
- F7: JobInput tasks `[T001]` + call `T999` → validated cleanly.
- F8: empty `job_title_sha256`/`job_file_sha256`/`isolation_mode` → `is_ok() == True` while the
  strict decoder rejected the same record.
- F9: `models.repair = ollama/modelB` vs `execution.repair_provider = claude` /
  `repair_model = modelA` → accepted.

## Round 10 test-count honesty (F11)
Every count in the handoff is taken from the packaged `verification_tests.json`. The broad CLI
regression is recorded as its own command; its known baseline failures (missing doc files absent
from this checkout) are recorded with the same command run against clean `main`, and are never
counted as green.

# Plan — Steps 9361-9560 — F012 hardening round 9 (external FINDINGS)

## Round 9 binding feature discovery (files READ, authoritative)
- `docs/roadmap/STATUS.md` — F001–F007/F010/F011 accepted; **F012 `[~]`** (built, not accepted);
  F008/F017 `[ ]` not started. Round 9 must keep F012 `[~]`.
- `T0_F012.md` — RunManifestV1 + EpisodeInputSnapshotV1, immutable per-episode records with a
  DERIVED root mirror + `run_manifest_index.json`, PreparedCallInput transport fingerprints,
  exit 0/1/2/4/5, the three-way identity model (round 8), the honesty rule
  ("recorded, not promised").
- `T0_F004.md`/`T0_F005.md` — raw streams are REFERENCED, never duplicated or reformatted; the
  schema/parse-retry modes behind PreparedCallInput `mode`.
- `T0_F010.md` — one postmortem per finally-failed call/task/job; F012 must not weaken it. The
  shared finalized-call context is the same record `_collect_calls` reads, which is why round 9
  VERIFIES that record rather than normalizing it.
- `T0_F011.md` — stop durability + stop-request retention. A stop publication must CONVERGE on
  retry (round 9's F13 matrix proves the Stop-retry path), and the stop request id stays
  SEPARATE terminal metadata, never an input.
- `T0_F017.md`/`T0_F018.md`/`T0_F147.md` — not started. F018's invocation limits are why the
  material controls resolve explicit > persisted > default. Not implemented here.
- `T3_F084.md`/`T7_F140.md` — replay/demo compare RECORDED inputs across separate executions and
  consume the anchored, allowlisted artifact trust chain. This is why a PUBLISHED terminal
  manifest must be a complete reference: a replay cannot compare against "some of the calls".
- Feature tree searched for manifest/index/coverage clauses; **no material difference found
  between the committed contract and this prompt.**

## Round 9 production boundary (per fix)
| Fix | Production boundary |
|---|---|
| F1 | `validate_run_manifest(mode=...)` + `_require_valid_manifest` — the canonical LOADER and the WRITER, not an Evidence-only rule |
| F2 | `canonical_index_bytes` / `require_canonical_index_bytes` at `load_index_verified`, `validate_index_and_tree`, `build_verified_manifest_tree`, `read_index`, recovery, export, writer append |
| F3 | `_decode_existing_episode` — the idempotent AND concurrent-create reads in `write_run_manifest` |
| F4 | `_mirror_and_index` — rebuilt from the canonical episode chain |
| F5 | `_collect_calls` — verify per-run sequence, derive the job-wide position |
| F6 | `decode_job_input_definition_v1` + `VALID_ISOLATION_MODES` (from `JobPlan.isolation_mode`) |
| F7 | `validate_input_snapshot` crosschecks |
| F8 | `_is_safe_key` / `_valid_pythonhashseed` in `validate_input_snapshot` |
| F9 | `secure_fs.json_bytes(allow_nan=False)` + `strict_json_loads(parse_constant=...)` |
| F10 | `job_evidence._write_run_manifest_export` + `manifest_tree_is_present` |
| F11 | repo guard test over the F012 production set |
| F12 | `read_manifest_tree_bytes_anchored` → `_open_dir_anchored_or_missing` |
| F13 | shared `assert_canonically_readable` matrix over every writer/recovery path |
| F14 | `T0_F012.md` + docs tests |

## Round 9 audit — raw `json.loads`, permissive parsing, name-based prechecks in F012 paths
- `run_manifest.py`: ONE `json.loads`, inside `strict_json_loads` (duplicate-key hook +
  `parse_constant`). Pinned by a guard test that fails if any other function calls it.
- `manifest_schema.py`, `call_identity.py`, `apps/cli/commands/job_rerun_cmd.py`: zero
  `json.loads` — guard-tested.
- `job_evidence.py`: `json.loads` remains ONLY on non-manifest evidence (traces, token truth,
  verification packets). The manifest export decodes the index via `decode_index_v1`; a
  guard test fails on any `json.loads` inside a manifest-named function or on any line naming
  manifest/index/artifact data.
- `pingpong_job.py`: `_json.loads` on the JOB FILE and on raw-stream lines — neither is manifest
  data; the F012 snapshot/manifest paths use `decode_*_v1`.
- Permissive constructors: `from_trusted_json` only, banned from disk paths by the guard test.
- Name-based prechecks: none left in the manifest/recovery/canonical/tree-reader paths;
  `_open_dir_anchored_or_missing` is the existence decision. Guard-tested per function.

## Round 9 findings (all fixed as one block)
F1/F14 `ManifestValidationMode` — a published terminal reference needs COMPLETE coverage with
every call artifact bound (exit 1), a current candidate may be incomplete with a bounded problem
(exit 5) · F2 canonical Index raw bytes at every reader · F3 strict idempotent + concurrent-create
existing-episode reads · F4 the Index append reconstructs from the canonical chain · F5 persisted
Call lineage verified, never renumbered · F6 complete required JobInputDefinition · F7 redundant
facts must agree (job file, role provider, role model) · F8 safe KEYS + bounded PYTHONHASHSEED ·
F9 standard JSON only, both directions · F10 every PRESENT tree validated (the marker changes
absence semantics only) · F11 no permissive raw JSON on manifest paths (guard test) · F12 no
name-based precheck in the anchored tree reader · F13 writer/recovery success implies immediate
canonical readability (shared matrix).

## Round 9 real defects reproduced against production BEFORE fixing
- F1: the writer published an incomplete `completed` manifest that the loader then accepted.
- F2: a pretty-printed index was accepted.
- F3: an idempotent write reported success over a noncanonical stored episode the loader rejected.
- F4: an unknown `EXTRA` field survived an index append.
- F5: a tampered `sequence=999` was renumbered to 1 and published with `coverage=complete`.
- F9: `Infinity` was emitted and accepted; invalid UTF-8 raised a raw `UnicodeDecodeError`.
- F10: an unmarked job's malformed tree was skipped because the marker was absent.

## Round 9 data-model discoveries (real, not test artifacts)
- Persisted run records number calls **per RUN** from 1; the manifest requires a job-wide
  contiguous 1..N. Verify the stored value in its run, derive the published position.
- `JobPlan.isolation_mode` is `"copy"` by default (`"worktree" | "copy"`) — the F6 vocabulary
  comes from production, not from the schema's imagination.
- `models[role]` is `"<provider>"` when the role runs the provider default and
  `"<provider>/<model>"` when a model is pinned; an unset declared model is not a contradiction.

# Plan — Steps 9161-9360 — F012 hardening round 8 (external FINDINGS)

## Round 8 binding clauses (committed feature files, authoritative)
- `T0_F012.md` — RunManifestV1, EpisodeInputSnapshotV1, immutable episodes, derived
  mirror/index, PreparedCallInput transport fingerprints, exit 0/1/2/4/5, honesty rule.
- `T0_F004.md`/`T0_F005.md` — raw streams referenced not duplicated; the schema/parse-retry
  modes behind PreparedCallInput `mode`.
- `T0_F010.md`/`T0_F011.md` — shared finalized context; stop durability + request retention.
- `T0_F017.md`/`T0_F018.md`/`T0_F147.md` — not started.
- `T3_F084.md`/`T7_F140.md` — replay/demo compare RECORDED inputs across separate executions,
  which is exactly why logical input identity must exclude random execution identifiers.
- No material difference found between the committed contract and this prompt.

## Round 8 `.from_json()` audit (F3/F14)
UNTRUSTED (persisted disk) → now `decode_*_v1`:
`_collect_calls` (run records), `_episode_snapshot_bound_ok` + `_write_run_manifest_record`
(JobPlan snapshots), `validate_index_and_tree` root mirror, `_read_episode_manifest_anchored`,
`_verified_episode_export`, `job_evidence` per-episode coverage, `read_run_manifest`,
`_mirror_and_index` re-issue.
TRUSTED (in-memory canonical) → renamed `from_trusted_json` and guard-tested off disk paths:
`RunManifestV1`, `EpisodeInputSnapshotV1`, `InputSnapshot`, `FinalizedCall`,
`PreparedCallInput`, `CallIdentity`. (`RuntimeState.from_json` in `packages/runtimes/` is not an
F012 type and is out of scope.)

## Round 8 findings (all fixed as one block)
F1 logical-vs-provenance identity · F2 outcome out of the logical hash · F3/F4/F5 strict decoder
at every persisted boundary · F6 exact InputSnapshot schema · F7 exact JobInputDefinitionV1 ·
F8 exact PreparedCallInput · F9 prompt_len_bytes bound · F10 is_ok validates nested input ·
F11 raw canonical byte equality + duplicate keys · F12 writer round-trip + aggregate limits ·
F13 strict root mirror/export · F14 permissive decoders quarantined · F15 no name-based trust
prechecks · F16 identity model documented + pinned by docs tests.

# Plan — Steps 8961-9160 — F012 hardening round 7 (external FINDINGS)

## Round 7 binding clauses (committed feature files, authoritative)
- `T0_F012.md` — RunManifestV1, EpisodeInputSnapshotV1, immutable episodes, derived mirror/index,
  PreparedCallInput transport fingerprints, exit 0/4/5/1, honesty rule.
- `T0_F005.md` — the reviewer schema/parse-retry modes behind PreparedCallInput `mode`.
- `T0_F010.md`/`T0_F011.md` — exact finalized-context handoff; stop durability + request
  retention (F3 recovery must keep a stop resumable).
- `T0_F017.md`/`T0_F018.md`/`T0_F147.md` — not started; F018's invocation limits are why the
  material controls resolve explicit>persisted>default.
- `T3_F084.md`/`T7_F140.md` — replay/demo consume the canonical history + the anchored,
  allowlisted artifact trust chain and the bound per-call fingerprints.
- No material difference found between the committed contract and this prompt.

## Round 7 findings (all fixed as one block)
F1/F2/F16 typed CLI + tree-builder never throw, no name-based prechecks · F3 trusted-root
containment · F4 strict raw-JSON decoders · F5 snapshot claims enforced · F6 job-input hash
binding · F7 prepared-input fingerprint binding · F8 published-call artifacts · F9 strict
identities · F10 closed coverage enum · F11 uniform size limits · F12 missing resumable
workspace · F13 required terminal metadata · F14 exact allowlist · F15 exclusive stream flags.

# Plan — Steps 8761-8960 — F012 hardening round 6 (external FINDINGS)

## Round 6 binding clauses (committed feature files, authoritative)
- `T0_F012.md` — RunManifestV1, EpisodeInputSnapshotV1, immutable per-episode manifests, root
  mirror + `run_manifest_index.json` (derived), exit 0/4/5/1, honesty rule.
- `T0_F004.md` — raw streams referenced not duplicated/altered.
- `T0_F010.md` / `T0_F011.md` — exact finalized-context handoff; stop durability + request
  retention after manifest failure (F3 recovery must keep the stop resumable).
- `T0_F017.md`/`T0_F018.md` — not started; invocation-level limits (F018) are why the material
  invocation controls must resolve explicit>persisted>default with a real omission sentinel.
- `T3_F084.md` / `T7_F140.md` — replay/demo consume the canonical linear history + anchored,
  allowlisted artifact trust chain.

## Round 6 findings (all fixed as one block)
F1 CLI omission sentinel · F2 shared RunInvocation · F3/F4 immutable-episode recovery + txn model ·
F5 validate-before-copy export allowlist · F6 no synthetic legacy snapshot · F7 complete strict
schema · F8 terminal JobPlan/index/manifest agreement · F9 collector I/O→incomplete + FD close ·
F10 typed CLI canonical load · F11 resumable-workspace current-state · F12 clean review scope.

# Plan — Steps 8561-8760 — F012 hardening round 5 (external FINDINGS)

## Round 5 binding clauses (committed feature files, authoritative)
- `docs/roadmap/features/T0_F012.md` — RunManifestV1, EpisodeInputSnapshotV1, per-episode
  immutable manifests, `on_call_finalized` seam, honesty rule, exit codes 0/4/5/1.
- `T0_F004.md` — raw-stream evidence is referenced by the manifest, never duplicated/altered.
- `T0_F010.md` — F010 postmortems consume the SAME finalized context; not weakened.
- `T0_F011.md` — stop durability transaction; stop request retained after manifest failure.
- `T0_F017.md`/`T0_F018.md` — NOT started (budget_exhausted reserved).
- `T3_F084.md` / `T7_F140.md` — consume the canonical episode history + anchored artifact
  trust chain; worktree replay (F140) is the declared per-call coverage gap → exit 5.

## Round 5 findings (all fixed as one block)
F1 failed-snapshot hard block · F2 execute resolved controls · F3 omission sentinel ·
F4 embed wrapper · F5 stopped-episode ownership · F6 strict snapshot validator ·
F7 same-size mutation · F8 exact ordered history · F9 complete JobPlan/index cross-check ·
F10 canonical-index-derived append · F11 no name-based trust ops · F12 workspace-tree failure ·
F13 runtime/manifest truth test · F14 authoritative verification runs recorded.

# Plan — Steps 8361-8560 — F012 hardening round 4 (external FINDINGS)

## Round 4 discovery (binding docs)
Read STATUS.md, T0_F004/F010/F011/F012/F017/F018.md, T3_F084.md, T7_F140.md.
- F018 (budgets) will add invocation-level limits via CLI/config — F2's invocation controls
  (timeout, profile, output-limit, stream_evidence, max_tasks) are material NOW and must be in
  the input definition. Precedence stays explicit > persisted > default.
- F140 replay keys by call sequence/hash and verifies the recorded prompt hash — the anchored
  artifact trust chain (F7) is what F140 will consume. F084 replays through normal writers —
  needs the canonical loader (F9) + verified artifacts (F7).
- F012 contract preserved: RunManifestV1, immutable per-episode manifests, index+root mirror,
  PreparedCallInput fingerprints, artifact_sha256, episode-owned calls, exit 0/4/5.

## Round 4 findings (external FINDINGS on remedy-review-20260715-122656)
F1 typed persisted EpisodeInputSnapshotV1 (no terminal re-probe, blocking capture failure);
F2 invocation controls in ExecutionConfig + job_input; F3 FD-verified untracked reader
(lstat/open race closed); F4 typed dirty state; F5 episode_ordinal monotonic order (no
rollback); F6 prior-episode DAG validation (no cycle/future/unknown); F7 anchored artifact
trust chain; F8 anchored export (no Path reads/symlink follow); F9 load_episode_manifest_verified;
F10 F010 receives the exact context object; F11 versioned snapshot type; F12 review-zip tests
git-independent; F13 JobPlan/index cross-check; F14 table-driven material-field test.
F012 stays [~]. F017 not started.

# Plan — Steps 8181-8360 — F012 hardening round 3 (external FINDINGS)

## Round 3 discovery (binding docs)
Read: STATUS.md, T0_F004/F010/F011/F012/F017.md, T3_F084.md, T7_F140.md.
- **F140 (replay)** keys the replay provider "by call sequence/hash" and verifies "the
  outgoing prompt's hash matches the recorded one" — so per-call SEQUENCE + fingerprint +
  EPISODE ownership is exactly the contract F140 will consume. Confirms F4/F6 direction.
- **F084 (demo)** replays a recorded fake job through the normal evidence writers — needs a
  trustworthy canonical manifest + index (F8/F11).
- **F012 contract** (T0_F012.md): RunManifestV1, episode model under
  `run_manifests/<episode_id>/`, index, root mirror, PreparedCallInput fingerprints,
  artifact_sha256, exit 0/4/5. All preserved.

## Round 3 findings (external FINDINGS on remedy-review-20260715-113936)
F1 complete job-input schema; F2 Remedy dirty-content identity; F3 strict Git collector (no
fail-open, no symlink follow, special files); F4 per-episode call ownership +
episode-start workspace tree; F5 per-episode timestamp; F6 single finalized context (F010
does not recompute); F7 validate_run_manifest everywhere; F8 index trust-chain validation;
F9 anchored read-only evidence traversal; F10 immutable artifact conflict on idempotent write;
F11 load_latest_manifest_verified; F12 docs. F012 stays [~]. F017 not started.

# Plan — Steps 8021-8180 — F012 hardening round 2 (external FINDINGS)

## Goal
Every completed or stopped persisted ping-pong job gets exactly one versioned, canonical,
hashable INPUT manifest. `remedy job rerun <id> --check-manifest` rebuilds the would-be
inputs, diffs against the stored manifest, and classifies drift as blocking vs informational.
Honesty rule pinned by a docs test: **inputs are reproducible and verified; LLM outputs are
recorded, not promised.**

## Contract baseline
`docs/roadmap/features/T0_F012.md` as committed on `main` at `b0ba27a`. It matches this
prompt: RunManifestV1 (manifest_v=1, job id, created_at, Remedy repo sha, worktree evidence
snapshot, resolved config {value,source} secrets redacted by key-name denylist, REMEDY_* env,
model ids per role, provider CLI versions best-effort "unavailable" allowed, incremental
{call_dir, sha256} list, python+platform); ONE shared `on_call_finalized` hook consumed by
this feature and the postmortem writer; `diff_manifests` split blocking vs informational;
`remedy job rerun <id> --check-manifest` (exit 0 clean, exit 4 blocking); exactly one manifest
per finished/stopped job (stop path writes it in the STOPPED-persist code path); planning-only
job → valid manifest with empty hash list; record PYTHONHASHSEED if set. **No material
difference from this prompt.**

## Discovery — the actual seams (Phase 1)

1. **JobPlan model + serializer** — `pingpong_job.py`: `JobPlan`, `_export_job`/`_import_job`,
   `_persist_job(job)` → `<data_root>/task_jobs/<job_id>/job.json`, `load_job_plan`.
2. **Completed finalization** — `run_job` (`if all_done: job.status = JOB_COMPLETED` ~1764,
   then final_job_review, then `_persist_job` ~1816, `finally: _finalize_job_workspace`).
3. **STOPPED finalization** — `pingpong_job._stop_job` durable transaction (archive →
   post-mortem → event → STOPPED → persist → acknowledge).
4. **Worktree/base snapshot** — `worktrees.WorktreeHandle.base_commit/head_commit`,
   `snapshot()`, `write_tree()`; on the job: `worktree_base_commit`, `worktree_head`,
   `job_initial_tree`.
5. **Resolved config + source** — `config.get_config()` → `RemedyConfig.values: {key:
   ConfigValue{value, source: ConfigSource, ...}}`; `all_key_specs()`; `spec.secret`,
   `spec.env_only`; `to_summary_dict()` already redacts secrets by spec flag and abs paths via
   `_redact_abs_path`.
6. **Model/provider per role** — `job.execution_config`: `builder`, `builder_model`,
   `reviewer`, `reviewer_model`, `repair_provider`, `repair_model` (+ `_source` for each).
7. **Provider command construction** — `pingpong_provider.build_claude_cli_args`.
8. **Version-probe helper** — `pingpong_provider.ClaudeCliProvider._resolve_version`
   (`subprocess.run([claude, "--version"], timeout=5, cwd=…)`, never raises). Generalised into
   a bounded, no-shell, no-network probe in `run_manifest.py`.
9-11. **Prompt finalization** — `pingpong_loop.run_pingpong`: builder trace appended ~2482,
   reviewer attempt trace ~2660 and the bounded parse-retry trace via `_rev_trace`. Each
   `prompt_trace.build_trace_entry` carries `prompt_sha256`, role, round, phase, provider.
12-13. **Stream/fallback call dirs** — per-task `stream_evidence_dir`; `_begin_stream_call`.
14. **Postmortem call finalization** — `pingpong_loop._record_call_failure` (failure only;
    F010). No pre-existing GENERIC finalization seam — so F012 introduces the single one.
15. **Evidence export (job level)** — `job_evidence.export_job_evidence` + `_write_json`;
    `postmortem_integrity.json` (`POSTMORTEM_INTEGRITY_FILE`) blocks the final verifier
    (`final_verifier.py` ~873, `postmortem_integrity_blocked` in `gates_blocked`).
16. **`job rerun`** — none exists; nearest is `resume_job_plan` + the `do job-*` group. F012
    adds `remedy job rerun <id> --check-manifest` in the `job` command group.
17. **Fake-provider injection** — `run_job(builder_provider=, reviewer_provider=)`.
18. **Git/worktree SHA** — `worktrees._git(root, "rev-parse", "HEAD")`; Remedy's own sha from
    `git rev-parse HEAD` in the repo root.
19. **Redaction helpers** — `config._redact_abs_path`, `secure_fs`, `failure_postmortem.safe_text`,
    `stream_evidence.is_sensitive_key`, `common/path_redaction`.
20. **Canonical JSON/hash** — `secure_fs.json_bytes(payload, sort_keys=True)`; `hashlib.sha256`.

## Design decisions
- **Two hashes.** `record_sha256` over the full serialized manifest (includes created_at);
  `logical_input_sha256` over the comparison projection (excludes created_at, python/platform,
  provider CLI versions — the informational fields). Two identical fake jobs on different data
  roots/timestamps share the logical hash, never the record hash.
- **The single seam.** `on_call_finalized(FinalizedCallContext)` in `run_manifest.py`. The
  ping-pong loop calls it once per finalized logical provider call (builder attempt, reviewer
  attempt, bounded parse retry) and it appends a `FinalizedCall{call_dir, role, kind, round,
  sha256, artifact}` to `result.finalized_calls`. The manifest's call list is built ONLY from
  these records — never by globbing call directories, so there is no second walker.
- **Honest check-manifest.** The candidate manifest is rebuilt from CURRENT config/git/models/
  env plus a reconstructable `job_input_sha256` = sha over (job_file_sha256, ordered task
  bodies, models per role). Per-call recorded prompt hashes are NOT fabricated for the
  candidate: they are compared only when both sides have them (pure `diff_manifests`), and in
  CLI check-mode the candidate marks them as coverage="recorded_only". Prompt drift is detected
  through the reconstructable `job_input_sha256` (a real prompt-shaping input), so the CLI
  quartet is honest.
- **Manifest integrity** mirrors postmortem integrity: `manifest_integrity.json {ok, failures}`
  in the export, added to `final_verifier` `gates_blocked`.

## Not in scope
Raw stream format, per-call directory layout, retry/timeout policy, F010 postmortem semantics,
F011 stop semantics, F017, F018, F084, F140. No LLM rerun, no database.

## Status
F012 `[~]` — implementation round; not externally accepted.


## Implementation complete (2026-07-15)
T001 `run_manifest.py` (RunManifestV1, canonical serialize, two hashes, secret redaction,
version probe, anchored exactly-once writer, `diff_manifests`). T002 the single
`on_call_finalized` seam wired into `pingpong_loop` at each finalized provider call, persisted
in run JSON, aggregated into the job manifest at completed/stopped finalization; manifest
integrity in `job_evidence` + `final_verifier`. T003 `remedy job rerun --check-manifest`
(honest candidate: no fabricated call hashes) + the drift quartet through the CLI.
F012 stays `[~]`. F017 not started.


## Hardening round 1 (external FINDINGS on `remedy-review-20260715-091841`)
All twelve findings fixed as one block: exact provider-transport fingerprints
(`call_identity.PreparedCallInput`, computed in each provider); unique per-call identity
(`CallIdentity`); real contained call artifacts + integrity resolution; current-state candidate
(`build_current_candidate`, live git inspection); coverage states + exit 5; start-time
`InputSnapshot`; the episode model (`run_manifests/<episode_id>/` + index, stop-<reqid> ids);
manifest in the F011 stop transaction (publish before acknowledge); the `run_manifest_required_v`
legacy marker; blocking missing coverage; and one shared `shared_call_id` seam consumed by F010
and F012. F012 stays `[~]`. F017 not started.


## Hardening round 2 (external FINDINGS on `remedy-review-20260715-104127`)
Six findings fixed: working-tree CONTENT digest (`target_tree` hashes binary diffs + untracked
content, not porcelain); idempotent episode/root/index consistency (mirror from the on-disk
canonical episode); whole-artifact integrity (`FinalizedCall.artifact_sha256`, tamper-proof);
episode-tree export invariants (index + latest == root mirror, else blocking); precise
complete-vs-incomplete verification (exit 5 real jobs, exit 0 zero-call, `diff_manifests` the
full path, docs de-overclaimed); one shared `finalized_call_context` consumed by F012 and F010.
F012 stays `[~]`. F017 not started.

## Round 4 — COMPLETE (all 14 findings fixed as one block)

Evidence job `e35a4ec9baf842ce` (operator-attested, 0 provider calls; T001/T002/T003 in
worktrees off base `b0ba27a`; linked prior `d02d1a62dfa842e8`). ZIP
`remedy-review-20260715-150655-READY_FOR_REVIEW.zip` (sha256
`8de799409b98f45a3c6b05c377e6915adf0e907d92fd9cb55ab061b5655835d5`). manifest_integrity.ok +
postmortem_integrity.ok True; fresh_evidence_gate PASS; final_verifier PASS_WITH_RISKS. F012
stays `[~]`, not accepted, not committed.

### 37 proofs
1. `EpisodeInputSnapshotV1` typed wrapper (snapshot_v/episode_id/captured_at/capture_phase/status/problems/input) round-trips (episode_graph::test_wrapper_round_trips_and_reports_status).
2. `build_run_manifest(snapshot=None)` RAISES — no terminal re-probe (episode_graph::test_failed_capture_is_blocking_not_reprobed).
3. `_capture_input_snapshot` records `status=failed` data on capture error, never `{}` (capture_episode_input_snapshot).
4. Pre-work stop captures an explicit `pre_work_stop` snapshot; stop-retry reuses the bound one (`_episode_snapshot_bound_ok`).
5. Finalizer blocks on a missing/failed/foreign snapshot (`_write_run_manifest_record` raises → run_manifest_error).
6. F2 timeout_sec moves `job_input_sha256` (material_input_fields::timeout_sec).
7. F2 timeout_profile moves identity (material_input_fields::timeout_profile).
8. F2 max_output_chars moves identity (material_input_fields::max_output_chars).
9. F2 stream_evidence moves identity (material_input_fields::stream_evidence).
10. F2 max_tasks moves identity (material_input_fields::max_tasks).
11. Every `_source` companion moves identity (material_input_fields::*_source cases).
12. No ExecutionConfig field is absent from the hashed definition (material_input_fields::test_no_material_field_is_silently_missing_from_definition).
13. Clean tree → `dirty is False` (security::test_clean_tree_is_false).
14. Unstaged change → `dirty is True` (security::test_unstaged_change_is_true).
15. Untracked file → `dirty is True` (security::test_untracked_file_is_true).
16. Non-git dir → `dirty is None` (security::test_non_git_dir_is_none).
17. Untracked symlink target CONTENT is never read into the digest (security::test_untracked_symlink_content_is_never_read).
18. FIFO/special raises `_UntrackedSpecial` — never opened, cannot hang (security::test_special_file_and_symlink_are_never_opened_by_the_reader).
19. Symlink raises `_UntrackedSymlink` carrying link text, not file bytes (same test).
20. Two ordered episodes validate clean; latest = max ordinal (episode_graph::test_two_episodes_validate_clean).
21. Index rollback to a lower-ordinal episode is rejected (episode_graph::test_rollback_latest_to_older_episode_is_rejected).
22. Duplicate ordinals rejected (episode_graph::test_duplicate_ordinals_are_rejected).
23. Non-contiguous ordinals rejected (episode_graph::test_non_contiguous_ordinals_are_rejected).
24. Self prior rejected (episode_graph::test_self_reference_is_rejected).
25. Unknown prior rejected (episode_graph::test_unknown_prior_is_rejected).
26. Future/equal-ordinal prior rejected (episode_graph::test_future_ordinal_prior_is_rejected).
27. Cycle rejected by DFS (episode_graph::test_cycle_is_rejected).
28. ordinal<1 / previous-not-a-prior / first-with-previous invalid (episode_graph::TestManifestOrdinalValidation).
29. Clean episode artifacts validate through anchored reads (security::test_clean_episode_artifacts_validate).
30. Tampered call artifact caught by sha256 (security::test_tampered_call_artifact_is_caught).
31. Undeclared call artifact caught (security::test_undeclared_artifact_is_caught).
32. Symlinked episode dir refused, outside bytes never enter `files` (security::test_symlinked_episode_dir_is_refused_not_followed).
33. Missing episode manifest reported as a problem (security::test_missing_episode_manifest_is_a_problem).
34. `load_episode_manifest_verified` used by idempotent retry/repair/export (pingpong_job `_write_run_manifest_record`; job_evidence).
35. F010 records against the exact `FinalizedCallContext` (pingpong_loop `_finalize_call` returns ctx; `_record_call_failure(finalized_context=ctx)`; job_rerun_manifest::test_f010_and_f012_build_the_same_context still green).
36. Zero-call equality is git-independent + no-Git yields exit 5 (job_rerun_manifest::test_public_cli_zero_call_job_exits_0, ::test_no_git_remedy_env_zero_call_exits_5).
37. Full sweep: F012 group 514 passed; verification run in-bundle 169 passed; broad orchestration+cli 6199 passed (42 pre-existing missing-doc failures only); compileall/`bash -n`/`git diff --check` clean.

## Round 5 — COMPLETE (all 14 findings fixed as one block)

Evidence job `1a50d766f7f84cf1` (operator-attested, 0 provider calls; T001/T002/T003 in worktrees
off base `b0ba27a`; linked prior `e35a4ec9baf842ce`). ZIP
`remedy-review-20260715-222252-READY_FOR_REVIEW.zip` sha256
`309bec028ed15d786a1634ed02fabb46e0e003f2b358a6b93a9fd757aa978f3d`. manifest_integrity.ok +
postmortem_integrity.ok True; fresh_evidence_gate PASS; final_verifier PASS_WITH_RISKS. Three
authoritative verification runs recorded: vr-0001 187 passed (F012), vr-0002 300 passed
(F010/F011 + stop), vr-0003 501 passed (CLI). F012 stays `[~]`, not accepted, not committed.

### 39 required proofs (all satisfied)
1. Failed episode-start snapshot → 0 provider calls (lifecycle::test_failed_snapshot_capture_blocks_before_any_provider_call).
2. Failed workspace-tree capture → 0 provider calls (lifecycle::test_failed_workspace_tree_capture_is_a_snapshot_failure).
3. No terminal re-probe (build_run_manifest requires the wrapper; episode_graph::test_failed_capture_is_blocking_not_reprobed).
4. Completed cannot survive snapshot failure (lifecycle::status==blocked).
5-8. Persisted timeout/output/max-tasks/stream reach the runtime (runtime_truth::test_persisted_invocation_controls_are_executed_and_recorded + test_persisted_max_tasks_actually_caps_the_run).
9. Explicit default overrides persisted (runtime_truth::test_explicit_default_overrides_persisted_nondefault).
10. Source fields match resolution (runtime_truth asserts *_source).
11. Runtime==JobPlan==Manifest for every control (runtime_truth).
12. Manifest embeds full EpisodeInputSnapshotV1 (lifecycle asserts ref.episode_snapshot.*).
13. Unsupported snapshot version refused (validate_episode_input_snapshot; is_ok False).
14. Invalid capture phase refused (validate_episode_input_snapshot).
15. status=ok+problems refused (episode_graph::test_wrapper_round_trips; validator).
16. Foreign snapshot episode refused (build_run_manifest expected_episode_id).
17. Stop snapshot/manifest/calls share one episode (lifecycle::test_stopped_manifest_snapshot_and_calls_share_one_episode).
18. Stop request id separate (same test; ref.stop_request_id != episode).
19. Pre-work stop one coherent episode (lifecycle::test_pre_work_stop_uses_one_coherent_episode).
20-21. Same-size mutation → incomplete, no mixed digest (security::test_same_size_in_place_mutation_during_read_is_a_race).
22. Previous is exactly ordinal N-1 (episode_graph::test_skipping_immediate_predecessor_is_rejected).
23. Out-of-order/incomplete history blocks (episode_graph::test_out_of_order_prior_list_is_rejected).
24. JobPlan created_at mismatch blocks (episode_graph::TestJobPlanIndexCrosscheck::test_created_at_mismatch_blocks).
25. JobPlan previous mismatch blocks (::test_previous_mismatch_blocks).
26. JobPlan latest mismatch blocks (::test_latest_mismatch_blocks).
27. Duplicate JobPlan episode blocks (::test_duplicate_jobplan_episode_blocks).
28. Next ordinal from canonical index (episode_graph::TestCanonicalOrderDerivation).
29. Tampered JobPlan cannot redirect order (_crosscheck_jobplan_vs_canonical refuses append; ::test_index_only_episode_blocks).
30. Symlinked/missing Evidence parents cause no outside creation (security::TestAnchoredExportReader + anchored ensure/exists).
31. Snapshot capture + finalization use no unsafe Path trust ops (episode_manifest_exists_anchored/ensure_evidence_root_anchored).
32. Zero-call complete job exits 0 (rerun::test_public_cli_zero_call_job_exits_0).
33. Ordinary call-bearing job exits 5 (rerun::test_public_cli_real_job_with_calls_exits_5).
34. Confirmed drift exits 4 (rerun::test_a_new_target_commit_causes_exit_4).
35. Integrity corruption exits 1 (rerun manifest_integrity path).
36. No secrets/absolute paths (redaction tests; review_manifest_privacy).
37. F010 green (vr-0002 300 passed).
38. F011 green (vr-0002 300 passed).
39. F012 `[~]` (STATUS.md unchanged marker).

## Round 6 — COMPLETE (all 12 findings fixed as one block)

Evidence job `f09eba2be5594829` (operator-attested, 0 provider calls; T001/T002/T003 in worktrees
off base `b0ba27a`; linked prior `1a50d766f7f84cf1`). ZIP
`remedy-review-20260715-235157-READY_FOR_REVIEW.zip` sha256
`7a7d7e8118eff8a2b07805cec92b9550ef408b5d59bcb26d505abdb404909a17`. manifest_integrity.ok +
postmortem_integrity.ok True; fresh_evidence_gate PASS; final_verifier PASS_WITH_RISKS. Three
authoritative verification runs: vr-0001 223 (F012), vr-0002 390 (F010/F011+evidence), vr-0003 524
(CLI). F012 stays `[~]`, not accepted, not committed. Stray F001/F003 scratch removed.

### 40 required proofs (all satisfied)
1-3. No-flag job-run preserves persisted max-tasks/stream/profile (cli_invocation_truth::test_no_flag_job_run_preserves_persisted_controls, ::test_persisted_profile_survives_no_flag).
4. Explicit --max-tasks 0 overrides persisted (::test_explicit_max_tasks_zero_overrides_persisted).
5. Explicit --no-stream-evidence overrides persisted true (::test_explicit_no_stream_evidence_overrides_persisted_true).
6. Explicit default timeout records invocation (::test_explicit_default_timeout_still_records_invocation).
7. job-resume preserves omission (::test_job_resume_preserves_omission).
8. job-flow uses the shared RunInvocation (no pre-resolution) — do_cmd dispatch + runtime_truth (F13) prove config==manifest.
9. Grouped CLI runtime==JobPlan agree (cli_invocation_truth spy vs persisted config).
10-12. Partial failure after episode/mirror/index publication recovers (recovery::TestRebuild + TestPartialPublicationConverges::test_missing_index_recovers_on_retry).
13. Stop retry after crash window converges (recovery::test_missing_index_recovers_on_retry).
14. Exactly one archive/postmortem/event/episode (job_stop_integration suite green in vr-0002).
15. Undeclared call file never in export (export_allowlist::test_undeclared_call_file_is_not_copied).
16. Unindexed episode never in export (::test_unindexed_episode_dir_is_not_copied).
17. Secret canary never enters bundle (::TestFullExportCopiesNothingWhenDirty::test_canary_never_enters_the_bundle).
18. Oversized undeclared file not read (::test_oversized_extra_file_is_not_read).
19. Valid allowlisted tree exports identically (::test_valid_tree_exports_the_declared_set).
20. Bare legacy snapshot rejected (schema::test_manifest_without_episode_snapshot_is_rejected).
21. Naive timestamp rejected (schema::test_naive_timestamp_is_rejected).
22. Unsafe stop request id rejected (schema::test_unsafe_stop_request_id_is_rejected).
23. Malformed job-input sha rejected (schema::test_bad_job_input_sha_is_rejected).
24. Malformed artifact sha rejected (schema::test_malformed_artifact_sha_is_rejected).
25. Duplicate config/env keys rejected (schema::test_duplicate_config_keys_are_rejected).
26. Non-REMEDY env / abs-path snapshot rejected (schema::test_non_remedy_env_key_is_rejected + validate_input_snapshot bounds).
27. Active episode differing from latest blocks (terminal_consistency::test_active_differs_from_latest_blocks).
28. Completed job with stopped latest blocks (::test_status_mismatch_blocks + ::test_completed_with_stopped_metadata_blocks).
29. Stopped JobPlan/manifest request-id mismatch blocks (::test_stopped_request_id_mismatch_blocks).
30. Latest created-at mismatch blocks (::test_created_at_mismatch_blocks).
31. Permission-denied untracked file returns incomplete (F9 OSError fold — worktree_identity; security suite green).
32. Root FD stable on collector failures (F9 finally-close; verified by import + security green).
33. Partial chain → CLI integrity exit 1 (load_latest_manifest_for_cli integrity_error → EXIT_ERROR).
34. Legacy unmarked job stays legacy/uncovered (job_evidence legacy note path; job_evidence suite green).
35. Resumable workspace drift detected/incomplete (build_current_candidate write_tree_for_path; F11).
36. F010 green (vr-0002 390 passed).
37. F011 green (vr-0002 390 passed).
38. F012 `[~]` (STATUS.md marker unchanged).
39. F017 untouched (not started).
40. No unexplained F001/F003 files remain in scope (removed; git status clean of self_run_goal_*).

## Round 7 — COMPLETE (all 16 findings fixed as one block)

Evidence job `7cd996b2a6fe4f51` (operator-attested, 0 provider calls; T001/T002/T003 in worktrees
off base `b0ba27a`; linked prior `f09eba2be5594829`). ZIP
`remedy-review-20260716-121351-READY_FOR_REVIEW.zip` sha256
`004400568916e993bf954c6faa6b0f9537eb6b673475f3daa0a2adae60787ce7`. manifest_integrity.ok +
postmortem_integrity.ok True; fresh_evidence_gate PASS; final_verifier PASS_WITH_RISKS. Four
authoritative verification runs: vr-0001 88 (new R7 suites), vr-0002 223 (all F012), vr-0003 390
(F010/F011/Evidence), vr-0004 581 (CLI). F012 stays `[~]`, not accepted, not committed.

### Production seams selected
- `manifest_schema.py` (new) — limits + strict raw-JSON primitives (F4/F11).
- `run_manifest.py` — `decode_*_v1`, `validate_input_snapshot`, `validate_job_input_definition`,
  `job_input_definition_sha256`, `validate_prepared_call_input`, `validate_call_identity`,
  `canonical_artifact_ref`, `_contained_root_fd`, `_open_dir_anchored_or_missing`,
  `load_latest_manifest_for_cli`, `build_verified_manifest_tree`, `build_current_candidate`.
- `job_evidence.py` — `_crosscheck_terminal_jobplan_manifest` (F13).
- `worktrees.py` — `write_tree_for_path` (F12).
- `apps/cli/grouped.py` — `_stream_group` + `_UsageError` (F15); `job_rerun_cmd.py` typed load.

### Required proofs (all satisfied)
1-2. Malformed index → typed integrity result + CLI Exit 1 without traceback (cli_rerun_integrity::test_malformed_index_*).
3. Tree builder returns problems, never throws (export_allowlist + F2 wrapper).
4-6. Evidence dir outside root / sibling / traversal / symlink refused; safe nested succeeds (root_containment).
7-8. JSON `"false"` and string integers rejected (external_schema::TestNoBoolean/IntegerCoercion).
9-12. Empty worktree status, remedy_dirty, sha/head, head/digest contradictions rejected (hash_bindings::TestSnapshotSafety).
13-16. Raw secret config/env, absolute provider path rejected; redacted snapshot passes (same).
17-18. Job-input hash mismatch + every mutated definition field blocks (hash_bindings::TestJobInputHashBinding).
19-20. Prepared-input fingerprint mismatch + malformed hashes block (::TestPreparedInputBinding).
21-22. Call without artifact + unsafe role/kind/task/run/job id block (::TestPublishedCallsAndIdentities).
23-25. Invalid coverage status, complete-with-problems, incomplete-without-problems block (::TestCoverageEnum).
26-30. Size boundary minus-one/exact/plus-one; writer record always exportable; oversized index bounded (size_limits).
31-33. Missing/symlinked stopped-job workspace incomplete; existing stays honest (resume_workspace).
34-37. Empty terminal active episode/timestamp/path and stop-request mismatch block (terminal_consistency + F13).
38-40. Extra episode-root file/dir rejected; no undeclared member in verified bytes/bundle (export_allowlist + F14).
41-42. Both stream flags → Exit 2 explained; omitted/positive/negative stay None/True/False (stream_tristate).
43. No secrets/absolute paths in manifest/hash/CLI/export (validate_input_snapshot canary tests).
44-45. F010/F011 green (vr-0003 390 passed).
46. F012 `[~]` (STATUS.md marker unchanged).
47. F017 untouched (`[ ] F017 — Scope fences`).

## Round 8 — COMPLETE (all 16 findings fixed as one block)

Evidence job `e4cb0a3c1c444309` (operator-attested, 0 provider calls; T001/T002/T003 in worktrees
off base `b0ba27a`; linked prior `7cd996b2a6fe4f51`). ZIP
`remedy-review-20260716-130448-READY_FOR_REVIEW.zip` sha256
`9e5ecba9456a9685ee589c86be52b8ba0a96ded08ac29305895595fb6a1faec0` (exactly one new ZIP this
round: 41 → 42). manifest_integrity.ok + postmortem_integrity.ok True; fresh_evidence_gate PASS;
final_verifier PASS_WITH_RISKS. Four verification runs: vr-0001 68 (new R8 suites), vr-0002 311
(all F012), vr-0003 390 (F010/F011/Evidence), vr-0004 581 (CLI). F012 stays `[~]`.

### Production boundary per fix
- `call_identity.py` — `logical_key()`, `prompt_len_bytes` bound into the fingerprint,
  `from_trusted_json` renames.
- `run_manifest.py` — `logical_input_projection`/`provenance_projection`/`provenance_sha256`,
  `decode_job_input_definition_v1`, exact InputSnapshot/PreparedCallInput schemas,
  `strict_json_loads` (duplicate keys), `require_canonical_bytes`, writer round-trip +
  aggregate limits, `_open_dir_anchored_or_missing` on all trust paths, strict `read_run_manifest`.
- `pingpong_job.py` — persisted JobPlan snapshots strict-decoded.
- `job_evidence.py` — per-episode coverage strict-decoded.

### 47 required proofs (all satisfied)
1-3. Different job/episode/run+call ids, same inputs → same logical hash (logical_identity::TestSyntheticProjections + ::TestTwoRealRunsShareLogicalIdentity, on REAL runs).
4. Record hashes differ for different provenance (same tests).
5. Completed vs stopped alone → same logical identity (::test_outcome_alone_does_not_change_logical_identity).
6-7. Changed provider fingerprint / call order blocks (::test_changed_provider_fingerprint_blocks, ::test_changed_call_order_blocks).
8-10. Persisted run `"ok":"false"`, string sequence, unknown prepared field rejected (persisted_run_call_schema).
11-12. Persisted JobPlan string boolean / unknown snapshot field rejected (persisted_episode_snapshot_schema).
13-16. Unknown InputSnapshot/worktree field, int config key/value, wrong worktree head type rejected (external_schema + hash_bindings).
17-20. Minimal/unknown/missing/wrong-typed JobInputDefinition rejected (job_input_definition_schema).
21-22. Unknown / secret-path PreparedCallInput field rejected (external_schema + hash_bindings).
23-24. Unicode prompt byte length correct; length tamper breaks the fingerprint (run_manifest::prepared-input tests + hash_bindings).
25. Invalid nested input → is_ok() false (persisted_episode_snapshot_schema::TestFullValidityPredicate).
26-28. Root mirror / episode wrong boolean, unknown snapshot secret field block (canonical_bytes).
29-30. Canary never in verified bytes or bundle (export_allowlist + canonical_bytes).
31-32. Duplicate JSON key blocks; noncanonical bytes rejected (canonical_bytes).
33-35. Aggregate episode/tree size rejected before write; writer output always round-trips (aggregate_limits).
36. No permissive decoder on persisted paths (strict_boundaries guard test).
37. No name-based trust precheck in F012 security paths (strict_boundaries guard test).
38-42. CLI Exit 0/4/5/1/2 all still work (job_rerun_manifest, job_rerun_integrity_errors, stream_evidence_tristate).
43. No secrets/absolute paths (validate_input_snapshot canary tests).
44-45. F010/F011 green (vr-0003 390 passed).
46. F012 `[~]`; 47. F017 `[ ] F017 — Scope fences`.


## Recorded contract difference #3 — pre-existing base failures (round 12)

`tests/cli/test_do_cmd_summary.py` and `tests/cli/test_product_spine.py` fail 18 tests at base
`b0ba27a` (proven on a pristine worktree of the base): they require `docs/core-product-spine-v0.md`
and other flat doc paths that an earlier docs restructure removed. Out of scope for F012 round 12;
recorded, not fixed, and excluded from the recorded CLI verification command rather than papered
over.
