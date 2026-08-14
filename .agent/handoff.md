# Handback — F077 Autonomy watchdog · R4

Feature F077 (T2), round R4 of 7. Branch: feature/f077-autonomy-watchdog.
Open findings: seventeen — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368,
R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380,
R-0381, R-0382. Next free id R-0383. No finding was resolved this round.

## Range
Review of 4bbb0c90..25b273f8 (the handback commit follows; see Next).

## Commits

### 32fc6ebe chore(f077): save the R4 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f077-r4.md | +235/-0 | the R4 block, byte-for-byte |
| .agent/last_block.md | +219/-78 | `cp` of the same bytes |

### 0b3dbc98 docs(f077): record the R3 verdict and re-sync state
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | blank line + the GATE-R3 slice, appended |
| .agent/plan.md | +26/-23 | current step R4/T001; round numbering re-synced |
| .agent/context.md | +7/-3 | config.py in scope; Steps line now R1-R7 |

### e60b54f0 feat(f077): add the three watchdog tripwire evaluators
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/watchdog.py | +335/-0 | Trip, thresholds, 3 evaluators, aggregate |

### 2baa5366 feat(f077): add watchdog threshold config keys
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/config.py | +52/-0 | four `watchdog.*` ConfigKeySpec entries |

### 25b273f8 test(f077): pin each watchdog tripwire and its near miss
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_watchdog.py | +268/-0 | 13 tests, in-process entry factory |

Handback commit, R-0149 self-reference exception: `.agent/handoff.md`, rewrite.

## External actions
`git worktree add .remedy-wt/probe_r4 HEAD` → created at 25b273f8 (gate 10);
`git worktree remove --force` + `git worktree prune` → OK, list back to 1 line.
No PR created, edited or merged; no `gh` command run. Push of this branch
follows this commit; its result is in the round report.

## Verification
1. `git status --porcelain` → exit 0, EMPTY. `git worktree list` → 1 line.
2. `cmp .agent/authored/f077-r4.md .agent/last_block.md` → exit 0. Shared
   sha256 `b3bfba41b762d4753e295811fff198a8f6a55b9a1c1ebb04ad5e8386f841b4c6`,
   18435 bytes, 235 lines (cap 400).
3. `grep -c "^Gate: R3 — PASS" .agent/live_review.md` → 1. `^## Steps` → 1.
4. `git show --numstat 0b3dbc98 -- .agent/live_review.md` → `2  0`; deletion
   column 0.
5. `^- R-\d+ — ` paragraphs → 17; `^Done: R-\d+ — ` → 0; `^Landed:` → 0. Open
   set = the seventeen ids named above.
6. `wc -l .agent/plan.md` → 44 (cap 50). context.md reader strings present:
   `## Active Branch`, `feature/f077-autonomy-watchdog`, `Steps`, `F077`,
   `resource`, `pytest` — all six found.
7. `pytest tests/orchestration/test_watchdog.py -q` → exit 0, `13 passed`.
8. `ruff check packages/orchestration/watchdog.py
   packages/orchestration/config.py tests/orchestration/test_watchdog.py` →
   exit 0, `All checks passed!`.
9. Purity grep `open\(|write_text|write_bytes|load_mission|save_mission|
   set_mission|append_ledger` on watchdog.py → exit 1, ZERO hits.
10. Red-proof probe in the disposable worktree `.remedy-wt/probe_r4` (G5).
    From inside it, `python3 -c "import packages.orchestration.watchdog as w;
    print(w.__file__)"` printed
    `/home/decodeux/Repos/remedy/.remedy-wt/probe_r4/packages/orchestration/watchdog.py`
    — the mutated copy, not the primary checkout. With the body of
    `evaluate_goal_drift` replaced by `raise AssertionError("probe")` the C4
    suite went RED; the failures were
    `test_goal_drift_fires_on_a_milestone_the_plan_never_named`,
    `test_goal_drift_stays_silent_when_every_dispatch_is_on_plan`,
    `test_evaluate_ledger_reports_trips_in_the_fixed_order`,
    `test_every_evaluator_tolerates_a_torn_entry_without_raising`.
    Worktree removed and pruned.
11. `pytest tests/orchestration/test_orchestrator_loop.py
    tests/orchestration/test_config.py -q` → exit 0, `258 passed` (196 + 62).
12. Canary `pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed`.
13. `pytest tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0, `142 passed`.
14. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`.
15. `git diff --name-only 4bbb0c90..HEAD` → the eight non-handoff files the
    Change line names (handoff.md lands in this commit).
    `git diff --stat 4bbb0c90..HEAD -- docs/` → EMPTY.
16. Insertions: 32fc6ebe 454 · 0b3dbc98 35 · e60b54f0 335 · 2baa5366 52 ·
    25b273f8 268. None over 500.
17. `test -e .agent/STOP` → does NOT exist; checked before the round started
    and again at handback.

## Authored-text proofs
GATE-R3 was extracted by a script under `.remedy-wt/` (gitignored) from the
COMMITTED `.agent/authored/f077-r4.md` between its `>>> GATE-R3 >>>` and
`<<< GATE-R3 <<<` markers and applied DISK-TO-DISK; never retyped. One physical
line, 3392 bytes, sha256
`1dc9ef39420fcf6b432ee7cd615e187bdb9264728bd690126550212e1cfe990f`.
`.agent/live_review.md` ends with exactly one blank line + that slice, and the
text above it still ends in a single newline (numstat `2 0` confirms nothing
above moved). Trailing-whitespace scan over all nine touched files: none.

## Deviations & assumptions
1. C4 carries 13 tests, not the 12 the block enumerated. The extra one,
   `test_no_progress_starts_a_new_run_on_a_different_milestone`, pins the C2
   sentence "A different milestone_id starts a new run", which the twelve
   ordered tests leave unexercised. Declared, not silent.
2. DECISION D15 stated-cause overage: this handback is 133 lines against
   the 60-line cap. The mandated content behind it: seventeen gate results with
   their real values (gate 10 alone names four failing test ids), five
   per-commit changed-files tables, the transport proof and the C0-C5
   item-status table. No section dropped, no prose padded.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0 | done | block saved verbatim, `cmp` exit 0 |
| C1 | done | GATE-R3 appended disk-to-disk; both mirrors re-synced |
| C2 | done | watchdog.py, pure, ruff clean, purity grep empty |
| C3 | done | four `watchdog.*` keys, test_config.py 62 passed |
| C4 | deviated | 13 tests, not 12 — see Deviations 1 |
| C5 | done | this file |

## Next
Re-read `.agent/STOP` from disk (Phase 1 rule 1,
docs/agents/self_drive_protocol.md) — a sentinel appearing mid-session is
otherwise invisible. Then the Open PR Gate (rule 2):
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
Then review 4bbb0c90..HEAD and issue the R4 verdict. On PASS, R5 = T002: the
pause seam, one decision per trip class, dedup and the ledger entry.
