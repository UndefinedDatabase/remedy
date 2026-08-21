# Handback — F009 R10, the audit half of T002

Round base `f7f43edf82974ea5ac999c0285358f56be94822f`, branch `feature/f009-single-write-channel`. State: 50 % (T001 gebaut · T002 zur Hälfte — Quittung steht, Nonce folgt in R11) — Schätzung

## Range

Review of `f7f43edf..HEAD` — twelve commits: C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, C8a and C9. C8a is an EXTRA commit and is declared below.

## Commits

### 6b55de93 docs(state): save the F009 R10 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r10.md | +326/-0 | the round's block, byte-exact |

### d0e7823e docs(state): mirror the F009 R10 step block into the live block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +254/-107 | written from the committed C0a blob |

### 5dcbede4 docs(state): set the plan to the F009 R10 audit round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-13 | PLANF009R10, applied byte-equal |

### 728247a9 docs(review): record the R9 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER10 appended; R9 PASSED |

### 7bd32ecd docs(decisions): rule DECISION F009 D14 on what an audited attempt requires
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +14/-0 | DECISION14 appended |

### e6dc6142 refactor(safe-points): make the job control fd helper a public name
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/safe_points.py | +10/-8 | pure rename plus the WHY comment; 6 call sites |

### 6b1fc056 feat(secure-fs): add the append-only line writer for audit records
| Path | +/- | Reason |
|---|---|---|
| packages/common/secure_fs.py | +65/-0 | `append_line_at`, in `__all__` |
| tests/orchestration/test_secure_fs.py | +149/-0 | new; 11 tests incl. 12-thread concurrency |

### adc7892c feat(command-audit): write the per-job audited attempt record
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/command_audit.py | +117/-0 | new; D6's record, D14's three halves |
| tests/orchestration/test_command_audit.py | +198/-0 | new; 17 tests |

### 8d050bb3 feat(ui-server): audit every refused command attempt at the write door
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +39/-1 | 7 call sites + `_audit_attempt` |
| tests/ui_server/test_command_channel.py | +202/-0 | 11 audit tests |

### 1305a9b0 test(rate-limit): observe mutual exclusion through the injected clock
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | the one `Landed: R-0634 — ` line |
| tests/ui_server/test_command_channel.py | +62/-1 | R-0634 repair; old test's docstring corrected |

### b60c6393 fix(ui-server): name the audit writer failures the door swallows — C8a, EXTRA
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +10/-1 | `except Exception` → a named tuple; G8 was RED on it |
| tests/ui_server/test_command_channel.py | +7/-1 | the raising-writer test now exercises all three |

### C9, this commit, docs(state): write the F009 R10 handback
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
| C6 | deviated | `json_bytes(indent=0)` emits interior newlines; `indent=None` used — see Deviations |
| C7 | done | |
| C8 | done | |
| C8a | deviated | EXTRA commit, not in the ordered bundle; repairs C7 after G8 went red |
| C9 | done | this commit |

## External actions

`gh pr list --state open` printed `[]` — this branch carries no pull request. One disposable worktree for G9: `git worktree add .remedy-wt/g9-f009-r10 b60c6393 --detach`, then `git worktree remove --force` and `git worktree prune`; `git worktree list` afterwards shows only the primary checkout. `git push` follows C9, the last commit of this round.

## Verification

Transcripts are in the round report (R-0582); one line per gate here. Every gate that names a commit was measured at `b60c6393`, the last code commit, which is C8a rather than C8 for the reason declared below.

- G1 STOP ABSENT at Step 0 and again before C9; branch `feature/f009-single-write-channel` at every reading; `git status --porcelain` 0 lines after each of C0a through C8a; round base as stated above.
- G2 EQUAL — the scratch file as received, `.agent/authored/f009-r10.md` at C0a and `.agent/last_block.md` at C0b are all sha256 `17a2f22543a4ac6f8d3c40d1313e5d611f20703d5bd8500788b3398125458271` over 28368 bytes and 326 lines, equal to the digest the prompt named; C0b was written from the committed C0a blob, not from the scratch file.
- G3 3 slices from my own ordered extraction out of the committed C0a blob: PLANF009R10 `8db516d9…` 2315 bytes 41 lines, DECISION14 `cd4dd401…` 4205 bytes 13 lines, LEDGER10 `db323595…` 3614 bytes 1 line; the aggregates are 3 slices, 10134 bytes and 55 lines, over a concatenation of sha256 `0073350c…`.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R10 at 41 lines against the 50-line cap; `^## Goal$` 1, `^## Next Steps$` 1, first `\bF\d{3}\b` match F009.
- G5 BOTH APPENDS HOLD UNDER BOTH READERS, each based on the round base. C2 over `.agent/live_review.md`: (a) prefix exact, remainder equals a newline plus LEDGER10, `db323595…` 3614 bytes 1 line, 433257 → 436872 bytes; (b) N COUNTED BY SCRIPT 1, the last 1 blank-line unit equal in order. C3 over `.agent/decisions.md`: (a) prefix exact, remainder equals a newline plus DECISION14, `cd4dd401…` 4205 bytes 13 lines, 434646 → 438852 bytes; (b) N COUNTED BY SCRIPT 7, the last 7 units equal in order. For each append a one-byte printable-ASCII flip of the FIRST appended paragraph is REJECTED by reader (a) and by reader (b) while the unflipped value is ACCEPTED by both — four outcomes per append, all as required.
- G6 line-anchored over `.agent/live_review.md` at the round base, C2 and C8: `^- R-\d+ — ` 200, 200 and 200 with every id DISTINCT at each; `^Done: R-\d+ — ` 1 at all three; `^> Next free id` 0 at all three; `^Landed: ` 0, 0 and 1; `^Gate: R\d+ — ` 9, 10 and 10 over that many DISTINCT keys. Max id at C8 is R-0634. My script printed 199 for item 10's rule at `1305a9b0` — line-anchored `^- R-\d+ — ` 200 minus line-anchored `^Done: R-\d+ — ` 1 (DECISION F009 D10). Over `.agent/decisions.md`, `^## DECISION F009 D\d+ — ` reads 13 at the round base and 14 at C3, over that many DISTINCT keys.
- G7 BASELINE half EXIT 0 for all four paths, each read as `git show <round base>:<path> | python3 -m ruff check --stdin-filename <path> -` and each printing `All checks passed!`; aggregate exit 0. HEAD half in the primary checkout at C8a over those four plus `command_audit.py`, `test_secure_fs.py` and `test_command_audit.py`: EXIT 0, `All checks passed!`.
- G8 all three EXIT 0, run SERIALLY in the primary checkout at C8a, never two pytest processes at once: the new units printed `106 passed` (total 106); the canary `tests/cli/test_golden_path.py` printed `42 passed` (total 42); the state-reader group printed `499 passed` (total 499). No count was predicted. This gate was RED at C8 and is the reason C8a exists.
- G9 PROBE, run ONLY in the disposable worktree, source restored byte-identically after each mutation (`byte-equal to the saved original = True`, worktree porcelain 0 lines afterwards). Control, unmutated: EXIT 0, `76 passed`. Probe 1, `audit_command_attempt` returning False without writing: EXIT 1, `9 failed, 67 passed` — the nine are `test_the_seam_is_audited_as_not_implemented`, `test_a_wrong_bearer_is_audited_as_rejected_token`, `test_a_wrong_csrf_header_is_audited_as_rejected_csrf`, `test_an_unresolvable_job_is_audited_as_rejected_job`, `test_a_shape_error_is_audited_as_rejected_shape`, `test_an_unexposed_command_is_audited_as_rejected_command`, `test_a_rate_limited_attempt_is_audited_as_rejected_rate`, `test_every_outcome_the_door_writes_is_in_the_ruled_vocabulary` and `test_the_raw_token_never_reaches_the_audit_file`, all in `TestCommandChannelDoor`. Two of the eleven audit tests SURVIVE that mutation and I name them rather than let a reader assume otherwise (R-0633): `test_a_wrong_credential_on_a_job_with_no_control_dir_leaves_no_file` measures the ABSENCE of a file, which a no-op writer also produces, and `test_an_audit_writer_that_raises_changes_neither_status_nor_body` replaces the writer itself. Probe 2, `with _COMMAND_RATE_LOCK:` → `if True:`: before mutating, that line reads 1 by whole-line, 1 indent-agnostic and 1 by substring, so the target is unique; over TEN runs every run EXITED 1 with `1 failed, 75 passed` and the single failing node id `TestCommandRateLimiter::test_the_lock_actually_excludes_a_second_caller` each time. `test_concurrent_callers_never_oversubscribe_one_budget` passed in all ten, which reproduces R-0634 exactly.
- G10 the range from the round base to C8a lists EXACTLY the twelve declared paths other than `.agent/handoff.md`, the set difference empty in both directions. Eleven commits, each with ONE parent, `git show --numstat` and `git diff --numstat` agreeing on every cell and every cell equal to the tables above; insertions 326, 254, 13, 2, 14, 10, 214, 315, 241, 64 and 17, all under the 500-insertion cap of DECISION F104 D1, so no split was needed. `^<<<SLICE ` and `^<<<END ` read 0 lines in `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md`. THIS ROUND'S eleven reflog rows — the entries whose recorded SHA is one of the eleven commits in the range — are all `commit`, with `amend`, `rebase` and `cherry` 0 each; no total is asserted over the whole reflog (R-0601). `git ls-files .remedy-wt` is 0.
- G11 parsing the AST of `packages/orchestration/ui_server.py` at the round base and at C8a gives 61 and 62 imported module names; the set difference ADDED is exactly `['packages.orchestration.command_audit']` and REMOVED is empty, so the only addition is the audit module. The `except` clause of `_audit_attempt` names `RuntimeError` rather than importing `StopControlError` precisely to keep that set at one.
- G12 this handback carries every mandated section of docs/agents/handback_template.md, an item-status table with one row for each of C0a through C9 plus the declared extra C8a, the round base SHA and one line per gate. Deviations, declared: `wc -l` measures it at 128 lines, over the 100 a bundle of more than five commits allows and under the 160 the template allows when a bundle of more than TEN commits needs the tables — this bundle is twelve. The overage is the `## Commits` section itself: twelve per-commit tables cost three header lines each before a single path row, and the template forbids dropping a mandated section to meet the cap (DECISION D15). No section was dropped and no transcript was added.

## Authored-text proofs

All three slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` and `<<<END ` marker lines with a script and applied programmatically: PLANF009R10 is byte-equal to `.agent/plan.md` at C1 (G4), and LEDGER10 and DECISION14 are proved as appends under two independent readers, each with its own script-counted N and its own negative control on the first appended paragraph (G5). No marker line reached any target file; nothing was retyped, rewrapped, reflowed or reindented.

## Deviations & assumptions

TWO DEVIATIONS, both declared here rather than only in the commit table (R-0485).

FIRST, AN EXTRA COMMIT, C8a `b60c6393`, breaking the block's "nothing comes between them". G8's third suite went RED at C8 on `tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals::test_no_broad_except_exception_in_dashboard`: the `except Exception:` I wrote in C7 to satisfy D14's fourth clause is forbidden in that module by a standing AST guard. I verified the guard is GREEN at the round base — 0 broad-except handlers in `ui_server.py` at `f7f43edf` — so C7 introduced the only one. C8 was already committed and history rewriting is forbidden, so the repair became its own commit: the clause now reads `except (OSError, RuntimeError, ValueError, TypeError)`, and the door's raising-writer test was widened to raise all three shapes. A reviewer should read C8a as part of C7.

SECOND, A SLICE-ADJACENT SPECIFICATION I DID NOT APPLY AS WRITTEN, WITH THE OBJECTION RECORDED. C6's specification says to serialise "with `secure_fs.json_bytes(..., indent=0)` onto one line". Those two clauses cannot both hold: I measured `json.dumps({"a": 1, "b": "x"}, indent=0, sort_keys=True)` and it returns `'{\n"a": 1,\n"b": "x"\n}'` — `indent=0` means newlines at zero indentation, not compact. A record built that way carries interior newlines, which C5's `append_line_at` refuses by design, so every audit write would have failed and the round's own G8 and G9 gates could not have been met. I applied the stated PROPERTY — one line — with `json_bytes(ordered, indent=None, sort_keys=False)`, and `sort_keys=False` is required on top, because the default `True` would sort the object alphabetically and destroy the field ORDER D6 fixes and two later features depend on. `args_fingerprint` still calls `json_bytes(args)` at its defaults, exactly as D14 spells it. THE OBJECTION, recorded and not acted on further: the block should have said `indent=None`.

No other instruction was departed from. The three authored slices were applied byte for byte as written and no objection to any of them arose.

## Next

No `.agent/STOP` is present. The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is EMPTY because this branch carries no pull request and F009 opens one at its own closure. Open findings at `1305a9b0` are 199 by item 10's rule — line-anchored `^- R-\d+ — ` 200 minus line-anchored `^Done: R-\d+ — ` 1 (DECISION F009 D10). The next free id, derived with `max` over the line-anchored entries, is R-0635. `.agent/candidates.md` is EMPTY. R11 is the nonce store per D8 — create-only publication, a validated nonce character class, and a replay that returns the ORIGINAL body; whether a replay spends rate budget is open and is that round's to rule. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630 and R-0633 stay routed to a paydown branch. R-0634 is LANDED this round and leaves that list.
