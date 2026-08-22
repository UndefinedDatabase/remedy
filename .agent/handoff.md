# Handback — F009 R27 (the queue-only import guard)

## Range

Review of `c98d57f0`..HEAD. Round base SHA `c98d57f03309b9ac82c54ac5e9e4e82b19b48494`, branch `feature/f009-single-write-channel`, no pull request created. The block's `Fortschritt:` line follows VERBATIM across all four of its lines:

Fortschritt: ~96 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen, melden sich auf dem SSE-Strom und sind jetzt
             import-seitig eingezäunt; offen bleibt nur noch die
             405-Routenprobe) — Schätzung

## Commits

### f8bf6c7f docs(state): save the F009 R27 guard block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r27.md | 438/0 | C0a — the received block, copied byte for byte |

### 80df4d3a docs(state): mirror the F009 R27 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 349/362 | C0b — written from the committed C0a blob |

### b40e79a4 docs(state): set the plan to the F009 R27 guard round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 9/9 | C1 — PLANF009R27, byte-equal |

### 56926662 docs(review): register R-0642 against the R26 block
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — FINDING642 appended, based on the round base |

### 3ee65a8b docs(review): record the R26 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C3 — LEDGER27 appended, based on C2 and not on the round base |

### e2b6fb96 docs(decisions): rule F009 D24, the P3 import contract as a set
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 14/0 | C4 — DECISION24 appended, based on the round base |

### ced6e1eb test(ui-server): guard the write door import set as F009 D24 rules
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_channel.py | 158/0 | C5 — the GUARD pair, append-shaped |

### C6 docs(state): write the F009 R27 handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see report | C6 — this file; a handback cannot table its own commit, so its numstat is in the round report |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |

## External actions

- `git worktree add --detach .remedy-wt/g10 ced6e1eb` — created for G10's red proof; `git worktree remove .remedy-wt/g10` then `git worktree prune` removed it and `git worktree list` reads 1 line.
- `git push origin feature/f009-single-write-channel` — C0a through C5 pushed; C6 is pushed immediately after it is committed and that outcome is in the round report.
- No `gh` command was run. No PR created, edited or merged.

## Verification

- G1 — `.agent/STOP` ABSENT before C0a and again before C6; `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel`; `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5; round base read at step 0 is `c98d57f03309b9ac82c54ac5e9e4e82b19b48494`.
- G2 — the authored blob at C0a, `.agent/last_block.md` at C0b and the bytes received are all sha256 `69e3b24fd4ba79b881c22ef4d50994df1b5be4fec8d38c79d50fd66bc4a3c2b8`, 35935 bytes, 438 lines, and byte-equal to one another; C0b was written from the committed C0a blob and never from the scratch copy.
- G3 — the script extracted 6 slices over 212 CONTENT lines from the committed C0a blob; constraint 8 re-measures off that same blob to TOTAL 438 and PROSE 226, both the block's own numerals, under DECISION F085 D6's 490 and D5's 400.
- G4 — `cmp .agent/plan.md <PLANF009R27>` exits 0, both sha256 `e8ff301fc5bc3499e798b545cdd51c857932196a20f6cc358c56eea94baeddff`; the negative control against `.agent/last_block.md` exits 1; `wc -l` 37 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 — all three appends pass both readers, each against the commit constraint 5 fixes: (a) the base blob is a byte-exact prefix and the remainder is exactly a newline plus the slice — FINDING642 at C2 on the round base `7670e9fc…` 2531 bytes 1 line, LEDGER27 at C3 on C2 `e73f5ac3…` 5815 bytes 1 line, DECISION24 at C4 on the round base `c8f82097…` 2870 bytes 13 lines; (b) N counted BY THE SCRIPT is 1, 1 and 7 and the last N blank-line units match the slice's paragraphs in order; an equal-length printable-byte flip in the FIRST appended paragraph is REJECTED by both readers in all three while both ACCEPT the true file; live_review 536117→538649 bytes and 1120→1122 lines at C2, then 538649→544465 and 1122→1124 at C3; decisions 477421→480292 bytes and 6925→6939 lines at C4.
- G6 — line-anchored at line START at the round base, C2 and C3: leading `- R-` entries 207, 208 and 208 with every id DISTINCT at each; leading `Done: R-` 3, 3 and 3; leading `Landed: ` 0, 0 and 0; leading `Gate: R` keys 26, 26 and 27 over that many DISTINCT keys; the `Gate: R27` key 0, 0 and 1; a leading `- R-0642` entry 0, 1 and 1; max REGISTERED id R-0641 then R-0642 then R-0642; open by DECISION F009 D10's rule (line-anchored `- R-` entries minus line-anchored `Done: R-` lines) 204, 205 and 205.
- G7 — for the GUARD pair, whole-line and indent-agnostic AGREEING on every cell: at the round base FROM 1 and TO 0, at C5 FROM 1 and TO 1; the base side was read with `git show <base>:<path>` into scratch and never written over the tracked file; my own script printed `TO contains FROM: true`, so the pair is APPEND-shaped and no FROM-zero count was ordered for it.
- G8 — ordered equality holds: C5's diff adds exactly the 158 lines the GUARD application introduces, compared as a list in file order against the slice's own lines; `git show --numstat` reads 158/0, the two numbers the reviewer measured on its own dry run, so there is no difference to flag.
- G9 — run serially in the primary checkout, never two pytest processes at once and never in a worktree: `python3 -m ruff check tests/ui_server/test_command_channel.py` exit 0, "All checks passed!"; `tests/ui_server/test_command_channel.py` exit 0, 95 passed; the `tests/cli/test_golden_path.py` canary exit 0, 42 passed; the four-path group exit 0, 522 passed.
- G10 — in the disposable worktree only: the anchor line reads 1 whole-line and 1 indent-agnostic at C5, both agreeing, inside `_dispatch_job_stop`; the unmutated control passes 5; mutation (a) failed exactly `test_the_door_imports_exactly_the_allowed_set` and `test_the_door_imports_nothing_from_a_forbidden_module`, (b) exactly `test_the_door_imports_exactly_the_allowed_set` and `test_the_door_reaches_storage_only_for_the_name_D21_rules`, (c) exactly `test_every_named_method_exists` and `test_the_door_imports_exactly_the_allowed_set` — the three ordered sets, with nothing to flag; each mutation was reverted and the file confirmed byte-equal to its C5 blob at sha256 `9e0f3880…` before the next; the worktree was removed and pruned and `git worktree list` reads 1 line.
- G11 — the range base→C5 lists exactly the 6 declared paths other than `.agent/handoff.md`, the set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/` or `docs/`; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree cell by cell and every cell equals the `+/-` column above; pre-handback insertions 438, 349, 9, 2, 2, 14 and 158, each under the 500 cap of DECISION F104 D1; leading `<<<SLICE ` and `<<<END ` read 0 LINES in all four slice targets; `git ls-files .remedy-wt` reads 0; this round's 7 reflog rows all classify as `commit`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog.
- G12 — this file, whose own `wc -l` against the 100-line cap is reported with the full gate transcripts in the round report rather than here (R-0582).

## Authored-text proofs

The bytes received were verified at step 0, before C0a, as sha256 `69e3b24f…` over 35935 bytes and 438 lines against the three values the delegation stated, and the emitted original is still on disk at `.remedy-wt/f009-r27.md` and compares byte-equal to both committed copies. Every slice was extracted from the COMMITTED C0a blob by its `<<<SLICE `/`<<<END ` marker lines and applied by script, never hand-transcribed: `.agent/plan.md` `cmp`s exit 0 against PLANF009R27 with a negative control at exit 1, all three appends are byte-exact prefix-plus-remainder under two independent readers with a flip control each, and C5 passes §4.9 ordered equality against GUARD_TO.

## Deviations & assumptions

- ASSUMPTION, G10 scope — the block fixes the three expected failure sets but names no pytest node for them. Each mutation was measured at the guard class `TestCommandDoorImportGuard`, where all three sets reproduce EXACTLY, and again at whole-file scope, where each mutation additionally reddens 21 or 22 unrelated HTTP tests because the mutated method sits on the live dispatch path. Both readings are in the round report; only the guard-class scope makes "exactly the ids listed" reachable, and all three ordered sets are subsets of the whole-file reds.
- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6 in that order, with no extra commit, no dropped commit and no reordering. R-0642 was minted and nothing was resolved — no `Done:` line and no `Landed:` line was written — so the next free id is R-0643.

## Next

The reviewer reviews `c98d57f0`..HEAD and issues the R27 verdict; the round after that lands the route-walking 405 test, the last piece of T003.
