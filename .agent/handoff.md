# Handback — F252 R1 (bookkeeping + D8 + D10 + D11)

## Range
Review of 7baff1d..217b6b2 + the handoff commit · feature/f252-standing-red-paydown · D8, D10, D11 done (D10 test-only) · delta done.

## Commits

### 1e75364 chore(f252): claim F252, reset agent state
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f252-r1-1/2/3.md | +33 | authored texts, sha256-verified |
| .agent/live_review.md · plan.md | +32/-41 | full replace by f252-r1-2 / -3 |
| .agent/last_block.md | +192/-86 | round block, OUTCOME pending |
| docs/roadmap/STATUS.md | +1/-1 | F252 `[ ]` → `[~]` |

### 54eb3db fix(f252): bind the flight-plan call to its own provider schema
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/intake.py | +19/-3 | D8 cause: the call_fn bound Ollama's native `format=` to JobIntake; new `make_structured_call_fn(model_cls)`, old name = alias |
| apps/cli/commands/do_cmd.py | +12/-3 | `do` + `do replan` planned with it → plans came back in intake shape; both now bind FlightPlan |
| tests/cli/test_scoped_listings.py · .agent/decisions.md | +27/-2 | `_create_job` gains `--no-llm` (Deviations); diagnosis |

### 19ff5e7 fix(f252): register a project in the discover-commands fixtures
| Path | +/- | Reason |
|---|---|---|
| tests/test_command_discovery.py | +39/-11 | D10 cause: fixtures ran `job create` with no project (exit 3 since F148), ignored rc → `job_id` `""`; now register the repo + assert rc |
| .agent/decisions.md | +14 | diagnosis |

### 217b6b2 fix(f252): raise FenceConfigError for malformed fence config
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/scope_fences.py | +12/-1 | D11 cause: `load_config` now RAISES `BudgetConfigError` on bad TOML, so the "Malformed TOML" diagnostic the loader scans for never appears; caught → `FenceConfigError` |
| .agent/decisions.md | +12 | diagnosis |

### handoff commit (self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md · .agent/last_block.md | rewrite · +1/-1 | this handback; OUTCOME → executed |

## External actions
PR gate `gh pr list --state open` → empty. 4 pushes to origin/feature/f252-standing-red-paydown, all OK; handoff commit last. No PR, no merge.

## Verification
- `pytest tests/docs/ -q` → 1, "13 failed, 279 passed"; comm vs baseline EMPTY.
- `pytest tests/cli/test_scoped_listings.py -q` → 0, "18 passed" (was 5F/13P).
- `pytest tests/test_command_discovery.py -q` → 0, "92 passed" (was 8F/84P).
- `pytest tests/orchestration/test_fence_e2e.py tests/orchestration/test_fences.py -q` → 0, "208 passed" (was 3F/205P).
- canary `pytest tests/cli/test_golden_path.py -q` → 0, "42 passed", after every slice.
- `pytest -n auto -q` → 1, "134 failed, 14172 passed, 8 skipped in 165.14s". vs churn_gate2_run1.txt: `comm -23` (new) EMPTY, no flake to name; `comm -13` = 20 gone: all 14 targets (D8 3, D10 8, D11 3), 2 D14 siblings sharing D8's cause, 4 D4 state-file ids the authored plan.md/live_review.md satisfied.

## Authored-text proofs
f252-r1-1/2/3: on-disk `sha256sum` matched the BEGIN markers exactly BEFORE any commit. Applied by copy — `cmp` exit 0 for live_review.md and plan.md; STATUS.md `grep -cF` old = 0, new = 1.

## Deviations & assumptions
- D10 has no product defect: with a project, `test discover <id> --json` gives rc=0 and schema-v1 JSON. Project-less `job create` would be a product CHANGE, class D5 — fix stayed in the fixtures.
- Two test edits, each in its class's own file, nothing weakened: the D10 fixtures, and `--no-llm` in `_create_job` — with D8 fixed, `do` makes a real 72s flight-plan call against that file's 30s timeout; the canary forces the same flag.
- `.agent/plan.md` is authored and cmp-verified, so untouched. `.agent/context.md` stays F046-era — not named by the block (its 2 dashboard ids stay baseline red).

## Next
Reviewer verdict on R1, then the next F252 class round.
