# Handoff — F157 round 7

## Session

SESSION 2 of feature F157 · round 7 · rounds so far 7. This round booked round 6's verdict,
appended DECISION F157 D6 and rewrote `.agent/plan.md`, then repaired R-1454 by stating in three
texts, with no behaviour change, what a run's degradations name.

Fortschritt: ~85 % (T001, T002 and T003 landed · the closure open) — Schätzung.

## Range

Review of `8d02e33ab`..`6267672ed`.

## Commits

### 60244e634 F157 R7 C1: book round 6, DECISION F157 D6, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r7.md` | +86/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | appends DECISION F157 D6 |
| `.agent/live_review.md` | +2/-0 | books round 6's Gate verdict PASS |
| `.agent/plan.md` | +6/-7 | rewritten: Current Step → round 7's repair, Next Steps → the closure sequence |

### 6267672ed F157 R7 C2: a run's degradations name what its provider pair runs in fallback whenever the feature is used
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/capability_routes.py` | +8/-3 | module docstring states D6 (1) and (3); a `# WHY:` line above `routed_claude_cli_build` states D6 (2); no code line changed |
| `docs/system/worker-adapter-contract-v2.md` | +15/-9 | the capability-matrix section's routes paragraph and its readers/reports paragraph say what a run's degradations name, and correct the routes paragraph's resume wording per D6 (1) and (3) |

## External actions

`git push origin feature/f157-capability-matrix` — run once immediately after this commit; no PR
opened, per the block's constraint.

## Verification

1. `git -C <repo> status --porcelain` → empty.
   `python3 .remedy-wt/f157-r7/prep/verify.py .` → every line `True`; last line `ALL True`; the
   `C3` row read `absent` at the time this gate ran, before this commit existed.

2. `python3 .remedy-wt/f157-r7/prep/run_selection.py . .remedy-wt/f157-r7-worker/selection-output.txt`
   → `exit 0`; last pytest line `3998 passed, 2 skipped in 28.46s`; no `FAILED`, no `ERROR`, no
   `process(es) behind` line anywhere in the output. The two `SKIPPED` lines: the pre-existing
   `test_install_smoke.py` (opt-in, needs network) and `test_agent_tooling.py` (a standing D12
   quarantine). Run once, as the block's rule states.

3. `python3 -m ruff check packages/orchestration/capability_routes.py` → `All checks passed!`,
   exit 0 (run twice while checking its result; see Deviations).
   `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, `"ok": true`, 6 of 6
   checks `pass`.

4. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `9`.

## Authored-text proofs

`.agent/authored/f157-r7.md`, applied at C1, compared disk-to-disk against the committed prepared
file `c1-.agent__authored__f157-r7.md` (itself byte-equal to `block.md`): byte-equal, 86 lines,
sha256 `938e4ccd5b239c07b51ac4b1e72f35620349cc52b5eb2ac103b58f93e20e8a1e` on both sides, and equal
to `block.md`'s own sha256. The other three C1 targets (`.agent/decisions.md` 4,098,098 bytes,
`.agent/live_review.md` 161,900 bytes, `.agent/plan.md` 1,167 bytes) were each compared disk-to-disk
against their own prepared `c1-*` file before the commit and read byte-equal; `verify.py`'s gate 1
re-confirms all four after the commit.

## Deviations & assumptions

One: gate 3's `ruff check packages/orchestration/capability_routes.py` was run twice rather than
once while confirming its result reads as a clean pass; both runs printed the identical
`All checks passed!` with no other output, so no mutation and no retry occurred, only a repeated
read of the same static check. The integrity check ran once. No other deviation: every ordered
commit, constraint and gate in the block matched what landed on disk; no production behaviour
changed this round, only the docstring, one comment and the documentation page.

For the operator: this round's test run covered a selection chosen for it, not the entire test
collection the repository holds; every test in that selection passed on its one run.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |
| R-1454 | done | repaired in C2, in the three texts D6 (3) names; its ledger entry is booked by the reviewer per `## Next` below |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | ruff run twice, see Deviations |
| Gate 4 | done | |
| Push | done | `git push origin feature/f157-capability-matrix` immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated.
3. Review round 7, then book its verdict and R-1454's resolution in the closure's first commit.
4. The closure sequence of `docs/roadmap/STATUS_closure_protocol.md`.
5. Operator questions open: 2.
6. Open findings count (gate 4): 9.
