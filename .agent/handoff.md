# Handback — F251 R4: R4 verdict + Ruling A persisted, F252 registered

## Range
Review of `6c98406..HEAD` — `feature/f251-suite-stabilization`, pushed, no PR; no closure work this round, as ordered.

## Commits
### c1b3341 chore(f251): persist the R4 PASS verdict + Ruling A plan
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r4-1.md | +43 | verdict text, sha256 e8932469… |
| .agent/authored/f251-r4-2.md | +25 | plan text, sha256 069a1e07… |
| .agent/live_review.md | +75 −43 | full replace from r4-1 (cmp 0) |
| .agent/plan.md | +56 −45 | full replace from r4-2 (cmp 0); `Done: R-0153` |

### 8a7c8e7 docs(f251): Ruling A — scope narrowed to flake stabilization
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r4-3.md | +18 | ruling text, sha256 68281fb6… |
| docs/roadmap/features/T1_F251.md | +18 −0 | inserted between Goal & Done and Rules |

### 7d4b586 docs(roadmap): register F252 + ledger pin 252 — ATOMIC
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r4-4..6.md | +72 | sha256 55350c40…, 8e361d6f…, 36e6c792… |
| docs/roadmap/features/T1_F252.md | +63 | full copy of r4-4 (cmp 0) |
| docs/roadmap/STATUS.md | +1 −0 | F252 line after F251 `[~]`, before F050 |
| docs/roadmap/ROADMAP.md | +9 −0 | Tier-1 entry after F251, before F050 |
| tests/docs/test_docs_consistency.py | +5 −3 | TOTAL_FEATURES 251→252, comment names F252 |

### this commit (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | rewrite | progress marks on the applied authored plan |
| .agent/handoff.md | rewrite | this handback — 100 lines (`wc -l`) |

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 verdict + plan (r4-1, r4-2) | done | c1b3341, both sha256 + cmp 0 |
| 2 T1_F251 Ruling A (r4-3) | done | 8a7c8e7, containment 0 |
| 3 atomic ledger (r4-4/5/6 + pin) | done | 7d4b586, one commit, never split |
| 4a FeatureLedger | done | 4 passed, 288 deselected |
| 4b full run vs catalogued 154 | **delta** | 152 — see below |
| 4c canary | done | 42 passed in 14.79s |
| 4d porcelain | done | empty |
| R-0153 | **Resolved** | authored plan applied verbatim |

## Authored-text proofs
All six texts hashed BEFORE any commit; every one matched the BEGIN marker
first time — no wrap recovery needed: r4-1 `e8932469…`, r4-2 `069a1e07…`,
r4-3 `68281fb6…`, r4-4 `55350c40…`, r4-5 `8e361d6f…`, r4-6 `36e6c792…`.
`cmp` exit 0: live_review←r4-1, plan←r4-2, T1_F252.md←r4-4.
Containment exit 0: r4-3→T1_F251.md, r4-5→STATUS.md, r4-6→ROADMAP.md.
STATUS numstat `1 0` — one line added, no other line touched. ROADMAP `9 0`.

## 4b — the full-run delta, stated plainly
    time python3 -m pytest -n auto -q
    → 152 failed, 14154 passed, 8 skipped in 182.49s; real 3m2.912s
    diff vs .agent/f251_baseline/churn_gate2_run1.txt → NOT byte-identical
    the 152 are a strict SUBSET of the catalogued 154; comm shows ZERO ids
    present now but absent from the catalog — no new failure, no regression
    the two missing ids are exactly the documented D4 pair, now GREEN:
      tests/orchestration/test_test_runner.py::
        TestNoBroadExceptAndDegradedSignals::test_live_review_has_steps_section
      tests/ui_server/test_dashboard_contract.py::
        TestLiveReviewAndAgentStateRefs::test_live_review_has_steps_section

**Mechanism, verified not assumed.** The assertion is a bare substring test,
`assert "Steps" in (.agent/live_review.md)`. The authored R4 verdict contains
the clause "(the current live_review has no Steps section)" — the sentence
*denying* a Steps section supplies the literal substring that makes the test
pass. This round's docs edits moved nothing; it is the D4 live-state coupling
behaving as F251 documented, opposite in direction to R3. Recorded, not
touched: F252 work-breakdown item 7.

## External actions
A push per commit (c1b3341, 8a7c8e7, 7d4b586, this one). No PR —
reviewer-gated. No merges.

## Verification
    4a  pytest tests/docs/test_docs_consistency.py -q -k FeatureLedger
        → 4 passed, 288 deselected in 0.17s
    4b  see above — delta of exactly the 2 D4 ids, both green
    4c  pytest tests/cli/test_golden_path.py -q → 42 passed in 14.79s
    4d  git status --porcelain → empty (before this commit)

## Deviations & assumptions
- 4b is reported as a delta, not green. The ordered criterion was byte-identical
  to the catalogued 154; the run is 152. Nothing regressed — the set shrank by
  the two ids the step flagged as state-coupled — but "byte-identical" would be
  false, so the claim is not made.
- `.agent/plan.md` carries progress marks on top of the verbatim authored text
  (applied cmp-clean at c1b3341): AGENTS.md requires plan.md current per commit. The divergence is stated in the file itself.
- No D-class edits. No closure work. F252 is registration only.
- The catalogued 154 in `.agent/f251_baseline/` is left as the F251 baseline
  of record; F252 inherits it via class_map.txt.

## Next
Closure round for F251 (its own reviewer-gated round, per the ruling).
**full suite: 0 quarantined, 0 churning, 154 standing red (catalogued)**
