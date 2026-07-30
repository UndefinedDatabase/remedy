# Handback — f052-r1 (Window 2 → Window 1)

## Range
Review of main..HEAD (`feature/f052-self-healing-rounds`, 6 commits, pushed, NO PR — the reviewer orders it after the integration gate).

## Commits

### 92c998c chore(f052): claim F052 + state reset
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | +1/-1 | `- [ ] F052` → `- [~] F052` (grep 1→0 / 0→1) |
| .agent/authored/f052-r1-{1,2,3}.md | +40 | 3 authored texts, hashes verified |
| .agent/live_review.md, .agent/plan.md | replace | := r1-1 / r1-2 (cmp 0) |
| .agent/last_block.md | +173/-87 | round block, OUTCOME pending |

### 7b27e5d feat(f052): classify a failed cycle verify and render it (VerifyOutcome)
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/long_run_executor.py | +95/-4 | `VerifyOutcome` + `as_verify_outcome` (bare-string steps unchanged), `VERIFY_CONFIG_ERROR`/`VERIFY_UNKNOWN_ERROR`, `cycle_verify_failure_class` via the EXISTING `failure_postmortem.classify`, `CycleRecord.verify_failure_class`, `render_cycle_summary_line` |
| apps/cli/commands/job.py | +6 | `remedy job run` prints one rendered line per cycle |
| tests/orchestration/test_self_healing_cycles.py | +235 | 14 tests |

### b97cde3 feat(f052): repair-round seam, findings payload and round cap
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/config.py | +14 | `cycles.repair_rounds`, default 2 |
| packages/orchestration/long_run_executor.py | +125 | `RepairStep`/`RepairOutcome`/`RepairPhase`, `build_cycle_repair_findings` (on `repair_context.build_repair_context`), `CycleLimits.repair_rounds`, 4 repair fields on `CycleRecord`, `_VERIFY_REPAIRABLE` |
| tests/orchestration/test_self_healing_cycles.py | +137 | 15 tests |

### e29da45 feat(f052): trigger the existing bounded repair loop from a failed cycle verify
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/long_run_executor.py | +175/-5 | `_run_repair_rounds`, `default_repair_step` → `builder_bridge.run_builder_bridge_loop(max_cycles=1)`, `repair` seam + `repair_stop_probe` in `run_cycles`, 2 ledger events |
| tests/orchestration/test_self_healing_cycles.py | +265/-1 | 10 tests |

### e295fcb test(f052): stubborn path, budget attribution, stop between rounds, A9 edges
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_self_healing_cycles.py | +257/-1 | 11 tests (T002) |

### \<handback\> chore(f052): handback R1
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | this file (R-0149 self-reference) |
| .agent/plan.md, .agent/decisions.md, .agent/last_block.md | edits | R1 done; 3 decisions; OUTCOME executed |

## INSPECT report (bundle item 1)
- **Where a cycle verify failure surfaces**: `long_run_executor.run_cycles`, the `verify_step(...)` call in the cycle body — `VERIFY_FAILED` is appended to `errors` and denies green via `_VERIFY_DENIES_GREEN`. No production caller injects a verify step today (`_no_verify` → `not_run`); the seam is caller-supplied by design.
- **Existing repair loop that accepts findings and EXECUTES**: `builder_bridge.run_builder_bridge_loop(build_fn, repo_path, *, job, data_dir, max_cycles)` — same core-`Job` world, `build_fn(repair_context) -> BuilderOutput`. Findings intake = `repair_context.build_repair_context(job_id, test_run_event, events) -> dict`. Round cap = its `max_cycles` (default 3); exhaustion reason `repair_budget_exhausted`. Used only by tests before this round — no production caller.
- **Ping-pong repair loop** (`pingpong_loop.run_pingpong`): real bounded rounds (`resolve_repair_rounds`, default 2 / hard cap 10; governance `make_repair_decision`; findings enter via `_build_builder_prompt(findings=…)`), but findings come from its OWN reviewer inside the invocation, there is no injection seam, and it belongs to `pingpong_job.JobPlan` — NOT reachable from `run_cycles`. **Not a STOP**: a reachable executing repair path does exist (above), so the block's stop condition was not met.
- **`repair_loop` v0/v1 and `repair_loop_v2`**: human-gated proposal flows by explicit module contract ("No real provider. No automatic apply. No test execution." / "NO model/provider/worker execution"). Unsuitable as the executor; not used.
- **Budgets and repair calls**: `run_cycles.counted_provider_call` increments `provider_calls`, read by `_default_counters` → `safe_points.should_stop`. A repair round run through that seam is counted with no separate accounting — proven by the two budget tests.
- **Postmortem test-failure class**: `failure_postmortem.FailureClass.TEST_FAILED` (`"test_failed"`, from `TERMINAL_STATUS_CLASSES`); harness cases are `CONFIG` / `UNKNOWN`. `PostmortemV1.evidence_refs` accepts `cycles/cycle_0001.json`, which is how the postmortem links the repair-round evidence.

## External actions
- `gh pr list --state open …` → `[]` (gate passed); `git checkout main && git pull --ff-only` → up to date.
- `git checkout -b feature/f052-self-healing-rounds`; `git push -u origin …` → new branch. Pushed after every commit. **No PR created, nothing merged.**

## Verification
`python3 -m pytest tests/orchestration/test_self_healing_cycles.py -q` → `50 passed in 0.22s`, exit 0.
`python3 -m pytest tests/orchestration/ -q` → `8788 passed, 7 skipped in 592.17s`, exit 0.
`python3 -m pytest tests/docs/ -q` → `293 passed in 0.26s`, exit 0.
`python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 18.92s`, exit 0.
Clean tree at gate time (`git status --porcelain` empty).

Healed-cycle evidence, rendered by `render_cycle_summary_line` — the line `remedy job run` prints:
```
  [repair round 1] findings -> ['tests/test_calc.py::test_add'] | tail='E   assert 4 == 5'
Job 211be8d2-1744-463c-aaaa-8287d59e83ba | cycles=1/2 terminal=all_green status=completed
  cycle 1: verify=passed tasks=1/1 | healed after 1 repair round
```
and the same facts in the on-disk cycle record: `"repair_rounds_used": 1, "healed_after_repair": true, "repair_summary": "healed after 1 repair round"`.

## Authored-text proofs
`sha256sum .agent/authored/f052-r1-*.md` — all three matched the BEGIN-marker hashes on FIRST computation (no transport fault, no rejoin):
```
8ba4dc102c31225686db256ac05863a8cf266a09525d6d936f0339bfc3990c96  .agent/authored/f052-r1-1.md
7c57cbadbe37f2dc61111c457fac71370cbf0f116361fc5fbaf137edd62c01d4  .agent/authored/f052-r1-2.md
7c0b8fd0a7679e9bc26f46548733ebf29d3e97d4d33b8a539c0cac0eef67d137  .agent/authored/f052-r1-3.md
```
`cmp f052-r1-1.md .agent/live_review.md` → 0; `cmp f052-r1-2.md .agent/plan.md` → 0 (plan.md then updated at handback, as the Commit Gate requires). STATUS line: old `grep -cF` 1→0, new 0→1, one line changed.

## Deviations & assumptions
1. **Four content commits instead of the two implied by T001/T002.** The combined diff was 875 lines, over the AGENTS.md 500-line limit, and genuinely separable — so it was split rather than declared oversize. Each commit is independently green. Rationale in `.agent/decisions.md`.
2. **`CycleLimits.repair_rounds` defaults to 0 while the config key defaults to 2.** A dataclass default of 2 silently turned every existing direct `CycleLimits(...)` construction into a self-healing one. Production goes through `limits_from_config`, which supplies 2. Documented on the field and in decisions.md.
3. **Budget attribution holds for the DEFAULT repair seam only.** An INJECTED repair seam receives no provider callable, so it cannot spend the counted seam; the budget tests therefore drive the production path (default seam, `run_builder_bridge_loop` monkeypatched to call `build_fn`). A first attempt that asserted attribution through an injected fake failed honestly and was rewritten — worth a reviewer's eye if an injected seam should also be counted.
4. **`default_repair_step` is exercised with a monkeypatched `run_builder_bridge_loop`**, not against a real workspace apply/test — real-provider behavior belongs to the integration gate, not to a unit round.

Item status: | 1 INSPECT done | 2 T001 done | 3 T002 done | no skips.

## Next
Reviewer verdict on f052-r1, then the integration-gate round. Open findings: 0. Next free ID: R-0158.
