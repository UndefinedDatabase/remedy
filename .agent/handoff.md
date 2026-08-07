# Handoff — F254 R3 (findings persisted, Acceptance amended, last 3 ids routed)
Feature T2_F254 · Round R3 · SPLIT · branch `feature/f254-model-alias-table`.
Length: 119 lines. Over 60 because this round owes an 11-row changed-files table,
7 pair counts under two shapes, two verbatim `rg` outputs and 21 test results. No
mandated section is dropped.

## Commits (range 807e3df7..HEAD)
- `1816f0a0` docs(f254): persist the R2 verdict, finding R-0212 and decision D11 —
  `.agent/` paths ONLY (3 receipts + live_review.md + plan.md), no code.
- `d8294663` docs(f254): clarify the acceptance scan covers every built-in id —
  T2_F254.md ONLY, no code. ROADMAP.md and STATUS.md untouched.
- `9a45a99a` feat(f254): route the remaining built-in model ids through the alias table
  — pushed, exit 0 (807e3df7..9a45a99a).
- commit 4 `chore(f254): rewrite handoff for the R3 handback` — SHA self-referential
  (this file is its only content), branch tip at handback; declared, not guessed.

## Changed files — GENERATED from `git diff --numstat 807e3df7..HEAD` (R-0210, not retyped)
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r3-1.md | +159 | -0 |
| .agent/authored/f254-r3-2.md | +67 | -0 |
| .agent/authored/f254-r3-3.md | +30 | -0 |
| .agent/live_review.md | +90 | -13 |
| .agent/plan.md | +13 | -13 |
| docs/roadmap/features/T2_F254.md | +7 | -0 |
| packages/orchestration/config.py | +6 | -1 |
| packages/providers/ollama_builder/provider.py | +5 | -1 |
| packages/providers/ollama_planner/provider.py | +5 | -1 |
| tests/orchestration/test_model_aliases.py | +26 | -4 |
| .agent/handoff.md | self-ref | written by commit 4; declared, not omitted |

## Transport proofs (A — copied with `cp`, never retyped)
`cmp <scratchpad>/f254-r3-N.md .agent/authored/f254-r3-N.md` → no output, **exit 0**, N = 1,2,3.
sha256 of the applied copies:
`6f1a622d0229186eff53d68f35bf9b3446f935f5cd1d0a99d061900670634489`  f254-r3-1.md
`70ed11a19b7f8a4ab174565184af3998735a47e3b8f60d456a4e47f92621eb90`  f254-r3-2.md
`66c5a335d0666068a4af8ac9e1abdf6d704d8b7e2c40ce7adc07a738a9f85937`  f254-r3-3.md

## Pair counts — EACH UNDER ITS OWN SHAPE
BEFORE editing all 7 FROMs occurred exactly **1x** — nothing ambiguous. AFTER:
- r3-1 P1/P2/P4 (REWRITE): FROM **0x**, TO **1x** each.
- r3-1 P3 (**APPEND**): FROM **1x** by construction (the TO contains the FROM verbatim),
  TO 1x, TO-ONLY block (the D11 text) **1x**. No 0x is claimed for it.
- r3-2 P1/P2 (REWRITE): FROM **0x**, TO **1x** each.
- r3-3 P1 (**APPEND**): FROM **1x**, TO 1x, TO-ONLY block (the new Acceptance bullet)
  **1x**. No 0x is claimed for it.
Structure holds: live_review.md has `## Steps`/`## Findings`/`## Decisions`/`## Verdicts`
1x each; plan.md has `## Goal` and `## Next Steps` 1x each, 47 lines (<50).

## `rg -n 'qwen3-coder-next' packages/ apps/ scripts/` — exit 0, REAL output
```
packages/providers/ollama_builder/provider.py:18:  4. Built-in default (qwen3-coder-next)
packages/providers/ollama_planner/provider.py:19:  4. Built-in default (qwen3-coder-next)
packages/orchestration/role_config.py:114:    qwen3-coder-next for ollama).
packages/orchestration/config.py:771:# model = "qwen3-coder-next"
packages/orchestration/config.py:774:# model = "qwen3-coder-next"
packages/orchestration/config.py:779:# model = "qwen3-coder-next"
packages/orchestration/model_aliases.py:46:    "ollama-default": "qwen3-coder-next",
```
Every remaining hit categorised: model_aliases.py:46 is **the alias table entry itself**,
the one place the id may live. The other six are **documentation prose** — two provider
docstring precedence lists, one role_config.py docstring sentence, three commented-out
sample-TOML lines. **No executable default survives outside the alias table**; there is
no hit I failed to route.

## `rg -n 'claude-opus-4-20250514|claude-sonnet-4-20250514' packages/ apps/ scripts/` — exit 0
```
packages/orchestration/model_aliases.py:42:    "claude-flagship": "claude-opus-4-20250514",
packages/orchestration/model_aliases.py:44:    "claude-workhorse": "claude-sonnet-4-20250514",
```
Still exactly the two model_aliases.py lines, unchanged by this round.

## Verification — every command run for real, every exit code recorded
`python3 -c "import packages.orchestration.config"` in a fresh interpreter → **exit 0**:
no import cycle (model_aliases imports nothing from packages.orchestration).
Gate set, `python3 -m pytest <path> -q`, all **exit 0**: test_model_aliases 21 ·
test_role_config 32 · test_config 62 (the file exists, run as written) · test_provider_mode
24 · tests/docs/ 294 · dashboard contract 70 · test_test_runner 51 · resource safety 21 ·
golden path 42.
`rg -l 'ollama_builder|ollama_planner' tests/` found 14 files; the 12 not already gated
were each run, all **exit 0**: test_do_cmd_cli_path 9 · test_builder_bridge_smoke 3+1skip ·
test_builder_eval 69+1skip · test_builder_prompt_quality 14 · test_escalation 66 ·
test_long_run_executor 74 · test_real_ollama_smoke 2+3skip (opt-in `real_ollama` marker) ·
test_structured_planner_cli 15 · test_cli_main 48 · test_ollama_builder 18 ·
test_ollama_provider 19 · test_run_log_cli 61. No failures anywhere.
Round gate + canary only — NO full-suite claim. `python3 -m ruff check` on all four touched
Python paths → "All checks passed!", exit 0. `git status --porcelain` empty at every commit.
No force-push, no history rewrite, no `git worktree`, no PR created, main untouched.

## Deviations, assumptions, observations
- No deviation from the ordered change set: exactly the 11 listed paths changed; nothing
  under scripts/, apps/ or .claude/; no other test edited.
- Declared addition inside an in-scope file: `test_model_aliases.py`'s MODULE DOCSTRING
  now names the two new sources it covers. Not ordered explicitly; done because leaving it
  stale would misdescribe the file being extended. Flagged, not hidden.
- Assumption: the one-line WHY comment above each routed definition is the same convention
  R2 used, not creep. Nothing else in those three files changed — the docstring line
  "4. Built-in default (qwen3-coder-next)" is untouched in both providers, per D11.
- Behaviour checked, not assumed: a fresh interpreter reports `_DEFAULT_MODEL` =
  `qwen3-coder-next` for both providers and `get_key_spec("ollama.model").default` the same.
- OBSERVATION, not fixed by me: after r3-2 P2, `.agent/plan.md` still carries its old
  trailing bullet "Then the integration gate, then closure per …STATUS_closure_protocol.md",
  which now duplicates the new R6/R7 bullets. It sat outside every authored FROM block, so
  removing it would have been improvisation. Flagged for the next authored receipt.
- Open findings: **0**. R-0212 was registered and closed in the same commit; next ID R-0213.

## Item status
| Item | Status | Reason |
|---|---|---|
| A receipts persist first | done | 1816f0a0, `.agent/` paths only, before any code |
| B feature-file amendment | done | d8294663, T2_F254.md only, APPEND pair, +7/-0 |
| C route the 3 built-in ids | done | 2 providers + `ollama.model` spec, no import cycle |
| D extend test_model_aliases | done | 3 tests added to `TestRelocationIsFaithful`, 21 total |
| E commit, push, handoff | done | 3 commits pushed; this file is commit 4 |

## Next
Reviewer re-reads `git diff 807e3df7..HEAD` bottom-up and re-runs the gate above. On PASS,
LAST_REVIEWED_SHA advances to the tip and R4 opens: the config-driven known-dead list and
the `remedy doctor` check that reads it. No PR exists for this branch.
