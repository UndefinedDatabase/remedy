# Handback — F079 R1 (claim + candidate sweep + R-0199 diagnosis + T001)

Branch: feature/f079-context-handoffs (from main @ 38854f60 after PR #180
merged at the Open PR Gate). Commits 7d8fe554 · 42ee0b46 · 2a75cbf8 ·
6ef34950 · 33db3aa5 (+ this handoff). No PR — closure creates it.

## Changed files per commit
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 7d8fe554 | .agent/last_block.md | +309/-257 | R1 block saved verbatim |
| 42ee0b46 | .agent/authored/f079-r1-{1..6}.md | +139/-0 | six texts, sha256 verified |
| 2a75cbf8 | .agent/live_review.md | +49/-117 | F079 ledger, R-0200..R-0202 |
| 2a75cbf8 | .agent/candidates.md | +5/-25 | four candidates swept, now empty |
| 2a75cbf8 | .agent/plan.md · context.md | +36/-39 | F079 plan/scope |
| 2a75cbf8 | docs/roadmap/STATUS.md | +1/-1 | F079 `[ ]` -> `[~]` |
| 2a75cbf8 | docs/roadmap/features/T3_F106.md | +9/-0 | R-0201 routing note |
| 6ef34950 | packages/orchestration/handoff.py | +499/-0 | T001 composer (NEW) |
| 33db3aa5 | tests/orchestration/test_handoff.py | +416/-0 | T001 tests (NEW, 23) |

Authored-text hashes: all six matched their BEGIN-marker sha256 before any
application (verified with sha256sum; no mismatch, nothing retyped).

## Verification transcripts
| Command | Exit | Tail |
|---|---|---|
| `git status --porcelain` (preflight) | 0 | (empty) |
| `gh pr merge 180 --merge --delete-branch` | 0 | `Fast-forward … 15 files changed` |
| `python3 -m pytest tests/docs/ -q` | 0 | `293 passed in 0.48s` |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 21.74s` |
| `python3 -m pytest tests/orchestration/test_handoff.py -q` | 0 | `23 passed in 0.22s` |
| `ruff check packages/orchestration/handoff.py tests/…` | 0 | `All checks passed!` |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary, final) | 0 | `42 passed in 19.23s` |
| `git status --porcelain` (final) | 0 | (empty) |

## R-0199 diagnosis (measured, no fix — R2 orders it)
Hypothesis CONFIRMED as mechanism: `data_root_digest` hashes every file
under the operator's REAL data root, twice per run.
- Call sites (production): `gauntlet_runner.py:461` (before the run) and
  `gauntlet_runner.py:533` (after, always, even on crash). No others
  outside tests. -> 2 calls/run x 10 frozen orders = **20 calls/campaign**
  (`gauntlet_orders.load_order_set()` = 10 orders; campaign loop
  `gauntlet_runner.py:632-638`).
- Root resolved (not guessed): `run_campaign` -> `real_data_root or
  resolve_data_root()` (`gauntlet_runner.py:632`), resolved BEFORE any
  isolation; `REMEDY_DATA_DIR` unset and no `data_dir` config here, so
  `data_paths.py:50-52` -> **`/home/decodeux/Repos/remedy/.data`**.
- Measured (throwaway script outside the repo, deleted after):
  file_count **2,495,115** · total_bytes **143,655,667,319** (133.79 GiB)
  · walk-only 66.8 s · **one `data_root_digest()` call = 394.8 s**
  (digest `sha256:9c5c18dc…`). No timeout — well inside the 15-min cap.
- Breakdown: `job_workspaces` = 143.37 GB / 2,240,761 files = **99.80 %**
  of the bytes; every other subtree together is < 0.3 GB.
- Bytes per campaign today = 143.66 GB x 20 = **~2,873 GB** (~2.9 TB), and
  ~7,900 s (2.2 h) of pure hashing. The attempt-03 observation of ~872 GB
  is **consistent** with this mechanism at the root size of that date:
  872 / 20 = 43.6 GB per call, i.e. a `.data` roughly a third of today's —
  the cost scales with operator history exactly as the hypothesis says.

## Reuse surfaces (slice 6) — what T001–T003 must call
| Piece | Where | Used by |
|---|---|---|
| Dossier renderer | `mission_dossier.py:198 render_dossier` / `:187 render_dossier_body`; newest stored text `:828 newest_dossier_text`, version `:414 latest_dossier_version`, live state `:808 load_dossier_state` | T001 |
| Evidence-area path scheme | `mission_state.py:282 mission_evidence_dir` (+ `mission_dossier.py:365 DOSSIER_VERSION_TEMPLATE` = the `_v<N>` accumulation precedent) | T001 |
| Checkpoint ref + verification | `checkpoints.py:98 Checkpoint` (`content_hash` `:135`, `next_intent`), `:396 load_latest_valid`, `:234 resolve_worktree_head`, `:250 resolve_live_worktree_head` (stale-head check), `:80 AllCheckpointsCorruptError` | T001 / T002 |
| Open decisions | `decision_queue.py:62 list_decisions(job, events)` + `:439 open_decisions`; events via `timeline.py:68 load_run_events`; job via `storage.py:100 load_job_safe` / `pingpong_job.py:299 load_job_plan` | T001 / T002 |
| Next intent | `checkpoints.py:113 Checkpoint.next_intent` (recorded) with fallback `mission_dossier` `next_step` (narrated) | T001 |
| Recall harness | `mission_dossier.py:1037 run_recall_harness` + `:975 RECALL_FIXTURE_FACTS` (10 seeded facts) + `:1074 recall_report`; fixture mission goal `"The seeded mission goal is met"`, budget `RECALL_BUDGET_TOKENS=120`; exercised by `tests/orchestration/test_mission_dossier.py:1010-1081` | T003 |
| Redaction denylist | `run_manifest.py:102 is_secret_key` (`_SECRET_TERMS`, `:77`) + `stream_evidence.py:155 is_sensitive_key` / `:174 redact_text` | T001 |

T001 reuses, verbatim, all of the above except the T002/T003-only rows:
renderer + evidence path + accumulation precedent, checkpoint loader,
decision queue + event/job loaders, both redactors. It implements only the
composition, the gap naming and the `handoff_v<N>` accumulation.

## Notes for the reviewer
- Idempotence finding (fixed in-slice): the decision queue DERIVES stop
  reasons with a wall-clock `created_at`, so carrying that field made two
  builds of unchanged state differ. Decision rows now carry id/type/
  severity/summary/next_actions only; `test_derived_open_decisions_do_not_
  break_byte_identity` pins it.
- Oversize commit declared (AGENTS.md exception, first in this feature):
  7d8fe554 is 566 changed lines — the R1 block is ONE authored artifact
  saved verbatim; splitting it would corrupt the transported bytes. The
  ordered "COMMIT 1" was therefore split so the authored texts (42ee0b46,
  139 lines) ride separately; every other commit is < 500 lines.

## Item status
| Item | Status | Reason |
|---|---|---|
| 0 preflight | done | porcelain empty on feature/amend0805-v3 |
| 1 Open PR Gate | done | PR #180 merged, main pulled @ 38854f60 |
| 2 branch | done | feature/f079-context-handoffs |
| 3 state commits | deviated | ordered COMMIT 1 split into 7d8fe554 + 42ee0b46 to honour the < 500-line constraint; contents and order unchanged |
| 4 docs gates | done | 293 + 42 passed, both exit 0 |
| 5 R-0199 diagnosis | done | numbers above; no fix made |
| 6 reuse inspection | done | table above, read-only |
| 7 T001 | done | 23 tests, exit 0 |
| 8 handback | done | canary re-run 0, porcelain empty, branch pushed |
