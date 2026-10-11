# Handback — F297 round 7: book round 6, land T017 and T018

## Session

SESSION 1 of feature F297 · round 7 · rounds so far 7

Context self-assessment: the session verified the block and all 17 prepared files' digests before
any write, read every diff in full against the current tree before staging, and executed the
three commits and six gates in one uninterrupted pass with no retries; context remains comfortable
at handback.

Fortschritt: ~72 % (T001 to T018 landed · T019 to T025 open) — Schätzung

## Range

Review of `d7d77fa40`..`HEAD`.

## Commits

### fe9dad08e F297 R7 C1: book round 6 and the resolution of R-1149, DECISION F297 D8

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r7.md` | +125/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r7/prep/block.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D8: how round 7 repairs R-1139 and R-1158, and what R-1225's measurement found |
| `.agent/live_review.md` | +4/-0 | appended the `Gate: F297 R6` paragraph (VERDICT PASS) and the `Done:` paragraph for R-1149 |
| `.agent/plan.md` | +7/-8 | rewritten in full for F297 round 7 |

### cf3d9d855 F297 R7 C2: every test run records the CPU time of each test module, and a closure names the modules that carry a rise (R-1139)

| Path | +/- | Reason |
|---|---|---|
| `scripts/closure_suite_cost.py` | +50/-3 | reads `module_cpu_seconds` off each record line and names, via `module_rises`/`module_report`, the test modules whose CPU time rose most since the previous closure's own full-suite line |
| `tests/conftest.py` | +30/-2 | `pytest_runtest_protocol` adds each test's CPU time to its module's total; `pytest_testnodedown` folds an xdist worker's totals into the controller's; the session finish hands the controller's totals to `workeroutput` and into `build_record` |
| `tests/load_governor.py` | +23/-5 | `process_cpu_seconds` (renamed from `_cpu_seconds`), new `test_module` and `add_module_cpu` helpers, and `build_record` gains the optional `module_cpu` parameter that becomes `module_cpu_seconds` on the written line |
| `tests/orchestration/test_closure_suite_cost.py` | +41/-1 | new coverage for `module_rises`, `module_report` and the end-to-end command-line report of the modules that carry a rise, read from the previous closure's own line |
| `tests/regression/test_test_load_governor.py` | +22/-1 | new coverage: a two-worker run's module totals reach the controller's one line, a zero-worker run still records its modules, and totals are added by the module a node id names |

### 1820cf328 F297 R7 C3: the closure cost limit follows the spread of repeated runs (R-1158)

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/integration_gate.md` | +6/-3 | precondition 2's text now names the limit, how it is derived, and the module-rise report, instead of a fixed 10 percent |
| `docs/roadmap/STATUS_closure_protocol.md` | +8/-5 | the same precondition's page states the derived limit instead of the fixed one |
| `scripts/closure_suite_cost.py` | +49/-9 | new `run_spread_percent` (the largest spread between clean full-suite runs of the record that collected the same tests, excluding the judged run) and `cost_limit` (the larger of 10 percent and that spread); `compare` and `main` take the derived limit instead of the fixed `LIMIT_PERCENT` |
| `tests/orchestration/test_closure_suite_cost.py` | +46/-2 | new coverage: the spread calculation excludes the judged run and non-matching/non-clean runs, the limit never falls below 10 percent, a rise inside the spread stays within the limit, and the command line reports the derived limit end to end |

### this commit F297 R7 C4: handback

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
`d7d77fa4089ed2e2952f05a5d95b9bab9261104f`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`; `.agent/STOP` absent.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r7/prep/block.md`
read `125`; `sha256sum` read
`e590d18025cb5bbd67a3cfdc3c64b98ab2b536dc4032d24b47360a80cabca81c` — both equal to the values the
prompt delivered. All 17 Bundle-listed prepared files (the 11 `dry-*` files, the two C2 `c-`/`c2-`
snapshots, the two `append-*.txt` files, `verify.py`, `run_selection.py` and `selection.txt`) hashed
via a python3 script under `.remedy-wt/f297-r7-worker/check_hashes.py`: every one read `True`,
final line `ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the three `dry-*` whole files and the block to
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/authored/f297-r7.md`;
each printed `cmp_equal=True`. `git branch --show-current` read `feature/f297-findings-paydown-v7`
before staging. `git diff --cached --numstat` read exactly `125 0 .agent/authored/f297-r7.md`,
`12 0 .agent/decisions.md`, `4 0 .agent/live_review.md`, `7 8 .agent/plan.md` — matching the
block's required readings. The full staged diffs of all four files were read before committing:
`.agent/plan.md`'s rewrite matched the round's goal exactly; the `.agent/live_review.md` and
`.agent/decisions.md` diffs were each small enough (4 and 12 lines) to read in full and matched
the block's "For the record" description and DECISION F297 D8's text verbatim.

**C2:** `python3 -I c2_copy.py` copied the five files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `50 3 scripts/closure_suite_cost.py`, `30 2 tests/conftest.py`,
`23 5 tests/load_governor.py`, `41 1 tests/orchestration/test_closure_suite_cost.py`,
`22 1 tests/regression/test_test_load_governor.py` — matching the block exactly. Every diff was
read in full before staging against the current tree: `load_governor.py`'s rename of
`_cpu_seconds` to `process_cpu_seconds` and the new `test_module`/`add_module_cpu` helpers;
`conftest.py`'s new hook functions and the `workeroutput` hand-off; the two test files' new
coverage. `git branch --show-current` read `feature/f297-findings-paydown-v7` before staging.

**C3:** `python3 -I c3_copy.py` copied the four files; each printed `cmp_equal=True`. `git diff
--cached --numstat` read `6 3 docs/agents/integration_gate.md`,
`8 5 docs/roadmap/STATUS_closure_protocol.md`, `49 9 scripts/closure_suite_cost.py`,
`46 2 tests/orchestration/test_closure_suite_cost.py` — matching the block exactly. Every diff was
read in full before staging, against the C2 state of the two script/test files: the new
`run_spread_percent` and `cost_limit` functions, `compare`/`main` taking the derived limit, and
the two docs pages' reworded precondition text. `git branch --show-current` read
`feature/f297-findings-paydown-v7` before staging.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r7/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (11
file-equality checks and the two ledger/decisions base-plus-slice checks), last line `ALL True`,
exit 0.

**Gate 2:** `python3 -m ruff check` over the 5 named paths → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r7/prep/run_selection.py /home/decodeux/Repos/remedy` → 11
SKIPPED lines (`tests/test_agent_tooling.py:43` D12 quarantine,
`tests/regression/test_f293_acceptance.py:191`, `tests/regression/test_f294_acceptance.py:73`,
six `tests/regression/test_named_bugs.py` D3-quarantine lines,
`tests/test_install_smoke.py:175` opt-in install smoke,
`tests/test_repair_context_reviewer_memory.py:257` UI source not found), no FAILED or ERROR line,
no `process(es) behind` line, summary `3532 passed, 11 skipped in 28.51s`, `exit 0` — exactly the
reviewer's dry-tree reading the block states.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1139', 'R-1156', 'R-1157', 'R-1158', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235',
'R-1240', 'R-1241', 'R-1246', 'R-1248', 'R-1249', 'R-1251']` — the 15 ids in the required order,
exit 0.

**Gate 6:** `git log --format=%s d7d77fa40..HEAD` → the three subjects of C1 to C3, newest first,
exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4: the reviewer ran seven in its dry
tree). No full suite was run; `REMEDY_TEST_MAX_WORKERS` was never set. No two test commands ran at
once; each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 17-file digest pre-check (above)
additionally confirmed every prepared source's sha256 against the Bundle's stated values before
any copy, and a post-commit script re-hashed every committed file to confirm the same digests:

1. `.remedy-wt/f297-r7/prep/block.md` → `.agent/authored/f297-r7.md`: 125 lines both, sha256
   `e590d18025cb5bbd67a3cfdc3c64b98ab2b536dc4032d24b47360a80cabca81c` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256
   `3011a1e742008de678cad9c6e2385ffebb00bd29672daa5678df559710e634fa` both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256
   `73d597a02602f321f369f5e1fe0fe95a913f6f52d0d079cf4e3fc4c3b66f73f3` both.
4. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256
   `64ae5aab9a37520b3b6775c5b9f78fa3401c045940673687977cb497d83fd1af` both.
5. `dry-load_governor.py` → `tests/load_governor.py`: cmp equal, sha256
   `3e64993291618886af22469cf06e1f9f1bd693422ac6113a342aa0527cc4fe14` both.
6. `dry-conftest.py` → `tests/conftest.py`: cmp equal, sha256
   `bc3f64e54878552463c01eb961a25cb8ed44c5e77f9281d2c525a7677d8b7be1` both.
7. `dry-test_test_load_governor.py` → `tests/regression/test_test_load_governor.py`: cmp equal,
   sha256 `dbf32d60d1322bfb3be26e651bc18535e062afb1530b72a5e83d4681cc0ad8d0` both.
8. `c-modules-closure_suite_cost.py` → `scripts/closure_suite_cost.py` (C2 snapshot): cmp equal,
   sha256 `cea7549512141fbf1196f5582f0c6fc087894b8d1d97c4516324cbbf8644b4e7` both.
9. `c2-test_closure_suite_cost.py` → `tests/orchestration/test_closure_suite_cost.py` (C2
   snapshot): cmp equal, sha256 `6d168ceeaed4a0d6869ec9064a4221597f90e8914924375c04d51431d73584d8`
   both.
10. `dry-closure_suite_cost.py` → `scripts/closure_suite_cost.py` (C3 edit): cmp equal, sha256
    `16898b0c30b5c54ebe4dff90366f8319eb3917c7a9b32c97b8857137a87384a9` both.
11. `dry-test_closure_suite_cost.py` → `tests/orchestration/test_closure_suite_cost.py` (C3 edit):
    cmp equal, sha256 `e0e4c457a6040fac355bc258dc61ca2c09dac8440544fd5c0d0772ff1c8f59a7` both.
12. `dry-integration_gate.md` → `docs/agents/integration_gate.md`: cmp equal, sha256
    `6e7148458b96e2dba2272efa03a073032170d6fe62c98047dc72a9936778b237` both.
13. `dry-STATUS_closure_protocol.md` → `docs/roadmap/STATUS_closure_protocol.md`: cmp equal,
    sha256 `559045eee914a31e8dd7e534649cb9f27fd54a196fbf6bb336354d2226e78e7b` both.

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
   `.remedy-wt/f297-r7-worker/`. (Same note as F297's prior rounds' handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r7/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during
the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 7's verdict and the resolutions of R-1139, R-1225 and R-1158 in the next round's
   first commit.
5. T019 to T021: R-1156 with R-1157, and R-1230.

Operator questions open: 0.
Open findings: 15, all owned by F297 except R-1248, owned by F305, and R-1251, owned by the next
findings paydown.

## For the operator, in plain sentences

This round first wrote last time's results permanently into the project's record. It then made
every place in the project that runs the full set of checks start keeping track of how much
processor time each piece of that work actually used, broken down by which part of the project it
belonged to, so that if a future check takes noticeably longer, the record can point at exactly
which part grew instead of only saying the total grew. After that, it changed how a runaway cost
is judged. Before this round, a single fixed percentage decided whether a slower run counted as a
real problem. Now that percentage adjusts itself upward when the record itself shows that running
the same checks twice already produces a difference close to or past that size, so a slower run is
only flagged when it is slower than ordinary noise would explain, and that adjustment can never be
done by a person typing in a bigger number by hand. Every one of these changes is backed by a test
that fails without the change and passes with it. This round's own results will be written
permanently into the record at the start of next time's work, which will then take on the next
items from the remaining list. Nothing is waiting on you right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 6, resolution of R-1149, DECISION F297 D8; numstat matched exactly |
| C2 | done | T017 landed: every test run records each test module's CPU time, and the closure script names the modules whose time rose most; numstat and diff content matched exactly |
| C3 | done | T018 landed: the cost limit follows the largest spread between repeated full-suite runs, never below 10 percent; numstat and diff content matched exactly |
| C4 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `3532 passed, 11 skipped`, exit 0, exactly the reviewer's dry-tree reading |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 15 ids, exact order |
| Gate 6 | passed | three subjects, newest first |
| T017 (R-1139, R-1225) | done | `tests/conftest.py`, `tests/load_governor.py` and `scripts/closure_suite_cost.py` record and report per-module CPU seconds; DECISION F297 D8 (3) carries R-1225's measurement |
| T018 (R-1158) | done | `scripts/closure_suite_cost.py`'s limit is the larger of 10 percent and the largest spread between matching full-suite runs, held by a test, and the two docs pages state it |
