# Handback — F306 round 2: book round 1, then T003 (R-1251), repaired under amendment 1

## Session

SESSION 1 of feature F306 · round 2 · rounds so far 2

Context self-assessment: C1 was mechanical bookkeeping (prepared-bytes copies, verified digest by
digest). C2, written against the original block, implemented R-1251 correctly and passed every
test, but gate 3 then read two structure-ratchet findings the block's own two steps had caused —
a re-export the ledger-tracked `dev_server.py` could not absorb, and a new branch that pushed
`_run_app_once` over its 100-line cap — so the round stopped and reported rather than patch
ledger/pin files outside its declared scope. The reviewer confirmed the stop was correct and sent
amendment 1, which moves the ownership check beside the runner (no re-export) and sharpens the
semantics so a denied connections read answers unproven rather than foreign; C2b applies it, and
every gate now passes clean.

Fortschritt: ~30 % (T001 to T003 landed · T004 to T008 open) — Schätzung

## Range

Review of `58a280f34`..`fbae12a81`

## Commits

### accb73a87 F306 R2 C1: book round 1 and its two prose slips, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r2.md` | +130/-0 | NEW FILE, byte copy of `block.md` (130 lines, sha256 `6a80fe0c1e5057c03826a1cdde51b30d1f5cab4aa3642517219429d01b6bd25d`) |
| `.agent/live_review.md` | +2/-0 | round 1's PASS verdict appended, byte-identical to `append-live_review.txt` |
| `.agent/prose_slips.md` | +2/-0 | round 1's two prose slips appended, byte-identical to `append-prose_slips.txt` |
| `.agent/plan.md` | +8/-10 | replaced by `dry-plan.md` |

### 013656215 F306 R2 C2: a runtime-flow check refuses a health answer from a process it did not start (R-1251)

| Path | +/- | Reason |
|---|---|---|
| `packages/runtimes/dev_server_ports.py` | +31/-0 | `port_listener_in_session(port, session_id)` added: True/False/None over a psutil scan of the process group |
| `packages/runtimes/dev_server.py` | +3/-0 | the new name re-exported alongside the others moved in round 1 |
| `packages/orchestration/dod_runners.py` | +16/-3 | `_run_app_once` calls the ownership check after readiness, before `body`, inline |
| `tests/orchestration/test_dod_runners.py` | +79/-1 | `write_runtime_config` moved off the literal `5173`; squatter test and two-checks-racing test added to `TestRuntimeFlowRunner` |
| `tests/runtimes/test_dev_server_ports.py` | +99/-0 | NEW FILE: true/false/none unit coverage of the new function |
| `docs/system/runtime-harness-v1.md` | +6/-0 | one paragraph documenting the ownership confirmation |

Superseded by C2b below: the inline branch in `_run_app_once` (pushed it to 105 lines, over the
100-line function cap) and the `dev_server.py` re-export (grew the ledger-tracked file from 1989 to
1992 lines) — both flagged by `tests/test_structure_ratchet.py` in this round's first gate-3 run.

### fbae12a81 F306 R2 C2b: the ownership check lives beside the runner, and a denied read is unproven, not foreign (R-1251)

| Path | +/- | Reason |
|---|---|---|
| `packages/runtimes/dev_server.py` | +0/-3 | restored byte-for-byte to its content at `58a280f34` (`git diff 58a280f34 --` prints nothing); the new function is no longer re-exported here |
| `packages/runtimes/dev_server_ports.py` | +28/-11 | `port_listener_in_session` now distinguishes a vanished session member (`psutil.NoSuchProcess`, skipped) from any other unreadable one (access denied, zombie: answers None, never False); unused `contextlib` import dropped |
| `packages/orchestration/dod_runners.py` | +29/-14 | imports `port_listener_in_session` from `packages.runtimes.dev_server_ports` directly; the inline branch moved into a new module function `_confirm_app_owns_port(port, proc, health_path, log) -> tuple[str, str]`, called with `proc.pid` as the session id (not `os.getpgid(proc.pid)`), bringing `_run_app_once` back under the 100-line cap |
| `tests/orchestration/test_dod_runners.py` | +3/-1 | the two-racers test's "at least one did not pass" assertion replaced by a comment: the two checks may not overlap in time, so only the property every interleaving keeps is asserted; the squatter test is the deterministic proof |
| `tests/runtimes/test_dev_server_ports.py` | +17/-0 | new test: an idle child in its own session, with `psutil.Process.connections` (and `net_connections` where present) monkeypatched to raise `psutil.AccessDenied`, reads None |

### (this commit) F306 R2 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this handback, full rewrite per `docs/agents/handback_template.md` |
| `.agent/authored/f306-r2-amend1.md` | this commit | NEW FILE, byte copy of `amend1.md` (49 lines, sha256 `4d9fece9eb13c9cd1ee6513cebf6d3af473a17870a9095541a08f57ddbdea6ed`) |

## External actions

- Push after C3: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8` — result in the session's final reply (with retry-on-500 up to three times per the block).
- No PR opened — the block explicitly says not to.
- No worktree added or removed. No `gh pr merge` or `gh pr edit`.

## Verification

Preconditions confirmed before C1, before C2, and again before C2b: `git branch --show-current` read `feature/f306-findings-paydown-v8`; `git rev-parse HEAD` matched the expected parent each time; `git status --porcelain` was clean before each commit's staging.

Every prepared-file digest matched before use: `block.md` (130 lines, `6a80fe0c1e...`), `append-live_review.txt` (`8e62fe470d...`), `append-prose_slips.txt` (`eed20ceaaf...`), `dry-plan.md` (`fcfb8700ae...`), `verify.py` (`8c36800af9...`), `run_selection.py` (`1507309fd8...`), `selection.txt` (`48451e3847...`), and later `amend1.md` (49 lines, `4d9fece9eb...`).

C1: before commit, `git diff --cached --numstat` read exactly `130 0 .agent/authored/f306-r2.md`, `2 0 .agent/live_review.md`, `8 10 .agent/plan.md`, `2 0 .agent/prose_slips.md` — matching the block's specification exactly.

C2: before commit, `git diff --cached --numstat` read `6 0`, `16 2`, `3 0`, `31 0`, `79 1`, `99 0` across the six named paths — 231 insertions total, under the 500-insertion cap. Self-review ran over `git diff --cached` before the commit; all new/changed tests were run serially beforehand (`test_dev_server_ports.py` 3/3, the squatter test alone, the race test alone twice, then the full `test_dod_runners.py` file: 58 passed), with no leftover `flow_app.py` process after any run.

**First gate run (against C2, before the amendment):**
- Gate 1: `git status --porcelain` empty; `verify.py` → `ALL True` (reads C1 only).
- Gate 2: `ruff check` on the five named files → `All checks passed!`.
- Gate 3 — **RED**: `run_selection.py` exit 1.
  ```
  FAILED tests/test_structure_ratchet.py::test_every_function_equals_its_row
  FAILED tests/test_structure_ratchet.py::test_every_file_equals_its_row
  2 failed, 3753 passed, 3 skipped in 121.45s (0:02:01)
  ```
  No "process(es) behind" line. Root cause (confirmed by direct re-run of `tests/test_structure_ratchet.py`): `_run_app_once` (`packages/orchestration/dod_runners.py`) measured 105 lines, over the 100-line cap and with no ledger row; `packages/runtimes/dev_server.py` measured 1992 lines against the ledger's recorded 1989 — both a direct, unavoidable consequence of the block's own C2 steps 1 and 2 (confirmed: ruff's default `combine-as-imports=false` forces every `as X` self-re-export onto its own 3-line statement, so the re-export could not be added without growing the file; repairing the ratchet would have needed edits to `docs/system/structure-ledger-v1.md` and `tests/test_structure_ratchet.py`'s pins, neither named in C2's paths, plus a DECISION under the structure rule's rule 5). The session stopped per the block's own contingency ("a red gate you cannot fix within the block's scope: stop and report"), reverted its uncommitted investigative fix (`git checkout --`) so the tree matched `013656215` exactly, and reported. Gates 4 and 5 were still run for completeness: gate 4 `fail_count` 0; gate 5 `['R-1235', 'R-1246', 'R-1251', 'R-1252']`.

The reviewer's amendment 1 confirmed the stop was correct and both red nodes were caused by the block, then ordered C2b.

C2b: before commit, `git diff --cached --numstat` read `29 14 packages/orchestration/dod_runners.py`, `0 3 packages/runtimes/dev_server.py`, `28 11 packages/runtimes/dev_server_ports.py`, `3 1 tests/orchestration/test_dod_runners.py`, `17 0 tests/runtimes/test_dev_server_ports.py` — 77 insertions total. `git diff 58a280f34 -- packages/runtimes/dev_server.py` printed nothing before staging, confirming the byte-for-byte restore. Self-review ran over `git diff --cached` before the commit. New/changed tests run serially beforehand: `test_dev_server_ports.py` 4/4 (including the new denied-read test), the squatter test alone, the race test alone, then the full `test_dod_runners.py` file: 58 passed, and `tests/test_structure_ratchet.py` directly: 5/5 — no leftover `flow_app.py` process after any run.

**Second gate run (against C2b, the one that counts):**
- Gate 1: `git status --porcelain` empty; `verify.py` → `ALL True` (reads C1 only, still valid per the amendment).
- Gate 2: `ruff check` on the five named files → `All checks passed!`.
- Gate 3: `run_selection.py` exit 0.
  ```
  SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
  SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
  SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
  3756 passed, 3 skipped in 126.57s (0:02:06)
  ```
  No FAILED/ERROR line, no "process(es) behind" line.
- Gate 4: `python3 -m apps.cli.main integrity check --json` → exit 0:
  ```
  {"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
  ```
- Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` → exit 0: `['R-1235', 'R-1246', 'R-1251', 'R-1252']`.

## Authored-text proofs

- `.agent/authored/f306-r2.md` against `block.md`: byte-equal, 130 lines, sha256 `6a80fe0c1e5057c03826a1cdde51b30d1f5cab4aa3642517219429d01b6bd25d` (Gate 1's "equal at F306 R2 C1 True .agent/authored/f306-r2.md").
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (Gate 1).
- `.agent/prose_slips.md` against the base plus `append-prose_slips.txt`: byte-equal (Gate 1).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (Gate 1).
- `.agent/authored/f306-r2-amend1.md` against `amend1.md`: byte-equal, 49 lines, sha256 `4d9fece9eb13c9cd1ee6513cebf6d3af473a17870a9095541a08f57ddbdea6ed` (`cmp` printed nothing).

No other reviewer-authored text applied this round: C2 and C2b are this session's own code, proved by the gates above rather than by digest comparison to a prepared file.

## Deviations & assumptions

- **Commit trailer model name.** Every commit carries `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` — the model this session actually runs on — per the standing operator instruction, not a fixed name typed into a block or amendment.
- **Gate 3 read red after C2, before the amendment.** Recorded in full above rather than only here: the round stopped, reverted its uncommitted diagnostic fix, and reported, exactly as the block's own contingency directed. The reviewer's amendment 1 confirmed the stop was correct. No commit was rewritten; `accb73a87` and `013656215` stand unchanged.
- No extra commit beyond C1, C2, C2b, C3; no dropped one; no reordering.

## For the operator, in plain sentences

This round first recorded the previous round's acceptance and the plan for this one. It then closed
one of the four open problems: two checks that both start a local preview server could, in rare
timing, end up pointed at the same network port, and the one whose own server failed to start could
be told it passed because it happened to see the OTHER check's server answering instead. The runner
now confirms that the process answering is the one it itself started, and refuses the check
otherwise, while a case where that confirmation cannot even be attempted is logged as unproven
rather than silently accepted or silently rejected. The first attempt at this fix tripped two of the
project's own size rules in ways neither this session nor the block anticipated; the session
correctly stopped rather than patch around them, the reviewer agreed and sent a repair, and the
repair closes clean — every check now passes. Three more pieces of clean-up work remain for later
sessions, plus one problem that a current permission restriction prevents this session from
touching, which will be handed to whichever session runs this clean-up next. Nothing waits on the
operator right now.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. The Open PR Gate (none expected — this feature stays on its own branch with no PR this round).
3. Book round 2's verdict and R-1251's resolution in the next round's first commit.
4. T004 and T005: the workspace-identity step of `run_manifest.py`, then R-1252.

Operator questions open: 0.
Open findings: 4, all owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `accb73a87` |
| C2 | done | `013656215` — correct, but tripped gate 3 (see Verification) |
| C2b | done | `fbae12a81`, per amendment 1 |
| C3 | done | this commit |
| Amend1 step 1 | done | `dev_server.py` restored byte-for-byte to `58a280f34` |
| Amend1 step 2 | done | ownership check moved to `_confirm_app_owns_port`, imported from `dev_server_ports` directly, `proc.pid` as session id, `_run_app_once` back under 100 lines |
| Amend1 step 3 | done | `port_listener_in_session`: `NoSuchProcess` skipped, any other read failure answers None, never False |
| Amend1 step 4 | done | denied-connections-read test added to `tests/runtimes/test_dev_server_ports.py` |
| Amend1 step 5 | done | two-racers test's "at least one did not pass" assertion replaced with the explanatory comment |
| Gate 1 (first run, against C2) | passed | `ALL True` |
| Gate 2 (first run, against C2) | passed | `All checks passed!` |
| Gate 3 (first run, against C2) | failed | 2 failed, 3753 passed, 3 skipped — both findings caused by the block (see Verification) |
| Gate 4 (first run, against C2) | passed | `fail_count` 0 |
| Gate 5 (first run, against C2) | passed | `['R-1235', 'R-1246', 'R-1251', 'R-1252']` |
| Gate 1 (second run, against C2b) | passed | `ALL True` |
| Gate 2 (second run, against C2b) | passed | `All checks passed!` |
| Gate 3 (second run, against C2b) | passed | exit 0, `3756 passed, 3 skipped`, no FAILED/ERROR/"process(es) behind" |
| Gate 4 (second run, against C2b) | passed | six checks pass, `fail_count` 0 |
| Gate 5 (second run, against C2b) | passed | `['R-1235', 'R-1246', 'R-1251', 'R-1252']` |
| Push | pending at write time | runs after this commit; result in the session's final reply |
