# Handback — F199 round 3: book round 2 and R-1266's resolution, DECISION F199 D2, and the checks snapshots, worktrees and providers

## Session

SESSION 1 of feature F199 · round 3 · rounds so far 3

Context self-assessment: the block, the three source modules it named and round 2's handback were enough to write every check without a second look; the one thing I could not see beforehand was whether git prints the `prunable` key on this machine, which the worktree test now pins against a real repository.

Fortschritt: ~45 % (T001 complete · T002, T003 and the closure open) — Schätzung

## Range

Review of `4f0fa7474`..HEAD (round 3: C1 to C4, then C5; this handback is C5).

## Commits

### 42af75304 F199 R3 C1: book round 2 and R-1266's resolution, DECISION F199 D2, save the round 3 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f199-r3.md` | +193/-0 | NEW FILE, byte copy of `block.md` (193 lines, sha256 `83a73df57727a553cfb7ddac5cd23bccbb2070085cef0ff338759452de3c993c`) |
| `.agent/live_review.md` | +4/-0 | byte copy of `dry-live_review.md` |
| `.agent/prose_slips.md` | +1/-0 | byte copy of `dry-prose_slips.md` |
| `.agent/decisions.md` | +12/-0 | byte copy of `dry-decisions.md` (DECISION F199 D2) |
| `.agent/plan.md` | +8/-9 | byte copy of `dry-plan.md` |

### 5383a717e F199 R3 C2: the health checks of the snapshots, the worktrees and the providers (T001)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/self_health.py` | +155/-1 | `check_snapshot_manifests`, `check_worktrees`, `check_providers`, their hints and `SNAPSHOT_SAMPLE`; `run_health_checks` answers seven |
| `apps/cli/command_catalog_doctor.py` | +3/-2 | the `doctor.health` description names the seven checks |

### fb05abb14 F199 R3 C3: the snapshot, worktree and provider checks' tests (T001)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_self_health.py` | +196/-3 | snapshot, worktree and provider tests; the set test answers seven |
| `tests/cli/test_doctor_health_cmd.py` | +5/-4 | the fixture also fixes `check_providers`; counts become seven (8 lines, `1 of 7`) |

### f66fa7bc9 F199 R3 C4: the self-health page names seven checks

| Path | +/- | Reason |
|---|---|---|
| `docs/system/self-health-v1.md` | +16/-6 | banner, three table rows, the warn-and-exit-0 sentence, the example, "Not yet" |
| `docs/README.md` | +1/-1 | the system-table row names seven checks |

### (this commit) F199 R3 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this handback |

## External actions

- `git push origin feature/f199-self-health` runs after this commit; its result is in the session's final reply. No pull request opened, no worktree added.

## Verification

Preconditions: branch `feature/f199-self-health`, HEAD `4f0fa7474`, `git status --porcelain` empty. Digests of `block.md` (193 lines), `run_selection.py`, `selection.txt` and the four `dry-*` files matched.

Gate 1: `git -C /home/decodeux/Repos/remedy status --porcelain` — empty.

Gate 2: the ordered `python3 -m ruff check` over the four paths — `All checks passed!`

Gate 3 (HEAD `f66fa7bc9`, run once): exit 0, `4393 passed, 3 skipped in 30.43s`; no FAILED, ERROR, `absent in tree:` or `process(es) behind` line (the saved output was searched). SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine F252), `tests/test_install_smoke.py:175` (opt-in install smoke), `tests/test_repair_context_reviewer_memory.py:257` (UI source not found).

Gate 4: `python3 -m apps.cli.main integrity check --json` — `fail_count` 0, `ok` true, 6 checks.

Gate 5: `open_finding_ids` -> `['R-1235', 'R-1246', 'R-1251', 'R-1252']`.

Gate 6: `python3 -m apps.cli.main doctor health` — exit 0:
```
Remedy health: PASS
  [PASS] config: every configured value has its declared type
  [PASS] ledgers: 2 of 2 token ledgers passed SQLite's integrity check
  [PASS] snapshots: 20 of 20 newest workspace snapshots passed their hash check
  [PASS] worktrees: 12 repositories checked; no worktree is prunable
  [PASS] providers: reachable: claude-cli, ollama; not reachable: claude; no provider was called
  [PASS] staging_copies: 0.0 GB of staging copies can be freed, below the warning level of 5 GB
  [PASS] disk: 1185712205824 bytes free; no floor is configured (budget.min_free_disk_bytes)
```

## Authored-text proofs

C1's four `dry-*` files were copied over their paths; `git diff --cached --numstat` named exactly five paths with `193 0`, `12 0`, `4 0`, `8 9`, `1 0`. The block copy `.agent/authored/f199-r3.md` has 193 lines and sha256 `83a73df57727a553cfb7ddac5cd23bccbb2070085cef0ff338759452de3c993c`, equal to the delivering prompt.

## Deviations & assumptions

1. The `doctor.health` description is split over three source lines; the joined string equals the block's text.
2. `check_snapshot_manifests` catches nothing: `_check_snapshot_integrity` already absorbs unreadable manifests, and the block names no exception class for it. A manifest that is valid JSON but not an object would raise; I did not add a handler the block did not order.
3. The `run_health_checks` example in the page shows a WARN for `providers` and one for `staging_copies`, so the example's first line stays `Remedy health: WARN`.
4. Gate 6 here shows `worktrees` reading 12 repositories; that count comes from this machine's registered projects, not from the tests.

## For the operator, in plain sentences

The health command now has seven checks. It also looks at the saved copies Remedy keeps to undo a change, at leftover working folders whose files are gone, and at whether any model service can be reached from this machine. That last one only warns, so a machine that just builds and tests stays healthy.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. Phase 1 rule 2: the Open PR Gate.
3. The next round's first commit books round 3's verdict.
4. T002, the local crash report.

Operator questions open: 0.
Open findings: 4 — R-1235, R-1246, R-1251 and R-1252, owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five paths, numstat as ordered; block copy 193 lines and digest equal |
| C2 | done | three checks, hints, order of seven, catalog description |
| C3 | done | snapshot, worktree, provider and set tests; command tests at seven |
| C4 | done | page and index row |
| C5 | done | this handback |
| Gate 1 | passed | status empty |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | exit 0, `4393 passed, 3 skipped`, first run |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | exact open-finding set |
| Gate 6 | passed | exit 0, all seven checks PASS |
| T001 | done | the command and its seven checks, tests and page |
