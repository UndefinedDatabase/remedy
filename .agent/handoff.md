# Handback — F297 round 3: book round 2, land T010 to T012

## Session

SESSION 1 of feature F297 · round 3 · rounds so far 3

Context self-assessment: the session read the full bundle once, verified every prepared file's
digest before use, and executed the four commits in one uninterrupted pass with no retries;
context remains comfortable at handback.

Fortschritt: ~45 % (T001 to T012 landed · T013 to T025 open) — Schätzung

## Range

Review of `60e2e51e6`..`HEAD`.

## Commits

### feddd9af3 F297 R3 C1: book round 2 and the resolutions of R-1143, R-1176, R-1196, R-1138 and R-1162, DECISION F297 D4

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r3.md` | +144/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r3/prep/block.md` |
| `.agent/live_review.md` | +12/-0 | appended the `Gate: F297 R2` paragraph (VERDICT PASS) and the `Done:` paragraphs for R-1143, R-1176, R-1196, R-1138, R-1162 |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D4: how round 3 repairs R-1237, R-1239 and R-1238 |
| `.agent/prose_slips.md` | +2/-0 | two dated lines for F297's round 2 |
| `.agent/plan.md` | +7/-7 | rewritten in full for F297 round 3 |

### fb91599aa F297 R3 C2: an upkeep job carries the project's open findings, whichever mission left them (R-1237)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_upkeep.py` | +8/-7 | `open_findings` drops its `mission_id` parameter and reads every `job_closed` line of the project's ledger once each, keeping each finding's own line `mission_id`; `plan_upkeep` and `upkeep_preview` call it with no mission filter (R-1237) |
| `tests/orchestration/test_mission_upkeep.py` | +11/-7 | the mission-scoped assertions are replaced with project-wide ones that also check the kept `mission_id` |
| `docs/system/mission-upkeep-v1.md` | +2/-2 | "What an upkeep job carries" rule 1 now names the project's jobs, whichever mission ran them |

### 428fd9428 F297 R3 C3: the findings an upkeep job carries and its structure limits are settings (R-1239)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config_keys_mission.py` | +30/-0 | three new `ConfigKeySpec` entries: `mission.upkeep_max_findings` (5), `mission.upkeep_function_lines` (100), `mission.upkeep_file_lines` (1000) (R-1239) |
| `packages/orchestration/mission_upkeep.py` | +33/-15 | `UPKEEP_MAX_FINDINGS` constant replaced by three keyed settings read through a shared `_whole_number_setting` helper; `_structure_item` takes `function_limit`/`file_limit`; `plan_upkeep` takes `config` and reads all three settings |
| `tests/orchestration/test_mission_upkeep.py` | +38/-0 | new coverage: the three settings are registered with today's values as defaults, the plan reads them, and a bad value is refused |
| `docs/guides/environment.md` | +3/-0 | three new rows for `REMEDY_MISSION_UPKEEP_MAX_FINDINGS`, `REMEDY_MISSION_UPKEEP_FUNCTION_LINES`, `REMEDY_MISSION_UPKEEP_FILE_LINES` |
| `docs/system/mission-upkeep-v1.md` | +6/-3 | rules 1 and 2 name the three settings and their unset values; a sentence states each is a whole number of at least 1 or refused |

### 02c382007 F297 R3 C4: a step an upkeep job was made in place of is named in the answer, the ledger and the digest (R-1238)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_upkeep.py` | +25/-2 | `make_upkeep_job_if_due` takes `step` and records it as `deferred_step` on the planned line and the job metadata when given; new `upkeep_deferred_step` reads it back while the upkeep job is still the mission's latest job (R-1238) |
| `apps/cli/commands/mission_cmd.py` | +9/-3 | `_upkeep_before_continue` passes the step through; `_cmd_mission_continue` answers `step_deferred` and `deferred_step` under `--json`, and the text line names the deferred step |
| `packages/orchestration/orchestrator_dispatch.py` | +1/-1 | `dispatch_milestone_job` passes `payload["step"]` to `make_upkeep_job_if_due` |
| `packages/orchestration/client_digest.py` | +4/-2 | `_mission_entry` adds `upkeep_deferred_step` from the new reader |
| `apps/cli/client_interface.py` | +4/-2 | `CLIENT_INTERFACE_VERSION` rises to `1.10`; `upkeep_deferred_step` added to `DIGEST_KEY_TREE` |
| `docs/system/machine-client-contract-v1.md` | +4/-4 | interface version and the three generated key-tree listings regenerated for `upkeep_deferred_step` |
| `docs/system/mission-upkeep-v1.md` | +8/-5 | the command-line and digest sections name `deferred_step`/`step_deferred`/`upkeep_deferred_step` |
| `tests/orchestration/test_mission_upkeep.py` | +19/-0 | new coverage: the deferred step reads back until a later job links, and defers none when no step is given |
| `tests/cli/test_mission_cmd.py` | +7/-0 | new coverage: the `--json` answer, the printed text line, and the digest seen through `status --json` |
| `tests/cli/test_status_cmd.py` | +1/-0 | the digest test now also asserts `upkeep_deferred_step == ""` when none is due |
| `tests/cli/test_client_interface.py` | +1/-1 | the interface-version assertion now reads `1.10` |
| `tests/orchestration/test_orchestrator_dispatch.py` | +3/-1 | the dispatch-upkeep test now reads `deferred_step` off the planned ledger line |

### this commit F297 R3 C5: handback

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
`60e2e51e65a4fe50a3f41f75f29f4bf05cf8a2fc`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r3/prep/block.md`
read `144`; `sha256sum` read
`0b41848487c4bb7963a4a109a7d84fa0e7ec438ee0ee81377778344a7c96ae6e` — both equal to the values the
prompt delivered. All 31 Bundle-listed prepared files (`block.md`, 23 `dry-*` files, 3 `c2-*`/`c3-*`
files, 3 `append-*.txt` files, `verify.py`, `run_selection.py`, `selection.txt`) hashed via a
python3 script under `.remedy-wt/f297-r3-worker/check_hashes.py`: every one read `True`, final line
`ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the block and the four `dry-*` whole files to
`.agent/authored/f297-r3.md`, `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/prose_slips.md`, `.agent/plan.md`; each printed `cmp_equal=True`. `git branch
--show-current` read `feature/f297-findings-paydown-v7` before staging. `git diff --cached
--numstat` read exactly `144 0 .agent/authored/f297-r3.md`, `12 0 .agent/decisions.md`,
`12 0 .agent/live_review.md`, `7 7 .agent/plan.md`, `2 0 .agent/prose_slips.md` — matching the
block's required readings. The staged diff of all five files was read in full and matched the
block's "For the record" description and DECISION F297 D4's text exactly.

**C2:** `python3 -I c2_copy.py` copied the three files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `2 2 docs/system/mission-upkeep-v1.md`,
`8 7 packages/orchestration/mission_upkeep.py`,
`11 7 tests/orchestration/test_mission_upkeep.py` — matching the block exactly. The staged diff was
read in full: `open_findings` loses its `mission_id` parameter, reads every `job_closed` line
unfiltered, and keeps each finding's own `mission_id`; `plan_upkeep` and `upkeep_preview` call it
with no filter.

**C3:** `python3 -I c3_copy.py` copied the five files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `3 0 docs/guides/environment.md`,
`6 3 docs/system/mission-upkeep-v1.md`, `30 0 packages/orchestration/config_keys_mission.py`,
`33 15 packages/orchestration/mission_upkeep.py`,
`38 0 tests/orchestration/test_mission_upkeep.py` — matching the block exactly. The staged diff was
read in full: three new `ConfigKeySpec` entries; `UPKEEP_MAX_FINDINGS` replaced by three keyed
settings through a shared `_whole_number_setting` helper; `_structure_item` and `plan_upkeep` take
the new limits; `measure_repository`'s existing `function_limit`/`file_limit` keywords are reused
unchanged.

**C4:** `python3 -I c4_copy.py` copied the twelve files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `4 2 apps/cli/client_interface.py`,
`9 3 apps/cli/commands/mission_cmd.py`, `4 4 docs/system/machine-client-contract-v1.md`,
`8 5 docs/system/mission-upkeep-v1.md`, `4 2 packages/orchestration/client_digest.py`,
`25 2 packages/orchestration/mission_upkeep.py`,
`1 1 packages/orchestration/orchestrator_dispatch.py`,
`1 1 tests/cli/test_client_interface.py`, `7 0 tests/cli/test_mission_cmd.py`,
`1 0 tests/cli/test_status_cmd.py`, `19 0 tests/orchestration/test_mission_upkeep.py`,
`3 1 tests/orchestration/test_orchestrator_dispatch.py` — matching the block exactly. The staged
diff was read in full: `make_upkeep_job_if_due` takes `step` and records `deferred_step`;
`upkeep_deferred_step` reads it back while the upkeep job is still the mission's latest (confirmed
`Mission.latest_link()` is an existing method used elsewhere in the same file); the CLI, the
orchestrator's dispatch (confirmed `payload["step"]` is the same key the function already reads
two lines below), the client digest and the client interface (`1.10`) each thread it through; no
other line changed.

Every `git branch --show-current` run immediately before a commit (C1 through C4) read
`feature/f297-findings-paydown-v7`.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r3/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (19
file-equality checks and the three ledger/decisions/prose_slips base-plus-slice checks), last line
`ALL True`, exit 0.

**Gate 2:** `python3 -m ruff check` over the 11 named paths → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r3/prep/run_selection.py /home/decodeux/Repos/remedy` → 10
SKIPPED lines (`tests/regression/test_f293_acceptance.py:191`, six
`tests/regression/test_named_bugs.py` D3-quarantine lines at 295/312/321/383/392/399,
`tests/test_agent_tooling.py:43` D12 quarantine, `tests/test_repair_context_reviewer_memory.py:257`
UI source not found, `tests/test_install_smoke.py:175` opt-in install smoke), no FAILED or ERROR
line, no `process(es) behind` line, summary `5799 passed, 10 skipped in 107.50s (0:01:47)`,
`exit 0` — identical to the reviewer's dry-tree reading of `5799 passed, 10 skipped`.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1139', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1219', 'R-1220', 'R-1225', 'R-1230',
'R-1235', 'R-1236', 'R-1237', 'R-1238', 'R-1239', 'R-1240', 'R-1241', 'R-1246', 'R-1247', 'R-1248',
'R-1249', 'R-1250']` — the 21 ids in the required order, exit 0.

**Gate 6:** `git log --format=%s 60e2e51e6..HEAD` → the four subjects of C1 to C4, newest first,
exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4: the reviewer ran its eight in its dry
tree). No full suite was run; `REMEDY_TEST_MAX_WORKERS` was never set. No two test commands ran at
once; each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 31-file digest pre-check (above)
additionally confirmed every prepared source's sha256 against the Bundle's stated values before
any copy:

1. `.remedy-wt/f297-r3/prep/block.md` → `.agent/authored/f297-r3.md`: 144 lines both, sha256
   `0b41848487c4bb7963a4a109a7d84fa0e7ec438ee0ee81377778344a7c96ae6e` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256
   `a40577464f139767e31a13b774fbd3623975fd381eea4c58eb8b25513ad9b8c7` both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256
   `83f587c2ccf6f4eb68155a0c62ba2dd7500408f3aeb1e54ba818ecf06dc54a84` both.
4. `dry-prose_slips.md` → `.agent/prose_slips.md`: cmp equal, sha256
   `e8ce38926c3cdd6be3f752c2a8912fc02d829227fe21e92bb54ecc9471aca26d` both.
5. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256
   `f783a8ba249b74e3b7edbc3ff4bb7b7c38e253797ea7847aa296dd987ef1576d` both.
6. `c2-mission_upkeep.py` → `packages/orchestration/mission_upkeep.py` (at C2): cmp equal, sha256
   `5aeb9871735646b5b39e4cf85d3ef0bb8b70b44b2d4b07fb762b40c2b982568a` both.
7. `c2-test_mission_upkeep.py` → `tests/orchestration/test_mission_upkeep.py` (at C2): cmp equal,
   sha256 `4f56a1a1d40282960a51cc5a4f27f62134f03db3065624738fef523d157da624` both.
8. `c2-mission-upkeep-v1.md` → `docs/system/mission-upkeep-v1.md` (at C2): cmp equal, sha256
   `ff5b63cb803067c9c0de27a55a200034e5c74d4442dbf9e75136fd2a924bc77f` both.
9. `dry-config_keys_mission.py` → `packages/orchestration/config_keys_mission.py`: cmp equal,
   sha256 `e78dbfa916558f5130c59e0894080bbe7e6cc00ca92ebab1012f2fbeb0920d12` both.
10. `c3-mission_upkeep.py` → `packages/orchestration/mission_upkeep.py` (at C3): cmp equal, sha256
    `36dd4cfd8dca93216b3558f1280dff8ad0ae7650029595afa3440d9e6984f17f` both.
11. `c3-test_mission_upkeep.py` → `tests/orchestration/test_mission_upkeep.py` (at C3): cmp equal,
    sha256 `dac7f6cea90b463a445567cd6b7964e448977204fb0369931bdaaa0b4ae35935` both.
12. `dry-environment.md` → `docs/guides/environment.md`: cmp equal, sha256
    `45452ce1c3fdc0fe97be59a96c1e6fb06be8889f35d2b828f3df886c0075c5f7` both.
13. `c3-mission-upkeep-v1.md` → `docs/system/mission-upkeep-v1.md` (at C3): cmp equal, sha256
    `297f356d4733d3eceba6616c0a5ad7ae88bc32cc06df84228410a78669baa638` both.
14. `dry-mission_upkeep.py` → `packages/orchestration/mission_upkeep.py` (at C4): cmp equal, sha256
    `855668263319bdfa68974d3d6894894796ed4fbebefef28516e91cae9d576c1d` both.
15. `dry-test_mission_upkeep.py` → `tests/orchestration/test_mission_upkeep.py` (at C4): cmp equal,
    sha256 `1e341c1b8f0be031841952a8b8ba977af32a0c52148d87ea8f70c05929c8aaa2` both.
16. `dry-mission-upkeep-v1.md` → `docs/system/mission-upkeep-v1.md` (at C4): cmp equal, sha256
    `2b7368a8101d185898a369991d38e1d64657719b44272b31cb8e456f286ba9ba` both.
17. `dry-mission_cmd.py` → `apps/cli/commands/mission_cmd.py`: cmp equal, sha256
    `860eccba8ba82f64e362fbfec30ec556f6296bb3d4d426837dc93ea969934948` both.
18. `dry-orchestrator_dispatch.py` → `packages/orchestration/orchestrator_dispatch.py`: cmp equal,
    sha256 `3b563a0aa344d75d5e58192f4cce43c72110876525b36cf16fa203f7874a155f` both.
19. `dry-client_digest.py` → `packages/orchestration/client_digest.py`: cmp equal, sha256
    `8ef1dad8ee6ed22373f12b4b6dfe0f2d8519801ab14b0f1c00ac484be10ea6de` both.
20. `dry-client_interface.py` → `apps/cli/client_interface.py`: cmp equal, sha256
    `155c32b45ea323a2253c465695e2b6675a5bc4e22a7364a76f5d9a13497cbd8a` both.
21. `dry-machine-client-contract-v1.md` → `docs/system/machine-client-contract-v1.md`: cmp equal,
    sha256 `871fd9dfe3f2790aebca28f7b76ce2bd48b8d6c5bc80acd1b9ef52f78c1dd7ab` both.
22. `dry-test_client_interface.py` → `tests/cli/test_client_interface.py`: cmp equal, sha256
    `3523c4fdf21b22292ef76fabe3f9fa01dc06ce924e3a2914aec1b66b69981962` both.
23. `dry-test_mission_cmd.py` → `tests/cli/test_mission_cmd.py`: cmp equal, sha256
    `a96f89cd0574dd1b3b2dbc3955d9977101f5303fa71567ec1b00992453c1e4b6` both.
24. `dry-test_status_cmd.py` → `tests/cli/test_status_cmd.py`: cmp equal, sha256
    `163d151efbdfc448a28bdbd81f93dbdcb4edbddc6be334bff355f1ecc6adff21` both.
25. `dry-test_orchestrator_dispatch.py` → `tests/orchestration/test_orchestrator_dispatch.py`: cmp
    equal, sha256 `f324c28b4900e955f002769d34142646c49c72597d0b621d1288c1bfbaa7fa4b` both.

The three `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`,
`append-prose_slips.txt`) were listed in the Bundle and digest-checked (all `True`), but C1 orders
copying the four whole `dry-*.md` files, which already carry that content baked in; the
`append-*.txt` files were not applied separately, and nothing in the block calls for that (same
note as F297 round 2's handback).

## Deviations & assumptions

1. **Shell shape.** Most read-only checks this round (`git status`, `git branch --show-current`,
   `git add`, `git diff --cached`, `git commit`, `git log`, `wc -l`, `sha256sum`, the ruff
   invocation, `integrity check`) were run as `cd /home/decodeux/Repos/remedy && <one command>`
   rather than `git -C ... <command>` as the top-level task instructions prefer; none were refused
   by the sandbox. All copy/hash steps needing more than one operation used the mandated python3
   scripts under `.remedy-wt/f297-r3-worker/`. (Same note as F297 rounds 1 and 2's handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag, so
   the round 1/2 handbacks' `-A` caveat does not apply here.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r3/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during
the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 3's verdict and the resolutions of R-1237, R-1239 and R-1238 in the next round's
   first commit.
5. T013 and T014: R-1247 and R-1250.

Operator questions open: 0.
Open findings: 21, all owned by F297 except R-1248, owned by F305.

## For the operator, in plain sentences

This round first wrote last time's results permanently into the project's record. It then made
three small repairs to how the system keeps the project tidy between jobs: the maintenance work it
schedules now looks at every open issue the whole project has left behind, not only the issues left
by one particular line of work; how much maintenance work it takes on at once, and how large a
piece of code has to grow before it is flagged, are now choices that can be set rather than fixed
numbers; and when that maintenance work takes the place of a step you asked for, the system now
says plainly which step was set aside, both when you ask it to continue and in the summary anyone
checking on the project can read. Every one of the three repairs is backed by a test that fails
without it and passes with it. This round's own results will be written permanently into the
record at the start of next time's work, which will then take on two more items from the remaining
list. Nothing is waiting on you right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 2, resolutions of R-1143/R-1176/R-1196/R-1138/R-1162, DECISION F297 D4; numstat matched exactly |
| C2 | done | T010 (R-1237) landed; numstat and diff content matched exactly |
| C3 | done | T011 (R-1239) landed; numstat and diff content matched exactly |
| C4 | done | T012 (R-1238) landed; numstat and diff content matched exactly |
| C5 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `5799 passed, 10 skipped`, exit 0, identical to the dry tree |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 21 ids, exact order |
| Gate 6 | passed | four subjects, newest first |
| T010 (R-1237) | done | `open_findings` carries the project's open findings, whichever mission left them |
| T011 (R-1239) | done | the findings carried and the structure limits are settings, today's values as defaults |
| T012 (R-1238) | done | the deferred step is named in `mission continue`'s answer, the upkeep ledger and the client digest; interface `1.10` |
