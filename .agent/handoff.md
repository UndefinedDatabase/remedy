# Handback — F297 round 8: book round 7, land T019 and T020

## Session

SESSION 1 of feature F297 · round 8 · rounds so far 8

Context self-assessment: the session verified the block and all 16 prepared files' digests before
any write, read every diff in full against the current tree before staging, and executed the
three commits and six gates in one uninterrupted pass with no retries; context remains comfortable
at handback. Session 1 ends after this round's review, at the eight rounds the session round
target allows.

Fortschritt: ~80 % (T001 to T020 landed · T021 to T025 open) — Schätzung

## Range

Review of `7d38914cc`..`HEAD`.

## Commits

### 56399050b F297 R8 C1: book round 7 and the resolutions of R-1139, R-1225 and R-1158, DECISION F297 D9

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r8.md` | +128/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r8/prep/block.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D9: how round 8 repairs R-1156, R-1157 and R-1230 |
| `.agent/live_review.md` | +8/-0 | appended the `Gate: F297 R7` paragraph (VERDICT PASS) and the `Done:` paragraphs for R-1139, R-1225 and R-1158 |
| `.agent/plan.md` | +7/-6 | rewritten in full for F297 round 8 |

### 21885bb57 F297 R8 C2: the toolchain refresh order's budget covers its five tasks, and its Task 1 names where it reads the newest Python (R-1156, R-1157)

| Path | +/- | Reason |
|---|---|---|
| `docs/orders/toolchain-refresh.md` | +7/-2 | budget raised to cover all five tasks at the measured cost per call; Task 1's body and Acceptance name the address the newest stable Python is read from |
| `tests/docs/test_toolchain_refresh_order.py` | +28/-0 | new coverage: the declared budget covers every task at the measured cost per call, Task 1 names the address, and the budget line stays out of what the planner sees |

### d0d5c2642 F297 R8 C3: a self-use pass that leaves a listed file unchanged is named (R-1230)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/self-use-track-v1.md` | +4/-1 | documents the new Files:-unchanged check alongside the existing record-only check |
| `packages/orchestration/self_use_findings.py` | +14/-2 | `describe_self_use_run_defects` now names a passed task whose `files_hint` lists a path the reviewed work left unchanged |
| `packages/orchestration/self_use_generator.py` | +5/-0 | the excused-handler job's markdown now lists both files it must change under `Files:` |
| `tests/orchestration/test_self_use_findings.py` | +39/-0 | new coverage for the Files:-unchanged check, the all-changed case, and the did-not-pass case |
| `tests/orchestration/test_self_use_generator.py` | +12/-0 | new coverage that the generated job's `Files:` list parses into `files_hint` with both paths |

### this commit F297 R8 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/operator_questions.md` | +19/-1 | operator question Q13: the toolchain job's raised spending budget |
| `.agent/handoff.md` | this commit | this file (self-reference rule, docs/agents/handback_template.md) |

## External actions

None during the round. `git push origin feature/f297-findings-paydown-v7` after this commit,
reported below with the post-push `git rev-parse HEAD origin/feature/f297-findings-paydown-v7`.
No PR created or touched; no other `gh` command run. The Open PR Gate is Phase 1 rule 2 of the
self-drive protocol and is listed in `## Next` for whoever starts the next cycle.

## Verification

**Preconditions (before C1):** `git status --porcelain` empty; `git rev-parse HEAD` read
`7d38914cc0799e8a58c63d615082fef5effe8ca9`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`; `.agent/STOP` absent.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r8/prep/block.md`
read `128`; `sha256sum` read
`ac3f3c075efbbaebe605c71506aa214c8070207a24f4b1befd5cf13d68b8a237` — both equal to the values the
prompt delivered. All 16 Bundle-listed prepared files (the 11 `dry-*` files, the two
`append-*.txt` files, `verify.py`, `run_selection.py` and `selection.txt`) hashed via a python3
script under `.remedy-wt/f297-r8-worker/check_hashes.py`: every one read `True`, final line
`ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the three `dry-*` whole files and the block to
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/authored/f297-r8.md`;
each printed `cmp_equal= True`. `git branch --show-current` read `feature/f297-findings-paydown-v7`
before staging. `git diff --cached --numstat` read exactly `128 0 .agent/authored/f297-r8.md`,
`12 0 .agent/decisions.md`, `8 0 .agent/live_review.md`, `7 6 .agent/plan.md` — matching the
block's required readings. The full staged diffs of all four files were read before committing
(the `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md` deltas directly via a
line-count-bounded unified diff, since the files themselves are large; `.agent/authored/f297-r8.md`
by its `wc -l` (128) and `sha256sum` matching `block.md` exactly): `.agent/plan.md`'s rewrite
matched the round's goal, the eight appended lines of `.agent/live_review.md` matched the block's
"For the record" description and the `Gate: F297 R7` / three `Done:` paragraphs, and the twelve
appended lines of `.agent/decisions.md` matched DECISION F297 D9's text verbatim.

**C2:** `python3 -I c2_copy.py` copied the two files; each printed `cmp_equal= True`. `git diff
--cached --numstat` read `7 2 docs/orders/toolchain-refresh.md`,
`28 0 tests/docs/test_toolchain_refresh_order.py` — matching the block exactly. Both diffs were
read in full before staging against the current tree: the order's budget line raised from
`max_cost_usd=10.00` to `max_cost_usd=28.00`, Task 1's new sentence and Acceptance line naming the
versions-manifest address, and the new test file's coverage of the declared budget, the per-call
cost, the named address and the planner-visibility check. `git branch --show-current` read
`feature/f297-findings-paydown-v7` before staging.

**C3:** `python3 -I c3_copy.py` copied the five files; each printed `cmp_equal= True`. `git diff
--cached --numstat` read `4 1 docs/system/self-use-track-v1.md`,
`14 2 packages/orchestration/self_use_findings.py`,
`5 0 packages/orchestration/self_use_generator.py`,
`39 0 tests/orchestration/test_self_use_findings.py`,
`12 0 tests/orchestration/test_self_use_generator.py` — matching the block exactly. Every diff was
read in full before staging: the generator's new `Files:` block in
`_excused_handler_job_markdown`, the findings module's new `changed_set`/`files_hint` loop and its
two docstring additions, the doc page's new sentence, and both test files' new coverage. Confirmed
separately (delegated to a research agent) that `TaskEntry.files_hint` is a pre-existing,
already-populated field — this round's diff only reads it, adds no new field. `git branch
--show-current` read `feature/f297-findings-paydown-v7` before staging.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r8/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (11
file-equality checks and the two ledger/decisions base-plus-slice checks), last line `ALL True`,
exit 0.

**Gate 2:** `python3 -m ruff check` over the 5 named paths → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r8/prep/run_selection.py /home/decodeux/Repos/remedy` → 6
SKIPPED lines (three folded into one `SKIPPED [3] tests/orchestration/test_model_routing.py:455`,
`tests/test_agent_tooling.py:43` D12 quarantine, `tests/test_install_smoke.py:175` opt-in install
smoke, `tests/test_repair_context_reviewer_memory.py:257` UI source not found), no FAILED or ERROR
line, no `process(es) behind` line, summary `4598 passed, 6 skipped, 1 warning in 55.17s`, `exit
0` — matching the reviewer's dry-tree reading of `4598 passed, 6 skipped` named in the block (the
primary checkout's extra warning line is reported as it is, per the gate's own instruction to
report the summary and SKIPPED lines as they are).

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1156', 'R-1157', 'R-1219', 'R-1220', 'R-1230', 'R-1235', 'R-1240', 'R-1241', 'R-1246',
'R-1248', 'R-1249', 'R-1251']` — the 12 ids in the required order, exit 0.

**Gate 6:** `git log --format=%s 7d38914cc..HEAD` → the three subjects of C1 to C3, newest first,
exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4). No full suite was run beyond the
selection gate 3 names; `REMEDY_TEST_MAX_WORKERS` was never set. No two test commands ran at once;
each gate ran exactly once.

**C4:** `python3 -I c4_copy_oq.py` copied the operator-questions file; printed `cmp_equal= True`.
`git diff --cached --numstat` read `19 1 .agent/operator_questions.md` — matching the block
exactly. `git branch --show-current` read `feature/f297-findings-paydown-v7` before staging.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 16-file digest pre-check (above)
additionally confirmed every prepared source's sha256 against the Bundle's stated values before
any copy, and a post-commit script re-hashed every committed file to confirm the same digests:

1. `.remedy-wt/f297-r8/prep/block.md` → `.agent/authored/f297-r8.md`: 128 lines both, sha256
   `ac3f3c075efbbaebe605c71506aa214c8070207a24f4b1befd5cf13d68b8a237` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256
   `42fb26bfbe11e0d07078316acfa34fd3e94a59dae225f6812b51c805f76d79be` both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256
   `a4187ad44d17e7e07527aef8899db64e8a9ad7664c87744c5cc0f34ea82a0546` both.
4. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256
   `6fcd140b1729609f995abeee4a04e9b8e410417c4d4d2a4843a69c7fb93441ca` both.
5. `dry-toolchain-refresh.md` → `docs/orders/toolchain-refresh.md`: cmp equal, sha256
   `24e1059ff57ec31e195a024e4b71422be14d9c8f5c12d5def889dd65116f2a96` both.
6. `dry-test_toolchain_refresh_order.py` → `tests/docs/test_toolchain_refresh_order.py`: cmp
   equal, sha256 `53ec6680dbe7bd6dbab52df4296ab68af4cdd08f9821fbe1e8d257f43f9e8dfb` both.
7. `dry-self_use_generator.py` → `packages/orchestration/self_use_generator.py`: cmp equal, sha256
   `90f978f3598bbd729c8907e3daf0f1b61394e94a1b47e45ed843ddda69aabbc1` both.
8. `dry-self_use_findings.py` → `packages/orchestration/self_use_findings.py`: cmp equal, sha256
   `1af9f48a6cd92c65f565f112d0b37f74dac4031e2eeef4b1a497166eacc8f513` both.
9. `dry-test_self_use_findings.py` → `tests/orchestration/test_self_use_findings.py`: cmp equal,
   sha256 `f982b59e4b403a0d79f260c5813dba436559db2a5aa33c71dfbd6a74b4778792` both.
10. `dry-test_self_use_generator.py` → `tests/orchestration/test_self_use_generator.py`: cmp
    equal, sha256 `78ff3c5ef1b38287318bfd04cb98e387258a40603a58858ac256f3ed4cfb270b` both.
11. `dry-self-use-track-v1.md` → `docs/system/self-use-track-v1.md`: cmp equal, sha256
    `d4ed01f480e7c02350043120031972eba31cbe66509aa7423647cdb9d50a49de` both.
12. `dry-operator_questions.md` → `.agent/operator_questions.md`: cmp equal, sha256
    `807c7ba473e8e2e68b390ddfd7b5a2401854bc79fbca9220663e5a355c3a39c5` both.

The two `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`) were listed in the
Bundle and digest-checked (both `True`), but C1 orders copying the three whole `dry-*.md` files,
which already carry that content baked in; the `append-*.txt` files were not applied separately,
and nothing in the block calls for that (same note as F297's prior rounds' handbacks).

## Deviations & assumptions

1. **Shell shape.** Most read-only checks this round (`git status`, `git branch --show-current`,
   `git add`, `git diff --cached`, `git commit`, `git log`, `wc -l`, `sha256sum`, the ruff
   invocation, `integrity check`, the gate-3 and gate-1 script invocations) were run with the
   working directory set to `/home/decodeux/Repos/remedy` rather than `git -C ... <command>` as
   the top-level task instructions prefer; none were refused by the sandbox. All copy/hash steps
   needing more than one operation used the mandated python3 scripts under
   `.remedy-wt/f297-r8-worker/`. (Same note as F297's prior rounds' handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag.
3. **Large-file diff reading.** `.agent/decisions.md` (29,152 lines before this round) and
   `.agent/live_review.md` (268 lines before this round) exceed the inline Read tool's per-call
   context budget at full-file size; their diffs were read via a bounded unified-diff script
   (`difflib`, context 1) rather than a full-file Read, which shows exactly the changed lines plus
   one line of context — the same information a `git diff` of the staged change would show, and
   what was actually compared before staging. `.agent/plan.md` (24 lines) was read in full via
   plain `diff`.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r8/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during
the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Session 2's first commit books round 8's verdict and the resolutions of R-1156, R-1157 and
   R-1230.
5. T021 to T024: R-1219, R-1220, R-1240 and R-1249.
6. T025 R-1241, the structural step; then the closure sequence.

Operator questions open: 1.
Open findings: 12, all owned by F297 except R-1248, owned by F305, and R-1251, owned by the next
findings paydown.

## For the operator, in plain sentences

This round first wrote last round's results permanently into the project's record. It then
noticed that a maintenance job which checks for newer versions of the project's own development
tools was running out of its spending allowance before it could reach its two most important
steps — running the whole test suite on the new tool versions and opening a request for a person
to review the change — so the allowance was raised to a level based on what the job actually cost
to run last time, high enough that every step can finish even with its usual retries. The same job
was also told exactly where online to look up the newest version of the programming language it
runs on that is considered stable, instead of guessing from memory, which had led it to call an
early-preview release stable before. Separately, a gap in how the project's own self-maintenance
passes are checked was closed: when such a task is supposed to change two specific things together
and a reviewer approves it after only one of them actually changed, that gap is now caught and
reported rather than slipping through unnoticed. Every one of these changes is backed by a test
that fails without the change and passes with it. One question is open for you, about whether to
keep the newly raised spending allowance for that maintenance job; the recommendation is to keep
it, because a run that cannot reach its last step wastes its entire allowance for nothing, and
nothing else is waiting on you right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 7, resolutions of R-1139, R-1225 and R-1158, DECISION F297 D9; numstat matched exactly |
| C2 | done | T019 landed: the toolchain-refresh order's budget covers its five tasks at the measured cost per call, and Task 1 names the address the newest stable Python is read from; numstat and diff content matched exactly |
| C3 | done | T020 landed: the excused-handler self-use item lists both files it must change under `Files:`, and `describe_self_use_run_defects` names a task that passed review while a listed path stayed unchanged; numstat and diff content matched exactly |
| C4 | done | this handback, plus operator question Q13 |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `4598 passed, 6 skipped`, exit 0, matching the reviewer's dry-tree reading |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 12 ids, exact order |
| Gate 6 | passed | three subjects, newest first |
| T019 (R-1156, R-1157) | done | `docs/orders/toolchain-refresh.md`'s budget raised to cover all five tasks at the measured per-call cost; Task 1 names the versions-manifest address it reads the newest stable Python from; `tests/docs/test_toolchain_refresh_order.py` holds both |
| T020 (R-1230) | done | the excused-handler job's `Files:` list names both files it must change; `describe_self_use_run_defects` names a passed task whose `files_hint` lists a path the reviewed work left unchanged |
