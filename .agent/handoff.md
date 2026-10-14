# Handback — F055 round 2 — book round 1 and R-1316, land T002 (the rehearsal's record and summary), repair R-1316

## Session

SESSION 1 of feature F055 · round 2 · rounds so far 2

Context self-assessment: C1 to C3 landed clean on the first attempt; gate 3's first run (after
C3) came back red on a guard the block never named, `tests/test_ble001_ratchet.py`, over my own
new excused handler; I stopped before C4 and reported it rather than routing around it, the
coordinator sent amendment 1, and the fix plus its one-line golden update, applied as C4, left
every gate green on the one further run gate 3 is allowed.

Fortschritt: ~60 % (T001 and T002 landed · T003 open) — Schätzung

## Range

Review of `153c503d2`..`9ca5196d1` (then this commit).

## Commits

### `b6e34d5ea` F055 R2 C1: book round 1 and R-1316, DECISION F055 D2
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r2.md` | +199/-0 | byte copy of `block.md` |
| `.agent/decisions.md` | +12/-0 | byte copy of `dry-decisions.md` (DECISION F055 D2 appended) |
| `.agent/live_review.md` | +4/-0 | byte copy of `dry-live_review.md` (F055 R1 booked, R-1316 registered) |
| `.agent/plan.md` | +14/-8 | byte copy of `dry-plan.md` |
| `.agent/prose_slips.md` | +2/-0 | byte copy of `dry-prose_slips.md` |

### `cdcf7e3ef` F055 R2 C2: a rehearsal writes its record and summary beside the job
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/do-run-v1.md` | +13/-0 | `src-guide.md` inserted before `## JSON output` |
| `packages/orchestration/do_rehearsal.py` | +388/-6 | NEW: `build_job_rehearsal`, `render_rehearsal_summary`, `write_job_rehearsal`; `stop_walk_for_rehearsal` now writes each job's rehearsal before its Next lines |

### `d5cb55bab` F055 R2 C3: the rehearsal's record, its golden summary, and the applicator counter's proof
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_rehearsal.py` | +38/-0 | scenarios (k) and (l), including R-1316's positive control |
| `tests/orchestration/fixtures/rehearsal/golden/rehearsal.md` | +41/-0 | NEW: golden summary |
| `tests/orchestration/test_do_rehearsal.py` | +242/-0 | NEW: scenarios (a) to (j) |

### `9ca5196d1` F055 R2 C4: the head reader names its exceptions, and an unavailable whole-job estimate reads without a unit
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r2-amend1.md` | +26/-0 | byte copy of `amend1.md` (amendment 1) |
| `packages/orchestration/do_rehearsal.py` | +3/-2 | `_rehearsal_repo_head` catches `(OSError, subprocess.SubprocessError)`, no `noqa`; the whole-job line carries no unit when unavailable |
| `tests/orchestration/fixtures/rehearsal/golden/rehearsal.md` | +1/-1 | the whole-job line only |
| `tests/orchestration/test_do_rehearsal.py` | +22/-0 | the priced whole-job USD-form test |

### (this commit) F055 R2 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | — |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` (read-only, re-checked
  before writing this handback, since the round ran long enough to be worth a fresh look): `[]` —
  no open pull request.
- No branch created this round: C0 found `feature/f055-rehearsal` already at `153c503d2`, matching
  origin, clean, no `.agent/STOP`.
- Push after C5 follows this commit: `git push -u origin feature/f055-rehearsal`; its outcome is
  reported in the session's final reply only — it does not exist yet when this file is written.
- No worktree added or removed beyond the pre-existing `.remedy-wt/f055-r2-worker/` scratch
  directory the block named for copy/hash/measure scripts; nothing under it is tracked.
- No `gh pr merge`, `gh pr edit`, `gh pr create`, no STATUS edit, no ledger rotation, no self-use
  run, no provider call — none ordered by this block or its amendment. `tests/cli/test_rehearsal.py`
  scenario (l) is the one real `--apply` run this round made, through the fake builder/reviewer
  providers the fixture already wires, exactly as its sibling scenarios do.

## Verification

**Block verified before anything else**: `block.md` 199 lines /
`62e74df689f44ce7ab85080b8d7207dcee7e659c0438e0046082178469cd6c23` — matched. `verify.py`
(original) `b295c9565970b461f5ae6cbeadbc57979c26a1e12db6a8b457c89de1b1d1f2ca`, `run_selection.py`
`aca3c3bba1921d12b1d6d57e9d7b518daa64c3d0ec98428c70da8e09b770f389`, `selection.txt`
`1efbc969c1043485b6afc1c9c4be6bd673fffdccb88c625ef59b25ff4dc2183f`, `src-guide.md`
`3afec791b0272c6b581aeaa4a6348a567193ec77bba1a58bc24bbce0c5afd689`, `dry-live_review.md`
`e4fab0470010a5b040bb811d17f9c6a4bf5324594347c9b6050bed671bfa0bbc`, `dry-prose_slips.md`
`9e7f5425f6bee1072ff77b2168a18ec94beee40158f43130af7883e108fe2e63`, `dry-decisions.md`
`a08efd1674e1f9d6e96bbc9412bec2b1d1fa7b507c1dec6182d45a6ee310305d`, `dry-plan.md`
`2bb782617e5659b2415661917b09c6af1af11ec02986270cd7b73652f95f3b08` — all matched.
**Amendment 1**, read after gate 3's first run: `amend1.md` 26 lines /
`4d34335049a6a38eb9acc14dec064e6e1ddbc667473b1e55241339669fc16652` — matched. Replacement
`verify.py` 110 lines / `9912622c1496bdc6854d7a2a9baf7a6c215a69f9edfe96a7c6db7ab2b00dbaaf` —
matched.

**Gate 1** — `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r2/prep/verify.py /home/decodeux/Repos/remedy`
(the replaced `verify.py`, run after C4):
```
True b6e34d5ea has the single parent 153c503d2
True b6e34d5ea subject begins 'F055 R2 C<n>:'
True cdcf7e3ef has the single parent b6e34d5ea
True cdcf7e3ef subject begins 'F055 R2 C<n>:'
True d5cb55bab has the single parent cdcf7e3ef
True d5cb55bab subject begins 'F055 R2 C<n>:'
True 9ca5196d1 has the single parent d5cb55bab
True 9ca5196d1 subject begins 'F055 R2 C<n>:'
True the commit C1 exists
True the commit C2 exists
True the commit C3 exists
True the commit C4 exists
[... 5 C1-path-equality lines, 4 path-set checks, C2's guide + 13 needle checks + prefix-once
check, and C4's amendment-copy, no-BLE001, exception-names, golden-unit and golden-single-line
checks — all True ...]
ALL True
```
(42 checks total, every one `True`.)

**Gate 2** — `python3 -m ruff check` over the three files the block and the amendment name
(`do_rehearsal.py`, `test_do_rehearsal.py`, `test_rehearsal.py`): `All checks passed!`, run once
after C4.

**Gate 3** — `python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r2/prep/run_selection.py
/home/decodeux/Repos/remedy <output file>`, run TWICE this round, as amendment 1 orders and
reports:
- First run, after C3, before C4 — RED:
  ```
  FAILED tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises
  SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252)
  SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in
  SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
  79 paths
  1 failed, 3507 passed, 3 skipped in 69.18s (0:01:29)
  exit 1
  ```
  Decisive line: `AssertionError: 286 excused blind handlers, above the frozen 285: narrow the
  new handler to the exceptions it expects instead of excusing it`
  (`tests/test_ble001_ratchet.py:42`) — my own new `# noqa: BLE001` in `_rehearsal_repo_head`,
  a guard the block never named. No `process(es) behind` line either run.
- Second run, after C4 (the one amendment 1 counts) — GREEN:
  ```
  SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252)
  SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in
  SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
  79 paths
  3509 passed, 3 skipped in 56.42s
  exit 0
  ```
  No FAILED or ERROR line, no line naming a process left behind.

**Gate 4** — `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

**Gate 5** —
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', 'R-1278', 'R-1279', 'R-1280', 'R-1281', 'R-1282', 'R-1283', 'R-1284', 'R-1285', 'R-1286', 'R-1287', 'R-1288', 'R-1289', 'R-1290', 'R-1291', 'R-1292', 'R-1293', 'R-1294', 'R-1295', 'R-1296', 'R-1297', 'R-1298', 'R-1299', 'R-1300', 'R-1301', 'R-1302', 'R-1303', 'R-1304', 'R-1305', 'R-1306', 'R-1307', 'R-1308', 'R-1309', 'R-1310', 'R-1311', 'R-1312', 'R-1313', 'R-1316']
```
40 ids: `R-1246`, then `R-1276` to `R-1313`, then `R-1316`, in order, as required.

**Gate 6** — the golden fixture `tests/orchestration/fixtures/rehearsal/golden/rehearsal.md`,
printed in full:
```
# Rehearsal of job job-rehearsal-fixture

Rehearsed at 2026-10-14T00:00:00+00:00 on /tmp/rehearsal-fixture at commit deadbeefcafef00dfacade0123456789abcdef0. No job was run, no builder or reviewer was built, nothing was applied, and nothing was written to the repository.

## What planning cost

2 planning call(s) recorded in the job's prompt trace (intake, task_plan): about 500 prompt tokens, estimated from 2000 prompt characters. The answers' tokens and the price of these calls are not recorded, so no cost in dollars is claimed. The study and the mission's own plan are not counted here.

## What the run would cost

| Task | Title | Plan band | Estimate in USD |
|---|---|---|---|
| T001 | Write the thing | M | 80.0000–80.0000 |
| T002 | Polish it | none | not available |

Whole job: not available. Basis: estimate_unavailable.

## Risks

- the fixture might drift

Normalization:
- merge T001, T002 → T001: too small to split

## Definition of done

| Check | Kind | Blocking | Source |
|---|---|---|---|
| tests-pass | custom_cmd | yes | compiled |
| lint-clean | custom_cmd | no | standard |

Not compiled: lint-clean.

## What the run could write

- would write `src/app.py`
- would be blocked `.git/config`: denied:builtin:git directory

## To run it for real

- `remedy job run job-rehearsal-fixture`
```

## Authored-text proofs

`.agent/authored/f055-r2.md` against `block.md`: byte-identical, sha256
`62e74df689f44ce7ab85080b8d7207dcee7e659c0438e0046082178469cd6c23`, confirmed twice — once by my
own copy script and again independently by `verify.py`'s Gate 1 (`git show <C1>:<path>` compared
to the prep file's bytes). `.agent/authored/f055-r2-amend1.md` against `amend1.md`: byte-identical,
sha256 `4d34335049a6a38eb9acc14dec064e6e1ddbc667473b1e55241339669fc16652`, same double
confirmation. The four `dry-*.md` copies applied in C1 (`live_review.md`, `prose_slips.md`,
`decisions.md`, `plan.md`) were each confirmed byte-equal by sha256 at copy time and again by
Gate 1's per-path check. No other reviewer-authored text was applied this round.

## Deviations & assumptions

1. **Gate 3 ran twice, not once**, by amendment 1's own order: its first run (after C3, before
   C4) came back red on `tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises`
   — a guard the block never named, tripped by my own `# noqa: BLE001` excuse in
   `_rehearsal_repo_head`. Per my standing instructions I stopped before C4, pushed nothing, and
   reported the exact reading. The coordinator's amendment 1 narrowed the handler's exception
   tuple instead of excusing it, adjusted the whole-job line's unit to match, and declared this
   the C4 that resolves the blocker; gate 3's second run, after that C4, is the one the amendment
   counts, and is reported above as green. Both readings are kept in Verification, not just the
   final one, per the amendment's own instruction.
2. **The whole-job line's unit**, originally `Whole job: <low>–<high> USD, or "not available".`
   as one phrase, is now two: a unit only when both bounds are measured
   (`Whole job: <low>–<high> USD. Basis: ...`), and none when not
   (`Whole job: not available. Basis: ...`) — amendment 1's own fix for a template gap the
   original block left open; the golden file changed in that one line only, confirmed by gate 1's
   `verify.py`.

No other departure from the block's or the amendment's ordered sequence.

## For the operator, in plain sentences

This round booked the previous round's verdict and a test-coverage gap it found, then built the
rehearsal's own record and readable summary: what the planning cost, what each task and the whole
job would cost, the plan's risks and what was normalized, every check of the definition of done
and which were not compiled, and which files a real run could write or would be blocked from,
all written beside the job without running anything. A positive-control test now proves the
applicator counter other tests rely on actually counts. One blocker came up mid-round: a frozen
count of exception handlers that excuse themselves from a stricter lint rule, which a narrower
exception list resolved along with a small wording gap in the summary's cost line the same fix
exposed. All six checks the round requires came back clean on the run that counts. One round
remains before this feature closes: reusing a rehearsed plan for a real run without planning
twice.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. Book round 2's verdict in the next round's first commit.
4. T003, under DECISION F055 D3.

Operator questions open: 0.
Open findings: 40 (R-1316 owned by F055, R-1246 and R-1276 to R-1313 by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | preconditions held: HEAD and origin both `153c503d2`, clean, no STOP |
| C1 | done | Gate 1 `ALL True`; 223 insertions |
| C2 | done | all needles present; 395 insertions |
| C3 | done | 10 + 2 new tests pass; 321 insertions |
| C4 | done | amendment 1's fix; ratchet back to 285; golden's one-line change confirmed; 52 insertions |
| C5 | done | this commit |
| Gate 1 | done | `ALL True`, replaced `verify.py` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | first run (after C3) RED — `test_the_count_of_excused_handlers_never_rises`, 286 excused handlers; second run (after C4, the counted one) GREEN — 3509 passed, 3 skipped, exit 0 |
| Gate 4 | done | `fail_count` 0 |
| Gate 5 | done | 40 ids, in order |
| Gate 6 | done | golden printed in full above |
| R-1316 | done | `tests/cli/test_rehearsal.py` scenario (l): a real `--apply` run reads `apply_job` above zero on `count_applicator_calls` |
