# Handback — F297 round 4: book round 3, land T013 and T014

## Session

SESSION 1 of feature F297 · round 4 · rounds so far 4

Context self-assessment: the session verified every prepared file's digest before use, read the
full bundle once, and executed the four commits and six gates in one uninterrupted pass with no
retries; context remains comfortable at handback.

Fortschritt: ~52 % (T001 to T014 landed · T015 to T025 open) — Schätzung

## Range

Review of `4798211ed`..`HEAD`.

## Commits

### 7431af18c F297 R4 C1: book round 3 and the resolutions of R-1237, R-1239 and R-1238, DECISION F297 D5

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r4.md` | +133/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r4/prep/block.md` |
| `.agent/live_review.md` | +8/-0 | appended the `Gate: F297 R3` paragraph (VERDICT PASS) and the `Done:` paragraphs for R-1237, R-1239, R-1238 |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D5: how round 4 repairs R-1250 and R-1247, and the boundary `plan_order_job` gains first |
| `.agent/plan.md` | +11/-12 | rewritten in full for F297 round 4 |

### ee066733b F297 R4 C2: an order over several repositories is accepted by none unless every mission can take it (R-1250)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_sequence.py` | +5/-9 | `_step_plan` calls the new `accept_order_in_each` in place of its own per-target acceptance loop (R-1250) |
| `packages/orchestration/repo_mission.py` | +38/-4 | new `_refusal`, `order_refusal` and `accept_order_in_each`; `accept_order` reuses `_refusal` for its own check |
| `tests/cli/test_do_several_projects.py` | +23/-0 | new coverage: a paused second repository's mission leaves the first without a new batch, and no job is planned |
| `tests/orchestration/test_repo_mission.py` | +37/-0 | new coverage: `order_refusal`'s read-only answer, `accept_order_in_each`'s refuse-before-accept and its shared correlation id, and that `order_refusal` creates nothing |

### 1a9a17119 F297 R4 C3: structural step, the boundary of plan_order_job and its first step

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +6/-1 | `plan_order_job`'s boundary written; the row falls from 269 to 252 lines |
| `packages/orchestration/do_sequence.py` | +23/-18 | step (1) taken: the record a plan that cannot be parsed leaves becomes `_record_unparsed_plan`, moved out unchanged |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FUNCTION_LINES` lowered from 31044 to 31027 |

### 2ec737bbc F297 R4 C4: a failed shape step leaves no stopped job linked, and an unparsed plan leaves its job stopped (R-1247)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_sequence.py` | +12/-4 | `_record_unparsed_plan` now saves the job stopped with `plan_parse_failed`, never pending; `_stop_unrun_shape_jobs` calls the new `unlink_order_jobs` on each target mission (R-1247) |
| `packages/orchestration/repo_mission.py` | +15/-0 | new `unlink_order_jobs` drops job ids out of a mission's chain so none of them is ever its latest link |
| `tests/orchestration/test_do_sequence_order_digest.py` | +16/-0 | new coverage: an unparsed plan's job reads `stopped`/`plan_parse_failed` with a `finished_at` |
| `tests/orchestration/test_order_shape_repair.py` | +12/-2 | the shape-step test now links a real mission and asserts the stopped job leaves its chain |

### this commit F297 R4 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, docs/agents/handback_template.md) |

## External actions

None during the round. `git push origin feature/f297-findings-paydown-v7` after this commit,
reported below with the post-push `git rev-parse HEAD origin/feature/f297-findings-paydown-v7`.
No PR created or touched; no other `gh` command run. The Open PR Gate is Phase 1 rule 2 of the
self-drive protocol and is listed in `## Next` for whoever starts the next cycle.

## Verification

**Preconditions (before C1):** `git status --porcelain` empty; `git rev-parse HEAD` read
`4798211ed92fdf3fab72be63847609b54ddf99dd`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r4/prep/block.md`
read `133`; `sha256sum` read
`d16c9f9e116bdcf9b8acb13c41ea9d56682025bb3c31014759c4334e719804c4` — both equal to the values the
prompt delivered. All 20 Bundle-listed prepared files (`block.md`, 15 `dry-*` files, 2 `c2-*`
files, 1 `c3-*` file, 2 `append-*.txt` files, `verify.py`, `run_selection.py`, `selection.txt`)
hashed via a python3 script under `.remedy-wt/f297-r4-worker/check_hashes.py`: every one read
`True`, final line `ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the block and the three `dry-*` whole files to
`.agent/authored/f297-r4.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`;
each printed `cmp_equal=True`. `git branch --show-current` read `feature/f297-findings-paydown-v7`
before staging. `git diff --cached --numstat` read exactly `133 0 .agent/authored/f297-r4.md`,
`12 0 .agent/decisions.md`, `8 0 .agent/live_review.md`, `11 12 .agent/plan.md` — matching the
block's required readings. The staged diff of all four files was read in full and matched the
block's "For the record" description and DECISION F297 D5's text exactly.

**C2:** `python3 -I c2_copy.py` copied the four files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `5 9 packages/orchestration/do_sequence.py`,
`38 4 packages/orchestration/repo_mission.py`, `23 0 tests/cli/test_do_several_projects.py`,
`37 0 tests/orchestration/test_repo_mission.py` — matching the block exactly. The staged diff was
read in full: `accept_order_in_each` asks every target through `order_refusal` before any accepts,
shares one correlation id only over more than one target, and `_step_plan` calls it in place of
its own loop.

**C3:** `python3 -I c3_copy.py` copied the three files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `6 1 docs/system/structure-ledger-v1.md`,
`23 18 packages/orchestration/do_sequence.py`, `1 1 tests/test_structure_ratchet.py` — matching
the block exactly. The staged diff was read in full: the boundary is written onto the ledger, step
(1) extracts `_record_unparsed_plan` unchanged (confirmed `save_job_plan` stays imported at its
other, still-used call site inside `plan_order_job`), and the row/pin fall from 269/31044 to
252/31027. No behaviour changed.

**C4:** `python3 -I c4_copy.py` copied the four files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `12 4 packages/orchestration/do_sequence.py`,
`15 0 packages/orchestration/repo_mission.py`,
`16 0 tests/orchestration/test_do_sequence_order_digest.py`,
`12 2 tests/orchestration/test_order_shape_repair.py` — matching the block exactly. The staged
diff was read in full: `_record_unparsed_plan` now sets the job `stopped`/`plan_parse_failed` with
a `finished_at` before saving; `_stop_unrun_shape_jobs` calls the new `unlink_order_jobs` on each
target mission so a stopped job leaves the chain and is never its latest link.

Every `git branch --show-current` run immediately before a commit (C1 through C4) read
`feature/f297-findings-paydown-v7`.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r4/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (12
file-equality checks and the two ledger/decisions base-plus-slice checks), last line `ALL True`,
exit 0.

**Gate 2:** `python3 -m ruff check` over the 7 named paths → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r4/prep/run_selection.py /home/decodeux/Repos/remedy` → 3
SKIPPED lines (`tests/test_agent_tooling.py:43` D12 quarantine,
`tests/test_install_smoke.py:175` opt-in install smoke,
`tests/test_repair_context_reviewer_memory.py:257` UI source not found), no FAILED or ERROR line,
no `process(es) behind` line, summary `4596 passed, 3 skipped in 92.77s (0:01:32)`, `exit 0` —
identical to the reviewer's dry-tree reading of `4596 passed, 3 skipped`.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1139', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1219', 'R-1220', 'R-1225', 'R-1230',
'R-1235', 'R-1236', 'R-1240', 'R-1241', 'R-1246', 'R-1247', 'R-1248', 'R-1249', 'R-1250']` — the 18
ids in the required order, exit 0.

**Gate 6:** `git log --format=%s 4798211ed..HEAD` → the four subjects of C1 to C4, newest first,
exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4: the reviewer ran its five in its dry
tree). No full suite was run; `REMEDY_TEST_MAX_WORKERS` was never set. No two test commands ran at
once; each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 20-file digest pre-check (above)
additionally confirmed every prepared source's sha256 against the Bundle's stated values before
any copy:

1. `.remedy-wt/f297-r4/prep/block.md` → `.agent/authored/f297-r4.md`: 133 lines both, sha256
   `d16c9f9e116bdcf9b8acb13c41ea9d56682025bb3c31014759c4334e719804c4` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256
   `89a9d2246b27ffc0aa8675150a8bff7a3c732b9337ae479db9380b8447c7591e` both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256
   `dfb648323a4c22b81421c946fee94b4244fc55aed9784a256deafcbfa8daa455` both.
4. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256
   `12d7b808801494ceb026b2a8a5be9a873197c66d22fc7bb8b7b89292d2899ad8` both.
5. `c2-repo_mission.py` → `packages/orchestration/repo_mission.py` (at C2): cmp equal, sha256
   `6e3178a6be7a4bfa2d3d3aead953e75fadbce111ae4528ce84bbd282c9873db5` both.
6. `c2-do_sequence.py` → `packages/orchestration/do_sequence.py` (at C2): cmp equal, sha256
   `4e9e0c65646458b53b0027adbdc546bfcde5fbb9eecf63d740e5ee4f22243800` both.
7. `dry-test_repo_mission.py` → `tests/orchestration/test_repo_mission.py`: cmp equal, sha256
   `76beb3762afa9d12bece8d9ae071b5dda183f1e9166767032dbfa529e19cdd26` both.
8. `dry-test_do_several_projects.py` → `tests/cli/test_do_several_projects.py`: cmp equal, sha256
   `ba9f8ab17d49bb44d5761d0682f50bb4b75337c74311ffe2f556d559f648bdf9` both.
9. `c3-do_sequence.py` → `packages/orchestration/do_sequence.py` (at C3): cmp equal, sha256
   `6c172ef514a53be717bdf477a74b90ba986754e5659662f04c34dedf90c3cb7e` both.
10. `dry-structure-ledger-v1.md` → `docs/system/structure-ledger-v1.md`: cmp equal, sha256
    `2528035cb1dfb0a873e4e7c87b9a6a719c975f64cc348c98239c2e8b419cd785` both.
11. `dry-test_structure_ratchet.py` → `tests/test_structure_ratchet.py`: cmp equal, sha256
    `47336edff4dde8b27754d7651dfd93e78f3fa323ebab8991288eb9567d5e052d` both.
12. `dry-do_sequence.py` → `packages/orchestration/do_sequence.py` (at C4): cmp equal, sha256
    `555738a86085a7d851f6ce997b80e5a82f6c86ed0e76d9b2d454473368e0a0a5` both.
13. `dry-repo_mission.py` → `packages/orchestration/repo_mission.py` (at C4): cmp equal, sha256
    `10ab774436e153827d05cf68d62d6c531a1f64b0b8ceaee158634496452a172f` both.
14. `dry-test_order_shape_repair.py` → `tests/orchestration/test_order_shape_repair.py`: cmp
    equal, sha256 `780dea282c2da3d9ee9cc0f46c37cae8bd888c2c985ef6bbf9763bdb2beabbe6` both.
15. `dry-test_do_sequence_order_digest.py` → `tests/orchestration/test_do_sequence_order_digest.py`:
    cmp equal, sha256 `4398d0e2533aac3982cb338373dc82d33116fe6ea59e80b9a92c16782387b1cf` both.

The two `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`) were listed in the
Bundle and digest-checked (both `True`), but C1 orders copying the three whole `dry-*.md` files,
which already carry that content baked in; the `append-*.txt` files were not applied separately,
and nothing in the block calls for that (same note as F297's prior rounds' handbacks).

## Deviations & assumptions

1. **Shell shape.** Most read-only checks this round (`git status`, `git branch --show-current`,
   `git add`, `git diff --cached`, `git commit`, `git log`, `wc -l`, `sha256sum`, the ruff
   invocation, `integrity check`, the gate-3 script invocation) were run as
   `cd /home/decodeux/Repos/remedy && <one command>` rather than `git -C ... <command>` as the
   top-level task instructions prefer; none were refused by the sandbox. All copy/hash steps
   needing more than one operation used the mandated python3 scripts under
   `.remedy-wt/f297-r4-worker/`. (Same note as F297's prior rounds' handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r4/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during
the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 4's verdict and the resolutions of R-1250 and R-1247 in the next round's first
   commit.
5. T015: R-1236.

Operator questions open: 0.
Open findings: 18, all owned by F297 except R-1248, owned by F305.

## For the operator, in plain sentences

This round first wrote last time's results permanently into the project's record. It then made
two repairs. When an order asks several repositories to do the same thing at once, the system now
checks that every one of them is free to take it before committing any of them, so a repository
that cannot take the order never leaves a partial trace in the others. It also fixed how a failed
planning attempt is recorded: when a plan cannot be understood, the piece of work it would have
run is now marked as stopped instead of being left waiting, and when a step fails partway through,
the pieces of work it already created are fully removed from the project's record rather than
lingering as if they might still run. Along the way, a part of the planning logic that had grown
too large was given a documented boundary and its first internal split, with no change in what it
does. Every one of these repairs is backed by a test that fails without it and passes with it.
This round's own results will be written permanently into the record at the start of next time's
work, which will then take on one more item from the remaining list. Nothing is waiting on you
right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 3, resolutions of R-1237/R-1239/R-1238, DECISION F297 D5; numstat matched exactly |
| C2 | done | T014 (R-1250) landed; numstat and diff content matched exactly |
| C3 | done | structural step: `plan_order_job`'s boundary written and step (1) taken; numstat and diff content matched exactly |
| C4 | done | T013 (R-1247) landed; numstat and diff content matched exactly |
| C5 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `4596 passed, 3 skipped`, exit 0, identical to the dry tree |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 18 ids, exact order |
| Gate 6 | passed | four subjects, newest first |
| T013 (R-1247) | done | a failed shape step leaves no stopped job linked to any mission's chain; a plan that cannot be parsed leaves its job stopped, not pending |
| T014 (R-1250) | done | an order over several repositories is accepted by none of their missions unless every one can take it |
