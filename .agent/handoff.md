# Handback — F079 R2 (R-0199 fix + T002 + T003)

Branch: feature/f079-context-handoffs. Range 79621fc0..8a25af2d, 9 commits
(+ this handoff). No PR — closure creates it.

## Changed files per commit
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 1be0d87a | .agent/last_block.md | +223/-281 | R2 block saved verbatim (rides alone) |
| c72c0e60 | .agent/authored/f079-r2-{1,2}.md | +111/-0 | two texts, sha256 verified |
| b3a0291e | .agent/live_review.md · plan.md | +83/-61 | R1 PASS persisted, R2 plan |
| e249ea15 | packages/orchestration/gauntlet_runner.py | +33/-14 | R-0199: metadata-manifest digest |
| e249ea15 | tests/orchestration/test_gauntlet_runner.py | +33/-0 | remove/resize/mtime/prefix tests |
| 0cdb2019 | packages/orchestration/handoff.py | +193/-4 | T002 consumption + root discipline |
| 0cdb2019 | packages/orchestration/checkpoints.py | +17/-0 | `worktree_drift_message` — ONE wording |
| 0cdb2019 | apps/cli/commands/job.py | +3/-6 | resume now uses that one wording |
| 2860fa7d | apps/cli/command_catalog.py | +13/-0 | `mission.handoff` entry |
| 2860fa7d | apps/cli/commands/mission_cmd.py | +41/-0 | `_cmd_mission_handoff` + handler |
| 2860fa7d | packages/orchestration/orchestrator_loop.py | +75/-3 | boundary build + seed seam |
| 0ee4157f | tests/orchestration/test_handoff.py | +245/-0 | T002 triggers/consumption tests |
| 0ee4157f | tests/cli/test_mission_cmd.py | +63/-0 | explicit-trigger CLI tests |
| c6e8dc89 | packages/orchestration/handoff.py | +113/-0 | T003 boundary recall eval |
| 8a25af2d | tests/orchestration/test_handoff.py | +140/-0 | T003 threshold + archived report |

Authored hashes: f079-r2-1 `8077b273…`, f079-r2-2 `d4c7bcd3…` — both matched
their BEGIN markers before application; nothing retyped.

## Verification transcripts
| Command | Exit | Tail |
|---|---|---|
| `git status --porcelain` (preflight) | 0 | (empty) |
| `pytest tests/orchestration/test_gauntlet_runner.py -q` | 0 | `45 passed in 0.56s` |
| `pytest tests/orchestration/test_gauntlet_evaluator.py test_gauntlet_evidence.py -q` | 0 | `104 passed in 0.29s` |
| `pytest tests/orchestration/test_self_run_gauntlet.py -q` | 0 | `21 passed in 0.57s` |
| `pytest tests/orchestration/test_handoff.py -q` (final) | 0 | `39 passed in 0.33s` |
| `pytest tests/cli/test_mission_cmd.py -q` | 0 | `83 passed in 36.71s` |
| `pytest tests/orchestration/test_orchestrator_loop.py -q` | 0 | in `345 passed in 37.90s` (with handoff+cli+checkpoints) |
| `pytest tests/orchestration/test_worktree_resume_cli.py test_resume_kill.py -q` | 0 | `23 passed in 4.28s` |
| `pytest tests/docs/ -q` | 0 | `293 passed in 0.25s` |
| `pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 19.41s` |
| `ruff check` (every touched source) | 0 | `All checks passed!` |
| `git status --porcelain` (final) | 0 | (empty) |

## R-0199 — consumers inspected (2a) and the fix's proof (2d)
Consumers of the value / of `data_root_hash_before|after`, all string-opaque:
- `gauntlet_runner.py:461` (before) and `:533` (after) — the two producers;
  frequency unchanged, 2 per run.
- `gauntlet_runner.py:556`, `:585` — the field written into `run.json` bodies.
- `gauntlet_evidence.py:73-74`, `:199-200` — RunEvidence fields + loader.
- `gauntlet_evaluator.py:362-377` `_check_data_root` — the ONLY semantic
  consumer: it compares before vs after for equality and reports absence.
  Equality of two values from the same run is all it needs, so the digest
  definition is free to change under it.
- `gauntlet_matrix.py` — no reference (checked).
- tests: `test_gauntlet_runner.py:187-256,437,506-511,571`,
  `test_gauntlet_evidence.py:44-86`, `test_gauntlet_evaluator.py:196-336`,
  and 10 recorded fixtures under `tests/orchestration/fixtures/gauntlet/`
  (literal strings, compared only within their own run — unaffected).
New definition: sha256 over sorted `relpath\tsize\tmtime_ns` lines, no content
reads, value prefixed `meta-sha256:` so an old content digest can never
compare equal to a new one. Docstring states the honest contract (detects
add/remove/move/resize/mtime; does NOT detect a forged same-size same-mtime
edit — threat model is accidental writes).
TIMING on the real root (throwaway script outside the repo, deleted after):
**34.611 s**, digest `meta-sha256:e1308ade…` — against the R1 baseline of
394.8 s content-hashing (66.8 s walk-only). **11.4x faster**, and bytes read
drop from ~143.66 GB to ~0 per call: a campaign's 20 calls go from ~2.9 TB /
~2.2 h to ~692 s of metadata walking.

## T002 — pattern and seams
- CLI pattern followed: `CommandEntry` in `apps/cli/command_catalog.py:1625`
  (`mission.handoff`, `write_metadata`, `--json`) + handler entry in
  `mission_cmd.py:COMMAND_HANDLERS` — the same two-part registration
  `mission.ledger` uses. Unknown mission → `Error: no mission '…' exists to
  hand off` on stderr, exit 1.
- Loop seam (build): `orchestrator_loop.py:934` (stop terminal) and `:1112`
  (iteration limit) both return through
  `orchestrator_loop.build_boundary_handoff` (`:736`). A build failure lands
  in `MissionRunResult.handoff_error` and NOTHING else — the terminal is never
  masked (pinned by `test_a_build_failure_does_not_mask_the_terminal`).
- Loop seam (consume): `orchestrator_loop.py:915` seeds from
  `resume_seed_text` when the mission already has ledger history, and
  `assemble_context(handoff_seed=…)` adds `SECTION_HANDOFF` on iteration one
  only (`:115`, `:974`).
- R-0203: documented at the consumption seam (handoff.py module docstring,
  "ROOT DISCIPLINE") and made visible by `handoff_root_conflict`, which names
  a mission-root/data-root split instead of composing two worlds silently.
- Context-pressure detection stays unbuilt, documented in the same docstring.

## Reused pieces (T002/T003)
| Piece | Where | Used for |
|---|---|---|
| Checkpoint load rules | `checkpoints.py:396 load_latest_valid`, `:80 AllCheckpointsCorruptError` | reference verification |
| Live head | `checkpoints.py:250 resolve_live_worktree_head` | drift detection |
| Drift wording | `checkpoints.py:273 worktree_drift_message` (extracted from `job.py`'s resume refusal, now its only source) | stale-head refusal |
| Recall harness | `mission_dossier.py:1037 run_recall_harness` + `:975 RECALL_FIXTURE_FACTS` + `:1074 recall_report` | T003 measurement |
| Threshold citation | `run_recall_harness` docstring "Open facts must all be answerable. Resolved ones MAY compress away" + `RecallResult.recalled_all_open` | `RECALL_THRESHOLD_OPEN_ITEMS = 1.0` |
| Dossier writers | `mission_dossier.py:375 write_dossier_version`, `:796 save_dossier_state` | storing the eval's dossier |

T003 result: 5 open fixture facts all answerable from the handoff seed ALONE
(100%, threshold met), resolved facts compressed away and named; the report is
archived at `<mission evidence>/handoff_recall_eval.md`.

## Notes for the reviewer
- Scope deviation, declared: `checkpoints.py` and `apps/cli/commands/job.py`
  are outside the block's change list. Reason: the order requires the stale
  head to refuse "with the checkpoint feature's own message, never a new one";
  the wording lived inline in `job.py`, so it was extracted into
  `checkpoints.worktree_drift_message` and both callers now use it. Copying
  the sentence into handoff.py would have created the second implementation
  the order forbids. Byte-identical wording; resume tests green (23 passed).
- Oversize commit declared (first this feature): 1be0d87a is 504 changed
  lines — the R2 block is one authored artifact saved verbatim (R-0198 rule
  says it rides alone). Every other commit is < 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 state commits | done | A/B/C in order, hashes verified before applying |
| 2 R-0199 fix | done | consumers listed, metadata digest, 34.611 s measured |
| 3 T002 | deviated | built in full; +2 files beyond the change list for the shared drift wording (declared above) |
| 4 T003 | done | threshold met, report archived, harness reused verbatim |
| 5 handback | done | canary 0, porcelain empty, branch pushed |
