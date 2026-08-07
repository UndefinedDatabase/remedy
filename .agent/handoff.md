# Handoff — F254 R2 (alias module + defaults relocated)
Feature T2_F254 · Round R2 · SPLIT · branch `feature/f254-model-alias-table`.
Length: 96 lines. Over 60 because of the 9-row changed-files table, the 13-line verbatim
`rg` output this step ordered recorded, and one declared deviation that must not be
compressed into a slogan. No mandated section is dropped.

## Commits (range 5fed2fca..HEAD)
- `4254503b` docs(f254): persist the R1 verdict and finding R-0211 — .agent paths ONLY,
  committed BEFORE any code, as ordered.
- `3713867a` feat(f254): add the model alias module and route defaults through it. Pushed, exit 0.
- commit 3 `chore(f254): rewrite handoff for the R2 handback` — SHA self-referential
  (this file is its only content), branch tip at handback; declared, not guessed.

## Changed files — GENERATED from `git diff --numstat 5fed2fca..HEAD` (R-0210 fix, not retyped)
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r2-1.md | +138 | -0 |
| .agent/authored/f254-r2-2.md | +64 | -0 |
| .agent/live_review.md | +74 | -13 |
| .agent/plan.md | +17 | -14 |
| packages/orchestration/model_aliases.py | +84 | -0 |
| packages/orchestration/pingpong_provider.py | +7 | -1 |
| packages/orchestration/role_config.py | +10 | -5 |
| tests/orchestration/test_model_aliases.py | +98 | -0 |
| .agent/handoff.md | self-referential | written by commit 3; declared, not omitted |

## Verification — all 11 run for real as `python3 -m pytest <path> -q`, every exit 0
orchestration/test_model_aliases 18 passed 0.15s · test_role_config 32 passed 0.08s ·
test_pingpong 33 passed 0.48s · test_provider_mode 24 passed 0.63s · test_token_truth 37
passed 0.11s · test_final_verifier 97 passed 0.24s · tests/test_do_job_flow 178 passed
22.37s · ui_server/test_dashboard_contract 70 passed 5.03s · orchestration/test_test_runner
51 passed 4.77s · regression/test_resource_safety 21 passed 10.94s · cli/test_golden_path
42 passed 22.03s. No failures, no skips. Round gate + canary only — NO full-suite claim.
`ruff check` on the four touched paths: "All checks passed!", exit 0. `git status
--porcelain` empty at every commit. No force-push, no history rewrite, no `git worktree`,
no PR created, main untouched.

## Transport proofs (A — copied with `cp`, never retyped) and pair counts
`cmp <scratchpad>/f254-r2-N.md .agent/authored/f254-r2-N.md` → no output, exit 0 for N = 1,2.
sha256, identical both sides: r2-1 `bc9d849e89acf099ca48e3566c56590c017013aa50d97b6bfd4a307bec9d71ad`
r2-2 `c9803e370c304b522c7284ee348df8b76fea717f8d4347833ed8df824b6ba3d9`
BEFORE editing: r2-1 pairs 1-4 FROM 1x each, r2-2 pairs 1-2 FROM 1x each — all six exactly
1x, nothing ambiguous. AFTER: all six FROM **0x**, TO **1x** (REWRITE shape). Structure
holds — live_review.md has `## Steps`/`## Findings`/`## Decisions`/`## Verdicts` 1x each;
plan.md has `## Goal` and `## Next Steps` 1x each, 47 lines (<50).

## `rg -n 'claude-opus-4-20250514|claude-sonnet-4-20250514|qwen3-coder-next' packages/ apps/ scripts/` — exit 0
```
packages/providers/ollama_builder/provider.py:18:  4. Built-in default (qwen3-coder-next)
packages/providers/ollama_builder/provider.py:33:_DEFAULT_MODEL = "qwen3-coder-next"
packages/providers/ollama_planner/provider.py:19:  4. Built-in default (qwen3-coder-next)
packages/providers/ollama_planner/provider.py:32:_DEFAULT_MODEL = "qwen3-coder-next"
packages/orchestration/role_config.py:114:    qwen3-coder-next for ollama).
packages/orchestration/config.py:115:        default="qwen3-coder-next",
packages/orchestration/config.py:766:# model = "qwen3-coder-next"
packages/orchestration/config.py:769:# model = "qwen3-coder-next"
packages/orchestration/config.py:774:# model = "qwen3-coder-next"
packages/orchestration/model_aliases.py:42:    "claude-flagship": "claude-opus-4-20250514",
packages/orchestration/model_aliases.py:44:    "claude-workhorse": "claude-sonnet-4-20250514",
packages/orchestration/model_aliases.py:46:    "ollama-default": "qwen3-coder-next",
```

## Deviations, assumptions, observations
- DEVIATION, declared: the Done-when "hits ONLY in model_aliases.py" is NOT met and cannot
  be met inside the declared change set. Nine hits survive in five files; four of those
  files (ollama_builder/provider.py, ollama_planner/provider.py, orchestration/config.py,
  role_config.py:114's prose, which the step ordered left untouched) are outside the paths
  this round may edit. Scope discipline won — AGENTS.md: prefer smaller changes.
- What IS true, narrower: both DATED ids now occur only in model_aliases.py.
  `rg 'claude-opus-4-20250514|claude-sonnet-4-20250514' packages/ apps/ scripts/` returns
  exactly those 2 lines, exit 0; only undated `qwen3-coder-next` survives elsewhere. The
  feature file's acceptance says "no hardcoded DATED model string", so R4 must decide
  explicitly whether its repo scan covers dated ids only or every built-in id — if the
  latter, R4 needs the two ollama providers and config.py inside ITS change set.
- Assumption: the one-line WHY comment above `_PROVIDER_DEFAULT_MODELS` and above the new
  `_DEFAULT_CLAUDE_MODEL` is AGENTS.md Code Discoverability for definitions touched anyway,
  not scope creep. No other line of either file changed.
- Observation: the R4 docs/ deferral is right — the alias module's public surface is final
  only once R3 consumes `builtin_model_ids()`; documenting it now would be rewritten.
- Behaviour unchanged: the five ids were read out of `git show HEAD:…` and compared
  programmatically before the table was written, so every evaluated default is byte-identical
  to R1. 0 open findings; next free ID R-0212.

## Item status
| Item | Status | Reason |
|---|---|---|
| A receipts persist first | done | 4254503b, .agent paths only, before any code |
| B model_aliases.py | done | 5 aliases, 3 accessors, imports nothing from the package |
| C role_config + pingpong routing | done | 5 + 1 literals relocated, nothing else touched |
| D test_model_aliases.py | done | 18 tests; no network, no ANTHROPIC_API_KEY |
| E commit, push, handoff | done | 2 commits pushed; this file is commit 3 |

## Next
Reviewer re-reads `git diff 5fed2fca..HEAD` and re-runs the 11 gate commands. On PASS,
LAST_REVIEWED_SHA advances to the tip and R3 opens (known-dead list + doctor check),
carrying the scan-scope question above. No PR exists for this branch.
