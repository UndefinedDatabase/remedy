# Handback — F070 R2 (SPLIT, LARGE: findings + R-0170 + docs + T003 + gate)

## Range
Review of `b053516a`..`58969e5d` on `feature/f070-orchestrator-loop`.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 save 4 authored + sha256 | done | 4/4 match BEGIN digests |
| 2 apply r2-1/r2-2 by copy | done | r2-3/r2-4 held for Phase C as ordered |
| 3 commit + docs gate + canary | done | |
| 4 R-0170 fix + `Done:` append | done | |
| 5 R-0170 tests + verify | done | |
| 6 apply r2-3 (handback cap) | done | both FROM 1→0, TO 0→1 |
| 7 apply r2-4 (gate hardening) + `Done:` append | done | both FROM 1→0, TO 0→1 |
| 8 docs gate + canary | done | |
| 9 T003 e2e fixture mission | done | scenario exactly as ordered |
| 10 CLI run + ledger | done | `mission.run` gains a MODE (F047 pattern) |
| 11 push at phase boundaries | done | |
| 12 integration gate + evidence | done | branch 0 / base 0, dist hash unchanged |

## Commits
### 0abc0e74 chore(f070): persist the R1 PASS verdict and findings R-0169..R-0171
| Path | +/- | Reason |
| .agent/authored/f070-r2-1..4.md | +164/-0 | the four authored texts, verified |
| .agent/live_review.md | +63/-29 | r2-1 applied by copy |
| .agent/plan.md | +17/-13 | r2-2 applied by copy |
### 08bd8c5e fix(f070): refuse an achieved claim on a mission with no compiled plan
| packages/orchestration/orchestrator_loop.py | +10/-2 | R-0170: `not ids` refusal |
| tests/orchestration/test_orchestrator_loop.py | +66/-0 | 6 tests, loop-level |
| .agent/live_review.md | +1/-0 | `Done: R-0170` append only |
### c2b07445 docs(f070): amend the handback cap and harden the integration gate
| docs/agents/handback_template.md | +5/-2 | r2-3, the R-0149 DECISION |
| docs/agents/integration_gate.md | +11/-4 | r2-4, R-0169 hardening |
| .agent/live_review.md | +1/-0 | `Done: R-0169` append only |
### 762fe3e2 feat(f070): the two-milestone mission runs end to end, unattended
| packages/orchestration/orchestrator_loop.py | +25/-4 | `next_iteration_index` (F047 pattern) |
| tests/orchestration/test_mission_e2e.py | +411/-0 | 24 tests, no evidence-seam override |
### 7fcc3ebc feat(f070): add remedy mission run (orchestrator mode) and mission ledger
| apps/cli/commands/mission_cmd.py | +109/-0 | run-loop + ledger handlers |
| apps/cli/commands/worker_facade_cmd.py | +42/-0 | resolved mode branch |
| apps/cli/command_catalog.py | +20/-3 | `--iterations`, `--no-llm`, `mission.ledger` |
| packages/orchestration/intake.py | +8/-1 | optional `model=` on the shared factory |
| tests/cli/test_mission_cmd.py | +148/-0 | 12 tests incl. catalog uniqueness |
| .agent/decisions.md | +39/-0 | 3 decisions |
### 58969e5d chore(f070): integration-gate evidence for R2
| .agent/gate_f070_r2/ | +966/-0 | 17 files (raw runs, comms, hashes, README) |
### (this commit) chore(f070): handback R2
| .agent/handoff.md | rewrite | this file (self-reference exception) |

### R-0171 correction — R1's final commit `b053516a`, omitted from its table
| .agent/handoff.md | +134/-65 | the R1 handback (was tabled) |
| .agent/decisions.md | +3/-2 | backup-branch deletion note (WAS OMITTED) |
Note: the finding cites `+5/-2` for that file; `git show --numstat` reports
`+3/-2`. Reporting the measured value.

## External actions
- `git push origin feature/f070-orchestrator-loop` after each phase (A, B, C, D, E). No force-push this round.
- `git worktree add -b tmp/base-gate-f070 <scratchpad>/base-wt afbe2639` for the base run.
- `git worktree remove --force` + `git worktree prune` + `git branch -D tmp/base-gate-f070`.
- `cp -r apps/ui/node_modules apps/ui/dist` into the base worktree (COPY, never symlink).
- No PR created (SPLIT round). No gh commands. No mutation/red-proof runs.

## Verification
```
PHASE A  pytest tests/docs/ -q                    293 passed          exit 0
         pytest tests/cli/test_golden_path.py -q   42 passed          exit 0
PHASE B  pytest tests/orchestration/test_orchestrator_loop.py -q
                                                  100 passed          exit 0
         pytest tests/cli/test_golden_path.py -q   42 passed          exit 0
PHASE C  pytest tests/docs/ -q                    293 passed          exit 0
         pytest tests/cli/test_golden_path.py -q   42 passed          exit 0
PHASE D  pytest tests/orchestration/test_mission_e2e.py -q
                                                   24 passed          exit 0
         pytest tests/cli/test_mission_cmd.py -q    78 passed          exit 0
         pytest tests/cli/test_golden_path.py -q    42 passed          exit 0
         runner tests/orchestration/ -n auto   RED twice — see below
         pytest tests/orchestration/test_product_smoke.py -q (serial)
                                                   76 passed          exit 0
PHASE E  runner -n auto -q (branch)     15274 passed, 0 failed        exit 0
         runner -n auto -q (base afbe2639, parity copy, NO_AUTO_BUILD=1)
                                        15094 passed, 0 failed        exit 0
         comm -13 (branch-only) = empty ; comm -23 (base-only) = empty
         dist/ hash before == after (5ff2033a…) — neutralization held
```
The Phase D scoped gate went red twice with a DIFFERENT failing set each time,
all in `tests/orchestration/test_product_smoke.py`: run 1 three ids
(`TestAppStartsGreen::test_a_clean_app_passes`, `::test_the_app_is_always_stopped`,
`TestRetryAndPortConflict::test_a_flaky_start_passes_on_retry_and_says_so`),
run 2 one different id (`TestCorePathsRun::test_ok_paths_pass`) with run 1's
three passing. Serially that file is 76/76 and the Phase E branch full suite has
zero failures — the xdist-flake class of integration_gate.md step 4 (F135/F052).
No F070 file is involved. Raw logs: `.agent/gate_f070_r2/scoped_slice_run{1,2}.txt`.

## Authored-text proofs
`sha256sum .agent/authored/f070-r2-*.md` — all four equal their BEGIN digests:
```
8f10901bd053cc6c81bbf3e4713dbb9b5a18524657040cbff7a6d2697ae9dfe4  f070-r2-1.md
d357c08a7e0bfc6e2b6514018b734d29851b58800fe19dcb8ac533151291db43  f070-r2-2.md
7655458d7cad32fccd5d8cd6c1a486f02c3528a26d1c1d141957769b19b557e2  f070-r2-3.md
fae3c5a06a699f0093ec61d98970b15e9be5b2cb446d4fcd48febb63a63c5f34  f070-r2-4.md
```
Disk-to-disk (`cp`), applied-file digest vs authored digest, at commit 0abc0e74:
```
f070-r2-1.md -> .agent/live_review.md  IDENTICAL (8f10901b…)
f070-r2-2.md -> .agent/plan.md         IDENTICAL (d357c08a…)
```
r2-3 / r2-4 (FROM→TO, applied by a script that PARSES the saved file — the
replacement text is never retyped):
```
handback_template.md  EDIT 1  FROM 1 -> 0, TO 0 -> 1
handback_template.md  EDIT 2  FROM 1 -> 0, TO 0 -> 1
integration_gate.md   EDIT 1  FROM 1 -> 0, TO 0 -> 1
integration_gate.md   EDIT 2  FROM 1 -> 0, TO 0 -> 1
```
The only edits to `.agent/live_review.md` after Phase A are the two ordered
`Done: R-0169` / `Done: R-0170` appends (+1 line each). No verdict written.

## Gate evidence
`.agent/gate_f070_r2/` — 17 files, every one `.txt` or `.md`, none gitignored,
README lists them all. Branch/base raw runs, exit codes, both (empty) FAILED
lists, both (empty) comm sets, the dist/ hashes and their verdict, the two red
scoped runs, the serial re-run, and the worktree teardown proof
(`git worktree list` shows only the primary checkout).

## Deviations & assumptions
1. **`mission run` gains a MODE, it does not replace one.** The name already
   belonged to the pre-F070 dogfood facade keyed on a run id; the feature file
   mandates the same spelling for a mission id. Resolved as F047 resolved
   `job resume`: one command, two modes, mode RESOLVED by looking the id up as
   a mission (never guessed from its shape), every failure to resolve keeping
   the old path. A test pins catalog uniqueness; the facade's own tests pass.
2. **`make_structured_call_fn` gained an optional `model=`** so
   `orchestrator.model` actually selects a model instead of documenting an
   intention. Additive; every existing caller is unchanged. Config surface, not
   a routing-policy change.
3. **Ledger iteration numbering now continues across runs** (`next_iteration_index`).
   Found BY the e2e, not by review: two runs left a ledger numbered 1,2,3,4,1,2,3.
   Same fix F047 made for cycle numbering. Not ordered; recorded in decisions.md.
4. **One e2e assertion was corrected during authoring**: the escalated decision
   cannot appear in a run-1 prompt, because it is raised while iteration 4 is
   deciding and that iteration's context was already assembled. Replaced with
   what is true — exactly one decision genuinely open at the pause, and run 2's
   first prompt showing it resolved.
5. **The gate-evidence commit `58969e5d` is 966 lines** — the feature's first
   and only oversize commit (R1 split all three of its own). Inseparability: it
   is one evidence artifact set that the gate procedure requires committed
   whole; 880 of those lines are raw pytest transcripts, and splitting them
   across commits would leave the evidence non-atomic and unverifiable as a set.
6. **R-0171 correction row** is above, with a measured-vs-cited discrepancy
   noted honestly rather than silently adopting the finding's figure.
7. Phase D's scoped gate red is recorded as evidence, not waved away: two runs,
   two different failing sets, serial green, full-suite green, no F070 file
   involved. If the reviewer reads it as a blocker instead, the CLI commit is
   the only one that would need to move.

## Next
Reviewer gate verdict for R2. On PASS: closure per
`docs/roadmap/STATUS_closure_protocol.md`, its own round.
