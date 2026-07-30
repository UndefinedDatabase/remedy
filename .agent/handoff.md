# Handback — f052-r2 (Window 2 → Window 1)

## Range
Review of 21638c6..HEAD (`feature/f052-self-healing-rounds`, pushed, no PR, nothing merged). Closure is NOT part of this round.

## Commits

### 897381a chore(f052): persist R1 verdict (PASS) + DECISION D1
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +31/-4 | R1 Steps bullet := r2-1, `- (none yet)` := r2-2 (DECISION D1), `- R1: PENDING` := r2-3 (PASS) |
| .agent/authored/f052-r2-{1,2,3,4}.md | +37 | 4 authored texts, hashes verified before use |
| .agent/last_block.md | +226/-122 | R2 block, OUTCOME pending |

### a712dc0 docs(f052): How-it-fits amendment (D1) + Built State
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/features/T1_F052.md | +70 | r2-4 as its own paragraph closing "## How it fits"; new "## Built State" written from the committed f052-r1 diff only |

### \<handback\> chore(f052): handback R2 (integration gate records)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | this file (R-0149 self-reference) |
| .agent/last_block.md | 1 line | OUTCOME pending → executed |

## External actions
- `git worktree add /tmp/f052-base c0a3b34…` (base run) and `git worktree add -b tmp/f052-base-named /tmp/f052-base-named c0a3b34…` (attribution proof). Both `git worktree remove --force` + `git worktree prune`; branch `tmp/f052-base-named` deleted. Proof: `git worktree list` → only `/home/decodeux/Repos/remedy  a712dc0 [feature/f052-self-healing-rounds]`; both /tmp paths gone.
- `git push` after each commit. No PR, no merge.

## Integration gate records (merge base c0a3b34ad3951cf1d195c39a7a3aff32ba4068d8)

**Parity restore (R-0155 amendment, first live application).** Method: `cp -a` from the primary checkout into the base worktree, verified with `diff -rq` / entry counts. First attempt copied what the amendment names — ROOT `node_modules` + `apps/ui/dist`; both were ABSENT in the fresh worktree, confirming the finding. That run still failed 10 ids. **Direct evidence why: the amendment names the wrong path.** The ROOT `node_modules` holds only a `.vite` cache (0 package entries, 20K); the real tree is `apps/ui/node_modules` (205 entries, 305M) — raw base error: `Cannot find package 'vitest' imported from /tmp/f052-base/node_modules/.vite-temp/…`. Base run repeated with `apps/ui/node_modules` copied too (205/205 entries, `comm -3` diff 0, `vitest` + `dist` present).

**Branch run** — `python3 -m pytest -n auto -q`, repo root:
`14486 passed, 19 skipped in 121.01s (0:02:01)`, exit 0, WALL 2:01.54. `grep '^FAILED'` → **0 lines** (`branch_failed.txt` empty).

**Base run (parity restored)** — identical command in the worktree:
`2 failed, 14434 passed, 19 skipped in 150.87s (0:02:30)`, exit 1, WALL 2:31.36. `base_failed.txt`:
```
FAILED tests/cli/test_self_dogfood_execution_cli.py::test_approved_execute_awaits_candidate
FAILED tests/cli/test_self_dogfood_execution_cli.py::test_status_and_reconcile_json
```
(Pre-parity base run, for the record: `10 failed, 14421 passed, 24 skipped in 139.31s`, exit 1 — the 8 extra ids were 6× `tests/ui_server/test_live_state.py::TestUIServerIntegration::*`, `test_dashboard_contract.py::…::test_typescript_compiles`, `test_test_runner.py::…::test_vitest_passes`. All 8 disappeared under parity: that IS their per-id environment attribution.)

**comm -13 (branch-only failures): 0.** Nothing to attribute under step 4; no blocker from the branch side.

**comm -23 (base-only): 2**, both attributed by direct evidence, neither a genuine base regression:
- `test_approved_execute_awaits_candidate`, `test_status_and_reconcile_json` — `self_dogfood_execution.current_branch()` reads `Path(".git") / "HEAD"` and returns `""` when that file is absent; in ANY linked worktree `.git` is a regular FILE, so the guard reports `main_branch_unsafe` and the CLI answers `blocked` / zero attempts instead of `awaiting_external_candidate` / one attempt. Measured: primary `.git` = directory → `current_branch()` = `'feature/f052-self-healing-rounds'`, `mutation_safe=True`; worktree `.git` = regular file → `current_branch()` = `''`, `mutation_safe=False`. Serial re-run at base reproduces (`2 failed, 4 passed in 2.11s`); a second worktree with a NAMED branch at the same commit fails identically, so it is not the detached HEAD but the missing `.git` DIRECTORY. The same file passes 6/6 serially in the primary checkout. Missing artifact per id: a real `.git` directory — a NEW environment-coupled class, sibling to R-0155's build outputs.

Wall clock both runs ≈ 2 min, under the ~5 min perf-note threshold.
**No gate verdict issued here** — recorded for the reviewer.

## Verification
`python3 -m pytest tests/docs/ -q` → `293 passed in 0.25s`, exit 0.
`python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 19.01s`, exit 0.
Clean tree at gate time (`git status --porcelain` empty).

## Authored-text proofs
`sha256sum .agent/authored/f052-r2-*.md` — all four matched the BEGIN-marker hashes on FIRST computation (no transport fault, no rejoin):
```
18191e99e68643978c3deb8a115fe17a0724dc66253d51a94f7588313b93b5df  .agent/authored/f052-r2-1.md
bd8975dc0d697872a6259009bd52bffdf470900e3e7e25760e517e64929f7365  .agent/authored/f052-r2-2.md
651db15ca9c3b850a75205ce8bb77c18bc001bf9232ddef50fba22385bdeb42c  .agent/authored/f052-r2-3.md
9926c85c9579fc8af181657bc8fd4bb13e41e32c92089c62b8cf1a83ec518e8f  .agent/authored/f052-r2-4.md
```
`cmp` of each applied region against its authored file → 0 for all three live_review regions (Steps, Findings, Verdicts); `- R1: PENDING (reviewer).` and `- (none yet)` occurrences after: 0. r2-4 occurs exactly 1× in `T1_F052.md`.

## Deviations & assumptions
1. **The base run was executed twice.** The first, following the R-0155 amendment literally (ROOT `node_modules` + `apps/ui/dist`), did not achieve parity because the amendment names a path that holds only a build cache. The second restored `apps/ui/node_modules` as well. Both runs are recorded above; the second is the gate's base run.
2. **Candidate finding for the reviewer (no R-id spent, per the closure-candidate rule):** the R-0155 amendment in `docs/agents/integration_gate.md` should name `apps/ui/node_modules` — the ROOT `node_modules` contains only `.vite`. Evidence above.
3. **Candidate finding for the reviewer:** the two `test_self_dogfood_execution_cli.py` ids cannot pass in any linked worktree, so they land in `comm -23` on EVERY integration gate. `current_branch()` could read the worktree's real HEAD instead of assuming `.git` is a directory. Not fixed here — out of this round's scope, and the fix is its own reviewer-gated round.
4. **Built State was written by me**, not from an authored text, as the block directed; every claim is traceable to the f052-r1 diff.

Item status: | 1 persist verdict+D1 done | 2 feature file done | 3 integration gate done (records only) | 4 gates+handback done | no skips.

## Next
Reviewer issues the integration-gate verdict for f052-r2, and rules on the two candidate findings. Open findings: 0 registered. Next free ID: R-0158.
