# Handback — F085 R68 (ledger round, worker)

Branch `feature/f085-sandbox-hardening` · base SHA a8ba453d · head before C3 ea2a458f.

## Range

Review of a8ba453d..HEAD.

## Commits

### f7462027 docs(f085): save the R68 record block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r68.md | +344/-0 | C0a — block saved byte-verbatim |

### 5934347a docs(f085): mirror the R68 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +261/-303 | C0b — mirror of the authored block |

### e9d4eca6 docs(f085): advance the plan to the R68 ledger round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +5/-5 | C1 — PLAN22F→PLAN22T |

### ea2a458f docs(f085): record the R67 FAIL, resolve two findings and register the false sweep clause
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +88/-0 | C2 — RECORD36 appended: R67 entry, Done R-0561 and R-0562, registers R-0563, correction to RECORD35 |

### C3 — this commit (self-reference; a handoff cannot table the commit that writes it)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3 — this handback |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C3. No PR, no merge, no worktree add/remove.

## Verification

G1 STATE PASS. `.agent/STOP` absent on both re-reads (before C0a, before C3); `git status --porcelain` empty at round start and after each of the four commits before C3; `git worktree list` one line at start and one at the end — no worktree created, none ordered.
G2 TRANSPORT PASS. Received block digest verified before use. Committed `.agent/authored/f085-r68.md`, committed `.agent/last_block.md` and BOTH working copies: all four byte-EQUAL, sha256 f064a5dee523d030e4477585eea3e54fa31731e6741ad5ca1499fbae7c7cfcac, 27537 B, 344 lines, 6 marker lines each. Sizes read from the committed file: TOTAL 344 ≤ 490; slices PLAN22F 13 + PLAN22T 13 + RECORD36 88 = 114; PROSE 344 − 114 = 230 ≤ 400; RECORD36 88 ≤ 140.
G3 SHAPES PASS, measured separately per pair and per path. PLAN22F→PLAN22T on `.agent/plan.md` at e9d4eca6 is a REWRITE: `TO contains FROM: false`, FROM 1x pre-commit and 0x post-commit, TO exactly 1x post-commit, and re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit blob BYTE-EXACTLY (true). RECORD36 on `.agent/live_review.md` at ea2a458f — ordered equality on every clause: pre-commit blob is a byte-exact PREFIX (true), slice is an exact SUFFIX (true), `pre + slice` == post byte for byte (true), ADDED lines == slice lines IN ORDER (88 and 88); no FROM measured, none exists. numstat: e9d4eca6 `5 5 .agent/plan.md`; ea2a458f `88 0 .agent/live_review.md` — the deletion column for `.agent/live_review.md` at C2 is 0, which is constraint 6 read off the diff. Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$` at HEAD: `.agent/plan.md` 0, `.agent/live_review.md` 0.
G4 SUITES PASS — primary checkout, serially, one pytest process at a time, each exit 0. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → `160 passed in 20.32s`, exit 0. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 20.34s`, exit 0. Both counts equal their base readings.
G5 PLAN CONTRACT PASS. `.agent/plan.md` after C1 is 40 lines ≤ 50 (the block projected 40); contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true (`F085`).
G6 ARITHMETIC PASS. a8ba453d: 177 registered / 28 done / 0 landed, 149 open, max registered R-0562, max resolved R-0558, next free id R-0563. HEAD: 178 / 30 / 0, 148 open, max registered R-0563, max resolved R-0562, next free id R-0564. Registered symmetric difference EXACTLY {R-0563}; done symmetric difference EXACTLY {R-0561, R-0562}; landed symmetric difference EMPTY. Duplicate registration ids 0 and resolutions naming an unregistered id 0 at both SHAs. RECORD36 carries exactly one `- R-` line and exactly two `Done:` lines.
G7 TRUTH PASS — all four readings. READING A `git grep -n "spawn unsupervised" <sha> -- packages/ apps/ docs/ tests/`: exit 0 with EXACTLY 2 hits at a8ba453d and EXACTLY 2 at HEAD; the paths are exactly `docs/system/exec-guard-limitations-v0.md` (line 36) and `packages/orchestration/exec_guard.py` (line 20) at both SHAs — no third or fourth hit. READING B `git grep -ic "unsupervised" <sha> -- docs/agents/planner_reviewer_prompt.md`: NO MATCH at a8ba453d and at HEAD, exit code 1 with empty stdout at both. READING C at a8ba453d: `git grep -ic "unsupervised" -- packages/runtimes/dev_server.py` → `4`, exit 0 (NON-ZERO); `git grep -ic "spawn unsupervised" -- packages/runtimes/dev_server.py` → no match, exit 1, empty stdout. READING D: the string `and an example sentence in` occurs EXACTLY 1 time in `.agent/live_review.md` at a8ba453d and EXACTLY 1 time at HEAD — RECORD35's retracted clause is untouched on disk, which is constraint 6 proved rather than promised.
G8 HYGIENE PASS. `git diff --name-only a8ba453d..HEAD` measured BEFORE C3 is exactly `.agent/authored/f085-r68.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — the block's change set minus `.agent/handoff.md`, and nothing else; NO path under `packages/`, `apps/`, `docs/`, `tests/` or `scripts/` appears (empty list). Insertions per commit before C3: f7462027 344, 5934347a 261, e9d4eca6 5, ea2a458f 88 — none exceeds 500, so the spent oversize allowance is not touched. All four commits single-parent. C3's own numstat goes in the round report, since a commit cannot measure itself.

## Authored-text proofs

All three slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r68.md` by marker pair under the block's CONVENTION — bytes strictly between the marker lines, including the newline terminating the last content line — and applied with `bytes.replace` (PLAN22) and `pre + slice` (RECORD36), with no joiner and no terminator byte added. RECORD36 carries its own leading blank line, so the target's paragraph separation is measured bytes and not a reasoned join shape. Disk-to-disk comparison of the applied file against the committed authored file: EQUAL, sha256 f064a5de…7cfcac. Nothing was retyped, reflowed or re-wrapped; no marker line reached a target file (G3).

## Deviations & assumptions

NONE. No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3 were committed in exactly that order, with C1 the first substantive commit ahead of the record per constraint 5. No extra, dropped or reordered commit. No worktree created, no mutation, no revert and no red control ordered or invented (constraint 13). No ledger text authored by the worker and RECORD36 was applied byte-verbatim (constraint 8). Nothing already present in `.agent/live_review.md` at a8ba453d was edited, moved or deleted (constraint 6, proved by G3's PREFIX reading, the 0 deletion column and G7 reading D).
NO DISAGREEMENT to declare this round. Every RECORD36 claim the worker could re-measure independently reproduces: the R67 transport digest 8f1d0218…2a99db1 / 29948 B / 386 lines / 14 marker lines with authored and last_block byte-EQUAL at a8ba453d; RECORD35's 71 and 71 at 60057260; 175 / 28 / 0 and 147 open at 261dce53; `.agent/plan.md` 40 lines at a8ba453d; the new limitations heading, all six stage-1 class names, `SCOPE ruling` and `can hang` present and the old heading 0x at a8ba453d; the retired `exec_guard` sentence 0x with `runtime_server_exec_policy` and `run_guarded_runtime_build_command` present at a8ba453d. On R-0563's own evidence: `unsupervised` matches 4 LINES in `packages/runtimes/dev_server.py` at a8ba453d (5 raw occurrences — line 1043 is `OWNER_UNSUPERVISED = "unsupervised"`, two on one line), and every one of them belongs to the `OWNER_UNSUPERVISED` constant or its literal value, so RECORD36's characterisation holds exactly.

## Next

FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk` — ahead of the PR Gate.
ONE: R69 measures T2_F085's remaining acceptance line — a network access from a guarded test command fails under deny — against a loopback server that is really listening, with the red control that line needs; the integration gate and closure follow it.
TWO: R68 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4 item 13); R69 carries it, and R69's record is also where R-0563 is marked `Done:` if the reviewer's re-reading of the appended correction agrees.
THREE: 148 findings open; next free id R-0564.
Fortschritt: ~99 % (T001 gebaut · R13-R65 PASS · R66 und R67 FAIL, beide Fehler des Reviewers, beide
in der jeweils nächsten Runde repariert · T002 KOMPLETT · T003 fast fertig: Netz-Posture verdrahtet
und gepinnt, Limitations-Dokument steht, verlinkt und inhaltlich korrekt; offen bleibt allein die
Akzeptanzmessung am echt lauschenden Server) — Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

Deviations, declared (DECISION D15 stated-cause overage): this handback is 80 lines against the 60-line cap. The mandated content behind the overage is the per-commit changed-files tables for five commits, the item-status table, and the eight gate transcripts G1-G8 with their exit codes — G3, G6, G7 and G8 each carry multi-clause readings the block orders reported individually. No section was dropped.
