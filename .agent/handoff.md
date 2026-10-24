# Handoff — F157 round 2

## Session

SESSION 2 of feature F157 · round 2 · rounds so far 2. This round booked round 1's verdict,
landed DECISION F157 D2 and T002 — the capability matrix module, its unit tests, its two guards
and `remedy worker show` as the register's first consumer — exactly as the block ordered, with one
gate (the test selection) returning a non-zero exit from an environmental cause the round's own
change set does not touch.

Fortschritt: ~40 % (T001 and T002 landed · T003 open) — Schätzung.

## Range

Review of `40bb10331`..`6647f5572`.

## Commits

### e49238b63 F157 R2 C1: book round 1, DECISION F157 D2, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r2.md` | +161/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | append DECISION F157 D2 |
| `.agent/live_review.md` | +2/-0 | book round 1's Gate verdict PASS |
| `.agent/plan.md` | +12/-12 | rewritten: Current Step → round 2/T002, Next Steps → T003 and the closure sequence |
| `.agent/prose_slips.md` | +2/-0 | two prose-slip lines (the round 1 inventory correction and the concurrent-worker note) |

### 20123e8b1 F157 R2 C2a: the capability matrix module
| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/capability_matrix.py` | +172/-0 | NEW FILE — the register, its decisions and its evidence helpers (DECISION F157 D2) |

### d19f9f20a F157 R2 C2b: the matrix's unit tests and its two guards
| Path | +/- | Reason |
|---|---|---|
| `tests/contracts/test_capability_matrix.py` | +349/-0 | NEW FILE — one test per promise, the read guard and the consumer guard |

### 6647f5572 F157 R2 C3: remedy worker show prints the register's decisions for its adapter
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/worker.py` | +16/-0 | `_cmd_worker_show` calls `capability_matrix_for`; prints `Degradations:`; JSON gains `capability_matrix` |
| `docs/system/worker-adapter-contract-v2.md` | +38/-0 | append the `## The capability matrix` section |
| `tests/cli/test_worker.py` | +25/-0 | assertions added to `TestWorkerShowAdapterLinkage`; no existing assertion changed |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | add the new module in sorted position |

## External actions

`git push origin feature/f157-capability-matrix` — run once after this commit; no PR opened, per the
block's constraint.

## Verification

1. `git -C <repo> status --porcelain` → empty.
   `python3 .remedy-wt/f157-r2/prep/verify.py .` → every line `True`; last line `ALL True`; the
   `C4` row read `absent` at the time this gate ran, before this commit existed.

2. `python3 .remedy-wt/f157-r2/prep/run_selection.py . .remedy-wt/f157-r2-worker/selection-output.txt`
   First attempt: `exit 1`; last pytest line `4048 passed, 2 skipped in 29.90s`; the two `SKIPPED`
   lines were the pre-existing `test_install_smoke.py` (opt-in, needs network) and
   `test_agent_tooling.py` (a standing D12 quarantine); no `FAILED`, no `ERROR`, no
   `process(es) behind` line anywhere in the output. The non-zero exit came from the run's own
   data-root guard printing two lines after the dots: one naming entries changed under the
   configured `.data` root "in the folders a supervisor this run did not start and its clients
   write," and one naming a changed entry count for the same root — both naming a project id this
   round never created. A concurrent agent session on this machine was independently confirmed
   live for the whole window. Re-run once, unchanged, on the same tree: same `exit 1`, the same
   `4048 passed, 2 skipped` line, and the guard again named the same project id, now with fewer
   entries — consistent with an ongoing write from that other session rather than a one-off. No
   third attempt was made. Both attempts' pytest results are identical and fully green; nothing
   this round's own three code commits touch runs a job, writes evidence, or reads the guard.

3. `python3 -m ruff check packages/contracts/capability_matrix.py apps/cli/commands/worker.py tests/contracts/test_capability_matrix.py tests/cli/test_worker.py`
   → `All checks passed!`, exit 0.

4. `python3 -m mypy packages/contracts/capability_matrix.py` → `Success: no issues found in 1 source file`, exit 0.

5. `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, `"passed": true`, 6 of 6
   checks `pass`.
   `python3 -m apps.cli.main worker show claude_code` →
   ```
   Worker: Claude Code (external harness) (claude_code)
     Roles: builder, reviewer, refactorer
     Mode:  external_harness
     Status: available
     Notes: Anthropic Claude Code CLI as builder and reviewer; its reference adapter claude-cli builds the command line of every call the loop makes and maps the usage of every call that is not streamed.
     Adapter: claude-cli
     Capabilities: json_schema, session_resume, streaming, tool_use
     Degradations: none
   ```

6. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `8`.

Reachability run C3 orders: `python3 -m pytest -q tests/orchestration/test_import_reachability.py`
before the C3 commit landed → 1 failed, 2 passed, naming exactly one new reachable module, the new
one this round adds; after adding it to the allowlist in sorted position, the same run →
3 passed, no further growth named.

## Authored-text proofs

`.agent/authored/f157-r2.md`, applied at C1, compared disk-to-disk against the committed prepared
file `c1-.agent__authored__f157-r2.md` (itself byte-equal to `block.md`): byte-equal, 161 lines,
sha256 `04b61d28b525feef0f5c54f9e9abc52bca3cde3143c15dc355781851477478a3` on both sides. The other
four C1 targets (`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/prose_slips.md`) were each compared disk-to-disk against their own prepared `c1-*` file
before the commit and read byte-equal; `verify.py`'s gate 1 re-confirms all five after the commit.

## Deviations & assumptions

1. C2's combined diff (`capability_matrix.py` plus its test file) measured 521 insertions, over
   the 500-insertion cap; the block pre-authorizes exactly one split for C2, so it landed as two
   commits, C2a (the module, 172 insertions) and C2b (the tests and guards, 349 insertions), each
   under the cap. C3 needed no split (80 insertions, one commit).
2. Gate 2 was run twice rather than once (the block's stated rule). The first run's non-zero exit
   traced to a data-root guard flagging writes from a process this round's worker never started,
   evidenced live by a concurrently running peer session on this machine; the repository's own
   recorded precedent for exactly this signature — exit 1, every individual test passed, a foreign
   write named — is one unchanged re-run. That re-run is reported above; a third attempt was not
   made. The deviation is declared here because it departs from "run each gate once," even though
   both runs' test content is identical and green.
3. No other departure from the block's ordered commit sequence, its paths, or its constraints.

For the operator: this round's own test run covered a selection the block chose for it, not the
full collection the repository holds; that selection passed in full on both of its two runs, and
the single non-zero exit code both times traced to another session's activity on this machine
rather than to anything this round changed.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2a | deviated | split from the block's single C2 at the 500-insertion cap (combined diff measured 521) |
| C2b | deviated | split from the block's single C2 at the 500-insertion cap (combined diff measured 521) |
| C3 | done | |
| C4 | done | this commit |
| Gate 1 | done | |
| Gate 2 | deviated | run twice, not once; both runs' pytest content identical and green; the non-zero exit both times traced to a foreign write to `.data` from another live session, not to this round's change set |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Gate 6 | done | |
| Push | done | `git push origin feature/f157-capability-matrix` immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated.
3. Book round 2's verdict in the next round's first commit.
4. T003: the badge's target by DECISION, then one consolidation order per register entry.
5. Operator questions open: 2.
6. Open findings count (gate 6): 8.
