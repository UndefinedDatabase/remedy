# Handback — F009 R13, the plan-approval extraction

Round base `9a46a4489d0b067563b2a68f92fe54d193022da4`, branch `feature/f009-single-write-channel`. State: 65 % (T001 gebaut · T002 gebaut bis auf die Publikation · T003 begonnen: die Extraktion) — Schätzung

## Range

Review of `9a46a448..HEAD` — six commits: C0a, C0b, C1, C2, C3 and C4, in that order. Nothing came between them, none was dropped and none was added. THIS ROUND IS A REFACTOR AND NOTHING ELSE: no endpoint code, the 501 seam stands, no `accepted` outcome is written, no nonce record is published, and R-0636 and R-0637 stay unpaid — constraint 6 orders all of it to the next round.

## Commits

### 97f364be docs(state): save the F009 R13 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r13.md | +351/-0 | the round's block, byte-exact |

### 19aec738 docs(state): mirror the F009 R13 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +286/-117 | written from the committed C0a blob |

### f9c51774 docs(state): set the plan to the F009 R13 extraction round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-14 | PLANF009R13, applied byte-equal |

### a97d4004 docs(review): record the R12 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER13 appended; R12 PASSED |

### c204f0b5 refactor(orchestration): extract the flight-plan approval into a package function
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/flight_plan.py | +43/-0 | EXTRACT appended: `resolve_flight_plan_approval` |
| apps/cli/commands/decision.py | +6/-16 | the three rewrites B, A, C — the CLI becomes its first caller |

### C4, this commit, docs(state): write the F009 R13 handback
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
| C4 | done | this commit |

## External actions

`gh` was not run; this branch carries no pull request. ONE worktree was created and removed for G10: `git worktree add .remedy-wt/probe-r13 c204f0b5 --detach`, then `git worktree remove .remedy-wt/probe-r13` and `git worktree prune`, after which `git worktree list` prints 1 line — the primary checkout alone. `git push` follows C4, the last commit of this round.

## Verification

Transcripts are in the round report (R-0582); one line per gate here. Every gate that names a commit was measured at the SHA named in that line.

- G1 STOP ABSENT at Step 0 and again before C4; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel` at every reading; `git status --porcelain` printed 0 lines after each of C0a through C4; the round base read at Step 0 is `9a46a4489d0b067563b2a68f92fe54d193022da4`, which was also HEAD at Step 0.
- G2 EQUAL — the scratch file as received, `.agent/authored/f009-r13.md` at C0a and `.agent/last_block.md` at C0b are all sha256 `23b45930601cfdfe083f267acb946475c378f41c24331daa7ca4aaa380a63ed8` over 23444 bytes and 351 lines, equal to the digest the task prompt named; C0b was written from the committed C0a blob, never from the scratch file again.
- G3 9 slices from my own ordered extraction out of the committed C0a blob: PLANF009R13 `6e374ec7…` 2322 B 41 L, LEDGER13 `ef4dd09e…` 3822 B 1 L, EXTRACT `96192641…` 1717 B 43 L, CLIFROM_B `078e1359…` 205 B 3 L, CLITO_B `17c0bb63…` 195 B 3 L, CLIFROM_A `ec41a914…` 229 B 6 L, CLITO_A `bc9b8e9b…` 196 B 5 L, CLIFROM_C `21b5f2ed…` 1348 B 28 L, CLITO_C `e58ad609…` 997 B 19 L; the aggregates my script printed are 9 slices, 11031 bytes and 149 lines.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R13 (both sha256 `6e374ec7…`) at 41 lines against the 50-line cap; `^## Goal$` 1, `^## Next Steps$` 1, first `\bF\d{3}\b` match `F009`.
- G5 THE C2 APPEND HOLDS UNDER BOTH READERS. (a) the round-base blob is a byte-exact PREFIX of the C2 blob and the remainder is sha256 `e913b82d…` over 3823 bytes and 2 lines, EQUAL to a newline plus LEDGER13 (`ef4dd09e…`, 3822 B, 1 L); the file goes 454664 → 458487 bytes and 1082 → 1084 lines. (b) N COUNTED BY MY SCRIPT is 1, the whole file holds 222 blank-line units, and the last 1 of them equals LEDGER13's 1 paragraph in order. NEGATIVE CONTROL on the FIRST appended paragraph, one printable-ASCII byte flipped at offset 454665 (`G` → `F`): reader (a) ACCEPTS the true file and REJECTS the flip; reader (b) ACCEPTS the true file and REJECTS the flip — all four outcomes as required. Nothing already in the file was edited.
- G6 line-anchored over `.agent/live_review.md` at the round base and at C2: `^- R-\d+ — ` 203 and 203 with every id DISTINCT at each (203/203 both times); `^Done: R-\d+ — ` 2 and 2; `^Landed: ` 0 and 0; `^> Next free id` 0 and 0; `^Gate: R\d+ — ` 12 and 13 over that many DISTINCT keys (12/12 and 13/13); `^Gate: R13 — ` 0 and 1. Max id at C2 is R-0637. My script printed 201 for item 10's rule at `a97d4004` — line-anchored `^- R-\d+ — ` 203 minus line-anchored `^Done: R-\d+ — ` 2 (DECISION F009 D10).
- G7 (a) at C3 the round-base blob of `packages/orchestration/flight_plan.py` is a byte-exact PREFIX of the C3 file and EXTRACT is an exact SUFFIX of it; the file goes 29907 → 31624 bytes and 792 → 835 lines; C3's diff ADDS 43 lines to that path and my script printed True for the ordered equality of those added lines against EXTRACT's 43 lines, in order (R-0531). (b) in `apps/cli/commands/decision.py`, for each of the three pairs the whole-line and the indent-agnostic readings AGREE at every point: CLIFROM_B 1 → 0 and CLITO_B 0 → 1, CLIFROM_A 1 → 0 and CLITO_A 0 → 1, CLIFROM_C 1 → 0 and CLITO_C 0 → 1, base then C3. The reconstruction — the round-base blob with the three replacements applied in the order B, A, C — is byte-equal to the C3 blob: one boolean, True.
- G8 `python3 -m ruff check` over `packages/orchestration/flight_plan.py` and `apps/cli/commands/decision.py` EXITS 0 at C3 in the primary checkout (`All checks passed!`). At the round base, taken WITHOUT writing to either tracked file — `git show <base>:<path>` piped into `python3 -m ruff check --stdin-filename <path> -`, so `per-file-ignores` still resolves by path — both paths also EXIT 0. Both readings are zero, so no rule-code multiset comparison is owed.
- G9 both suites EXIT 0, run SERIALLY in the primary checkout at C3, never two pytest processes at once: the four-path behaviour-preservation group printed `191 passed in 52.25s` (passed+skipped 191) at exit 0, and `python3 -m pytest tests/cli/test_golden_path.py -q -rf` printed `42 passed in 20.52s` (42) at exit 0. Neither count was predicted; each is what the run printed and each exit code is the one my script read from the process.
- G10 THE PROBE BITES, and it was run as a probe, not as a colour. Control: 191 passed, exit 0 (G9 command 1). In the disposable worktree at C3, with everything after `resolve_flight_plan_approval`'s docstring replaced by `    raise AssertionError("probe")` — 17 body lines replaced by one — the same command EXITS 1 at `16 failed, 175 passed in 52.06s`. The 16 failing node ids, taken from the run's own `-rf` short summary and never from a regex over `-v` output (R-0611): `tests/cli/test_plan_approval.py::TestDecisionResolve::test_approve_flow`, `::TestDecisionResolve::test_reject_flow`, `::TestApprovalGoldenPathCLI::test_full_approval_sequence`; `tests/cli/test_decision_answers.py::TestResolveWithAnswers::test_answer_persisted_as_human`, `::TestWriteBackAndImmutability::test_mixed_answer_and_default_persisted`, `::test_no_answers_records_all_defaults`, `::test_late_answer_rejected_as_already_resolved`, `::test_no_open_decision_after_approval`, `::test_reject_leaves_clarifications_untouched`, `::test_plan_without_questions_keeps_empty_list`, `::TestAssumptionsCommand::test_approval_writes_the_evidence_log`, `::TestAssumptionsCommand::test_command_prints_the_log`; `tests/cli/test_mission_cmd.py::TestApprovalOptIn::test_approving_without_the_flag_creates_no_mission`, `::test_approving_with_the_flag_creates_and_links_the_mission`, `::test_the_flag_works_even_when_intake_did_not_flag_the_goal`, `::test_a_job_already_in_a_mission_is_refused`. Both branches are covered — approve and reject — across three of the four test files, so the approval suites DO reach the extracted function and the extraction has a real behavioural proof. No code was adjusted to produce this. The source was then restored byte-identically: the worktree file's sha256 is `2298635f1e4151f8d9712786b7d5224223bc642f8cb3c95d6f123cb858a1730d`, equal to the C3 blob's, with `git status --porcelain` 0 lines in the worktree; the worktree was removed and pruned and `git worktree list` prints 1 line.
- G11 the range from the round base to C3 lists EXACTLY the six declared paths other than `.agent/handoff.md` — `.agent/authored/f009-r13.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/flight_plan.py`, `apps/cli/commands/decision.py` — the set difference EMPTY in both directions. Five commits, each with ONE parent, `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-` column of the tables above; insertions 351, 286, 17, 2 and 49, all under the 500-insertion cap of AGENTS.md DECISION F104 D1, so no split was needed. `^<<<SLICE ` and `^<<<END ` read 0 lines each in `.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/flight_plan.py` and `apps/cli/commands/decision.py` at C3. THIS ROUND'S five reflog rows — the entries above the round base — classify as `commit` 5, with `amend`, `rebase` and `cherry` 0 each; no total is asserted over the whole reflog (R-0601). `git ls-files .remedy-wt` is 0.
- G12 this handback carries every mandated section of docs/agents/handback_template.md, an item-status table with exactly one row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA and one line per gate. `wc -l` measures it at 82 lines against the 100 a bundle of more than five commits allows.

## Authored-text proofs

All nine slices were extracted from the COMMITTED C0a blob by their `<<<SLICE ` and `<<<END ` marker lines with a script and applied programmatically. PLANF009R13 is byte-equal to `.agent/plan.md` at C1 (G4); LEDGER13 is proved as an append under two independent readers with a script-counted N and a negative control on the first appended paragraph (G5); EXTRACT is proved as a code append by ordered equality of the diff's added lines, not by a per-line count (G7a, R-0531); the three FROM/TO pairs are proved by agreeing whole-line and indent-agnostic counts plus one byte-equal reconstruction (G7b). No marker line reached any target file; nothing was retyped, rewrapped, reflowed, reindented or whitespace-adjusted.

## Deviations & assumptions

None. The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly: no commit was added, dropped or reordered. All nine slices were applied byte for byte and NO OBJECTION to any of them arose (constraint 1). One assumption, checked rather than assumed: the extracted function re-reads `job.flight_plan` where the CLI held a local `fp` from `getattr(job, "flight_plan", None)`; `packages/core/models.py:237` declares `flight_plan: dict[str, Any] | None = None` as a plain field, not a copying property, so both names bind the same dict and the mutate-then-save sequence is unchanged. `.agent/context.md` and `.agent/decisions.md` were NOT touched: DECISION F009 D5 already records this extraction, and constraint 6 confines the round to its change set.

## Next

No `.agent/STOP` is present. Open findings at `a97d4004` are 201 by item 10's rule — line-anchored `^- R-\d+ — ` 203 minus line-anchored `^Done: R-\d+ — ` 2 (DECISION F009 D10). The next free id, derived with `max` over the line-anchored entries, is R-0638. `.agent/candidates.md` is EMPTY — it holds its header and an explicit EMPTY statement, and zero candidate entries. The next round is T003's effect table — the round that retires the 501 seam — and it therefore owes the fixes for R-0636 and R-0637, both of which depend on the publish call site it introduces. R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and R-0635 stay routed to a paydown branch.
