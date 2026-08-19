# Handback — F085 R63 (T002e final call site)
## Range
Review of cbe1b3e5..HEAD (C5 = this commit) · branch `feature/f085-sandbox-hardening` · base `cbe1b3e5` · open findings 146 · next free id R-0560.

## Commits
### 28dd3923 docs(f085): save the R63 call-site block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r63.md | +373/-0 | C0a — block saved byte-verbatim |
### 9a8e3161 docs(f085): mirror the R63 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +287/-170 | C0b — same bytes mirrored |
### 87c467db docs(f085): advance the plan to the R63 call-site round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +6/-11 | C1 — PLAN17F→PLAN17T rewrite |
### 1d1c6abc docs(f085): record the R62 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +39/-0 | C2 — RECORD31 appended |
### a045970b feat(f085): migrate the runtime-server CLI call site onto plan_child_spawn
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/runtime_cmd.py | +18/-1 | C3 — SITE4F→SITE4T rewrite in `_serve_supervisor` |
### 394c45af test(f085): pin the supervisor env handover at the Popen seam
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_runtime_cmd.py | +42/-0 | C4 — TESTCLI appended |
### C5 (this commit) docs(f085): write the R63 handback
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
G1 STATE: `.agent/STOP` absent before C0a and again before C5 (`os.path.exists` False at both points); `git status --porcelain` empty at round start, after every commit, and after the G8 worktree was removed; `git worktree list` 1 line at round start and 1 line at the end.
G2 TRANSPORT: committed `.agent/authored/f085-r63.md`, committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL — sha256 `b9230558fafe431bc69a62dadd059d93c1977510d53baceb817e7ef0a71c1d29`, 26177 B, 373 lines, 12 marker lines on every copy. SIZE from the committed file: TOTAL 373 ≤ 490; PROSE 226 counting the 12 marker lines as prose (214 without them) ≤ 400; RECORD31 39 ≤ 140. All three agree with constraint 9.
G3 SHAPES, one reading per pair. PLAN17F→PLAN17T, REWRITE over `.agent/plan.md` at 87c467db: `TO contains FROM` False, FROM 1x in the pre-commit blob, FROM 0x and TO exactly 1x in the post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit blob BYTE-EXACTLY (True). SITE4F→SITE4T, REWRITE over `apps/cli/commands/runtime_cmd.py` at a045970b: same five readings, `TO contains FROM` False, FROM 1x pre, FROM 0x / TO 1x post, byte-exact reproduction True. RECORD31 at 1d1c6abc over `.agent/live_review.md` (no FROM): PREFIX True, SUFFIX True, `pre + slice == post` True, ADDED lines == slice lines IN ORDER True (39 == 39). TESTCLI at 394c45af over `tests/cli/test_runtime_cmd.py` (no FROM): PREFIX True, SUFFIX True, `pre + slice == post` True, ADDED lines == slice lines IN ORDER True (42 == 42). numstat: `6 11`, `39 0`, `18 1`, `42 0`. Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$`: 0 in each of the four edited files.
G4 SUITES, all in the PRIMARY checkout, never a worktree. `python3 -m pytest tests/runtimes/ tests/cli/test_runtime_cmd.py tests/orchestration/test_exec_guard.py -q -rf` → exit 0, `305 passed in 234.31s`, no skips (base 304; C4 adds exactly one test). `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → exit 0, `160 passed in 19.80s` (base 160). CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.62s` (base 42).
G5 PLAN CONTRACT on `.agent/plan.md` after C1: 39 lines ≤ 50, matching the projected 39; `## Goal` True, `## Next Steps` True, `\bF\d{3}\b` True.
G6 ARITHMETIC: at cbe1b3e5 — 174 registered / 28 done / 0 landed, 146 open, max registered R-0559, max resolved R-0558, 0 duplicate ids, 0 resolutions naming an unregistered id. At HEAD — IDENTICAL on all eight readings. Symmetric differences: registered `[]`, done `[]`, landed `[]`, all EMPTY. Next free id R-0560.
G7 LINT, from the repository root with the repository's own configuration, no `--isolated`. `python3 -m ruff check apps/cli/commands/runtime_cmd.py tests/cli/test_runtime_cmd.py` → exit 0, `All checks passed!`. `python3 -m ruff check --preview apps/cli/commands/runtime_cmd.py tests/cli/test_runtime_cmd.py` → exit 0, `All checks passed!`.
G8 RED CONTROL, only inside the disposable worktree `.remedy-wt/g8` at HEAD 394c45af, never in the primary checkout. Reverted EXACTLY the one line `cwd=spawn_plan.cwd, env=spawn_plan.env,` to `cwd=str(source_root), env=env,` (worktree `git diff` shows that single-line hunk and nothing else), then `python3 -m pytest tests/cli/test_runtime_cmd.py -q -rf` → exit 1, `1 failed, 16 passed in 7.18s`. The failure is `tests/cli/test_runtime_cmd.py::TestTheSupervisorEnvironmentIsScrubbed::test_a_secret_parent_variable_never_reaches_the_supervisor` on its `assert "ANTHROPIC_API_KEY" not in env` line (`tests/cli/test_runtime_cmd.py:292`, `AssertionError: assert 'ANTHROPIC_API_KEY' not in {..., 'ANTHROPIC_API_KEY': 'sk-must-not-travel', ...}`), with the other 16 tests in that file still passing. Worktree removed and pruned; `git worktree list` back to 1 line and `git status --porcelain` empty in the primary checkout.
G9 HYGIENE, measured BEFORE C5: `git diff --name-only cbe1b3e5..HEAD` = `.agent/authored/f085-r63.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `apps/cli/commands/runtime_cmd.py`, `tests/cli/test_runtime_cmd.py` — exactly the change set minus `.agent/handoff.md`, and it holds NEITHER `packages/runtimes/dev_server.py` NOR `packages/runtimes/runtime_supervisor.py`. `git ls-tree cbe1b3e5 -- <path>` returned a blob for each of the four ordered paths: `apps/cli/commands/runtime_cmd.py` `01ab65ed`, `tests/cli/test_runtime_cmd.py` `d427ffc0`, `packages/runtimes/dev_server.py` `8def88af`, `packages/runtimes/runtime_supervisor.py` `f0d889d5` — all four exist. Per-commit insertions before C5: 373, 287, 6, 39, 18, 42 — none exceeds 500; C5's own insertions go in the round report. Every commit single-parent.

## Authored-text proofs
All six slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r63.md` by marker pair under the block's CONVENTION and applied byte-verbatim — `bytes.replace(FROM, TO)` for PLAN17 and SITE4, `pre + slice` for RECORD31 and TESTCLI, with no joiner and no terminator byte added. Disk-to-disk: the received `.remedy-wt/f085-r63.md` matched the ordered sha256 `b9230558…` exactly at receipt, and all four G2 copies are byte-equal; no digest fallback was needed. No marker line reached any target file (G3 counts 0 in all four).

## Deviations & assumptions
The ordered sequence C0a · C0b · C1 · C2 · C3 · C4 · C5 was followed exactly — no extra commit, none dropped, none reordered. The worker authored no ledger text: RECORD31 was applied unedited, no `Landed:` line and no `Done:` paragraph were added, and every reading RECORD31 states that this round could independently re-measure agrees with what was measured here — no disagreement to report. This handback is within the ≤100-line cap that the >5-commit per-commit table allows, so no DECISION D15 stated-cause overage is declared.

## External actions
`git worktree add .remedy-wt/g8 HEAD` → exit 0; `git worktree remove --force .remedy-wt/g8` → exit 0; `git worktree prune` → exit 0. `git push -u origin feature/f085-sandbox-hardening` after C5 — outcome in the round report. No PR, no merge.

## Next
ONE: T002e is COMPLETE — all three `runtime-server` call sites now take `plan_child_spawn` — so the next round is R64, which starts T003: the network posture, the limitations document and its README link. That document must state what the CHILD-half migrations do NOT bound, naming both cases the R62 plan already recorded: an app log written to a file takes no guard output cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
TWO: R63 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R64 carries it.
THREE: Open findings: 146. Next free id: R-0560.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`.

Fortschritt: ~99 % (T001 gebaut · R13-R62 PASS · T002a-T002d KOMPLETT · T002e KOMPLETT — die
`runtime-server`-Policy gebaut und ALLE drei Call-Sites migriert, die letzte mit einem
Popen-Seam-Test gepinnt, der ohne den Scrub rot wird · T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.
