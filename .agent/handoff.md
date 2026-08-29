# Handback — F040 · SESSION 1 · round 4 — THE DIGEST ENDPOINT (T001 PART 2)

> Written by the WORKER in C5, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe.

## Session

SESSION 1 of feature F040 · round 4 · rounds so far 4.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed.

## Range

Review of `2b063387`..`HEAD` on branch `feature/f040-completion-digest`. The
base is round 3's handback commit and was the tip of the branch when this round
opened. No new branch was cut, no pull request opened, nothing merged, nothing
force-pushed.

**T001 IS COMPLETE with this round.** The composition module landed in round 3;
this round serves it. `GET /api/jobs/<job_id>/digest` now answers the digest
envelope, and the route is pinned as a pass-through rather than described as one.

## Commits

### 519427cb docs(f040): save the round 4 step block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f040-r4.md` | +257 −0 | C0a — the block, copied with `shutil.copyfile` from `.remedy-wt/f040-r4-block.md`, never retyped |

### 4040fbda docs(f040): mirror the round 4 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +177 −241 | C0b — the same bytes, the same `shutil.copyfile` call |

### 8841291a docs(f040): retarget the plan at the digest endpoint

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +16 −16 | C1 — rewritten from slice PLAN4, byte for byte; the first substantive commit, ahead of the ledger append, per constraint 3 |

### 16f4c3bc docs(f040): book the round 3 verdict and R-0753

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 −0 | C2 — slice RECORD4 appended after ONE separator newline; the R3 PASS verdict and the R-0753 registration. Append-only: the numstat shows zero deletions |

### 96952511 feat(f040): serve the job digest from the ui server

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/ui_server.py` | +8 −0 | C3 — `_build_digest_json` immediately after its sibling `_build_decisions_json`, plus pair PAIRHANDLERS registering `"digest"`. ONE commit per constraint 8: a builder with no reference is dead code and a dict line naming a missing function is a NameError at import, so landing them apart would put a red commit on the branch |

### cf176ff6 test(f040): pin the digest route as a pass-through

| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_server/test_digest_route.py` | +161 −0 | C4 — seven route tests, written from the SPEC against the conventions of `tests/ui_server/test_decisions_endpoint.py` rather than a new harness |

### C5 — this commit (self-reference exception)

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C5 — the handback. A handoff cannot table the commit that writes it (R-0149 pattern). It is the verbatim rewrite of a single `.agent/**` state file and is therefore exempt from the 500-insertion cap by AGENTS.md DECISION F104 D1 |

## External actions

| Action | Outcome |
|--------|---------|
| `git worktree add --detach .remedy-wt/f040r4/wt-g3 HEAD` | exit 0 — G3's negative control |
| `git worktree remove --force .remedy-wt/f040r4/wt-g3` | exit 0 — `git worktree list` no longer holds it |
| `git worktree add --detach .remedy-wt/f040r4/wt-g6 HEAD` | exit 0 — G6's red proof |
| `git worktree remove --force .remedy-wt/f040r4/wt-g6` | exit 0 — `git worktree list` no longer holds it |
| `git push -u origin feature/f040-completion-digest` | run after C5; see below |
| PR create / merge / force-push | NONE. No pull request was opened, nothing was merged, nothing force-pushed |
| `remedy` console script | NOT INVOKED. The sandbox denies it (constraint 11) and no gate this round needed it; `python3 -m apps.cli.grouped` was not needed either |

## Verification

One line per gate, REAL exit codes.

### G1 TRANSPORT, at C0b — REAL EXIT 0

    0fbcdaa55a4219804489248f5c3d45a4f5114ae9d3e518838ba1d1440eb374e4  18243  .remedy-wt/f040-r4-block.md
    0fbcdaa55a4219804489248f5c3d45a4f5114ae9d3e518838ba1d1440eb374e4  18243  .agent/authored/f040-r4.md
    0fbcdaa55a4219804489248f5c3d45a4f5114ae9d3e518838ba1d1440eb374e4  18243  .agent/last_block.md
    ALL THREE EQUAL: True

### G2 THE PLAN, at C1 — REAL EXIT 0

    plan.md sha256 3b33b451bda9bf1672f5765d8095dc4a5ad6afa090a52d790004ae58d21e5eb3 bytes 1786
    PLAN4   sha256 3b33b451bda9bf1672f5765d8095dc4a5ad6afa090a52d790004ae58d21e5eb3 bytes 1786
    BYTE-EQUAL: True
    LINES: 38 UNDER 50: True
    has '## Goal': True  has '## Next Steps': True

### G3 THE RECORD APPEND, at C2 — REAL EXIT 0 (readings), REAL EXIT 0 (negative control)

Pre-commit length re-measured, not taken from the block:

    base bytes: 1662667  RECORD4 bytes: 5385  committed bytes: 1668053
    ARITHMETIC: 1662667 + 1 + 5385 = 1668053 == committed 1668053 -> True
    READING (a) WHOLE RECONSTRUCTION: True
    READING (b) N COUNTED: 2  PARAGRAPH ORDER (last N in order): True

The reviewer's reading of 1662667 at `2b063387` was confirmed exactly. N is 2:
RECORD4 is three lines — the verdict paragraph, one blank, the R-0753 paragraph.

NEGATIVE CONTROL, in the disposable worktree `.remedy-wt/f040r4/wt-g3`, control
FIRST:

    unflipped   REAL EXIT: 0   (a) True   (b) True
    flipped     REAL EXIT: 1   (a) False  (b) False, MISMATCH at appended paragraph 1
    restored    REAL EXIT: 0   (a) True   (b) True

The flip is one byte at offset 1662708, inside the FIRST appended paragraph
(`S` -> `s` in `THE COMPOSITION MODULE`), length-preserving — so the arithmetic
reading still passes and only the two content readings reject it, which is the
point. `git worktree list` afterwards holds only the primary checkout.

### G4 THE LEDGER, at C2 — REAL EXIT 0

    registered pattern ^- R-\d+ — (em dash)   resolved pattern ^Done: R-\d+
    registered distinct BEFORE: 313  AFTER: 314
    ADDED registered: ['R-0753']
    resolved distinct BEFORE: 53  AFTER: 53
    ADDED resolved: []
    ^Gate: F040 R3 —  lines: 1
    Done counts: {'R-0570': 0, 'R-0752': 0, 'R-0753': 0}
    OPEN COUNT (registered minus resolved): 261

### G5 THE WIRING, at C3 — REAL EXIT 0

    TO contains FROM: True  -> APPEND-shaped
    TO-only lines: 1  ['                "digest": _build_digest_json,']
    FROM occurrences in the committed file: 1   (expected exactly 1, NEVER 0)
    TO-only line among the 8 lines C3's diff ADDS: 1
    exact string '"digest": _build_digest_json,' occurrences: 1
    '_build_digest_json' occurrences in the whole file: 2
    handlers dict literal at line 3459 KEY COUNT: 16   keys distinct: True
    KEYS: dashboard, brain, brain-view-model, live-state, task-progress,
          decisions, next-action, guide, events, readiness, context-budget,
          story, checklist, diagnostics, diff, digest
    ruff check packages/orchestration/ui_server.py   REAL EXIT: 0
    python3 -m compileall -q packages/orchestration/ui_server.py   REAL EXIT: 0
    ROUND PATH SET: .agent/authored/f040-r4.md, .agent/last_block.md,
                    .agent/live_review.md, .agent/plan.md,
                    packages/orchestration/ui_server.py
    job_digest.py IN this round's path set: False

The 16 entries are COUNTED, not asserted: the file is parsed with `ast`, the one
`Assign` whose target is `handlers` and whose value is a `Dict` is located, and
its `keys` list is measured. Fifteen before, sixteen after.

### G6 THE ROUTE AND ITS RED PROOF, at C4 — REAL EXIT 0

Primary checkout:

    python3 -m pytest tests/ui_server/test_digest_route.py -q
    REAL EXIT: 0 | 7 passed in 1.03s

Disposable worktree `.remedy-wt/f040r4/wt-g6`, `__pycache__` purged before every
run and `python3 -B` throughout. THE UNMUTATED CONTROL IS REPORTED FIRST:

    UNMUTATED control   REAL EXIT: 0 | 7 passed in 5.37s
    COUNTED before deleting: '                "digest": _build_digest_json,'
      occurs 1 time in <worktree>/packages/orchestration/ui_server.py — 46 bytes
      deleted, file 194257 -> 194211 bytes, delta 46
    MUTATED (route unregistered)  REAL EXIT: 1 | 4 failed, 3 passed in 1.13s
    RESTORED (bytes equal original: True)  REAL EXIT: 0 | 7 passed in 1.13s

Four of the seven tests bite on the registration line alone. The three that
survive are the ones that must: the unknown-job 404, the neighbouring-endpoint
404 and the invalid-token 403 are answered before dispatch reaches the handlers
dict, so they are indifferent to whether `"digest"` is registered. That is the
discriminator — the red proof removes the WIRING and nothing else, so it proves
the tests pin the registration and not merely the builder.

    git worktree remove --force .remedy-wt/f040r4/wt-g6   exit 0
    git worktree list -> /home/decodeux/Repos/remedy  cf176ff6 [feature/f040-completion-digest]
    WORKTREE STILL LISTED: False

### G7 THE SUITES AND THE TREE, at C4 — REAL EXIT 0

Run serially, each its own REAL exit code:

    tests/ui_server/                            REAL EXIT: 0 | 515 passed in 32.70s
    tests/orchestration/test_job_digest.py      REAL EXIT: 0 | 40 passed in 0.33s
    tests/ui_contracts/                         REAL EXIT: 0 | 699 passed, 4 skipped in 5.71s
    tests/orchestration/test_integrity_gate.py  REAL EXIT: 0 | 16 passed in 0.28s
    tests/regression/test_resource_safety.py    REAL EXIT: 0 | 21 passed in 11.49s
    tests/cli/test_golden_path.py               REAL EXIT: 0 | 42 passed in 20.82s

THE REQUIRED RISE: `tests/ui_server/` was 508 at the base and is 515 now, a
DIFFERENCE of +7, which is exactly the number of tests C4 adds. The other five
suites are unchanged at 40, 699/4 skipped, 16, 21 and 42.

    git status --porcelain EMPTY: True
    git ls-files --others --exclude-standard count: 0

Per-commit insertions, C0a through C4, every one under 500:

    519427cb  +257   docs(f040): save the round 4 step block
    4040fbda  +177   docs(f040): mirror the round 4 block into last_block
    8841291a  +16    docs(f040): retarget the plan at the digest endpoint
    16f4c3bc  +4     docs(f040): book the round 3 verdict and R-0753
    96952511  +8     feat(f040): serve the job digest from the ui server
    cf176ff6  +161   test(f040): pin the digest route as a pass-through

## Authored-text proofs

Four authored units were extracted MECHANICALLY from
`.remedy-wt/f040-r4-block.md` by a script that reads the `<<<BEGIN NAME` /
`<<<END NAME` marker lines and takes the bytes between them; none was retyped.

| Unit | Bytes | Lines | sha256 | Disk-to-disk result |
|------|-------|-------|--------|---------------------|
| PLAN4 | 1786 | 38 | `3b33b451bda9bf1672f5765d8095dc4a5ad6afa090a52d790004ae58d21e5eb3` | `.agent/plan.md` BYTE-EQUAL (G2) |
| RECORD4 | 5385 | 3 | `5092301994187afc964091bc45f8bce840abb0b78e3e94e88dd997494712ca37` | appended after ONE newline; whole-file reconstruction exact (G3) |
| PAIRHANDLERS-FROM | 42 | 1 | `b3fa1c12a0ccb6938a6f16423c7b80c027fb95bfddace0f48d983695ded32640` | occurred exactly 1x before apply and 1x after (G5) |
| PAIRHANDLERS-TO | 88 | 2 | `9c0a00a7c51c26b023e41d16dfdb3c5280543be94cf8c36c0ea53cd00effe1b4` | applied by `str.replace(FROM, TO, 1)`; TO-only line 1x among C3's added lines (G5) |

The block itself: sha256
`0fbcdaa55a4219804489248f5c3d45a4f5114ae9d3e518838ba1d1440eb374e4` over 18243
bytes, equal on all three copies (G1).

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** Seven commits,
   C0a C0b C1 C2 C3 C4 C5, in that order, one path each, and the change set is
   exactly the seven paths the block names — nothing else was touched. No extra
   commit, no dropped commit, no reordering.

2. **The builder and the route tests were WRITTEN, not sliced** — the block
   supplied two SPECs rather than authored code, so the wording below is mine
   and is the reviewer's to judge. `_build_decisions_json`
   (`packages/orchestration/ui_server.py:2771` at the base, exactly as the block
   states) and `tests/ui_server/test_decisions_endpoint.py` were read first and
   their conventions followed. `_build_digest_json` sits IMMEDIATELY AFTER the
   decisions builder — "beside" is read as after, since inserting before it
   would separate the decisions builder from the task-progress builder it
   already follows. It imports `build_job_digest` LOCALLY inside its own body,
   carries a one-line docstring, calls `_load_events(job)` and returns
   `build_job_digest(job, events)` and nothing else. It adds, removes, defaults
   and renames NO key, per constraint 9. It does not restate `JOB_DIGEST_VERSION`
   — `job_digest.py` owns the version and `_send_json` does not wrap, so the
   builder's dict IS the response body.

3. **The unknown-job status was MEASURED, not assumed**, as the SPEC required.
   `_load_job` at `packages/orchestration/ui_server.py:232` returns
   `(None, (404, {"error": "job not found"}))` for a well-formed UUID that names
   no stored job, and the dispatcher returns it at :3449-3451 before any handler
   runs. A live request confirmed it on the wire: status **404**, body
   `{"error": "job not found"}`. The test asserts the measured value including
   the error string. Two neighbouring facts were measured at the same time and
   are worth the reviewer's attention: an id that is neither a UUID nor hex — a
   THIRD unknown-id shape — answers **400** `{"error": "invalid job id"}`, and a
   nonexistent endpoint under a REAL job answers **404** `{"error": "not found"}`,
   a DIFFERENT error string from the loader's. The neighbour test asserts that
   string, so it cannot pass by accidentally finding the job missing instead of
   the endpoint.

4. **A seventh test beyond the SPEC's five bullets.** The SPEC said "cover, at
   least". The file adds `test_digest_endpoint_refuses_an_invalid_token`, which
   the sibling also carries, so the new route is pinned as token-guarded rather
   than assumed to inherit the guard. The key-set bullet is split into two tests
   — the eight-key set, and `version == JOB_DIGEST_VERSION` — so a version bump
   and a shape change fail with different names. Seven tests total, which is the
   +7 G7 measured.

5. **The envelope's key set is a LITERAL in the test, deliberately.** The eight
   names are written out as `DIGEST_KEYS` rather than imported or derived from
   `build_job_digest`, because a set read back out of the module under test would
   make the assertion vacuous. `version` is the opposite case and is IMPORTED,
   exactly as the SPEC ordered, because there the point is that the route must
   not carry its own copy of the number.

6. **PLAN4 marks this round's work `done` at C1, before C3 and C4 existed.**
   That is inherent in the block's own ordering — constraint 3 puts the plan
   rewrite first and the slice is applied byte for byte — but it means the plan
   read forward for four commits. Declared rather than silently corrected; the
   claim is true at HEAD.

7. **One non-load-bearing imprecision in the block's prose, applied as given.**
   The C3 SPEC says "The dict at line 3467". At the base `2b063387`, line 3467 is
   `                "diff": _build_diff_json,` — the LAST ENTRY of the dict and
   the pair's FROM anchor; the dict literal's own assignment `handlers = {` is at
   line 3452. Everything else the block cites was verified EXACT at the base: the
   decisions builder at 2771, the path guard at 3445, the loader's error return
   at 3449-3451, and constraint 10's count — `digest` occurs 7 times in
   `ui_server.py` at the base, at lines 2640, 3285, 3296, 3305, 3315 and 3316
   (line 3316 carries it twice), every one a hash digest. No count reported in
   this handback is scoped to the bare word.

8. **PLAN4's provenance claim was checked and is true.**
   `git merge-base main feature/f040-completion-digest` is `f5b1e6c5`, whose
   subject is `Merge pull request #222 from
   UndefinedDatabase/feature/f033-hunk-approval-v2`.

9. **`packages/orchestration/job_digest.py` was NOT edited**, as constraint 3 of
   the change set requires, and nothing under `apps/` changed. G5 reports the
   round's measured path set to prove it rather than asserting it.

10. **Assumption: "a job with a real plan" means a job carrying real tasks.**
    The fixture is a `Job` with one `Task` and no `target_repo`, saved through
    `save_job` under a `REMEDY_DATA_DIR` `tmp_path` — the sibling's fixture,
    chosen for the same reason: it derives a decision card, so the digest's
    `decisions` and `primary_action` sections are non-trivial rather than
    every-field-absent. The digest it produces was probed first and is STABLE
    over a two-second gap, so the pass-through equality cannot flake on the
    time-dependent `decisions.peak_urgency`: the derived card's `age_seconds` is
    0 and `decision_urgency` returns `int((blocked + 1) * age)` = 0.

11. **The `remedy` console script was not invoked** (constraint 11); no gate
    needed it, and `python3 -m apps.cli.grouped` was not needed either.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f040-r4.md` | done | `shutil.copyfile`, 519427cb |
| C0b mirror the same bytes into `.agent/last_block.md` | done | `shutil.copyfile`, 4040fbda |
| C1 rewrite `.agent/plan.md` from PLAN4 | done | 8841291a, byte-equal |
| C2 append RECORD4 to `.agent/live_review.md` | done | 16f4c3bc, append-only |
| C3 `_build_digest_json` + pair PAIRHANDLERS | done | 96952511, one commit per constraint 8 |
| C4 create `tests/ui_server/test_digest_route.py` | done | cf176ff6, seven tests |
| C5 rewrite `.agent/handoff.md` | done | this commit |
| G1 TRANSPORT, at C0b | done | REAL EXIT 0 |
| G2 THE PLAN, at C1 | done | REAL EXIT 0 |
| G3 THE RECORD APPEND, at C2 | done | REAL EXIT 0; negative control REAL EXIT 0 |
| G4 THE LEDGER, at C2 | done | REAL EXIT 0 |
| G5 THE WIRING, at C3 | done | REAL EXIT 0 |
| G6 THE ROUTE AND ITS RED PROOF, at C4 | done | REAL EXIT 0 |
| G7 THE SUITES AND THE TREE, at C4 | done | REAL EXIT 0 |

## Open findings

Open count after C2: **261** (314 registered distinct, 53 resolved distinct).

Three are this feature's business:

- **R-0570** — OPEN, routed to the paydown branch. Not F040's to fix; its repair
  edits `README.md` and `tests/docs/test_docs_consistency.py`.
- **R-0752** — OPEN, routed to the same paydown branch. Its repair edits
  thirteen `docs/roadmap/features/` files F040 does not own.
- **R-0753** — OPEN, **CARRIED as this feature's documented risk**, registered by
  C2 this round. The persisted actuals record has no money field, so the digest's
  `cost.basis` can only ever answer `absent` in production. Not F040's to fix —
  the repair widens a persisted schema and its decoder, which is F104's surface.

## Next

Review this round: T001 is complete, so the expected next action is the round 4
verdict, and then T002 — the hero card, its trigger, dismiss and last-seen
mechanics, and the retirement of the TypeScript urgency copy per DECISION
F040 D2.
