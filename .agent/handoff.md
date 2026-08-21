# Handback — F009 R8, the command door's rate limit

Round base `43b438e330f7ea0ec23f958c7a37aacd8b99fbaa`, branch `feature/f009-single-write-channel`. State: 40 % (T001 gebaut · T002 begonnen — Limit steht, Quittung und Wirkung folgen in R9 und T003) — Schätzung

## Range

Review of `43b438e3..HEAD` — seven commits: C0a, C0b, C1, C2, C3, C4, C5.

## Commits

### 48987aec docs(state): save the F009 R8 step block as an authored artifact
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r8.md | +285/-0 | the round's block, byte-exact |

### 21f0467c docs(state): mirror the F009 R8 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +176/-164 | written from the committed C0a blob |

### 638d407c docs(state): set the plan to the F009 R8 rate-limit round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-16 | PLANF009R8, applied byte-equal |

### efba382d docs(decisions): rule where the command rate limit is consulted as F009 D13
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +14/-0 | DECISION13 appended |

### 69394fea docs(review): record the R7 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER8 appended; this round mints no id |

### 84c63d31 feat(ui-server): rate-limit the command door per token fingerprint and job
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/config.py | +15/-0 | the DECISION F009 D9 `ConfigKeySpec` |
| packages/orchestration/ui_server.py | +105/-3 | the fingerprint, the limiter, the 429 |
| tests/ui_server/test_command_channel.py | +235/-0 | the contract-G tests |

### C5, this commit, docs(state): write the F009 R8 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | a handback cannot table the commit that writes it |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## External actions

`git worktree add .remedy-wt/g10 84c63d31` exit 0, then `git worktree remove --force` and `git worktree prune` both exit 0, after which `git worktree list` holds only the primary checkout. `git push` follows C5. No `gh` command ran; this branch carries no pull request.

## Verification

Transcripts are in the round report (R-0582); one line per gate here.

- G1 STOP ABSENT at Step 0 and again before C4; branch `feature/f009-single-write-channel` at every reading; `git status --porcelain` 0 lines after each of C0a through C4; round base as stated above.
- G2 EQUAL — the scratch file as received, `.agent/authored/f009-r8.md` at C0a and `.agent/last_block.md` at C0b are all sha256 `b646a9886af360bfed256d66fbe7ba46a0606ce08c7e37585d64ce617ba15ddd` over 25972 bytes and 285 lines, equal to the digest the prompt named; C0b was written from the committed C0a blob.
- G3 3 slices from my own ordered extraction: PLANF009R8 `3f464048…` 2355 bytes 41 lines, DECISION13 `3f864d99…` 2101 bytes 13 lines, LEDGER8 `fa8138cf…` 6135 bytes 1 line; aggregate `49f9c299…` 10591 bytes 55 lines.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R8 at 41 lines against the 50-line cap; `^## Goal$` 1, `^## Next Steps$` 1, first `\bF\d{3}\b` match F009.
- G5 the C3 append HOLDS under both readers: (a) the C2 blob is a byte-exact prefix and the remainder is `73872996…` 6136 bytes 2 lines, equal to a newline plus LEDGER8; (b) with N COUNTED 1 against 212 blank-line units the last unit equals the slice in order; the one-byte flip of the first appended paragraph is REJECTED by both while the unflipped value is ACCEPTED by both.
- G6 the C2 append HOLDS the same two ways: remainder `9450fec0…` 2102 bytes 14 lines, N COUNTED 7 against 1116 units, control REJECTED by both and unflipped ACCEPTED by both. Measured, not predicted: `^## DECISION F009 D\d+ — ` 12 at the round base and 13 at C2, `^## DECISION ` 97 and 98, and 13 DISTINCT F009 keys D1 through D13 at C2.
- G7 line-anchored at the round base and at C3: `^- R-\d+ — ` 199 at both with every id DISTINCT at both, `^Done: R-\d+ — ` 1 at both, `^Landed: ` 0 at both, `^> Next free id` 0 at both, `^Gate: R\d+ — ` 7 then 8 over that many DISTINCT keys. Max id at C3 is R-0633. Of the 8 `Gate: ` lines, 7 match `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one less than the first; the single non-match reads `Gate: R1 — the F008 R36 entry.` Item 10's rule gives 198 open at `69394fea`, being line-anchored `^- R-\d+ — ` 199 minus line-anchored `^Done: R-\d+ — ` 1 (DECISION F009 D10).
- G8 read at C4 by importing both modules: key `ui.command_rate_limit_per_minute`, env_var `REMEDY_UI_COMMAND_RATE_LIMIT_PER_MINUTE`, `value_type` `int`, default 30, and `get_config().get("ui.command_rate_limit_per_minute")` returns 30 from source DEFAULT in a process with that variable absent. Registered specs 54 at the round base and 55 at C4; the set difference is exactly that one key added and nothing removed, and every other spec's full field tuple is unchanged.
- G9 all five EXIT 0 in the primary checkout, run serially: ruff over the three changed paths printed `All checks passed!`; `tests/ui_server/test_command_channel.py` 64 passed; `tests/orchestration/test_config.py` 63 passed; the state-reader group 487 passed; the canary `tests/cli/test_golden_path.py` 42 passed. This module's contribution from `--collect-only -q` is 64 tests collected.
- G10 the pair ran inside a disposable worktree at `84c63d31`, the primary checkout never written to: (a) UNMUTATED EXIT 0 at 64 passed; (b) MUTATED EXIT 1 at 8 failed and 56 passed, so (b) is RED where (a) is GREEN. The changed byte string was `if accepted >= limit:` in `packages/orchestration/ui_server.py`, occurrence count 1 in that file at C4 by both a whole-line and an indent-agnostic count. The eight node ids the run printed are in the round report; the worktree was removed and pruned before C5.
- G11 the range from the round base to C4 lists exactly the eight declared paths with the set difference empty in both directions; six commits, each with ONE parent, `git show --numstat` and `git diff --numstat` agreeing on every cell and every cell equal to the table above, insertions 285, 176, 17, 14, 2 and 355, all under the 500-insertion cap. `^<<<SLICE ` and `^<<<END ` read 0 lines in all six committed targets. This round's reflog rows are all `commit`, with `amend`, `rebase` and `cherry` 0 each and no total asserted over the whole reflog. `git ls-files .remedy-wt` is 0.
- G12 this handback carries every mandated section of docs/agents/handback_template.md, an item-status table with exactly one row for each of C0a through C5, the round base SHA and one line per gate; its line count against the 100 a bundle of more than five commits allows is in the round report, which measures the file this commit writes.

## Authored-text proofs

All three slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` and `<<<END ` marker lines with a script and applied programmatically: PLANF009R8 is byte-equal to `.agent/plan.md` at C1 (G4), and DECISION13 and LEDGER8 are proved as appends under two independent readers, each with its own counted N and its own negative control (G6, G5). No marker line reached any target file; nothing was retyped, rewrapped, reflowed or reindented.

## Deviations & assumptions

None. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 ran with nothing between the commits, no commit was added, dropped or reordered, and C4 stayed under 500 insertions so constraint 3's split was not reached. Constraint 6 was NOT exercised: no existing test in `tests/ui_server/test_command_channel.py` was edited, because none became unsatisfiable — every test starts a server with its own random token, so each holds its own budget under the default limit of 30. One judgement inside contract C is worth the reviewer's attention: a configured limit that is not a whole number falls back to the registered default rather than raising, so a typo in `remedy.toml` cannot turn every command into a 500, and a test pins that behaviour.

## Next

No `.agent/STOP` is present. The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch carries no pull request and F009 opens one at its own closure. Open findings at `69394fea` are 198 by item 10's rule — line-anchored `^- R-\d+ — ` 199 minus line-anchored `^Done: R-\d+ — ` 1 (DECISION F009 D10). The next free id, derived with `max` over the line-anchored entries, is R-0634. `.agent/candidates.md` is EMPTY. R9 is the nonce store and the audit record per D6, D7 and D8: a replay returns the ORIGINAL body, and every refusal this door already makes, the 429 included, becomes an audited rejection.
