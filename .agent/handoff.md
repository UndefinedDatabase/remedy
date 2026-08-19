# Handback — F085 R61 (T002e call sites, part 1)

Feature F085 · Round R61 · Branch `feature/f085-sandbox-hardening` · Base `5b9f935b`

## Range
Review of 5b9f935b..9727c5e3

## Commits
### 8f26c8bb docs(f085): save the R61 block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r61.md | +484/-0 | C0a — block saved byte-verbatim |

### 07d614fc docs(f085): mirror the R61 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +397/-166 | C0b — same bytes mirrored |

### 70c6c741 docs(f085): advance the plan to the R61 migration round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-10 | C1 — PLAN15F→PLAN15T rewrite |

### 603e39f7 docs(f085): record the R60 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +36/-0 | C2 — RECORD29 appended at EOF |

### 63c9fd46 feat(f085): spawn runtime-server apps under the exec guard policy
| Path | +/- | Reason |
|---|---|---|
| packages/runtimes/dev_server.py | +17/-2 | C3 — SITE2A then SITE2B |
| packages/runtimes/runtime_supervisor.py | +15/-1 | C3 — SITE3A then SITE3B |
| tests/runtimes/test_runtime_cli_process_boundary.py | +14/-4 | C3 — BOUNDA then BOUNDB, the boundary test the migration breaks |

### 9727c5e3 test(f085): pin the environment a launched app really inherits
| Path | +/- | Reason |
|---|---|---|
| tests/runtimes/test_dev_server.py | +49/-0 | C4 — TESTCODE appended at EOF |

### C5 (this commit — self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — this handback; a handoff cannot table its own commit |

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
`git push -u origin feature/f085-sandbox-hardening` after C5. No PR, no merge, no worktree add/remove, no gh command.

## Verification
G1 STATE — exit 0. `.agent/STOP` absent before C0a and again before C5; `git status --porcelain` empty at round start and after every one of C0a, C0b, C1, C2, C3, C4; `git worktree list` exactly one line at round start and at the end, none created in between.
G2 TRANSPORT — exit 0. Four copies BYTE-EQUAL: committed and working `.agent/authored/f085-r61.md`, committed and working `.agent/last_block.md` — each sha256 `bb18ff7d5cdb461883a2e3b35fa6e137f178bbf759362d312904c91cd5b80eab`, 30129 B, 484 lines, 32 marker lines. BLOCK SIZE re-measured from the committed file: TOTAL 484 (≤490), PROSE 269 (≤400), RECORD29 36 (≤140) — all three under the constraint-9 figures.
G3 SHAPES — exit 0, measured per pair and per path over the post-commit blobs.
 REWRITES, FROM 0x / TO 1x: PLAN15 at 70c6c741, numstat `9 10`; SITE2B and SITE3B and BOUNDA and BOUNDB at 63c9fd46.
 APPEND-SHAPED, FROM 1x / TO 1x (no zero count owed or reported): SITE2A and SITE3A at 63c9fd46.
 Re-applying each extracted FROM→TO to the pre-commit blob reproduces the post-commit blob BYTE-EXACTLY for all three C3 paths and for `.agent/plan.md`.
 ORDERED EQUALITY for the two FROM-less appends: RECORD29 at 603e39f7 — pre-commit blob a byte-exact PREFIX, slice an exact SUFFIX, `pre + slice` equals the post-commit blob byte for byte, ADDED lines exactly the slice's 36 lines IN ORDER, numstat `36 0`. TESTCODE at 9727c5e3 — same four readings, ADDED lines exactly the slice's 49 lines IN ORDER, numstat `49 0`.
 numstat at 63c9fd46: `17 2` dev_server.py, `15 1` runtime_supervisor.py, `14 4` test_runtime_cli_process_boundary.py.
 Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$` = 0 in every edited file: `.agent/plan.md`, `.agent/live_review.md`, `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`, `tests/runtimes/test_runtime_cli_process_boundary.py`, `tests/runtimes/test_dev_server.py`.
G4 LINT — both halves exit 1 at base AND at HEAD, as ordered; compared as rule-code multisets from `--output-format json`. `python3 -m ruff check <4 paths>`: base `{I001: 1}` (test_runtime_cli_process_boundary.py:10), HEAD `{I001: 1}` — SAME. `python3 -m ruff check --preview <4 paths>`: base `{E303: 1, I001: 1}` (E303 at dev_server.py:236), HEAD `{E303: 1, I001: 1}` — SAME. No new code, no second instance.
G5 SUITES — all four exit 0, PRIMARY checkout. `python3 -m pytest tests/runtimes/ -rf -q` → base `251 passed in 211.40s`, HEAD `252 passed in 210.94s`, no skips at either — base plus the one test C4 adds, exactly as ordered. `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q` → `36 passed in 14.24s`, UNCHANGED. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → `160 passed in 19.86s`, UNCHANGED. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 20.43s`.
G6 PLAN CONTRACT — exit 0. `.agent/plan.md` after C1 is 44 lines (≤50, and the figure the block projected); `## Goal` present true, `## Next Steps` present true, `\bF\d{3}\b` matches true.
G7 ARITHMETIC — exit 0. At 5b9f935b: 174 registered / 28 done / 0 landed, 146 open, max registered R-0559, max resolved R-0558. At HEAD: IDENTICAL — 174 / 28 / 0, 146 open, same two maxima. Registered, done and landed symmetric differences all EMPTY. Duplicate ids 0 and resolutions naming an unregistered id 0, at BOTH SHAs. Next free id R-0560.
G8 HYGIENE — exit 0. `git diff --name-only 5b9f935b..HEAD` before C5 = exactly `.agent/authored/f085-r61.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`, `tests/runtimes/test_dev_server.py`, `tests/runtimes/test_runtime_cli_process_boundary.py` — 8 paths, the change set minus `.agent/handoff.md`, and it does NOT hold `apps/cli/commands/runtime_cmd.py`. Per-commit INSERTIONS before C5: 484, 397, 9, 36, 46, 49 — none over 500. C5's own insertions go in the round report. All six commits single-parent.

## Authored-text proofs
PLAN15F/T, SITE2AF/T, SITE2BF/T, SITE3AF/T, SITE3BF/T, BOUNDAF/T, BOUNDBF/T, TESTCODE and RECORD29 were each extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r61.md` by marker pair under the block's CONVENTION and applied as byte-level operations (`str.replace(FROM, TO, 1)`, or `pre + slice` for the two FROM-less appends). None was retyped, hand-edited or reflowed. The four transport copies are byte-equal at the block's own digest (G2); the reviewer holds its own original for the disk-to-disk comparison. No marker line reached any target file.

## Deviations & assumptions
Commit sequence ran exactly as ordered — C0a, C0b, C1, C2, C3, C4, C5. No extra commit, no dropped commit, no reordering.
No ledger text was authored (constraint 7): no `Landed:` line, no worker `Done:` paragraph, RECORD29 unedited. No disagreement was found between RECORD29 and any reading taken here. `apps/cli/commands/runtime_cmd.py` was not touched.
Assumption, stated not assumed away: the base `tests/runtimes/` reading was taken after C1 and C2 (which touch only `.agent/`) rather than at 5b9f935b itself — the four G4/G5 source paths were still byte-identical to their 5b9f935b blobs at that moment, and no test under `tests/runtimes/` reads `.agent/plan.md` or `.agent/live_review.md` (verified by grep). The remaining base readings are the reviewer's own, as the block states.
Deviations, declared: this handoff is 94 lines against the ≤60-line cap, using the ≤100-line form the Bundle's seven items allow. DECISION D15 stated cause — the six mandated per-commit tables, the seven-row item-status table, and the G1-G8 transcripts with the transport, pair and ordered-equality proofs. No section dropped. The same mandated content puts the file at 9221 bytes, over the template's ≤800-token guidance; the overage is that content, not prose padding.

Fortschritt: ~98 % (T001 gebaut · R13-R60 PASS · T002a-T002d KOMPLETT · T002e — die
`runtime-server`-Policy gebaut, die beiden App-Call-Sites migriert und mit einem
Kind-Environment-Test gepinnt, `apps/cli/commands/runtime_cmd.py` offen · T003 offen) — Schätzung,
gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next
ONE: the next round is R62, which migrates the LAST `runtime-server` call site, `apps/cli/commands/runtime_cmd.py`, whose child is the Remedy supervisor rather than a project application, and whose declared keys are `REMEDY_DATA_DIR`, `REMEDY_RUNTIME_LOG_MAX` and `REMEDY_RUNTIME_PORT` — the first because the supervisor resolves its own runtime directory through `projects_dir()`, the second because `tests/runtimes/test_runtime_cli_process_boundary.py` passes it to the CLI to cap the log, the third because the supervisor reads it with `os.environ[...]` and dies without it.
TWO: R61 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R62 carries it.
THREE: 146 findings are open and the next free id is R-0560.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
