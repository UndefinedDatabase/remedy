# Handoff — F268 remedy do: the one-command start · Round 13 (closure round B)

## Session

SESSION 2 of feature F268 · round 13 · rounds so far 13

## Range

Review of c784f6b3..HEAD — branch `feature/f268-remedy-do`.

## Summary

Round 13 is closure round B:

- C1 booked round 12's verdict (PASS_WITH_RISKS, F268's closure verdict) and re-assigned R-0892 to F273, with one Acceptance line in `docs/roadmap/features/T2_F273.md`.
- C2 rotated the live-review ledger. The open-findings count is equal before and after.
- C3 is the closure commit, the last commit on the branch (Rule A4): STATUS `[x]`, README, SU-019 `consumed_by: "F268"`, the final `.agent/plan.md` and this handoff.
- C4 opens the pull request into `main` after the push. It is not merged.

## Commits

### b4aec4f5 F268 R13 C1: book round 12's verdict, PASS_WITH_RISKS, and re-assign R-0892 to F273
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r13-block.md` | +68 / -0 | Byte copy of the block |
| `.agent/authored/f268-r13-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f268-r13-pairs.json` | +44 / -0 | Byte copy of pairs.json |
| `.agent/authored/f268-r13-plan.md` | +23 / -0 | Byte copy of plan.md |
| `.agent/authored/f268-r13-pr_body.md` | +64 / -0 | Byte copy of pr_body.md |
| `.agent/live_review.md` | +3 / -1 | `c784f6b3` bytes, R-0892 `Owner: F268.` → `Owner: F273.`, + ledger.md (Gate F268 R12 PASS_WITH_RISKS) |
| `docs/roadmap/features/T2_F273.md` | +4 / -0 | `c784f6b3` bytes + the R-0892 Acceptance line |

### ceb91ba9 F268 R13 C2: rotate the live-review ledger, 594113 to 572794 bytes, 124 open findings before and after
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +0 / -50 | `scripts/rotate_live_review.py` moved 1 gate record and 12 finding pairs out |
| `.agent/live_review_archive.md` | +50 / -0 | The same records, appended byte-verbatim |

### C3 (this commit) F268 R13 C3: closure
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1 / -1 | C3 pair: F268 `[~]` → `[x]` with the reviewer's line |
| `README.md` | +11 / -3 | C3 pairs: 81 → 82 accepted, Tier 2 done 23 → 24, the F268 paragraph |
| `scripts/self_use_queue.json` | +1 / -1 | SU-019 `consumed_by: "F268"` (precondition 6) |
| `.agent/plan.md` | +6 / -6 | := plan.md |
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 208.

## External actions

- `git push` after C3 (this commit), pushing C1 to C3.
- C4, after the push: `gh pr create --base main --head feature/f268-remedy-do --title "F268 — remedy do: the one-command start" --body-file .agent/authored/f268-r13-pr_body.md`. The PR number cannot be written here because this commit precedes the PR; the round report carries it.
- No merge, no worktree, no evidence job and no zip this round.

## Verification

- **G1** (after C2), exit 0:
  - Transport: the block's digest was `59b2e1052f19a29397f5bb00f09047d5b241449d6e90520da2f7b04ef484bea2`, ledger.md `223aa2eb4554deb03ca8b07ddfc72cae976b179f1023755fc926ce8a11fdbe8e`, plan.md `a0e01933ed55ac23be79f1361ef84a3547ef3a9a3ca9764825c4d8dec9b1282d`, pairs.json `11aaea9655a636ac30dd13ae0a3883dad108edb1917cf2b9be0fe6cca1a08f0a` and pr_body.md `18bf4e32de5a22ceee93f52c2557bbdeace1b60786494f9c6ae090501e4c3a2c`. All five matched: `payload digests matched`.
  - The python byte check printed `True` for `.agent/live_review.md` at C1 == `c784f6b3` bytes with the owner pair applied + ledger.md.
  - It printed `True` for `docs/roadmap/features/T2_F273.md` at C1 == `c784f6b3` bytes with its pair applied.
  - Every pair was applied by a script asserting FROM count 1 before and TO count 1 after.
- **G2** `python3 scripts/rotate_live_review.py`, exit 0:
  ```
  gate records moved: 1
  finding pairs moved: 12 (24 records)
  old ledger size: 594113 bytes
  new ledger size: 572794 bytes
  old archive size: 3805822 bytes
  new archive size: 3827141 bytes
  open findings before: 124
  open findings after: 124
  ```
  - `count_open_findings` of `scripts/rotate_live_review.py`, called separately on the ledger: `open before 124` and `open after 124`. Equal.
- **G3** on C3's tree before its commit: `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py`, exit 0: `352 passed in 39.16s`, so 0 failed.
- **G4** on C3's tree: `run_integrity_checks()` printed `passed True fail_count 0`. All five checks read PASS: `handler_import` (handlers=147), `live_review_verdict`, `plan_consistency` (unchecked=0), `relevant_untracked` (untracked=0, relevant=0) and `high_blockers_open` (no open blocker/high findings).
- **G5** on C3's tree: the pair script counted each C3 TO string in the tree, and each FROM:
  - `docs/roadmap/STATUS.md TO count 1 FROM count 0`
  - `README.md TO count 1 FROM count 0` three times (the count line, the Tier 2 row, the F268 paragraph)
  - `grep -c -F` of the full STATUS TO line (without its leading `- `) in `docs/roadmap/STATUS.md`: `1`. `grep -c -F "82 of 281 registered items accepted." README.md`: `1`.
- **G6** after C4: the round report carries it.

## Authored-text proofs

- Byte copies are at `.agent/authored/f268-r13-{block.md,ledger.md,pairs.json,plan.md,pr_body.md}`, written from the verified payloads. The block copy's digest is `59b2e1052f19a29397f5bb00f09047d5b241449d6e90520da2f7b04ef484bea2`.
- `.agent/live_review.md` and `T2_F273.md`: byte checks `True` (G1).
- The STATUS line and the README paragraph: byte-identical to the payload's TO strings, count 1 each (G5).
- `.agent/plan.md` := plan.md, byte copy.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `b4aec4f5`; Gate F268 R12 booked, R-0892 owner F273 |
| C2 rotation | done | `ceb91ba9`; 124 open before and after |
| C3 closure commit | done | This commit |
| C4 pull request | done | After the push; the round report names it |

## Open findings

125 open by distinct id, from `.remedy-wt/f268-r4/count.py` at HEAD after C2: 128 registrations and 3 `Done:` ids in the rotated ledger. The rotation script's own counter reads 124 before and after. This round opens and resolves no finding; R-0892 moved from F268 to F273.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, then the PR). No extra commit.
- **Two open-finding counters.** `count.py` (distinct id) reads 125 and the rotation script's `count_open_findings` reads 124. They count differently; both are unchanged by the rotation.
- **The shell guard refuses `$?`.** Exit codes are the tool's own report; no gate returned non-zero.

## Next

Phase 1 rule 1 (`.agent/STOP`), then rule 2: merge F268's pull request at the Open PR Gate.

Operator questions open: 3
