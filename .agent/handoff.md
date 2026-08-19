# Handback — F085 R64 (T003 network posture)
## Range
Review of e26f1f3e..HEAD (C5 = this commit) · branch `feature/f085-sandbox-hardening` · base `e26f1f3e` · open findings 146 · next free id R-0560.

## Commits
### e96bd9e5 docs(f085): save the R64 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r64.md | +490/-0 | C0a — block saved byte-verbatim |
### 05ae9186 docs(f085): mirror the R64 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +419/-302 | C0b — same bytes mirrored |
### a8877d26 docs(f085): advance the plan to the R64 network-posture round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-9 | C1 — PLAN18F→PLAN18T rewrite |
### 2e6b772e docs(f085): record the R63 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +64/-0 | C2 — RECORD32 appended |
### 01fd653d feat(f085): give the guard a network posture and set it for the test class
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +39/-1 | C3 — GUARD1..GUARD6 applied in order |
### 25c75325 test(f085): pin the network posture at the guard and at a real child
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +57/-0 | C4 — TESTNET appended |
### C5 (this commit) docs(f085): write the R64 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — a handoff cannot table the commit that writes it |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## Verification
G1 STATE: `.agent/STOP` absent before C0a and again before C5 (`ls` → "No such file or directory" at both points); `git status --porcelain` empty at round start, after every commit, and after the G8 worktree was removed; `git worktree list` 1 line at round start and 1 line at the end.
G2 TRANSPORT: committed `.agent/authored/f085-r64.md`, committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL — sha256 `670a2563e54daff38b815a445493dba8b417024e65c5eba4e0b9cbcdb8ae2108`, 31314 B, 490 lines, 32 marker lines on every copy, and equal to the received `.remedy-wt/f085-r64.md` as well. SIZE from the committed file: TOTAL 490 ≤ 490; PROSE 274 counting the 32 marker lines as prose (490 − 216 slice-content lines) ≤ 400; RECORD32 64 ≤ 140. All three agree with constraint 9.
G3 SHAPES, one reading per pair, measured separately per path. PLAN18F→PLAN18T, REWRITE over `.agent/plan.md` at a8877d26: `TO contains FROM` False, FROM 1x in the pre-commit blob, FROM 0x and TO exactly 1x in the post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit blob BYTE-EXACTLY (True). Over `packages/orchestration/exec_guard.py` at 01fd653d, each FROM 1x in the pre-commit blob: GUARD1 REWRITE (`TO contains FROM` False) FROM 0x / TO 1x post; GUARD6 REWRITE (False) FROM 0x / TO 1x post; GUARD2, GUARD3, GUARD4 and GUARD5 are APPEND-shaped (`TO contains FROM` True for all four) and read FROM exactly 1x AND TO exactly 1x in the post-commit blob, with no FROM-zero reading taken, unattainable by construction. All six GUARD pairs re-applied IN ORDER to the pre-commit blob reproduce the post-commit blob BYTE-EXACTLY (True). RECORD32 at 2e6b772e over `.agent/live_review.md` (no FROM): PREFIX True, SUFFIX True, `pre + slice == post` True, ADDED lines == slice lines IN ORDER True (64 == 64). TESTNET at 25c75325 over `tests/orchestration/test_exec_guard.py` (no FROM): PREFIX True, SUFFIX True, `pre + slice == post` True, ADDED lines == slice lines IN ORDER True (57 == 57). numstat: `12 9`, `64 0`, `39 1`, `57 0`. Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$`: 0 in each of the four edited files.
G4 SUITES, all in the PRIMARY checkout, never a worktree, and run SERIALLY one pytest process at a time. `python3 -m pytest tests/orchestration/test_exec_guard.py tests/orchestration/test_test_runner.py tests/test_test_runner.py tests/orchestration/test_ci_run.py tests/orchestration/test_managed_builder_execution.py tests/orchestration/test_dod_runners.py -q -rf` → exit 0, `329 passed in 30.20s`, no skips (base 324; C4 adds exactly the five TESTNET tests). `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → exit 0, `160 passed in 20.07s` (base 160). CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.47s` (base 42).
G5 PLAN CONTRACT on `.agent/plan.md` after C1: 42 lines ≤ 50, matching the projected 42; `## Goal` True, `## Next Steps` True, `\bF\d{3}\b` True.
G6 ARITHMETIC: at e26f1f3e — 174 registered / 28 done / 0 landed, 146 open, max registered R-0559, max resolved R-0558, 0 duplicate ids, 0 resolutions naming an unregistered id. At HEAD — IDENTICAL on all eight readings. Symmetric differences: registered `set()`, done `set()`, landed `set()`, all EMPTY. Next free id R-0560.
G7 LINT, from the repository root with the repository's own configuration, no `--isolated`. `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` → exit 0, `All checks passed!`. `python3 -m ruff check --preview packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` → exit 0, `All checks passed!`.
G8 RED CONTROL, only inside the disposable worktree `.remedy-wt/rv64` at HEAD 25c75325, never in the primary checkout. Reverted EXACTLY the one line `        deny_network=True,` in `test_command_exec_policy` by deleting it (worktree `git diff --stat` = `1 file changed, 1 deletion(-)` and the hunk holds that line alone), then `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` → exit 1, `2 failed, 39 passed in 14.25s`. Both failing tests in full: `tests/orchestration/test_exec_guard.py::test_the_test_class_policy_denies_the_network_its_row_denies`, which fails on its `assert policy.deny_network is True` line (`tests/orchestration/test_exec_guard.py:806`, `AssertionError: assert False is True … deny_network=False).deny_network`) — the failure the block ordered — and `tests/orchestration/test_exec_guard.py::test_a_denied_child_really_receives_the_closed_port`, which fails on `assert dumped["HTTP_PROXY"] == exec_guard.DENIED_NETWORK_PROXY_URL` (`tests/orchestration/test_exec_guard.py:818`, `KeyError: 'HTTP_PROXY'`). The block ordered the first "among the failures", so the second is reported rather than treated as a deviation: it is the real-child half of the same one-line revert. Worktree removed and pruned; `git worktree list` back to 1 line and `git status --porcelain` empty in the primary checkout.
G9 HYGIENE, measured BEFORE C5: `git diff --name-only e26f1f3e..HEAD` = `.agent/authored/f085-r64.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/exec_guard.py`, `tests/orchestration/test_exec_guard.py` — exactly the change set minus `.agent/handoff.md`, and it holds NONE of `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`, `apps/cli/commands/runtime_cmd.py`. `git ls-tree e26f1f3e -- <path>`, one call per path, returned a blob for all five ordered paths: `packages/orchestration/exec_guard.py` `e0f0d4ea`, `tests/orchestration/test_exec_guard.py` `54fb38d0`, `packages/runtimes/dev_server.py` `8def88af`, `packages/runtimes/runtime_supervisor.py` `f0d889d5`, `apps/cli/commands/runtime_cmd.py` `e047746a` — all five exist. Per-commit insertions before C5: 490, 419, 12, 64, 39, 57 — none exceeds 500; C5's own insertions go in the round report. Every commit single-parent.

## Authored-text proofs
All ten slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r64.md` by marker pair under the block's CONVENTION and applied byte-verbatim — `bytes.replace(FROM, TO)` for PLAN18 and GUARD1..GUARD6, `pre + slice` for RECORD32 and TESTNET, with no joiner and no terminator byte added. Disk-to-disk: the received `.remedy-wt/f085-r64.md` matched the ordered sha256 `670a2563…` exactly at receipt (31314 B, 490 lines, 32 marker lines), and all four G2 copies are byte-equal to it; no digest fallback was needed. No marker line reached any target file (G3 counts 0 in all four).

## Deviations & assumptions
The ordered sequence C0a · C0b · C1 · C2 · C3 · C4 · C5 was followed exactly — no extra commit, none dropped, none reordered. The worker authored no ledger text: RECORD32 was applied unedited, no `Landed:` line and no `Done:` paragraph were added, and every reading RECORD32 states that this round could independently re-measure agrees with what was measured here — no disagreement to report. One measurement is reported rather than deviated: G8's one-line revert reddens TWO tests, not one, and the block named only the first as mandatory. This handback is within the ≤100-line cap that the >5-commit per-commit table allows, so no DECISION D15 stated-cause overage is declared.

## External actions
`git worktree add .remedy-wt/rv64 HEAD --detach` → exit 0; `git worktree remove --force .remedy-wt/rv64` → exit 0; `git worktree prune` → exit 0. `git push -u origin feature/f085-sandbox-hardening` after C5 — outcome in the round report. No PR, no merge.

## Next
ONE: R65 wires the remaining deny rows — `dod_process_exec_policy` in `packages/orchestration/exec_guard.py` and the builder policy in `packages/orchestration/managed_builder_execution.py` — each with the seam test its own class already has; T003's limitations document and its README link follow.
TWO: R64 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R65 carries it.
THREE: Open findings: 146. Next free id: R-0560.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`.

Fortschritt: ~99 % (T001 gebaut · R13-R63 PASS · T002 KOMPLETT — alle vier Klassen migriert ·
T003 begonnen: die Netz-Policy steht im Guard und die `test`-Klasse verweigert das Netz, die
restlichen deny-Zeilen und das Limitations-Dokument sind offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.
