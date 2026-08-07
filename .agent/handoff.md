# Handoff — F254 R4 (findings persisted, known-dead model list + loader)
Feature T2_F254 · Round R4 · SPLIT · branch `feature/f254-model-alias-table`.
No `remedy doctor` wiring this round — that is R5, by design.
Length: 122 lines, over the 60 target. Reason: five mandated tables (changed files, pair
counts, provenance, 16 test files, item status) are ~50 lines before any prose. No section
is dropped; no verbatim command transcript is pasted, which was last round's cause.

## Commits (range 513451b4..HEAD)
- `74baaa7b` docs(f254): persist the R3 verdict and finding R-0213 — `.agent/` paths ONLY.
- `5ecd0197` feat(f254): add the known-dead model list and its loader — pushed, exit 0
  (513451b4..5ecd0197). Diff 438 lines, under the 500 limit.
- commit 3 `chore(f254): rewrite handoff for the R4 handback` — SHA self-referential (this
  file is its only content), branch tip at handback; declared, not guessed.

## Changed files — GENERATED from `git diff --numstat 513451b4..HEAD` (R-0210, not retyped)
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r4-1.md | +121 | -0 |
| .agent/authored/f254-r4-2.md | +81 | -0 |
| .agent/live_review.md | +69 | -13 |
| .agent/plan.md | +16 | -17 |
| packages/orchestration/config.py | +13 | -0 |
| packages/orchestration/dead_model_list.py | +169 | -0 |
| scripts/dead_models.json | +16 | -0 |
| tests/orchestration/test_dead_model_list.py | +240 | -0 |
| .agent/handoff.md | self-ref | written by commit 3; declared, not omitted |

## Transport proofs (A — copied with `cp`, never retyped)
`cmp <scratchpad>/f254-r4-N.md .agent/authored/f254-r4-N.md` → no output, **exit 0**, N = 1,2.
sha256 (original and applied copy identical for both):
`ed6ea9fe238005a3a500322aa2b44f3701d73919e44500b1820f29b59474abd3`  f254-r4-1.md
`a5e7e73bbd4c18788eb7b58940be11820f8a4ec33de479a8f10f25ed3bd5019a`  f254-r4-2.md

## Pair counts — all six REWRITE-shaped
| Receipt → target | Pairs | FROM before | FROM after | TO after |
|---|---|---|---|---|
| f254-r4-1 → .agent/live_review.md | 1, 2, 3 | 1x each | 0x each | 1x each |
| f254-r4-2 → .agent/plan.md | 1, 2, 3 | 1x each | 0x each | 1x each |
Structure: live_review.md has `## Steps`/`## Findings`/`## Decisions`/`## Verdicts` 1x each;
plan.md has `## Goal` and `## Next Steps` 1x each, 46 lines (<50). The duplicated trailing
bullet IS gone — `grep -c 'Then the integration gate' .agent/plan.md` → **0**, and Next Steps
now ends at the R8 closure bullet.

## Provenance of every string in scripts/dead_models.json — nothing invented
| String | Source in this repo |
|---|---|
| `claude-opus-4-20250514` | `MODEL_ALIASES["claude-flagship"]`, packages/orchestration/model_aliases.py:42 |
| `claude-sonnet-4-20250514` | `MODEL_ALIASES["claude-workhorse"]`, packages/orchestration/model_aliases.py:44 |
| "May-2025 dated id … several generations stale as of Aug 2026" | T2_F254.md, "How it fits" |
| "choosing the successor is F232's job" | T2_F254.md header (Blocks/used by: F232) + Non-goals |
| `superseded_by` = `""` (both) | NO in-repo source names a replacement — honestly empty, not guessed |
`qwen3-coder-next` is deliberately NOT listed: nothing in this repo says it is dead.

## Verification — every command run for real, counts summarised (no verbatim transcripts)
Fresh interpreters, both **exit 0**: `python3 -c "import packages.orchestration.dead_model_list"`,
`python3 -c "import packages.orchestration.config"` — no import cycle.
`python3 -m ruff check` on all three touched Python paths → "All checks passed!", **exit 0**.
`python3 -m pytest <path> -q`, every one **exit 0**, run AFTER the final config-key placement:

| Test file | Passed |
|---|---|
| tests/orchestration/test_dead_model_list.py (new) | 23 |
| tests/orchestration/test_model_aliases.py | 21 |
| tests/orchestration/test_config.py | 62 |
| tests/cli/test_config_cmd.py | 14 |
| tests/ui_server/test_dashboard_contract.py | 70 |
| tests/orchestration/test_test_runner.py | 51 |
| tests/regression/test_resource_safety.py | 21 |
| tests/cli/test_golden_path.py | 42 |
| tests/orchestration/test_checkpoints.py | 37 |
| tests/orchestration/test_long_run_executor.py | 74 |
| tests/orchestration/test_mission_dossier.py | 103 |
| tests/orchestration/test_job_budgets.py | 76 |
| tests/orchestration/test_self_healing_cycles.py | 50 |
| tests/orchestration/test_run_manifest_schema.py | 13 |
| tests/orchestration/test_fence_e2e.py | 130 |
| tests/docs/ | 294 |
Config-key-registry search, as ordered: `rg -l '_CONFIG_KEY_SPECS|config_keys|key_spec' tests/`
found 10 files — 9 pre-existing (test_model_aliases, test_checkpoints, test_long_run_executor,
test_mission_dossier, test_job_budgets, test_self_healing_cycles, test_run_manifest_schema,
test_config, test_fence_e2e) plus the new one; ALL run, all green. `rg -n 'all_key_specs'`
also named apps/cli/commands/config_cmd.py and packages/orchestration/run_manifest.py as
consumers — their tests are in the table. No "every key is documented" test went red.
Round gate + canary only — NO full-suite claim. `git status --porcelain` empty at every
commit. No force-push, no history rewrite, no `git worktree`, no PR created, main untouched.

## Deviations, assumptions, observations
- No deviation from the ordered change set: exactly the 9 listed paths changed. Nothing under
  apps/, docs/, docs/roadmap/ or .claude/; model_aliases.py, role_config.py,
  pingpong_provider.py, both Ollama providers and every existing test are untouched.
- DEVIATION (placement, declared): the `doctor.dead_models` ConfigKeySpec was first written
  between `orchestrator.model` and `orchestrator.max_iterations`, which split that prefix
  pair. Self-review caught it and it was moved to sit AFTER the whole `orchestrator.*` group
  and before `dossier.max_tokens`, so every prefix group stays intact and the new key still
  neighbours the model-related keys. The full gate was re-run after the move; the table above
  is the post-move run.
- Assumption: `superseded_by` is allowed to be absent as well as empty in a hand-edited file,
  so the loader defaults it to `""`. `id` and `reason` are hard requirements.
- Assumption: config unavailability yields NO extension rather than an exception (the
  `product_smoke.smoke_config()` pattern), while the SHIPPED list's own failures raise. The
  guarantee is the shipped list; losing the optional extension must not take it down.
- Four names beyond the ordered surface, declared not hidden: `DEAD_MODEL_SCHEMA_VERSION`,
  `DEAD_MODEL_CONFIG_KEY`, `DEAD_MODEL_LIST_FILENAME`, `DeadModelListError`. The tests assert
  the schema version and key name without retyping them; the loader needs a typed error.
- Test isolation: config-reading tests resolve config from non-existent tmp_path TOML paths
  via `load_config(project_path=…, user_path=…)`, monkeypatch `config._CACHED_CONFIG`, and
  `reset_config()` on teardown — no global cache survives, no real remedy.toml is read.
- Open findings: **0**. R-0213 was registered and closed in commit 74baaa7b; next ID R-0214.

## Item status
| Item | Status | Reason |
|---|---|---|
| A receipts persist first | done | 74baaa7b, `.agent/` paths only, before any code |
| B shipped data file | done | scripts/dead_models.json, 2 entries, both traceable |
| C loader + config key | done | dead_model_list.py + one ConfigKeySpec; no import cycle |
| D unit tests | done | tests/orchestration/test_dead_model_list.py, 23 tests |
| E commit, push, handoff | done | 2 commits pushed; this file is commit 3 |

## Next
Reviewer re-reads `git diff 513451b4..HEAD` bottom-up and re-runs the gate above. On PASS,
LAST_REVIEWED_SHA advances to the tip and R5 opens: wire the dead-model check into
`remedy doctor core`. No PR exists for this branch.
