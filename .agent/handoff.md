# Handback — F058 round 8: book round 7, merge main after pull request 331, repair R-1264 and R-1265

## Session

SESSION 4 of feature F058 · round 8 · rounds so far 8

This round booked round 7 (stopped after its evidence job), merged `main` after pull request 331
into the branch in one merge commit per DECISION F058 D5, and repaired the two guards that merge
turned red: R-1264 (the structure ratchet, a structural move only) and R-1265 (the `--host` help's
retired word). Context self-assessment: every prepared-file digest, every expected script output
and every gate matched the block exactly, with no deviation and no improvisation needed.

Fortschritt: ~92 % (T001 to T003 and the documentation done, main merged in, R-1264 and R-1265 repaired · the one full suite, the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `1a20f8f37`..HEAD (round 8: C1 to C5; this handback is C5).

## Commits

### 215bf2dd6 F058 R8 C1: book round 7, register R-1264 and R-1265, DECISION F058 D5, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f058-r8.md` | +126/-0 | NEW FILE, byte copy of the round 8 block |
| `.agent/context.md` | +2/-1 | notes `main`'s merge-in |
| `.agent/decisions.md` | +12/-0 | DECISION F058 D5 |
| `.agent/live_review.md` | +6/-0 | `Gate: F058 R7` (STOPPED), R-1264 and R-1265 minted |
| `.agent/plan.md` | +10/-7 | round 8's plan |

### 431d9776d F058 R8 C2: merge main after pull request 331 into the branch

Two-parent merge commit (parents `215bf2dd6`, `2b7c6b7df`). `git show --numstat` on the merge
equals `git diff --numstat 215bf2dd6 431d9776d` exactly (checked; identical lines both ways), so
every line below is `main`'s own work carried in by the merge, not this round's:

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +3/-0 | `resolve_decisions.py` kept both sides' DECISION entries, branch first |
| `apps/cli/command_catalog.py` | +2/-2 | pull request 331's LAN wording |
| `apps/cli/commands/ui.py` | +2/-2 | pull request 331 |
| `docs/guides/environment.md` | +1/-1 | pull request 331 |
| `docs/system/architecture.md` | +1/-1 | pull request 331 |
| `docs/system/operator-cockpit-v1.md` | +5/-2 | pull request 331 |
| `packages/orchestration/config.py` | +5/-1 | pull request 331, merged by content with this branch's earlier key move |
| `packages/orchestration/ui_server.py` | +59/-15 | pull request 331's LAN bind/URL logic |
| `tests/regression/test_named_bugs.py` | +7/-5 | pull request 331 |
| `tests/ui_server/test_dashboard_contract.py` | +16/-14 | pull request 331 |
| `tests/ui_server/test_live_state.py` | +5/-5 | pull request 331 |

`.agent/context.md`, `.agent/plan.md` and `.agent/handoff.md` carried no diff against C1 (`--ours`
resolved them to the branch's own text already committed in C1); they are not in the table above
because the merge introduced no change to them.

### 43ad33712 F058 R8 C3: repair R-1264 (the UI keys and the server launch helpers move out, structural)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +6/-3 | the ledger rows for `config.py`/`ui_server.py` lowered, step (4) noted |
| `packages/orchestration/config.py` | +2/-33 | the three `ui.*` keys spliced out |
| `packages/orchestration/config_keys_ui.py` | +46/-0 | NEW FILE, `UI_KEY_SPECS`, moved unchanged |
| `packages/orchestration/ui_server.py` | +15/-78 | the launch helpers moved out; `start_ui_server` now calls them by name |
| `packages/orchestration/ui_server_launch.py` | +96/-0 | NEW FILE, the moved helpers plus `_ui_session_info` and `_print_ui_urls` |
| `tests/orchestration/import_reachability_allowlist.txt` | +2/-0 | both new modules added |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 74440 → 74394 |
| `tests/ui_server/test_dashboard_contract.py` | +2/-1 | the loopback-hosts pin follows `_UI_LOOPBACK_HOSTS` into `ui_server_launch.py` |

### b330202ee F058 R8 C4: repair R-1265 (the host option's help loses a retired word)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +1/-1 | `ui.start --host` help: "loopback" → "127.0.0.1" |

### (this commit) F058 R8 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this handback |

## External actions

None through C5. Immediately after this commit the round pushes
`git -C /home/decodeux/Repos/remedy push origin feature/f058-model-failover-chain`; its output is
reported in this session's final reply, not re-entered here (write-once rule).

## Verification

Preconditions, before any write: `git branch --show-current` → `main`; `git status --porcelain` →
empty; `.agent/STOP` absent; `gh pr list --state open --json number` → `[]`. After checkout:
`git rev-parse HEAD` and `git rev-parse origin/feature/f058-model-failover-chain` both
`1a20f8f37815a1582fc52238a259073eb6b86c5d`; `git log -1 --format=%H main` →
`2b7c6b7df92d5417f81c2008513f38d7d6b4c3f0`.

Gates, run after C4, before C5:

1. `git -C /home/decodeux/Repos/remedy status --porcelain` — exit 0, empty output.
2. `python3 .remedy-wt/f058-r8/prep/compare_sim.py /home/decodeux/Repos/remedy` — exit 0:
   ```
   C1 215bf2dd6113346e6832890081a78f99db370af3 ['.agent/authored/f058-r8.md'] True
   C2 431d9776da905c552809146845331ae74071820f ['.agent/authored/f058-r8.md'] True
   C3 43ad33712f6d5d102db05e66f814d2afef3d5b61 ['.agent/authored/f058-r8.md'] True
   C4 b330202ee01bb305aaec516c77074a21c4cfbe1e ['.agent/authored/f058-r8.md'] True
   C2 parents ['215bf2dd6113346e6832890081a78f99db370af3', '2b7c6b7df92d5417f81c2008513f38d7d6b4c3f0'] second is main True
   ALL True
   ```
3. `python3 -m ruff check packages/orchestration/config.py packages/orchestration/config_keys_ui.py packages/orchestration/ui_server.py packages/orchestration/ui_server_launch.py apps/cli/command_catalog.py tests/test_structure_ratchet.py tests/ui_server/test_dashboard_contract.py`
   — exit 0, `All checks passed!`.
4. `python3 .remedy-wt/f058-r8/prep/run_selection.py /home/decodeux/Repos/remedy .remedy-wt/f058-r8-worker/selection-output.txt`
   — exit 0, `4974 passed, 9 skipped in 100.40s (0:01:40)`, no FAILED/ERROR line, no
   "process(es) behind" line. SKIPPED lines, all pre-existing quarantines/opt-ins, none new:
   - `tests/test_agent_tooling.py:43` — D12 quarantine (F252)
   - `tests/regression/test_named_bugs.py:295,312,321,385,394,401` (6 lines) — D3 quarantine (F252)
   - `tests/test_install_smoke.py:175` — opt-in, needs `REMEDY_INSTALL_SMOKE=1`
   - `tests/test_repair_context_reviewer_memory.py:257` — UI source not found
5. `python3 -m apps.cli.main integrity check --json` — exit 0, `"fail_count": 0, "ok": true,
   "passed": true`.
6. `python3 .remedy-wt/f058-r8/prep/open_set.py /home/decodeux/Repos/remedy` — exit 0:
   `['R-1235', 'R-1246', 'R-1251', 'R-1252', 'R-1264', 'R-1265']`.

All six gates passed; nothing red.

## Authored-text proofs

`.agent/authored/f058-r8.md`, committed in C1, is a byte copy of the reviewer's prepared
`block.md`: `wc -l` 126, `sha256sum ba74fa953c249af1727bb72e9c1f3ead834497b9b33a6ed2e28268c3452b1cad`,
equal to the digest named in the delivering prompt. Gate 2 (`compare_sim.py`) additionally checked
this same file byte-equal across all four commits C1 to C4 (`True` on every line, `ALL True`). The
four state-file copies of C1 (`dry-live_review.md`, `dry-decisions.md`, `dry-context.md`,
`dry-plan.md` onto their `.agent/` targets) were each verified with `cmp`, which printed nothing on
all four, before staging.

## Deviations & assumptions

None. Every prepared-file digest matched, every script's output matched the block's stated exact
text, every conflict and status listing named exactly the paths the block predicted, and all six
gates passed on the first run.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. Phase 1 rule 2, the Open PR Gate: none expected (this round opens no pull request).
3. The next round's first commit books round 8's verdict.
4. Then the closure's one full suite on the merged tree, its CPU cost, the staging reclaim, the
   evidence job and the review package.

Operator questions open: 1.
Open findings: 6 — R-1235, R-1246, R-1251 and R-1252, owned by F306; R-1264 and R-1265, owned by
F058 and repaired in this round.

## For the operator, in plain sentences

The cockpit's home-network change was merged first, as the waiting question recommended. It had
made two automatic checks fail: one that keeps large program files from growing, and one that
keeps retired words out of the command help. So this round moved the cockpit's start-up helpers
and three of its settings into small files of their own without changing what they do, and
reworded one line of help for the cockpit's host option so that it no longer contains the retired
word. The failover feature was then brought up to date with that change. The full test collection
runs once more next, then the feature closes.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five paths byte-equal/empty-cmp to the prepared files |
| C2 | done | merge commit, conflicts in exactly the four expected files, resolved as ordered |
| C3 | done | eight paths, exact expected transform output |
| C4 | done | one path, exact expected transform output |
| C5 | done | this handback |
| Gate 1 | passed | `status --porcelain` empty |
| Gate 2 | passed | `ALL True` |
| Gate 3 | passed | `All checks passed!` |
| Gate 4 | passed | exit 0, 4974 passed, 9 skipped, no FAILED/ERROR |
| Gate 5 | passed | `fail_count` 0 |
| Gate 6 | passed | exact open-finding set |
| R-1264 | done | structural move, repaired this round |
| R-1265 | done | help text reworded, repaired this round |
