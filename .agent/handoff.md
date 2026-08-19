# Handback — F085 R65 (T003 remaining deny rows)
## Range
Review of e5eecb29..HEAD (C8 = this commit) · branch `feature/f085-sandbox-hardening` · base `e5eecb29` · open findings 147 · next free id R-0561.

## Commits
### fbef779d chore(f085): save the R65 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r65.md | +459/-0 | C0a — block saved byte-verbatim |
### 4b9aa98c chore(f085): mirror the R65 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +392/-423 | C0b — same bytes mirrored (numstat; the commit line reads +459/-490 under rewrite detection) |
### 73db31ec docs(f085): advance the plan to the R65 deny-row round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +7/-9 | C1 — PLAN19F→PLAN19T rewrite |
### 28a749e3 docs(f085): add checklist item 25 for destructive revert targets
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +10/-0 | C2 — CHECK25F→CHECK25T, lands before the record that cites it |
### 1439a831 docs(f085): record the R64 PASS and register R-0560
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +71/-0 | C3 — RECORD33 appended |
### aadcf5e1 feat(f085): deny the network for the dod-process row
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +5/-0 | C4 — DOD1 then DOD2 applied in order |
### 6b0edbef feat(f085): deny the network for the builder row
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/managed_builder_execution.py | +5/-0 | C5 — BUILD1 then BUILD2 applied in order |
### bf4c6645 test(f085): pin the dod-process row network posture
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +9/-0 | C6 — TESTDOD appended |
### a2aaff6d test(f085): pin the builder row network posture
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_managed_builder_execution.py | +14/-0 | C7 — TESTBUILDF→TESTBUILDT |
### C8 (this commit) docs(f085): write the R65 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C8 — a handoff cannot table the commit that writes it |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | |
| C8 | done | this commit |

## Verification
G1 STATE: `.agent/STOP` absent before C0a and again before C8 (`os.path.exists` False at both points); `git status --porcelain` empty at round start, after every commit, and after the G8 worktree was removed; `git worktree list` 1 line at round start and 1 line at the end.
G2 TRANSPORT: the committed `.agent/authored/f085-r65.md`, the committed `.agent/last_block.md`, BOTH working copies and the received `.remedy-wt/f085-r65.md` are all five byte-EQUAL — sha256 `f0fa416c8a4b343601435f75fb8f69a5c7e8f7198b7c433b4a9a9343ebd11399`, 31907 B, 459 lines, 32 marker lines on every copy; no digest fallback was needed. SIZE re-measured from the committed file: TOTAL 459 ≤ 490; PROSE 289 counting the 32 marker lines as prose (459 − 170 slice-content lines) ≤ 400; RECORD33 71 ≤ 140.
G3 SHAPES, one reading per pair, measured separately per path; every FROM occurred exactly 1x in its own pre-commit blob (measured at apply time, all seven). REWRITES, each FROM 0x and TO exactly 1x in the post-commit blob: PLAN19F→PLAN19T over `.agent/plan.md` at 73db31ec; CHECK25F→CHECK25T over `docs/agents/planner_reviewer_prompt.md` at 28a749e3; DOD1F→DOD1T and DOD2F→DOD2T over `packages/orchestration/exec_guard.py` at aadcf5e1; BUILD1F→BUILD1T and BUILD2F→BUILD2T over `packages/orchestration/managed_builder_execution.py` at 6b0edbef. APPEND-shaped: TESTBUILDF→TESTBUILDT over `tests/orchestration/test_managed_builder_execution.py` at a2aaff6d reads FROM exactly 1x AND TO exactly 1x post-commit, with NO FROM-zero reading taken — unattainable by construction. Re-applying each file's pairs IN ORDER to its pre-commit blob reproduces the post-commit blob BYTE-EXACTLY: True for all five paths. FROM-less appends, ordered equality on every clause — RECORD33 at 1439a831 over `.agent/live_review.md`: PREFIX True, SUFFIX True, `pre + slice == post` True, ADDED lines == slice lines IN ORDER True (71 == 71); TESTDOD at bf4c6645 over `tests/orchestration/test_exec_guard.py`: PREFIX True, SUFFIX True, `pre + slice == post` True, ADDED lines == slice lines IN ORDER True (9 == 9). numstat per path and commit: `7 9`, `10 0`, `71 0`, `5 0`, `5 0`, `9 0`, `14 0`. Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$`: 0 in each of the seven edited files.
G4 SUITES, all in the PRIMARY checkout, never a worktree, and run SERIALLY one pytest process at a time. `python3 -m pytest tests/orchestration/test_exec_guard.py tests/orchestration/test_test_runner.py tests/test_test_runner.py tests/orchestration/test_ci_run.py tests/orchestration/test_managed_builder_execution.py tests/orchestration/test_dod_runners.py -q -rf` → exit 0, `331 passed in 29.88s`, no skips (base 329; C6 and C7 add exactly one test each). `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → exit 0, `160 passed in 20.50s` (base 160). CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 22.07s` (base 42).
G5 PLAN CONTRACT on `.agent/plan.md` after C1: 40 lines ≤ 50, matching the block's projected 40; `## Goal` True, `## Next Steps` True, `\bF\d{3}\b` True.
G6 ARITHMETIC: at e5eecb29 — 174 registered / 28 done / 0 landed, 146 open, max registered R-0559, max resolved R-0558, 0 duplicate ids, 0 resolutions naming an unregistered id. At HEAD — 175 registered / 28 done / 0 landed, 147 open, max registered R-0560, max resolved still R-0558, 0 duplicate ids, 0 orphan resolutions. Symmetric differences: registered exactly `{R-0560}`, done EMPTY, landed EMPTY. Next free id R-0561.
G7 LINT, from the repository root with the repository's own configuration, no `--isolated`, over the four `.py` paths this round edits. `python3 -m ruff check packages/orchestration/exec_guard.py packages/orchestration/managed_builder_execution.py tests/orchestration/test_exec_guard.py tests/orchestration/test_managed_builder_execution.py` → exit 0, `All checks passed!`. The same four paths with `--preview` → exit 0, `All checks passed!`.
G8 RED CONTROL, only inside the disposable worktree `.remedy-wt/g8` at HEAD a2aaff6d, never in the primary checkout. The revert was applied as the DOD2T→DOD2F BYTE PAIR over the NAMED path `packages/orchestration/exec_guard.py`, in which the DOD2T bytes occur exactly 1x (measured in that file in that worktree before the replace — item 25 of the §3 checklist applied to this block's own control). Worktree `git diff --stat` = `1 file changed, 1 deletion(-)`, the hunk deleting `        deny_network=True,` from `dod_process_exec_policy` and nothing else. `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` → exit 1, `1 failed, 41 passed in 14.35s`. The one failing test in full: `tests/orchestration/test_exec_guard.py::test_the_dod_process_policy_denies_the_network_its_row_denies`, failing on its `assert policy.deny_network is True` line (`tests/orchestration/test_exec_guard.py:827`, `AssertionError: assert False is True … deny_network=False).deny_network`) — exactly the failure the block ordered, and the only one. Worktree removed and pruned; `git worktree list` back to 1 line and `git status --porcelain` empty in the primary checkout.
G9 HYGIENE, measured BEFORE C8: `git diff --name-only e5eecb29..HEAD` = `.agent/authored/f085-r65.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`, `packages/orchestration/exec_guard.py`, `packages/orchestration/managed_builder_execution.py`, `tests/orchestration/test_exec_guard.py`, `tests/orchestration/test_managed_builder_execution.py` — exactly the change set minus `.agent/handoff.md`, and it holds NONE of `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`, `apps/cli/commands/runtime_cmd.py`. `git ls-tree e5eecb29 -- <path>`, one call per path, returned a blob for all seven ordered paths — `packages/orchestration/exec_guard.py` `20e1c336`, `packages/orchestration/managed_builder_execution.py` `0d3767f2`, `tests/orchestration/test_exec_guard.py` `41ea7993`, `tests/orchestration/test_managed_builder_execution.py` `9135e85e`, `packages/runtimes/dev_server.py` `8def88af`, `packages/runtimes/runtime_supervisor.py` `f0d889d5`, `apps/cli/commands/runtime_cmd.py` `e047746a` — all seven exist. Per-commit insertions before C8: 459, 392, 7, 10, 71, 5, 5, 9, 14 — none exceeds 500, so the spent declared-oversize allowance is not touched; C8's own insertions go in the round report. Every commit single-parent.

## Authored-text proofs
All sixteen slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r65.md` by marker pair under the block's CONVENTION and applied byte-verbatim — `bytes.replace(FROM, TO)` for the seven FROM/TO pairs and `pre + slice` for RECORD33 and TESTDOD, with no joiner and no terminator byte added. Disk-to-disk: the received `.remedy-wt/f085-r65.md` matched the ordered sha256 `f0fa416c…` exactly at receipt (31907 B, 459 lines, 32 marker lines under `^(BEGIN|END)-[A-Z0-9]+$`), and all four G2 copies are byte-equal to it. No marker line reached any target file (G3 counts 0 in all seven).

## Deviations & assumptions
None. The ordered sequence C0a · C0b · C1 · C2 · C3 · C4 · C5 · C6 · C7 · C8 was followed exactly — no extra commit, none dropped, none reordered, and C2 landed before C3 as constraint 6 requires. The worker authored NO ledger text: RECORD33 was applied unedited, no `Landed:` line and no `Done:` paragraph were added, and every R64 reading RECORD33 states that this round could independently re-measure reproduces exactly (block sha256 `670a2563…`, 31314 B, 490 lines; per-commit insertions 490, 419, 12, 64, 39, 57, 32) — no disagreement to report. This handback is within the ≤100-line cap the >5-commit per-commit table allows, so no DECISION D15 stated-cause overage is declared.

## External actions
`git worktree add .remedy-wt/g8 HEAD` → exit 0; `git worktree remove --force .remedy-wt/g8` → exit 0; `git worktree prune` → exit 0. `git push -u origin feature/f085-sandbox-hardening` after C8 — outcome in the round report. No PR, no merge.

## Next
ONE: R66 writes T003's limitations document and its README link, stating what stage 1 does NOT prevent — a binary that ignores proxy variables reaches the network anyway, an app log written to a file takes no guard output cap, and the git, packaging and other classes never ran under the guard at all — after which the integration gate and closure follow.
TWO: R65 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R66 carries it.
THREE: Open findings: 147. Next free id: R-0561.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`.

Fortschritt: ~99 % (T001 gebaut · R13-R64 PASS · T002 KOMPLETT — alle vier Klassen migriert ·
T003 fast fertig: alle drei default-deny-Zeilen der D1-Tabelle sind verdrahtet und gepinnt, offen
bleibt allein das Limitations-Dokument mit seinem README-Link) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.
