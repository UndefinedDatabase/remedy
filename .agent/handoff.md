# Handback — F085 R60 (record round, no code)

Feature F085 · Round R60 · Branch `feature/f085-sandbox-hardening` · Base `d91d2ffa`

## Range
Review of d91d2ffa..a567afe3

## Commits
### 3948529b docs(f085): save the R60 record-round block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r60.md | +253/-0 | C0a — block saved byte-verbatim |

### 0bf99f9a docs(f085): mirror the R60 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +171/-365 | C0b — same bytes mirrored |

### ac7f5ac5 docs(f085): advance the plan to the R60 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +6/-6 | C1 — PLAN14F→PLAN14T rewrite |

### a567afe3 docs(f085): record the R59 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +47/-0 | C2 — RECORD28 appended at EOF |

### C3 (this commit — self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3 — this handback; a handoff cannot table its own commit |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C3. No PR, no merge, no worktree add/remove, no gh command.

## Verification
G1 STATE — exit 0. `.agent/STOP` absent before C0a and again before C3; `git status --porcelain` empty at round start and after every commit; `git worktree list` exactly one line at round start and at the end, none created in between.
G2 TRANSPORT — exit 0. Five copies BYTE-EQUAL disk-to-disk (no digest fallback): `.remedy-wt/f085-r60.md`, committed and working `.agent/authored/f085-r60.md`, committed and working `.agent/last_block.md` — each sha256 `ec373c9c3df936db9dd595afa7799255e80649b84b0212e93ca43f0e8678aa47`, 19312 B, 253 lines, 6 marker lines.
G3 SHAPES — exit 0. PLAN14F→PLAN14T is a REWRITE: `TO contains FROM: false`, FROM 1x pre-commit and 0x post-commit, TO exactly 1x post-commit; re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit blob BYTE-EXACTLY; numstat `6 6`. RECORD28 has no FROM and satisfies ordered equality: pre-commit blob is a byte-exact PREFIX, slice an exact SUFFIX, `pre + slice` equals the post-commit blob byte for byte, and the commit's ADDED lines are exactly the slice's 47 lines IN ORDER; numstat `47 0`. Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$` = 0 in both slice targets (`.agent/plan.md`, `.agent/live_review.md`).
G4 SUITES — both exit 0, PRIMARY checkout. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → `160 passed in 19.85s`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 20.46s`. Both equal the base readings, unchanged as ordered.
G5 PLAN CONTRACT — exit 0. `.agent/plan.md` after C1 is 45 lines (≤50, and the figure the block projected); `## Goal` present true, `## Next Steps` present true, `\bF\d{3}\b` matches true.
G6 ARITHMETIC — exit 0. At d91d2ffa: 174 registered / 28 done / 0 landed, 146 open, max registered R-0559, max resolved R-0558. At HEAD: IDENTICAL — 174 / 28 / 0, 146 open, same two maxima. Registered, done and landed symmetric differences all EMPTY. Duplicate ids 0 and resolutions naming an unregistered id 0, at BOTH SHAs. Next free id R-0560.
G7 HYGIENE — exit 0. `git diff --name-only d91d2ffa..HEAD` before C3 = `.agent/authored/f085-r60.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and nothing else: no `.py` path, and none of the three R61 call sites. `git ls-tree d91d2ffa -- <path>`, one call per path, resolves all three: `apps/cli/commands/runtime_cmd.py` blob 01ab65ed, `packages/runtimes/dev_server.py` blob 7715a28e, `packages/runtimes/runtime_supervisor.py` blob 9f3749ae. Per-commit INSERTIONS before C3: 253, 171, 6, 47 — none over 500. All four commits single-parent.
BLOCK SIZE re-measured from the committed `.agent/authored/f085-r60.md`: TOTAL 253, PROSE 170, RECORD28 47 — all three agree with the block's own figures and sit under 490 / 400 / 140.

## Authored-text proofs
PLAN14F, PLAN14T and RECORD28 were each extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r60.md` by marker pair under the block's CONVENTION and applied as byte-level operations, never hand-edited. Disk-to-disk equality of that committed file against the reviewer's `.remedy-wt/f085-r60.md` holds (G2). No marker line reached any target file.

## Deviations & assumptions
Commit sequence ran exactly as ordered — C0a, C0b, C1, C2, C3. No extra commit, no dropped commit, no reordering.
No ledger text was authored (constraint 7): no `Landed:` line, no worker `Done:` paragraph, RECORD28 unedited. No disagreement was found between RECORD28 and any reading taken here.
Reporting note, not a change: G3 requires marker LINES = 0 "in each edited file", while G2 requires the two block copies to carry the block's own 6 marker lines. Read as slice TARGETS, both are 0; the two transport copies are 6 by construction. Nothing was edited to reconcile this.
Deviations, declared: this handoff is 73 lines against the ≤60-line cap. DECISION D15 stated cause — the five mandated per-commit tables, the item-status table, and the G1-G7 transcripts with the transport and pair proofs. No section dropped.

Fortschritt: ~97 % (T001 gebaut · R13-R59 PASS · T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT ·
T002d KOMPLETT · T002e — die `runtime-server`-Policy gebaut und verifiziert, die drei Call-Sites
offen · T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next
ONE: the next round is R61, which migrates the three `runtime-server` call sites — `apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` — onto `runtime_server_exec_policy` via `plan_child_spawn`, each keeping its own `Popen` and its own supervision; that round's first task is to settle, per site, which keys its child needs on top of `RUNTIME_SERVER_ENV_ALLOWLIST`, because `apps/cli/commands/runtime_cmd.py` at d91d2ffa builds its child environment as `dict(os.environ)` plus `REMEDY_RUNTIME_PORT` and a scrub would drop whatever else that child reads.
TWO: R60 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R61 carries it.
THREE: 146 findings are open and the next free id is R-0560.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
