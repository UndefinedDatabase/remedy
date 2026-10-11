# Handback — F297 round 5: book round 4, register R-1251, land T015

## Session

SESSION 1 of feature F297 · round 5 · rounds so far 5

Context self-assessment: the session verified every prepared file's digest before use, read the
full bundle and every C2 diff against the current tree, and executed the two commits and six
gates in one uninterrupted pass with no retries; context remains comfortable at handback.

Fortschritt: ~58 % (T001 to T015 landed · T016 to T025 open) — Schätzung

## Range

Review of `fa4eb0c35`..`HEAD`.

## Commits

### e66bdd45e F297 R5 C1: book round 4 and the resolutions of R-1250 and R-1247, register R-1251, DECISION F297 D6

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r5.md` | +120/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r5/prep/block.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D6: how round 5 repairs R-1236, and R-1251 registered |
| `.agent/live_review.md` | +8/-0 | appended the `Gate: F297 R4` paragraph (VERDICT PASS) and the `Done:` paragraphs for R-1250, R-1247, plus the registration of R-1251 |
| `.agent/plan.md` | +7/-8 | rewritten in full for F297 round 5 |

### d5d4ee484 F297 R5 C2: the acceptance check reads its command and interpreter from the checkout, and refuses a command the job changed (R-1236)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/project_tests.py` | +45/-6 | new `base_lookup_dirs` and `changed_source_file`; `project_environment`, `project_python` and `find_project_test_command` now read the configured command, the virtual environment and the node tools from the repository's own checkout, never the job's worktree (R-1236) |
| `packages/orchestration/dod_runners.py` | +10/-0 | new `REASON_TEST_COMMAND_CHANGED`; `_run_project_tests` refuses the check, nothing run, when `changed_source_file` names a file the job's worktree holds different from the checkout |
| `packages/orchestration/project_constitution.py` | +2/-0 | `.remedy/config.toml` joins `_COMMON_PROTECTED`, listed when it exists |
| `docs/system/acceptance-checks-v1.md` | +11/-3 | documents the checkout-vs-worktree split for the configured command, the virtual environment and the node tools, and the `test_command_changed` refusal |
| `tests/orchestration/test_project_tests.py` | +42/-0 | new coverage: a worktree-only virtualenv/node tool is never the check's own, the worktree's configured command never overrides the checkout's, and `changed_source_file` names a changed config or `package.json` and stays empty otherwise |
| `tests/orchestration/test_dod_runners.py` | +43/-3 | the red control of `test_the_node_target_runs_for_real_with_npm_test` now rewrites a test file instead of the job's `package.json`, proving the refusal in its place; new coverage for a rewritten `package.json` and a rewritten `.remedy/config.toml`, each refused `test_command_changed` with nothing spawned |
| `tests/test_project_constitution.py` | +6/-0 | new coverage: `.remedy/config.toml` is protected only once it exists |

### this commit F297 R5 C3: handback

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
`fa4eb0c356d4f8efeb21d5cb9dadee7fb901d888`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r5/prep/block.md`
read `120`; `sha256sum` read
`1006a8a1c13160ea5c1bd9e9d07fdc4572eba90daa9683dea69b71e231383f10` — both equal to the values the
prompt delivered. All 16 Bundle-listed prepared files (`block.md`, 11 `dry-*` files, 2 `append-*.txt`
files, `verify.py`, `run_selection.py`, `selection.txt`) hashed via a python3 script under
`.remedy-wt/f297-r5-worker/check_hashes.py`: every one read `True`, final line `ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the three `dry-*` whole files and the block to
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/authored/f297-r5.md`;
each printed `cmp_equal=True`. `git branch --show-current` read `feature/f297-findings-paydown-v7`
before staging. `git diff --cached --numstat` read exactly `120 0 .agent/authored/f297-r5.md`,
`12 0 .agent/decisions.md`, `8 0 .agent/live_review.md`, `7 8 .agent/plan.md` — matching the
block's required readings. The staged diff of `.agent/plan.md` was read in full and matched the
round's goal exactly; the two large append-only files (`.agent/live_review.md` at 187 KB,
`.agent/decisions.md` at 3.3 MB whole) were verified by `cmp`/digest rather than by a full-file
read, and their new tails were read directly and matched the block's "For the record" description
and DECISION F297 D6's text.

**C2:** `python3 -I c2_copy.py` copied the seven files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `11 3 docs/system/acceptance-checks-v1.md`,
`10 0 packages/orchestration/dod_runners.py`, `2 0 packages/orchestration/project_constitution.py`,
`45 6 packages/orchestration/project_tests.py`, `43 3 tests/orchestration/test_dod_runners.py`,
`42 0 tests/orchestration/test_project_tests.py`, `6 0 tests/test_project_constitution.py` —
matching the block exactly. Every one of the seven diffs was read in full before staging (via
`diff -u` against the pre-copy tree): `base_lookup_dirs` returns the checkout alone;
`changed_source_file` compares the job's copy of the command's source file against the checkout's
and names it on any difference; `_run_project_tests` refuses `test_command_changed` before the
executable-allow-list check; `.remedy/config.toml` joins `_COMMON_PROTECTED`; the doc names the
checkout-only read and the refusal; the node-target red control rewrites a test file instead of
`package.json` so the refusal test can rewrite `package.json` in its place; the config-target test
proves a rewritten `.remedy/config.toml` is refused with `run_guarded_dod_process_command` never
called.

Every `git branch --show-current` run immediately before a commit (C1, C2) read
`feature/f297-findings-paydown-v7`.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r5/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (11
file-equality checks and the two ledger/decisions base-plus-slice checks), last line `ALL True`,
exit 0.

**Gate 2:** `python3 -m ruff check` over the 6 named paths → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r5/prep/run_selection.py /home/decodeux/Repos/remedy` → 3
SKIPPED lines (`tests/test_agent_tooling.py:43` D12 quarantine,
`tests/test_install_smoke.py:175` opt-in install smoke,
`tests/test_repair_context_reviewer_memory.py:257` UI source not found), no FAILED or ERROR line,
no `process(es) behind` line, summary `4343 passed, 3 skipped in 32.04s`, `exit 0` — identical to
the reviewer's dry-tree reading of `4343 passed, 3 skipped`. The R-1251 exception the block names
(`TestRuntimeFlowRunner` port contention) did not trigger: this run hit no FAILED line at all.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1139', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1219', 'R-1220', 'R-1225', 'R-1230',
'R-1235', 'R-1236', 'R-1240', 'R-1241', 'R-1246', 'R-1248', 'R-1249', 'R-1251']` — the 17 ids in
the required order, exit 0. R-1236 still reads open here by design: its code repair landed this
round, but the ledger's `Done:` line for it books in round 6's first commit (amend0827-process-diet
rule 1), which is exactly what `## Next` below orders.

**Gate 6:** `git log --format=%s fa4eb0c35..HEAD` → the two subjects of C1 and C2, newest first,
exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4: the reviewer ran six in its dry tree).
No full suite was run; `REMEDY_TEST_MAX_WORKERS` was never set. No two test commands ran at once;
each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 16-file digest pre-check (above)
additionally confirmed every prepared source's sha256 against the Bundle's stated values before
any copy:

1. `.remedy-wt/f297-r5/prep/block.md` → `.agent/authored/f297-r5.md`: 120 lines both, sha256
   `1006a8a1c13160ea5c1bd9e9d07fdc4572eba90daa9683dea69b71e231383f10` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256
   `d358e437dbc3ef5909a39c0f5d99e9b1927464a71b24a7918e5087a2866681b9` both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256
   `45456f1fb89860bb549fec2ca8842d61c712720ffef849d50dde7293c03ec780` both.
4. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256
   `654a9409c69a9217eff7d3dbfb54ac2b6fad6b69b72ad740f95bf1e09d96712b` both.
5. `dry-project_tests.py` → `packages/orchestration/project_tests.py`: cmp equal, sha256
   `0aabac26019dcf3e2ec6351bc93fcb32ac6843871600fc60f1e36e79dea9460a` both.
6. `dry-dod_runners.py` → `packages/orchestration/dod_runners.py`: cmp equal, sha256
   `702c2996d2d24f830fb17c2eecd4c86c329b4d1e2520b49742c23bf7b588d698` both.
7. `dry-project_constitution.py` → `packages/orchestration/project_constitution.py`: cmp equal,
   sha256 `1213e10bbb186fce70d876751a3d97f7fff6cd645cae855e9984d0342295ad65` both.
8. `dry-acceptance-checks-v1.md` → `docs/system/acceptance-checks-v1.md`: cmp equal, sha256
   `afad46c384f53c3760176c7e92186a9ef2f060e475edf99702531456cd06f18c` both.
9. `dry-test_project_tests.py` → `tests/orchestration/test_project_tests.py`: cmp equal, sha256
   `418bdb77eef68e40951f2b877432f83208c4229affa368d616197906e1793e4e` both.
10. `dry-test_dod_runners.py` → `tests/orchestration/test_dod_runners.py`: cmp equal, sha256
    `63e9688cf1620be3c75aa919f0f88b2a13f2d738bda6c89f0759e8bf151376ea` both.
11. `dry-test_project_constitution.py` → `tests/test_project_constitution.py`: cmp equal, sha256
    `d1bb891406ba26672fc0ae42b9f22de87950355ae631774481fec80e00a15515` both.

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
   `.remedy-wt/f297-r5-worker/`. (Same note as F297's prior rounds' handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag.
3. **Large-file review method.** `.agent/decisions.md` (29128 lines, 3.3 MB) and
   `.agent/live_review.md` (260 lines, 187 KB) could not be read whole in one pass; they were
   verified by `cmp`/sha256 against the prepared `dry-*` files (which is what the block's own
   `verify.py` gate also does) and their new tails were read with `tail` and matched against the
   `append-*.txt` files and DECISION F297 D6's text, rather than by reading either file end to end.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r5/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during
the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 5's verdict and the resolution of R-1236 in the next round's first commit.
5. T016: R-1149.

Operator questions open: 0.
Open findings: 17, all owned by F297 except R-1248, owned by F305, and R-1251, owned by the next
findings paydown.

## For the operator, in plain sentences

This round first wrote last time's results permanently into the project's record and added one
new small item to the list of things still to fix. It then made a repair so that a piece of work
can no longer influence the very check that is supposed to judge it. Before this fix, when a check
looked for which test command to run and where the necessary tools lived, it could end up reading
files from inside the very task it was checking, which that task had every ability to change.
Now the check always looks in the project's own untouched copy for the command, the tools and the
interpreter it needs, so a piece of work cannot quietly rewrite its own test instructions or plant
a tool that fakes success. On top of that, whenever a piece of work does change the file that a
check's command came from, that check is now refused outright, showing nothing passed, so a person
reviews it instead of letting it slip through as if it had passed on its own merits. The file
that carries this command is also now protected the same way other sensitive project files already
are. Every one of these changes is backed by a test that fails without the repair and passes with
it. This round's own results will be written permanently into the record at the start of next
time's work, which will then take on one more item from the remaining list. Nothing is waiting on
you right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 4, resolutions of R-1250/R-1247, register R-1251, DECISION F297 D6; numstat matched exactly |
| C2 | done | T015 (R-1236) landed; numstat and diff content matched exactly |
| C3 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `4343 passed, 3 skipped`, exit 0, identical to the dry tree; R-1251 exception not needed |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 17 ids, exact order |
| Gate 6 | passed | two subjects, newest first |
| T015 (R-1236) | done | the acceptance check reads its configured command, virtual environment and node tools from the repository's own checkout, never the job's worktree; `.remedy/config.toml` is protected; a job that changed the file its check's command comes from is refused `test_command_changed`, nothing run |
