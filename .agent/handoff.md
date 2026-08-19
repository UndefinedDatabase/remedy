# Handback — F085 R66 (T003 limitations document)
## Range
Review of 97caa9e1..HEAD (C5 = this commit) · branch `feature/f085-sandbox-hardening` · base `97caa9e1` · open findings 147 · next free id R-0561.

## Commits
### 23dfeb08 chore(f085): save the R66 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r66.md | +379/-0 | C0a — block saved byte-verbatim |
### 0d55eb26 chore(f085): mirror the R66 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +299/-379 | C0b — same bytes mirrored (`--numstat` reading) |
### 9cc64066 docs(f085): advance the plan to the R66 limitations-document round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +10/-10 | C1 — PLAN20F→PLAN20T rewrite |
### 70f09162 docs(f085): record the R65 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +51/-0 | C2 — RECORD34 appended |
### 69addbbf docs(f085): add the stage-1 execution guard limitations document
| Path | +/- | Reason |
|---|---|---|
| docs/system/exec-guard-limitations-v0.md | +71/-0 | C3 — DOCLIM written as the whole file, created |
### 5cc11db0 docs(f085): link the limitations document from both index tables
| Path | +/- | Reason |
|---|---|---|
| docs/README.md | +2/-0 | C4 — INDEX1F→INDEX1T then INDEX2F→INDEX2T |
### C5 (this commit) docs(f085): write the R66 handback
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

## External actions
No worktree was added or removed this round (none was ordered). `git push -u origin feature/f085-sandbox-hardening` after C5 — outcome in the round report. No PR, no merge.

## Verification
G1 STATE: `.agent/STOP` absent before C0a and again before C5 (`ls` reports "No such file or directory" at both points); `git status --porcelain` empty at round start and after every commit; `git worktree list` 1 line at round start and 1 line at the end — no worktree was created at all.
G2 TRANSPORT: the committed `.agent/authored/f085-r66.md`, the committed `.agent/last_block.md`, BOTH working copies and the received `.remedy-wt/f085-r66.md` are all five byte-EQUAL — sha256 `9a356739fc567d675cfb1a075b48b7916ad6c13fd4ad9eb587c8d216142000e6`, 26720 B, 379 lines, 16 marker lines on every copy; no digest fallback was needed. SIZE re-measured from the committed file: TOTAL 379 ≤ 490; PROSE 223 counting the 16 marker lines as prose (379 − 156 slice-content lines) ≤ 400; RECORD34 51 ≤ 140.
G3 SHAPES, one reading per pair, measured separately per path; every FROM occurred exactly 1x in its own pre-commit blob (measured at apply time, all three). REWRITES, each FROM 0x and TO exactly 1x in the post-commit blob: PLAN20F→PLAN20T over `.agent/plan.md` at 9cc64066 (`TO contains FROM: false`); INDEX1F→INDEX1T over `docs/README.md` at 5cc11db0 (`TO contains FROM: false`). APPEND-shaped: INDEX2F→INDEX2T over `docs/README.md` at that same commit reads `TO contains FROM: true`, FROM exactly 1x AND TO exactly 1x post-commit, with NO FROM-zero reading taken — unattainable by construction. Re-applying each file's pairs IN ORDER (both README pairs in order) to its pre-commit blob reproduces the post-commit blob BYTE-EXACTLY: True for both paths. FROM-less append, ordered equality on every clause — RECORD34 at 70f09162 over `.agent/live_review.md`: PREFIX True, SUFFIX True, `pre + slice == post` True, ADDED lines == slice lines IN ORDER True (51 == 51). WHOLE-FILE, no pre-image — DOCLIM at 69addbbf: `git ls-tree 97caa9e1 -- docs/system/exec-guard-limitations-v0.md` EMPTY, post-commit blob EQUALS the DOCLIM bytes exactly (sha256 `5c5bb0ca0793599731a5bf5882e5d56c9c6ca688db9aaaadff1c57126b393ce1`, 3644 B), ADDED lines == slice lines IN ORDER True (71 == 71). numstat per path and commit: `10 10`, `51 0`, `71 0`, `2 0`. Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$`: 0 in each of the four edited files.
G4 SUITES, all in the PRIMARY checkout, never a worktree, and run SERIALLY one pytest process at a time. `python3 -m pytest tests/docs/test_docs_consistency.py -q` → exit 0, `295 passed in 0.51s` (base 295). `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → exit 0, `160 passed in 20.52s` (base 160). CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 22.50s` (base 42).
G5 PLAN CONTRACT on `.agent/plan.md` after C1: 40 lines ≤ 50, matching the block's projected 40; `## Goal` True, `## Next Steps` True, `\bF\d{3}\b` True.
G6 ARITHMETIC: at 97caa9e1 — 175 registered / 28 done / 0 landed, 147 open, max registered R-0560, max resolved R-0558, 0 duplicate ids, 0 resolutions naming an unregistered id. At HEAD — IDENTICAL: 175 / 28 / 0, 147 open, max registered R-0560, max resolved R-0558, 0 duplicate ids, 0 orphan resolutions. All three symmetric differences EMPTY: registered `[]`, done `[]`, landed `[]`. Next free id R-0561.
G7 LINK INTEGRITY on `docs/README.md` after C4, all four readings: the string `system/exec-guard-limitations-v0.md` occurs EXACTLY 2 times; `docs/system/exec-guard-limitations-v0.md` resolves on disk at HEAD (True); that file is byte-identical to the DOCLIM slice (True, sha256 `5c5bb0ca…`); the quick-find row (INDEX1T's new line) occurs exactly 1x as a whole LINE and the system-table row (INDEX2T's new line) exactly 1x as a whole LINE.
G8 HYGIENE, measured BEFORE C5: `git diff --name-only 97caa9e1..HEAD` = `.agent/authored/f085-r66.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/README.md`, `docs/system/exec-guard-limitations-v0.md` — 6 paths, exactly the change set minus `.agent/handoff.md`, and it holds NO `.py` path at all (checked by suffix: False). `git ls-tree 97caa9e1 -- <path>`, one call per path, returned a blob for all four ordered paths — `packages/orchestration/exec_guard.py` `855655ce`, `packages/runtimes/dev_server.py` `8def88af`, `packages/runtimes/runtime_supervisor.py` `f0d889d5`, `apps/cli/commands/runtime_cmd.py` `e047746a` — all four exist and none is in the change set. Per-commit insertions before C5: 379, 299, 10, 51, 71, 2 — none exceeds 500, so the declared-oversize allowance spent at d4473f85 is not touched; C5's own insertions go in the round report. Every commit single-parent.

## Authored-text proofs
All eight slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r66.md` by marker pair under the block's CONVENTION and applied byte-verbatim — `bytes.replace(FROM, TO)` for the three FROM/TO pairs, `pre + slice` for RECORD34, and a straight whole-file write for DOCLIM, with no joiner and no terminator byte added. Disk-to-disk: the received `.remedy-wt/f085-r66.md` matched the ordered sha256 `9a356739…` exactly at receipt (26720 B, 379 lines, 16 marker lines under `^(BEGIN|END)-[A-Z0-9]+$`), and all four G2 copies are byte-equal to it. No marker line reached any target file (G3 counts 0 in all four).

## Deviations & assumptions
No commit deviation. The ordered sequence C0a · C0b · C1 · C2 · C3 · C4 · C5 was followed exactly — no extra commit, none dropped, none reordered, and C1 landed ahead of the record and both docs commits as constraint 5 requires. The worker authored NO ledger text: RECORD34 was applied unedited, no `Landed:` line and no `Done:` paragraph were added, and every R65 reading RECORD34 states that this round could independently re-measure reproduces exactly (175 / 28 / 0 and 147 open at 97caa9e1, max registered R-0560, max resolved R-0558; block sha256 `f0fa416c…`, 31907 B, 459 lines, 32 marker lines; `.agent/handoff.md` at 97caa9e1 90 lines) — no disagreement with RECORD34 to report.
DISAGREEMENT WITH DOCLIM, REPORTED PER CONSTRAINT 12 AND NOT EDITED. The section headed "Only three command classes run under the guard at all" appears FALSE at 5cc11db0 in three clauses. (a) Amendment F085 D1's table in `docs/roadmap/features/T2_F085.md` marks SIX classes `Stage 1 = yes` — `builder`, `test`, `dod-process`, `dod-app`, `runtime-server`, `runtime-build` — and THREE, not six, take `default-deny` in its network column; the document states the deny set as if it were the guarded set. (b) "Amendment F085 D1's table wires `builder`, `test` and `dod-process`" omits the other three rows that same table wires. (c) "The git, packaging, runtime and other call sites still spawn unsupervised" is false for `runtime` at 5cc11db0: `packages/orchestration/exec_guard.py` defines `runtime_build_exec_policy` and `runtime_server_exec_policy`, and they are called from `packages/orchestration/ui_server.py` (via `run_guarded_runtime_build_command`), `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py` and `apps/cli/commands/runtime_cmd.py`. `git`, `packaging` and `other` remain unsupervised, so only the `runtime` term of that list is wrong. No byte of DOCLIM was changed. The same conflation is carried by PLAN20T's "three classes of five run under the guard at all" in `.agent/plan.md`, which is likewise applied unedited.
This handback is 76 lines, within the ≤100-line cap the >5-commit per-commit table allows, so no DECISION D15 stated-cause overage is declared.

## Next
ONE: R67 measures T2_F085's remaining acceptance line — a network access from a guarded test command fails under deny — against a loopback server that is really listening, with the red control that line needs; the integration gate and closure follow it.
TWO: R66 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R67 carries it.
THREE: Open findings: 147. Next free id: R-0561.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`.

Fortschritt: ~99 % (T001 gebaut · R13-R65 PASS · T002 KOMPLETT · T003 fast fertig: alle drei
default-deny-Zeilen verdrahtet und gepinnt, das Limitations-Dokument steht und ist zweifach verlinkt;
offen bleibt allein die Akzeptanzmessung am echt lauschenden Server) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.
