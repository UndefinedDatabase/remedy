# Handback — F009 R11, the nonce half of T002

Round base `db50d0bbaa0d94ab6d6769c12980f3e78a5e9028`, branch `feature/f009-single-write-channel`. State: 60 % (T001 gebaut · T002 gebaut bis auf die Publikation — T003 öffnet die Wirkung) — Schätzung

## Range

Review of `db50d0bb..HEAD` — ten commits: C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and C8, in that order. Nothing came between them, none was dropped and none was added.

## Commits

### 45a67196 docs(state): save the F009 R11 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r11.md | +291/-0 | the round's block, byte-exact |

### 9c83f03f docs(state): mirror the F009 R11 step block into the live block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +187/-222 | written from the committed C0a blob |

### 29086a21 docs(state): set the plan to the F009 R11 nonce round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-17 | PLANF009R11, applied byte-equal |

### 37bd4fdc docs(review): register R-0635 against the R10 spec defect
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | R0635 appended |

### 90c59662 docs(review): record the R10 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER11 appended; R10 PASSED |

### 29ee4b08 docs(review): resolve R-0634 with the reviewer-verified record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +1/-1 | the ONE replacement: `Landed:` → DONE0634 |

### 74de46b2 docs(decisions): rule DECISION F009 D15 on nonce publication and lookup order
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +12/-0 | DECISION15 appended |

### 25e6e6ac feat(orchestration): add the create-only per-job command nonce store
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/command_nonce.py | +221/-0 | new; D8's store, D15's ordering |
| tests/orchestration/test_command_nonce.py | +227/-0 | new; 25 tests incl. an 8-thread race |

### e11fe949 feat(ui-server): answer a replayed command nonce from the store
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +53/-0 | nonce character class + the replay lookup |
| tests/ui_server/test_command_channel.py | +99/-0 | 8 replay tests (one parametrized ×4) |

### C8, this commit, docs(state): write the F009 R11 handback
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
| C5 | done | |
| C6 | deviated | `publish_nonce_result` gained a keyword-only `status` and returns the record — see Deviations |
| C7 | deviated | a replay is audited `not_implemented`; `accepted` is reserved — see Deviations |
| C8 | done | this commit |

## External actions

`gh` was not run; this branch carries no pull request. One disposable worktree for G10: `git worktree add --detach .remedy-wt/g10-r11 HEAD` (exit 0), then `git worktree remove --force` and `git worktree prune` (both exit 0); `git worktree list` afterwards shows only the primary checkout. `git push` follows C8, the last commit of this round.

## Verification

Transcripts are in the round report (R-0582); one line per gate here. Every gate that names a commit was measured at `e11fe949`, which is C7.

- G1 STOP ABSENT at Step 0 and again before C8; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel` at every reading; `git status --porcelain` printed 0 lines after each of C0a through C7; round base read at Step 0 is `db50d0bbaa0d94ab6d6769c12980f3e78a5e9028`.
- G2 EQUAL — the scratch file as received, `.agent/authored/f009-r11.md` at C0a and `.agent/last_block.md` at C0b are all sha256 `53fb09f242c458fb3da8c9d8f615668ded9330927d5ff5b4e01b44721a96bbb0` over 30270 bytes and 291 lines, equal to the digest the task prompt named; C0b was written from the committed C0a blob, never from the scratch file again.
- G3 5 slices from my own ordered extraction out of the committed C0a blob: PLANF009R11 `402d9aa6…` 2420 bytes 41 lines, R0635 `07fd9c15…` 2311 bytes 1 line, LEDGER11 `7a8dd2a8…` 4963 bytes 1 line, DONE0634 `48cd968c…` 1354 bytes 1 line, DECISION15 `5b6d9b57…` 3474 bytes 11 lines; the aggregates my script printed are 5 slices, 14522 bytes and 55 lines.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R11 at 41 lines against the 50-line cap; `^## Goal$` 1, `^## Next Steps$` 1, first `\bF\d{3}\b` match `F009`.
- G5 ALL THREE APPENDS HOLD UNDER BOTH READERS. C2 over `.agent/live_review.md` from the round base: (a) prefix exact, remainder equals a newline plus R0635 at 2312 bytes, 438145 → 440457; (b) N COUNTED BY SCRIPT 1, the last 1 unit equal in order. C3 from the C2 blob: (a) remainder a newline plus LEDGER11 at 4964 bytes, 440457 → 445421; (b) N 1. C5 over `.agent/decisions.md` from the round base: (a) remainder a newline plus DECISION15 at 3475 bytes, 438852 → 442327; (b) N COUNTED BY SCRIPT 6. For each append a one-byte printable-ASCII flip of the FIRST appended paragraph is REJECTED by reader (a) and by reader (b) while the unflipped value is ACCEPTED by both — four outcomes per append, twelve in all.
- G6 C4 is proved a REPLACEMENT, not an append. Over `.agent/live_review.md`: `^Landed: R-0634 — ` 1 line at C3 and 0 at C4; `^Done: R-0634 — ` 0 at C3 and 1 at C4; both blobs are 1076 lines, 445421 → 445503 bytes. My script rebuilt C3's bytes with that one line replaced by DONE0634's bytes and compared: RECONSTRUCTION == C4 blob is True, both sha256 `e58ef95f…`. `git show --numstat` for `29ee4b08` is `1  1  .agent/live_review.md` — the shape of a one-line replacement, not of an append.
- G7 line-anchored over `.agent/live_review.md` at the round base, C2 and C4: `^- R-\d+ — ` 200, 201 and 201 with every id DISTINCT at each; `^- R-0635 — ` 0, 1 and 1; `^Done: R-\d+ — ` 1, 1 and 2; `^Landed: ` 1, 1 and 0; `^> Next free id` 0 at all three. At the round base, C3 and C4, `^Gate: R\d+ — ` reads 10, 11 and 11 over that many DISTINCT keys. Max id at C4 is R-0635. My script printed 199 for item 10's rule at `29ee4b08` — line-anchored `^- R-\d+ — ` 201 minus line-anchored `^Done: R-\d+ — ` 2 (DECISION F009 D10). Over `.agent/decisions.md`, `^## DECISION F009 D\d+ — ` reads 14 at the round base and 15 at C5, over that many DISTINCT keys.
- G8 BASELINE half EXIT 0 for both paths, each read as `git show db50d0bb:<path> | python3 -m ruff check --stdin-filename <path> -` and each printing `All checks passed!`. C7 half in the primary checkout over those two plus `packages/orchestration/command_nonce.py` and `tests/orchestration/test_command_nonce.py`: EXIT 0, `All checks passed!`.
- G9 all three EXIT 0, run SERIALLY in the primary checkout at C7, never two pytest processes at once: the unit group printed `120 passed` (passed+skipped 120); the canary `tests/cli/test_golden_path.py` printed `42 passed` (42); the state-reader group printed `507 passed` (507). No count was predicted; each is what the run printed.
- G10 PROBE, run ONLY in the disposable worktree, source restored byte-identically after each mutation (sha256 `8566a889…` over 9981 bytes before and after both, worktree porcelain 0 lines, primary checkout unchanged). Control, unmutated: EXIT 0, `109 passed`. Probe A, `lookup_nonce_result` returning None unconditionally (its `def` line is unique, whole-line count 1): EXIT 1, `7 failed, 102 passed` — `TestCommandChannelDoor::test_a_replayed_nonce_answers_from_the_store_byte_for_byte`, `::test_a_replay_never_reaches_the_seam`, `::test_a_replay_spends_no_rate_budget`, and `test_command_nonce.py::test_a_published_body_reads_back_byte_equal`, `::test_a_second_publish_of_one_nonce_returns_the_first_body`, `::test_two_different_nonces_coexist`, `::test_concurrent_publishers_of_one_nonce_all_receive_the_same_body`. Probe B, `create_only=True` → `create_only=False` (target unique: whole-line 1 and indent-agnostic 1, agreeing): EXIT 1, `2 failed, 23 passed` — `::test_a_second_publish_of_one_nonce_returns_the_first_body` and `::test_concurrent_publishers_of_one_nonce_all_receive_the_same_body`. SURVIVORS I NAME rather than let a reader assume otherwise (R-0633): under A every MISS test survives — `test_an_unseeded_nonce_still_reaches_the_seam`, `test_an_unpublished_nonce_is_a_miss`, `test_a_job_with_no_control_directory_is_a_miss`, `test_a_job_with_no_nonce_store_is_a_miss`, `test_an_unreadable_record_is_a_miss_and_never_raises`, `test_a_record_without_a_usable_status_is_a_miss`, `test_a_nonce_is_scoped_to_its_own_job` and the unusable-nonce cases — because each asserts None and a lookup that always returns None satisfies that; they measure the miss contract, never a hit. `test_the_record_is_private_and_under_the_jobs_control_directory` and `test_the_record_carries_the_status_first_in_the_ruled_order` survive A because they read the FILE, not the lookup. Under B everything but the two survives, because only those two publish the same nonce twice and one publisher cannot tell an overwrite from a create-only link.
- G11 the range from the round base to C7 lists EXACTLY the nine declared paths other than `.agent/handoff.md`, the set difference empty in both directions. Nine commits, each with ONE parent, `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-` column of the tables above; insertions 291, 187, 17, 2, 2, 1, 12, 448 and 152, all under the 500-insertion cap of DECISION F104 D1, so no split was needed. `^<<<SLICE ` and `^<<<END ` read 0 lines in `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md`. THIS ROUND'S nine reflog rows — the entries above the round base — classify as `commit` 9, with `amend`, `rebase` and `cherry` 0 each; no total is asserted over the whole reflog (R-0601). `git ls-files .remedy-wt` is 0.
- G12 parsing the AST of `packages/orchestration/ui_server.py` at the round base and at C7 gives 62 and 63 imported module names; ADDED is exactly `['packages.orchestration.command_nonce']` and REMOVED is empty, so the door's one new import is the nonce module. Both call sites import it inside a method, the idiom this door already uses for the catalog and the audit writer.
- G13 this handback carries every mandated section of docs/agents/handback_template.md, an item-status table with exactly one row for each of C0a through C8, the round base SHA and one line per gate. Deviations, declared: `wc -l` measures it at 114 lines, over the 100 a bundle of more than five commits allows. The overage is the `## Commits` section: ten per-commit tables cost three header lines each before a single path row, and the template forbids dropping a mandated section to meet the cap (AGENTS.md DECISION D15). No section was dropped and no transcript was added.

## Authored-text proofs

All five slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` and `<<<END ` marker lines with a script and applied programmatically. PLANF009R11 is byte-equal to `.agent/plan.md` at C1 (G4); R0635, LEDGER11 and DECISION15 are proved as appends under two independent readers, each with its own script-counted N and its own negative control on the first appended paragraph (G5); DONE0634 is proved by byte reconstruction of the replaced line (G6). No marker line reached any target file; nothing was retyped, rewrapped, reflowed, reindented or whitespace-adjusted.

## Deviations & assumptions

TWO DEVIATIONS FROM THE SPECIFIED CODE, both declared here rather than only in the commit table (R-0485). Neither touches a slice: all five were applied byte for byte and no objection to any of them arose. The block's ordered commit sequence was followed exactly.

FIRST, `publish_nonce_result`'S SIGNATURE AND RETURN. C6 prints `publish_nonce_result(job_id, nonce, body, *, control_root_path=None)` returning "the body that is in force", while C7 requires that the store "keep the status alongside the body so a replay can reproduce both". Those cannot both hold: a body-only value cannot carry a status, and the race path has to hand the LOSER the winner's status too. I kept the printed positional shape and added a REQUIRED keyword-only `status`, and both functions return the record `{"status": …, "body": …}` — the body in force plus the status it was returned with. A default for `status` was rejected: a wrong frozen status is exactly the bug D15 exists to prevent.

SECOND, THE OUTCOME A REPLAY IS AUDITED WITH, WHICH IS AN OBJECTION RECORDED AND NOT ACTED ON. C7 orders the replay audited "with the outcome the ORIGINAL attempt would have carried". Under D15 a record is published only for an ACCEPTED command, so that outcome is `accepted` — and D14 RESERVES `accepted` for the round that retires the 501 seam, `command_audit.OUTCOMES` excludes it, and the shipped `test_the_outcome_vocabulary_is_the_closed_set_d14_ruled` and `test_every_outcome_the_door_writes_is_in_the_ruled_vocabulary` both fail if the door writes it. The two instructions collide. I wrote `not_implemented`, which IS the outcome of the only result this door can produce while the seam stands, and named the collision in a comment at the call site pointing at the T003 round that moves the token. THE OBJECTION: C7's sentence is unimplementable this round; the round that adds the publish call site must change that token in the same commit, and a record that could carry its own outcome would remove the collision entirely.

ONE ASSUMPTION, stated: the 400 for a nonce that fails the character class carries its own wording — "client_nonce must be 1-64 characters of letters, digits, '-' or '_'" — rather than repeating the non-empty check's message. C7 fixes the STATUS, the FIELD and the audited `rejected_shape`, all three of which are unchanged; the wording is mine, and reusing "must be a non-empty string" for `../escape` would be false on its face.

## Next

No `.agent/STOP` is present. The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch carries no pull request and F009 opens one at its own closure. Open findings at `29ee4b08` are 199 by item 10's rule — line-anchored `^- R-\d+ — ` 201 minus line-anchored `^Done: R-\d+ — ` 2 (DECISION F009 D10). The next free id, derived with `max` over the line-anchored entries, is R-0636. `.agent/candidates.md` is EMPTY. The next round is T003's effect table per D5 — the round that retires the 501 seam, and therefore the round that publishes a nonce record and writes D14's reserved `accepted` audit outcome. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and R-0635 stay routed to a paydown branch.
