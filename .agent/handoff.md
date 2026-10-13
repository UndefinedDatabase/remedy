# Handback — F306 round 1: claim, book F203 R10, and the first structural step (T002)

## Session

SESSION 1 of feature F306 · round 1 · rounds so far 1

Context self-assessment: this round was mechanical bookkeeping (prepared-bytes copies, verified
digest by digest) for C1, followed by a genuine structural edit for C2 — moving dev_server.py's
ports/readiness section into its own module — where the only real judgment calls were working out
which names needed an explicit re-export alias to satisfy ruff's unused-import check and
re-measuring the exact post-edit line count rather than trusting an early estimate; both gates
confirmed the result was right before anything was committed.

Fortschritt: ~15 % (T001 and T002 landed · T003 to T008 open) — Schätzung

## Range

Review of `f51232ee2`..`74a408a49`

## Commits

### 2ef38daf2 F306 R1 C1: claim F306, book F203 R10, re-head the ledger, DECISION F306 D1 and the slice list

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r1.md` | +124/-0 | NEW FILE, byte copy of `block.md` (124 lines, sha256 `c6668e5cfc087dba161c84f976c97328a62829d466502ad3e94208d282dae007`) |
| `docs/roadmap/STATUS.md` | +1/-1 | F306's line flipped `[ ]` to `[~]`, replaced by `dry-STATUS.md` |
| `.agent/live_review.md` | +16/-16 | re-headed at the F306 claim and booked F203 round 10's verdict, replaced by `dry-live_review.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F306 D1 appended, replaced by `dry-decisions.md` |
| `.agent/plan.md` | +14/-11 | replaced by `dry-plan.md` |
| `.agent/context.md` | +12/-15 | replaced by `dry-context.md` |
| `docs/roadmap/features/T2_F306.md` | +26/-0 | Task slicing and Acceptance sections appended, replaced by `dry-T2_F306.md` |

### 74a408a49 F306 R1 C2: dev_server's ports and readiness probe move to a module of their own (T002)

| Path | +/- | Reason |
|---|---|---|
| `packages/runtimes/dev_server_ports.py` | +83/-0 | NEW FILE: `port_is_free`, `pick_free_port`, `choose_port`, `RuntimeProbeResult` and `http_probe` moved byte-for-byte in their bodies, with `DEFAULT_HOST` now defined here (the one definition) |
| `packages/runtimes/dev_server.py` | +12/-75 | the moved section deleted; the five names (plus `DEFAULT_HOST`) imported back by name — `pick_free_port` and `port_is_free` as explicit `name as name` re-export aliases, since nothing left in this file calls them directly but `tests/runtimes/test_dev_server.py` imports them from `dev_server`; `import socket`/`urllib.error`/`urllib.request` dropped (no longer used in this file) |
| `docs/system/structure-ledger-v1.md` | +3/-2 | the `dev_server.py` row lowered `2052` → `1989`; its "Files" bullet gained the Step (1) sentence naming `dev_server_ports.py` |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` lowered `74364` → `74301` (the same 63-line drop the ledger row took) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.runtimes.dev_server_ports` added — the import-reachability guard test (in `selection.txt`) found it newly reachable from `packages.runtimes.dev_server`, one of the six D11 (c) entry points' closure |

### (this commit) F306 R1 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this handback, full rewrite per `docs/agents/handback_template.md` |

## External actions

- Push after C3: `git -C /home/decodeux/Repos/remedy push -u origin feature/f306-findings-paydown-v8` — result in the session's final reply (with retry-on-500 up to three times per the block).
- No PR opened — the block explicitly says not to.
- No worktree added or removed. No `gh pr merge` or `gh pr edit`.

## Verification

Preconditions (before any write): `git rev-parse HEAD` read `f51232ee2fd1e2367d8fad5045aa7d1a0805a3d4`; `git status --porcelain` empty; `gh pr list --state open ...` read `[]` (Open PR Gate clear — pull request 334 already merged into this exact commit). `git branch --show-current` read `main` at that point.

Every block/bundle digest matched before use: `block.md` (124 lines, sha256 `c6668e5cfc0...dae007`), `verify.py` (`a4135247e0...`), `run_selection.py` (`1507309fd8...`), `selection.txt` (`48451e3847...`), and the six `dry-*` bundle files, all against the sha256 readings the block and the environment gave.

Deviation in sequencing (see Deviations below): the C2 structural edit was made to the working tree, on `main`, before `git checkout -b` ran. Nothing was committed on `main` at that point (`git rev-parse HEAD` was still `f51232ee2` and `git status --porcelain` was non-empty only in the working tree). The C2 edits were stashed, the branch created and confirmed (`git branch --show-current` → `feature/f306-findings-paydown-v8`, `git rev-parse HEAD` → `f51232ee2`), C1 was staged, numstat-checked and committed, and only then was the stash popped and C2 staged and committed — so the commits landed in the block's exact order even though the editing session did not.

C1: before commit, `git diff --cached --numstat` read exactly `124 0 .agent/authored/f306-r1.md`, `12 15 .agent/context.md`, `12 0 .agent/decisions.md`, `16 16 .agent/live_review.md`, `14 11 .agent/plan.md`, `1 1 docs/roadmap/STATUS.md`, `26 0 docs/roadmap/features/T2_F306.md` — all matching the block's specification exactly. `git status --porcelain` before staging named only those seven paths. `git branch --show-current` read `feature/f306-findings-paydown-v8` immediately before the commit.

C2: before commit, `git diff --cached --numstat` read `3 2 docs/system/structure-ledger-v1.md`, `12 75 packages/runtimes/dev_server.py`, `83 0 packages/runtimes/dev_server_ports.py`, `1 0 tests/orchestration/import_reachability_allowlist.txt`, `1 1 tests/test_structure_ratchet.py` — 100 insertions total, well under the 500-insertion cap. `git status --porcelain` before staging named only those five paths. `git branch --show-current` read `feature/f306-findings-paydown-v8` immediately before the commit. Self-review ran over `git diff --cached` before the commit (see Deviations for what it found and fixed).

Gate 1 (`git status --porcelain` empty, then `python3 .../prep/verify.py /home/decodeux/Repos/remedy`) — exit implied 0, every line `True`:
```
found True F306 R1 C1: 2ef38daf2586d41bf6c1322f620b4a4be52676e8
C1 parent is the base True
equal at F306 R1 C1 True docs/roadmap/STATUS.md
equal at F306 R1 C1 True .agent/live_review.md
equal at F306 R1 C1 True .agent/decisions.md
equal at F306 R1 C1 True .agent/plan.md
equal at F306 R1 C1 True .agent/context.md
equal at F306 R1 C1 True docs/roadmap/features/T2_F306.md
equal at F306 R1 C1 True .agent/authored/f306-r1.md
F306 R1 C1 names exactly its paths True []
ALL True
```

Gate 2 (`python3 -m ruff check packages/runtimes/dev_server.py packages/runtimes/dev_server_ports.py tests/test_structure_ratchet.py`) — exit 0: `All checks passed!` (reached only after fixing two F401s the first run raised — see Deviations).

Gate 3 (`python3 .../prep/run_selection.py /home/decodeux/Repos/remedy /home/decodeux/Repos/remedy/.remedy-wt/f306-r1-worker/selection-output.txt`) — exit 0, no FAILED/ERROR line, no "process(es) behind" line. Summary: `3750 passed, 3 skipped in 121.78s (0:02:01)`. The three SKIPPED lines, verbatim:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

Gate 4 (`python3 -m apps.cli.main integrity check --json`) — exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

Gate 5 (`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`) — exit 0: `['R-1235', 'R-1246', 'R-1251', 'R-1252']`, exactly as ordered.

Gate 6 (`python3 -c "import packages.runtimes.dev_server as d, packages.runtimes.dev_server_ports as p; print(all(getattr(d, n) is getattr(p, n) for n in (...)))"`) — exit 0: `True`.

## Authored-text proofs

- `.agent/authored/f306-r1.md` against `block.md`: byte-equal, 124 lines, sha256 `c6668e5cfc087dba161c84f976c97328a62829d466502ad3e94208d282dae007` (confirmed independently and by Gate 1's "equal at F306 R1 C1 True .agent/authored/f306-r1.md").
- `docs/roadmap/STATUS.md` against `dry-STATUS.md`: byte-equal (Gate 1's corresponding line, sha256 `7857b15efe00f9d081835818b1f556ff7a7e0e60bceb6db21dfba69fdba2ed02`).
- `.agent/live_review.md` against `dry-live_review.md`: byte-equal (Gate 1's corresponding line, sha256 `c6d70b5ca636e37ac01088846b622a0ffc8a732ac41ef48c40b08e59f90d8821`).
- `.agent/decisions.md` against `dry-decisions.md`: byte-equal (Gate 1's corresponding line, sha256 `992fcd1f9393cc19669a01809078f52d090eac1b7ae05898e382a6441cf67a7b`).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (Gate 1's corresponding line, sha256 `0e517c1e9c4d5b5dfde833435e1cb53a3a91dee851f2ed15573f1041ab41b5c7`).
- `.agent/context.md` against `dry-context.md`: byte-equal (Gate 1's corresponding line, sha256 `3b533ca98336a113e81d7a3f96924a62def89eb38fba94ef32596f4f008d8e97`).
- `docs/roadmap/features/T2_F306.md` against `dry-T2_F306.md`: byte-equal (Gate 1's corresponding line, sha256 `98c2a6e8afdfdb5bec7136d4eb8ac9bb85c1fd84631b0689c5664feea8fe4a23`).

No other reviewer-authored text applied this round: C2 (the structural move) is this session's own write, proved by the gates above rather than by digest comparison to a prepared file.

## Deviations & assumptions

- **Branch-creation order.** The block's C0 step says to create the branch before any write. This session wrote C2's edits (the `dev_server.py` split) to the working tree while still on `main`, before running `git checkout -b`. Nothing was ever committed on `main`: `git rev-parse HEAD` stayed at `f51232ee2` throughout, and `git status --porcelain` was clean again (verified) the moment the C2 edits were stashed. The branch was then created and confirmed, C1 was committed first, and the stashed C2 edits were restored and committed second — so the final commit sequence matches the block exactly, but the session's editing order did not. Recorded here per the "any departure from the block's ordered sequence belongs here" rule, even though the commits themselves are in the right order and nothing unsafe happened.
- **Commit trailer model name.** The block (line 103) specifies the literal trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` for every commit. This session runs on the model named Sonnet 5 (stated directly by the environment's own system reminder), not Opus 5.5. Attributing the work to a model that did not do it would be a false record, and the standing operator instruction is that this trailer must name the model the worker actually runs on, never a fixed name typed into a block. All three commits in this round instead carry `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`. This is a deliberate, declared deviation from the block's literal text, not an oversight.
- **Ruff-driven re-export shape.** The first draft of C2 imported all five moved names (plus `DEFAULT_HOST`) in one plain `from packages.runtimes.dev_server_ports import (...)` statement. `ruff check` (run once, ad hoc, before staging — not counted as Gate 2, which ran once afterward and passed clean) flagged `pick_free_port` and `port_is_free` as F401 unused imports, because nothing left in `dev_server.py` calls them directly (only `choose_port`, which itself moved, used them) — but `tests/runtimes/test_dev_server.py` imports both by name from `packages.runtimes.dev_server`, so the block's "every existing `dev_server.<name>` keeps working" requirement still needs them re-exported. Fixed by splitting those two into explicit `name as name` self-import aliases, the same pattern already used in `packages/orchestration/ui_server.py` for `_build_project_summary_json`. `choose_port`, `http_probe`, `RuntimeProbeResult` and `DEFAULT_HOST` stay in the one plain import, since `dev_server.py`'s own remaining code still calls or uses them.
- **Line-count re-measurement.** Before the re-export shape above was finalized, the ledger row and `MAX_FILE_LINES` pin were provisionally set from a `wc -l` reading taken against an earlier draft of the import block (1985 lines). The explicit-alias fix added 4 lines. `tests/test_structure_ratchet.py::test_every_file_equals_its_row` (run directly, once, before staging) caught the mismatch immediately: `packages/runtimes/dev_server.py grew from 1985 to 1989 lines`. Both the ledger row and the `MAX_FILE_LINES` pin were corrected to the actual measured value (`1989`, pin `74301`, a 63-line drop from the original `2052`/`74364`) before anything was staged or committed; the test suite (run again, once) then passed clean. No incorrect value was ever committed.
- No extra commit, no dropped one, no reordering of the three commits themselves.

## For the operator, in plain sentences

This feature is the eighth rolling clean-up round, and this first working session claimed it,
recorded how the remaining work will be sliced, and made the one structural change this round
promised: a piece of the program that manages a project's own local preview server had grown large
enough that the project's own size rules asked for a cut, so the part that deals with network
ports and with checking whether that server is actually answering was moved into a file of its
own. Nothing about how that preview server behaves changed; the whole test collection still passes
exactly as it did before the move. Four small problems are still open and nothing new was added to
them. Three more pieces of clean-up work remain for later sessions, plus one problem that a current
permission restriction prevents this session from touching, which will be handed to whichever
session runs this clean-up next. Nothing waits on the operator right now.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. The Open PR Gate (none expected — this feature stays on its own branch with no PR this round).
3. The next round books round 1's verdict in its first commit.
4. T003: R-1251 (a port of its own per runtime-flow test, and the runner's refusal of a health answer from a process it did not start).

Operator questions open: 0.
Open findings: 4, all owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch `feature/f306-findings-paydown-v8` created from `f51232ee2`, confirmed before any commit |
| C1 | done | `2ef38daf2` |
| C2 | done | `74a408a49` |
| C3 | done | this commit |
| Gate 1 | passed | `ALL True` |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | exit 0, `3750 passed, 3 skipped`, no FAILED/ERROR/"process(es) behind" |
| Gate 4 | passed | six checks pass, `fail_count` 0 |
| Gate 5 | passed | `['R-1235', 'R-1246', 'R-1251', 'R-1252']` |
| Gate 6 | passed | `True` |
| Push | pending at write time | runs after this commit; result in the session's final reply |
