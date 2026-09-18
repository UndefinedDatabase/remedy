# Handoff — F269 Contract & contract templates · Round 13 (CI repair)

## Session

SESSION 3 of feature F269 · round 13 · rounds so far 13

Context self-assessment: the worker read the block, AGENTS.md's Commit Gate and Open PR Gate, the ledger payload and the handback template once each, and every figure below comes from a command run in this round.

## Range

Review of 35f209f4..HEAD — branch `feature/f269-contract`.

## Summary

Round 13 repairs pull request 257's hosted CI under AGENTS.md's Open PR Gate exception (amend0820-gate-autonomy). Run `35372747359` on `35f209f4` failed one node, `tests/cli/test_advertised_commands.py::test_every_group_only_advertisement_reaches_a_command`, because `README.md` line 145 advertised `remedy do --contract`, a form that reaches no command. Classification: a real defect in the README (R-0973), not a guard or a budget.

- C1 booked round 12's verdict (PASS) and registered R-0973, owner F269.
- C2 rewrote the README sentence to `remedy do "<order>" --contract <name>`; the guard is unchanged.
- C3 is this handoff.

## Commits

### ea05d9d4 F269 R13 C1: book round 12 verdict PASS and register R-0973, the README advertises remedy do --contract
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r13-block.md` | +62 / -0 | Byte copy of the block |
| `.agent/authored/f269-r13-ledger.md` | +4 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r13-plan.md` | +25 / -0 | Byte copy of plan.md |
| `.agent/authored/f269-r13-readme_from.txt` | +2 / -0 | Byte copy of readme_from.txt |
| `.agent/authored/f269-r13-readme_to.txt` | +3 / -0 | Byte copy of readme_to.txt |
| `.agent/authored/f269-r13-slips.md` | +1 / -0 | Byte copy of slips.md |
| `.agent/live_review.md` | +4 / -0 | `35f209f4` bytes + ledger.md (Gate F269 R12 PASS, R-0973 Owner F269) |
| `.agent/plan.md` | +8 / -5 | := plan.md |
| `.agent/prose_slips.md` | +1 / -0 | `35f209f4` bytes + slips.md |

110 insertions, 5 deletions (`git show --numstat`).

### 400c7688 F269 R13 C2: the README names remedy do "<order>" --contract <name>, a form that reaches do run (R-0973)
| Path | +/- | Reason |
|------|-----|--------|
| `README.md` | +3 / -2 | readme_from.txt (1x at `35f209f4`) replaced by readme_to.txt |

3 insertions, 2 deletions (`git show --numstat`).

### C3 (this commit) F269 R13 C3: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 110.

## External actions

- `git push` after C3 (this commit), pushing C1 to C3 to `origin/feature/f269-contract`, never forced. The push triggers pull request 257's hosted CI.
- Pull request 257 was not merged, commented on or edited. No worktree, no evidence job and no zip this round.

## Verification

- **Transport**, before any write: `sha256sum` of the block read `7895ebefd7e2414cae6a7ce283ad4bbe6cc81b163dc93997e83ecd0bde48fd53`, and all five payloads matched the block's digests: ledger.md `6e3c6d4a…0812`, slips.md `523fb4ff…30f4`, plan.md `fa2c3cc6…78b3`, readme_from.txt `5322be49…7ddc`, readme_to.txt `00531648…12ee`. At `35f209f4` README.md held FROM 1x and TO 0x, and TO does not contain FROM.
- **G1** at C2, python byte check, exit 0: `G1 True` — `.agent/plan.md` equals plan.md; `.agent/live_review.md` and `.agent/prose_slips.md` equal their `35f209f4` bytes + ledger.md and + slips.md; the six `.agent/authored/f269-r13-*` copies equal their payloads.
- **G2** at C2, same script, exit 0: `G2 FROM 0 TO 1`. `git show --numstat 400c7688` lists `3	2	README.md` alone.
- **G3** at C2, `python3 -m pytest -q -p no:cacheprovider tests/cli/test_advertised_commands.py tests/docs/ tests/cli/test_golden_path.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` (serial), exit 0: `503 passed in 57.57s`, so 0 failed. The same command on C2's tree before its commit read `503 passed in 57.93s`, exit 0.
- **G4** follows the push; the round report carries it.
- Full suite: not run (amend0917-throughput); the hosted CI re-runs it on the push.

## Authored-text proofs

- Byte copies are at `.agent/authored/f269-r13-{block.md,ledger.md,slips.md,plan.md,readme_from.txt,readme_to.txt}`, true against their payloads (G1). The block copy's digest is `7895ebefd7e2414cae6a7ce283ad4bbe6cc81b163dc93997e83ecd0bde48fd53`.
- `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/plan.md`: byte checks `True` (G1).
- `README.md`: the replacement asserted FROM 1x before, FROM 0x and TO 1x after (G2).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `ea05d9d4`; Gate F269 R12 booked, R-0973 registered, owner F269 |
| C2 README repair | done | `400c7688`; G2 FROM 0 TO 1, G3 503 passed |
| C3 handoff | done | This commit |

## Open findings

`.remedy-wt/f268-r4/count.py` (distinct id) at HEAD after C2 reads `registrations 130 done 3 open 127`. This round opens R-0973 and resolves none; its resolution is booked by the review of round 13.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, then the push). No extra commit.
- **G3 ran twice**, once on C2's tree before its commit so a red gate could leave nothing half-done, and once at the committed C2; both read 503 passed.
- **Driver scripts.** The byte copies, the README replacement and G1/G2 ran as inline python; no scratch file was added.

## Next

Phase 1 rule 1 (`.agent/STOP`), then the review of round 13, then the Open PR Gate on pull request 257 after its hosted CI.

Operator questions open: 5
