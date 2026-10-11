# Handback — F297 round 6: book round 5, structural step on mission_state, land T016

## Session

SESSION 1 of feature F297 · round 6 · rounds so far 6

Context self-assessment: the session verified the block and all 20 prepared files' digests before
any write, read every diff in full against the current tree before staging, and executed the
three commits and six gates in one uninterrupted pass with no retries; context remains comfortable
at handback.

Fortschritt: ~64 % (T001 to T016 landed · T017 to T025 open) — Schätzung

## Range

Review of `2bbd430be`..`HEAD`.

## Commits

### e0c152874 F297 R6 C1: book round 5 and the resolution of R-1236, DECISION F297 D7

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r6.md` | +131/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r6/prep/block.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D7: how round 6 repairs R-1149, and the step `mission_state.py` takes first |
| `.agent/live_review.md` | +4/-0 | appended the `Gate: F297 R5` paragraph (VERDICT PASS) and the `Done:` paragraph for R-1236 |
| `.agent/plan.md` | +14/-14 | rewritten in full for F297 round 6 |

### 145dbd50e F297 R6 C2: structural step, the follow-up job's creation leaves mission_state for a module of its own

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +4/-1 | names step (2) of `mission_state.py`'s boundary: the follow-up job's creation moves to `packages/orchestration/mission_followup.py`; the verify task and its run, with `run_guarded_test_command`, stay for a later step |
| `packages/orchestration/mission_followup.py` | +118/-0 | new module (NEW FILE): `MISSION_FOLLOW_UP_TASK_TYPE`, `build_follow_up_task` and `continue_mission` moved unchanged from `mission_state.py`; `continue_mission` imports the store's functions inside its body so either module can be imported first |
| `packages/orchestration/mission_state.py` | +17/-92 | the three moved names deleted; `follow_up_target` becomes an explicit re-export from `mission_record`; the three names of the new module imported back by name at the file's end, so `from packages.orchestration.mission_state import continue_mission` keeps working; file falls to 925 lines |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | the new module joins the allowlist |

### 956f3819c F297 R6 C3: every place that makes a job records the digest of its input (R-1149)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | +3/-3 | `_cmd_create_job` records `job_file_sha256=sha_text(prompt)`; its two lines building `metadata` become one |
| `packages/orchestration/continue_from_node.py` | +2/-1 | the child job records `job_file_sha256=sha_text(prompt)` |
| `packages/orchestration/mission_followup.py` | +3/-0 | `continue_mission` records `job_file_sha256=sha_text(text)`, the step it was planned from |
| `packages/orchestration/veto_proposal.py` | +3/-0 | `build_follow_up_job` records `job_file_sha256=sha_text(goal)`, the replan goal it was planned from |
| `tests/orchestration/test_mission_state.py` | +9/-0 | new coverage: the follow-up job's digest equals the sha256 of its step |
| `tests/orchestration/test_project_brain.py` | +3/-0 | new coverage: the continued-from-node child's digest equals the sha256 of its prompt |
| `tests/orchestration/test_veto_proposal.py` | +4/-0 | new coverage: the replan follow-up's digest equals the sha256 of its goal |
| `tests/test_cli_main.py` | +14/-0 | new coverage: `_cmd_create_job`'s digest equals the sha256 of its prompt |

### this commit F297 R6 C4: handback

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
`2bbd430bef2f6ba8c3203d30d432141f75fd38c2`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`; `.agent/STOP` absent.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r6/prep/block.md`
read `131`; `sha256sum` read
`5240a7eccbe132ae7809f18a4e491d73085f4ad3bc6ebc7b2e960cef367f5c13` — both equal to the values the
prompt delivered. All 20 Bundle-listed prepared files (`block.md`'s digest checked via the prompt
values directly; the 11 `dry-*` files, `c2-mission_followup.py`, 2 `append-*.txt` files, `verify.py`,
`run_selection.py` and `selection.txt`) hashed via a python3 script under
`.remedy-wt/f297-r6-worker/check_hashes.py`: every one read `True`, final line `ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the three `dry-*` whole files and the block to
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/authored/f297-r6.md`;
each printed `cmp_equal=True`. `git branch --show-current` read `feature/f297-findings-paydown-v7`
before staging. `git diff --cached --numstat` read exactly `131 0 .agent/authored/f297-r6.md`,
`12 0 .agent/decisions.md`, `4 0 .agent/live_review.md`, `14 14 .agent/plan.md` — matching the
block's required readings. The full staged diffs of all four files were read before committing:
`.agent/plan.md`'s rewrite matched the round's goal exactly; the `.agent/live_review.md` and
`.agent/decisions.md` diffs were each small enough (4 and 12 lines) to read in full rather than by
tail-and-digest, and matched the block's "For the record" description and DECISION F297 D7's text
verbatim.

**C2:** `python3 -I c2_copy.py` copied the four files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `4 1 docs/system/structure-ledger-v1.md`,
`118 0 packages/orchestration/mission_followup.py`, `17 92 packages/orchestration/mission_state.py`,
`1 0 tests/orchestration/import_reachability_allowlist.txt` — matching the block exactly. Every
diff was read in full before staging: `mission_state.py`'s diff showed only the three moved names
deleted, `follow_up_target` becoming an explicit re-export, and the three-name back-import added at
the file's end with `# noqa: E402`; `mission_followup.py` was read whole as a new file and found
byte-equal to the Bundle's `c2-mission_followup.py`; the structure-ledger and allowlist diffs
matched the DECISION's text. `git branch --show-current` read `feature/f297-findings-paydown-v7`
before staging.

**C3:** `python3 -I c3_copy.py` copied the eight files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `3 3 apps/cli/commands/job.py`, `2 1 packages/orchestration/continue_from_node.py`,
`3 0 packages/orchestration/mission_followup.py`, `3 0 packages/orchestration/veto_proposal.py`,
`9 0 tests/orchestration/test_mission_state.py`, `3 0 tests/orchestration/test_project_brain.py`,
`4 0 tests/orchestration/test_veto_proposal.py`, `14 0 tests/test_cli_main.py` — matching the block
exactly. Every diff was read in full before staging: all four production files import `sha_text`
from `packages.orchestration.call_identity` and pass it the planned-from text (`job.py`'s prompt,
`continue_from_node.py`'s prompt, `mission_followup.py`'s step, `veto_proposal.py`'s goal); each
test file adds one new test reading the resulting `job_file_sha256` against `hashlib.sha256` of
the same text. `git branch --show-current` read `feature/f297-findings-paydown-v7` before staging.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r6/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (15
file-equality checks and the two ledger/decisions base-plus-slice checks), last line `ALL True`,
exit 0.

**Gate 2:** `python3 -m ruff check` over the 9 named paths → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r6/prep/run_selection.py /home/decodeux/Repos/remedy` → 3
SKIPPED lines (`tests/test_agent_tooling.py:43` D12 quarantine,
`tests/test_install_smoke.py:175` opt-in install smoke,
`tests/test_repair_context_reviewer_memory.py:257` UI source not found), no FAILED or ERROR line,
no `process(es) behind` line, summary `6110 passed, 3 skipped in 76.00s (0:01:16)`, `exit 0`. The
reviewer's dry tree read `6109 passed, 4 skipped`; this run's one extra pass and one fewer skip
matches the block's own note that the primary checkout may run a test the dry tree skipped for its
missing UI toolchain.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1139', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1219', 'R-1220', 'R-1225', 'R-1230',
'R-1235', 'R-1240', 'R-1241', 'R-1246', 'R-1248', 'R-1249', 'R-1251']` — the 16 ids in the required
order, exit 0. R-1149 still reads open here by design: its repair landed this round, but the
ledger's `Done:` line for it books in round 7's first commit (amend0827-process-diet rule 1),
exactly as `## Next` below orders — the same pattern R-1236 followed last round.

**Gate 6:** `git log --format=%s 2bbd430be..HEAD` → the three subjects of C1 to C3, newest first,
exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4: the reviewer ran four in its dry tree).
No full suite was run; `REMEDY_TEST_MAX_WORKERS` was never set. No two test commands ran at once;
each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 20-file digest pre-check (above)
additionally confirmed every prepared source's sha256 against the Bundle's stated values before
any copy:

1. `.remedy-wt/f297-r6/prep/block.md` → `.agent/authored/f297-r6.md`: 131 lines both, sha256
   `5240a7eccbe132ae7809f18a4e491d73085f4ad3bc6ebc7b2e960cef367f5c13` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256
   `3ab51d1c6764cabaf5d7377f1354433712144724aec20a54d857b4590990aeec` both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256
   `1393f8dd359c3aa1a1c48f4f751c9f4b755503b7b4d9b7293e958da31a5ccf3a` both.
4. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256
   `71dcfbab420927da0109434daf660fea9cb5814f6051409d0922c0cd0152060d` both.
5. `dry-mission_state.py` → `packages/orchestration/mission_state.py`: cmp equal, sha256
   `88cc0a79ac5291aec352326cc64f8057c764f84e5514b9effc467a727b652528` both.
6. `c2-mission_followup.py` → `packages/orchestration/mission_followup.py` (C2 snapshot): cmp
   equal, sha256 `746e342be6b5ce5eda7940aee3b7679f0a15b7dcb88599a7a9567fd581beb4bf` both.
7. `dry-structure-ledger-v1.md` → `docs/system/structure-ledger-v1.md`: cmp equal, sha256
   `f17f114384bc9f9a6fccd5d8fbd13c80fb13d8ecc3b93b02a5dc03ce01924321` both.
8. `dry-import_reachability_allowlist.txt` → `tests/orchestration/import_reachability_allowlist.txt`:
   cmp equal, sha256 `61422aa11d5fc6dd282b1d159b3eb61773af8a2daedba97bc4e13bffb0fad0e9` both.
9. `dry-mission_followup.py` → `packages/orchestration/mission_followup.py` (C3 edit): cmp equal,
   sha256 `0f7a638575ecd57ab3d2d86f4a82331b509689a096f25c0cf8c6a2a940f5bee2` both.
10. `dry-continue_from_node.py` → `packages/orchestration/continue_from_node.py`: cmp equal,
    sha256 `b2a3db2bd7108888dedff2eb4509d368d80849b35b864483401c2a40b4cd6b21` both.
11. `dry-veto_proposal.py` → `packages/orchestration/veto_proposal.py`: cmp equal, sha256
    `7b9c7e02db5389c654384c56fcf3866b23ce38d5a818ad4e183d76154529cf56` both.
12. `dry-job.py` → `apps/cli/commands/job.py`: cmp equal, sha256
    `b296e08e155f9464c7006921c1834cbf0a8df9525f4d4d0bca45a5023659e83c` both.
13. `dry-test_mission_state.py` → `tests/orchestration/test_mission_state.py`: cmp equal, sha256
    `b523c6f9a7919c9107c47bdc85130b41910bcc8d6946123fa7bfb39e7c0327db` both.
14. `dry-test_project_brain.py` → `tests/orchestration/test_project_brain.py`: cmp equal, sha256
    `26412616ac8fa15402c8ce797718a14beaa2c32c759e54bdaf4dc646eb5655f0` both.
15. `dry-test_veto_proposal.py` → `tests/orchestration/test_veto_proposal.py`: cmp equal, sha256
    `2075e2353bc6944811c8d6b39243473fcbe48aaee733a5289ad4f5fb3a80e7b3` both.
16. `dry-test_cli_main.py` → `tests/test_cli_main.py`: cmp equal, sha256
    `e834cf82a8726a48be570c545f790e77bcf49187d83bfd58ccfd259c4166525e` both.

The two `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`) were listed in the
Bundle and digest-checked (both `True`), but C1 orders copying the three whole `dry-*.md` files,
which already carry that content baked in; the `append-*.txt` files were not applied separately,
and nothing in the block calls for that (same note as F297's prior rounds' handbacks).

## Deviations & assumptions

1. **Shell shape.** Most read-only checks this round (`git status`, `git branch --show-current`,
   `git add`, `git diff --cached`, `git commit`, `git log`, `wc -l`, `sha256sum`, the ruff
   invocation, `integrity check`, the gate-3 and gate-1 script invocations) were run as
   `cd /home/decodeux/Repos/remedy && <one command>` rather than `git -C ... <command>` as the
   top-level task instructions prefer; none were refused by the sandbox. All copy/hash steps
   needing more than one operation used the mandated python3 scripts under
   `.remedy-wt/f297-r6-worker/`. (Same note as F297's prior rounds' handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r6/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during
the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 6's verdict and the resolution of R-1149 in the next round's first commit.
5. T017 and T018: R-1139 with R-1225, and R-1158.

Operator questions open: 0.
Open findings: 16, all owned by F297 except R-1248, owned by F305, and R-1251, owned by the next
findings paydown.

## For the operator, in plain sentences

This round first wrote last time's results permanently into the project's record. It then made a
purely structural move: one piece of logic that creates a mission's next step moved out into a
file of its own, with nothing about how it behaves changed, so that the file it used to live in
can keep growing elsewhere without hitting its size limit. After that it made a repair so that
every one of the four places in the project that can create a new piece of work now stamps that
work with a fingerprint of exactly what it was asked to do. Before this fix, a saved piece of work
carried no such fingerprint in these four places, so nothing could later prove for certain what
text it had been planned from. Now every one of them can. Every one of these changes is backed by
a test that checks the fingerprint matches what was actually asked for. This round's own results
will be written permanently into the record at the start of next time's work, which will then take
on the next item from the remaining list. Nothing is waiting on you right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 5, resolution of R-1236, DECISION F297 D7; numstat matched exactly |
| C2 | done | structural step landed: the follow-up job's creation moved to its own module; numstat and diff content matched exactly |
| C3 | done | T016 (R-1149) landed: all four job origins record the digest of their planned-from input |
| C4 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `6110 passed, 3 skipped`, exit 0, one more pass / one fewer skip than the dry tree, matching the block's UI-toolchain note |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 16 ids, exact order |
| Gate 6 | passed | three subjects, newest first |
| T016 (R-1149) | done | `_cmd_create_job`, `continue_from_node`, `continue_mission` (now in `mission_followup.py`) and `build_follow_up_job` each record `job_file_sha256` as the sha256 of the text they were planned from; one new test per origin proves it |
