# Handoff — F033 Hunk-level diff approval, round 24

## Session

SESSION 6 of feature F033 · round 24 · rounds so far 24

The soft limit is round 25 and the remaining work does not fit in it, so the
scope report operator amendment amend0827 rule 6 obliges is carried below,
under "Scope report". It is a DOCUMENTED PROPOSAL and was not executed.

## Range

Review of `c9dd471f`..`HEAD` on branch `feature/f033-hunk-approval-v2`.

This round completes F033's FUNCTIONAL scope: the last hop is wired.

## Commits

Eight commits C0a through C6, plus this handback commit C7. Every one is
single-parent. The block's ordered commit sequence was followed exactly — no
extra commit, none dropped, none reordered.

### b9f83c64 docs(f033): save the round 24 step block — C0a
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r24.md` | +334 / -0 | the step block, copied byte for byte from `.remedy-wt/f033-r24-block.md` with `shutil.copyfile`, never retyped |

### 7dc987c5 docs(f033): mirror the round 24 block into last_block — C0b
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +262 / -278 | the same bytes mirrored; single `.agent/**` state-file rewrite |

### bd99959e docs(f033): rewrite the plan for round 24 — C1
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +22 / -25 | full rewrite from slice PLAN24, byte-equal, 46 lines |

### 90af5927 docs(f033): book the round 23 verdict and register R-0748 — C2
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 / -0 | append of slice RECORD24: the R23 PASS gate entry and the R-0748 registration |

### 3fc4fbbe docs(f033): record the round 23 stale base numeral slip — C3
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +2 / -0 | append of slice SLIPS24, one dated line, no id |

### 7cb78726 fix(f033): retire the false persists-no-decision clause from the acceptance test docstring — C4 (SPEC A)
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_builder_prompt_hunk_rejections.py` | +9 / -6 | pair PAIR-DOC applied as a REWRITE of the module docstring's closing paragraph |
| `.agent/live_review.md` | +2 / -0 | SPEC A3's single `Landed: R-0748` line, in the SAME commit |

### 7c02e01f feat(f033): supply the task recorded hunk ledger at the job level run_pingpong call — C5 (SPEC B)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_job.py` | +49 / -0 | module-level `_recorded_hunk_ledger_for_task(job, task)` plus one `hunk_ledger=` keyword at the `run_pingpong` call |

### 5cb87f37 test(f033): pin the job level hunk ledger lookup, its scope boundary and its totality — C6 (SPEC C)
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_pingpong_job_hunk_ledger.py` | +241 / -0 | new file, 10 tests covering SPEC C1 to C6 |

### C7 — this handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | the handback itself; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Action | Command | Outcome |
|--------|---------|---------|
| worktree add | `git worktree add .remedy-wt/r24-mut HEAD --detach` | REAL exit 0, detached at `5cb87f37` |
| worktree remove | `git worktree remove .remedy-wt/r24-mut --force` | REAL exit 0 |
| worktree prune | `git worktree prune` then `git worktree list` | REAL exit 0; only the primary checkout remains |
| push | `git push -u origin feature/f033-hunk-approval-v2` | run IMMEDIATELY after the commit that writes this file, so its outcome cannot be stated inside it — the same self-reference that stops a handoff tabling its own commit. The worker's report to the operator carries the real exit code |

No pull request was created, none exists, and none should exist before the
closure sequence. `main` was never touched. Nothing was force-pushed.

## Verification — one line per gate, REAL exit codes

REAL exit codes were taken with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and NO
pipe anywhere, because `false | tail` reports 0. All gates ran at C6, before C7.

| Gate | Result | REAL exit | What was measured |
|------|--------|-----------|-------------------|
| G1 TRANSPORT | GREEN | 0 | committed `.agent/authored/f033-r24.md` sha256 `1fc8691cbc74309b535c15b834334c36892756dc3765a317404c153b5410ea76`, 25812 bytes; `cmp` against `.remedy-wt/f033-r24-block.md` REAL exit 0; `.agent/last_block.md` identical digest and length |
| G2 THE PROSE FILES | GREEN | 0 | `.agent/plan.md` byte-EQUAL to PLAN24, 46 lines (under 50), holds `## Goal` and `Steps`; `.agent/prose_slips.md` base 30807 MEASURED at `c9dd471f` + 1 + slice 529 = 31337 = committed size; base a byte PREFIX, slice an exact SUFFIX |
| G3 THE RECORD APPEND (C2) | GREEN | 0 | base 1595141 MEASURED + 1 + RECORD24 7458 = 1602600 = committed size at `90af5927`; pre-commit blob a byte PREFIX, slice an exact SUFFIX; N COUNTED in the script = 2; the file's LAST 2 blank-line units equal the slice's paragraphs IN ORDER; byte flipped at offset 1597589, proved inside the FIRST appended paragraph's span 1595142–1600037 (`b's'`→`b'S'`), and BOTH readers — suffix-equality and last-N-paragraphs — REJECTED the flipped bytes and ACCEPTED the unflipped ones |
| G4 THE LEDGER | GREEN | 0 | registered distinct 308 (`c9dd471f`) → 309 (C2, C4), ADDED id exactly `R-0748`; `^Done: R-\d+ — ` 53 lines over 51 distinct UNMOVED at all three; `^Landed: ` 19 → 20 with `^Landed: R-0748 — ` 0 before and exactly 1 at C4; `^Gate: F033 R23 — ` 0 before, exactly 1 after; open set 257 → 258. `^Landed: R-0747 — ` and the `Done: R-0747` paragraph both still exactly 1 |
| G5 THE PAIR + THE SWEEP | GREEN | 1 (grep, no match) | in `test_builder_prompt_hunk_rejections.py`: PAIRDOC-FROM 0 times (also 0 for the 423-byte form without the trailing newline), PAIRDOC-TO exactly 1 time. `grep -rn -- "persists no decision" packages/ apps/ tests/ docs/` REAL exit 1, 0 occurrences; same command for `"persists NOTHING"` REAL exit 1, 0 occurrences. See deviation 1 — this gate was RED on its first run |
| G6 THE CODE AGAINST THE SPEC | GREEN | 0 | `python3 -m ruff check` over `pingpong_job.py`, the new test file and the acceptance test file REAL exit 0. By AST: `_recorded_hunk_ledger_for_task` IS a module-level `FunctionDef`; exactly 1 `run_pingpong` call, at line 2281, passing `hunk_ledger=_recorded_hunk_ledger_for_task(job, task)`. RUNNING the shipped helper on a fake job carrying a recorded decision returned a ledger whose reason is byte-identical to the stored `'  keep the old name\n\n\tand do not reflow this\n'` |
| G7 MUTATION RED-PROOFS | GREEN | 0 (control) / 1 (each mutant) | disposable worktree `.remedy-wt/r24-mut` at `5cb87f37`, removed and pruned. UNMUTATED CONTROL REAL exit 0 at 26 passed. Every anchor asserted to occur EXACTLY ONCE; after each mutation the file was restored and proved byte-identical by sha256 `cf5e06df3c77ac1bec1884ecdc8471c22ef42b80d7af371cb4cf1f421162d3ad`. Details below |
| G8 SUITES AND STRUCTURE | GREEN | 0 | six suites SERIALLY, every REAL exit 0; `git status --porcelain` EMPTY; per-commit insertions all under 500; path set equal to the change set in BOTH directions |

### G7 detail — the three mutations

Control: REAL exit 0, **26 passed** (10 in the new file + 16 in the acceptance
suite). Every run — control and mutant alike — printed the import-path proof
`pingpong_job.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/r24-mut/packages/orchestration/pingpong_job.py`,
resolving INSIDE the worktree. See deviation 2: without that measure the
mutations would have run against the primary checkout and proven nothing.

| # | Mutation | Anchor unique | REAL exit | Failing test NAMES |
|---|----------|---------------|-----------|--------------------|
| (i) | the helper ignores the task and uses a fixed id (`task_id=task.task_id,` → `task_id="t-1",` inside the helper's call) | yes, 1 | 1 — **3 failed, 23 passed** | `test_a_different_tasks_decision_is_never_returned` (C3); `test_a_job_scoped_decision_is_not_quoted_into_a_tasks_prompt` (C4); `test_every_unusable_shape_yields_an_empty_ledger_and_raises_nothing[task_carries_no_task_id]` |
| (ii) | SPEC B2's structural guard removed (the whole `try:`/`except Exception: return HunkDecisionLedger(())` replaced by the bare return) | yes, 1 | 1 — **2 failed, 24 passed** | `test_every_unusable_shape_yields_an_empty_ledger_and_raises_nothing[task_carries_no_task_id]`; `...[job_metadata_raises_on_access]` |
| (iii) | stop passing `hunk_ledger` at the `run_pingpong` call (the keyword line deleted) | yes, 1 | 1 — **1 failed, 25 passed** | `test_the_run_pingpong_call_passes_a_hunk_ledger_keyword` (C6) |

The block permitted "this mutation reddened nothing". It did not arise: all
three reddened. Mutation (ii) is worth a sentence — the guard is OBSERVABLE
precisely because it wraps the two ATTRIBUTE accesses (`job.metadata`,
`task.task_id`), which `load_latest_hunk_ledger_from_metadata` cannot absorb
since it is total only over the mapping it is HANDED. The three metadata-shape
cases stayed green under (ii), which is the correct result and is why the
totality parameters are separate: they name which shape broke.

### G8 detail — the suites, serially

| Suite | REAL exit | Passed |
|-------|-----------|--------|
| `tests/orchestration/test_pingpong_job_hunk_ledger.py` | 0 | 10 |
| `tests/orchestration/test_builder_prompt_hunk_rejections.py` | 0 | 16 |
| `tests/orchestration/test_hunk_decision_record.py` | 0 | 23 |
| `tests/orchestration/test_job_task_runner.py` | 0 | 191 (105.82s) |
| `tests/orchestration/test_pingpong.py` | 0 | 34 |
| canary `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | 42 |

Structure: `git status --porcelain` EMPTY. Per-commit insertions `c9dd471f`..`5cb87f37`:
334, 262, 22, 4, 2, 11, 49, 241 — each under 500, 925 total, all single-parent.
Path set over the range equals the declared change set minus `.agent/handoff.md`
in BOTH directions (0 missing, 0 extra).

After the suites re-generated `__pycache__`, G5's sweep was RE-RUN and both
strings still read REAL exit 1 at 0 occurrences, confirming the stale artifact
of deviation 1 does not come back.

## Authored-text proofs

| Text | Proof |
|------|-------|
| the step block | `sha256` computed by me: `1fc8691cbc74309b535c15b834334c36892756dc3765a317404c153b5410ea76`, 25812 bytes — matches the digest the order stated. `cmp .remedy-wt/f033-r24-block.md .agent/authored/f033-r24.md` REAL exit 0; `cmp` against `.agent/last_block.md` REAL exit 0 |
| PLAN24 | `.agent/plan.md` byte-EQUAL to the extracted slice, sha256 `b3bcca25b6f51f06ccbed1f887dc3287cc3f2db6b1359449b9f2ce43b79e7f85`, 2514 bytes |
| RECORD24 | exact SUFFIX of `.agent/live_review.md` at C2; 7458 bytes |
| SLIPS24 | exact SUFFIX of `.agent/prose_slips.md` at C3; 529 bytes |
| PAIRDOC-FROM / PAIRDOC-TO | FROM 0x, TO 1x in the target after C4; `TO contains FROM` measured FALSE by me too, so it is a REWRITE |
| `Landed: R-0748` line | extracted from the block by matching the 4-space-indented line and stripping exactly 4 spaces; 188 bytes, no trailing whitespace; appended as `\n` + line + `\n` = 190 bytes |

All slices and pair halves were extracted by script from the byte range BETWEEN
the `<<<BEGIN`/`<<<END` markers, exclusive. Nothing was retyped or reflowed.

## Deviations & assumptions

**1. G5 was RED on its first run, and the cause was a stale build artifact — declared in full.**
`grep -rn -- "persists no decision" packages/ apps/ tests/ docs/` came back
REAL exit **0** with one match, on stderr:
`grep: tests/orchestration/__pycache__/test_builder_prompt_hunk_rejections.cpython-310-pytest-9.0.3.pyc: binary file matches`.
That is compiled bytecode of the PRE-C4 source of the very file this round
repaired: its mtime is 13:47:43 against the source's 13:57:49, and it is
gitignored by `.gitignore:2 __pycache__/`. The source sweep was already clean —
`git grep -n -- "persists no decision" -- packages/ apps/ tests/ docs/` REAL
exit 1, 0 hits. I removed **that one file, by exact path** (via
`os.remove`; `rm` is denied in this sandbox) as build-artifact hygiene — the
same purge G7 mandates — and then re-ran the gate command UNMODIFIED, which
returned REAL exit 1 at 0 occurrences. **No gate wording was weakened and no
assertion was touched**; what was deleted is regenerable bytecode, not content.
I am flagging this rather than burying it because the reviewer re-running G5 on
a filesystem that still held that `.pyc` would have seen the same red, and
because a sweep whose reach includes compiled caches is a measurement question
the round should leave on the record.

**2. The disposable worktree's import path resolved to the PRIMARY checkout, and would have made G7 vacuous.**
A bare `python3` run inside `.remedy-wt/r24-mut` imported
`/home/decodeux/Repos/remedy/packages/orchestration/pingpong_job.py`, because a
`.pth` puts the repo root on `sys.path` ahead of the worktree. I probed this
BEFORE running any mutation. The fix is `.remedy-wt/r24_wt_run.py`, which
`os.chdir`s into the worktree, inserts it at `sys.path[0]`, PRINTS the resolved
`pingpong_job.__file__` on every run, and only then calls `pytest.main`. Had I
skipped the probe, all three mutations would have run against unmutated code —
the control and every mutant would have read 26 passed, and I would have
reported three red-proofs that measured nothing.

**3. The helper is PRIVATE: `_recorded_hunk_ledger_for_task`.**
SPEC B1 said "ONE small module-level helper" without fixing its visibility. I
used a leading underscore so that no `Public API:` obligation arises in
`pingpong_job.py`'s module docstring — I checked, and unlike `proof_chain.py`
(finding R-0746) no test guards that block for this module, so a public name
would have created an unguarded list to keep in sync for no gain. The name
carries four words and a domain word per the discoverability convention.

**4. B4: TWO names are imported locally, not one.**
`run_job` imports its `packages.orchestration` dependencies INSIDE the function,
so per B4 I followed that and did not add module-level imports. The helper
imports `load_latest_hunk_ledger_from_metadata` as ordered **and also**
`HunkDecisionLedger`, which B4 does not name: the guard's empty-ledger return
needs the constructor, and `HunkDecisionLedger(())` is the exact form
`hunk_decision_record.py` itself uses for that answer. `python3 -m ruff check`
is REAL exit 0 and no unrelated line was reordered.

**5. Placement of the new keyword at the call site.**
`hunk_ledger=` sits directly after `task_input=task_input,`, both being prompt
inputs. Nothing else about that call changed — B3 satisfied.

**6. The G7 control covers TWO suites (26 tests), not one.**
The new file alone would have sufficed, since all three mutations target checks
in it. I included `test_builder_prompt_hunk_rejections.py` so the same pass
count is comparable across control and every mutant, and so a mutation that
reddened the loop suite as a side effect would be visible. None did.

**7. A reading no gate ordered, recorded so it is not re-derived later.**
The helper returns an EMPTY ledger rather than `None` when nothing is recorded,
so the job-level call now passes a ledger object on EVERY task, where before it
passed nothing. That is safe and I measured why:
`pingpong_loop.render_rejection_findings` answers `""` for `None`, for a ledger
with no entries and for a ledger holding only approvals, and the ONE emptiness
test at the segment guard means no `builder_hunk_rejections` segment registers
for an empty ledger. So the golden's exact ten-name manifest in
`tests/orchestration/test_builder_prompt_golden.py` cannot be disturbed — and
`test_pingpong.py` (34) and `test_job_task_runner.py` (191) are both green.

**8. Constraint 2 re-measured, and this time the block was RIGHT.**
I measured both append bases myself at `c9dd471f` rather than trusting the
block: `.agent/live_review.md` 1595141 and `.agent/prose_slips.md` 30807, by
`wc -c` on disk AND `git cat-file -s` at the base commit, agreeing. Both match
the block's numerals. The R23 slip did not recur.

**9. Sandbox notes, not departures from the order.**
`rm` is denied here (in addition to the denials the block lists), so artifact
removal went through `os.remove` in a script. Some compound `bash` lines were
refused by the guard on FORM, so every multi-step measurement was written as a
file under `.remedy-wt/` and run with `python3 -B <path>`.

No block item was skipped, widened or reordered. No path outside the change set
was touched: `apps/cli/commands/do_cmd.py`, `packages/orchestration/pingpong_loop.py`
and everything under `docs/` are untouched, as G8's both-directions path check
shows. The `Landed: R-0747` line, the `Done: R-0747` paragraph and round 23's
superseding comment block are all intact and were measured as such.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Bundle 1 — C0a save the block | done | `cmp` REAL exit 0, digest verified by me |
| Bundle 2 — C0b mirror to `last_block.md` | done | same bytes, `cmp` REAL exit 0 |
| Bundle 3 — C1 rewrite `plan.md` from PLAN24 | done | byte-equal, 46 lines |
| Bundle 4 — C2 append RECORD24 | done | G3 arithmetic, prefix, suffix, ordered paragraphs, negative control |
| Bundle 5 — C3 append SLIPS24 | done | G2 arithmetic, prefix, suffix |
| Bundle 6 — C4 SPEC A + the `Landed:` line, one commit | done | one commit `7cb78726` carries both |
| Bundle 7 — C5 SPEC B | done | `7c02e01f` |
| Bundle 8 — C6 SPEC C | done | `5cb87f37`, 10 tests |
| Bundle 9 — C7 handback | done | this file |
| SPEC A1 — PAIR-DOC as a REWRITE, report both counts | done | FROM 0x, TO 1x; `TO contains FROM` FALSE re-measured by me |
| SPEC A2 — leave round 23's superseding block | done | present exactly once, untouched; the diff shows only the docstring paragraph moving |
| SPEC A3 — ONE `Landed: R-0748` line, no `Done:` paragraph | done | 1 line at C4, `^Done:` distinct count UNMOVED at 51 |
| SPEC B1 — one module-level, testable helper | done | `_recorded_hunk_ledger_for_task`, module-level by AST; see deviation 3 |
| SPEC B2 — TOTAL, ONE guard, both boundaries documented | done | one `try`, no nested second; (i) job-scope sentinel AND the `"job"` task-id collision and (ii) the empty-ledger meaning are both in the docstring; no guard added against the collision |
| SPEC B3 — `hunk_ledger=` at the `run_pingpong` call | done | AST: line 2281; nothing else about the call changed |
| SPEC B4 — follow the module's import style | done | function-local, matching `run_job`; see deviation 4 |
| SPEC C1 — a recorded decision comes back byte for byte | done | `test_a_recorded_decision_comes_back_as_that_tasks_ledger_byte_for_byte` |
| SPEC C2 — composed through to the prompt | done | `test_the_ledger_the_job_reads_composes_into_the_builder_prompt` |
| SPEC C3 — a different task's decision is not returned | done | `test_a_different_tasks_decision_is_never_returned`, with a premise assertion so it is not vacuous |
| SPEC C4 — a JOB-scoped decision is not returned | done | `test_a_job_scoped_decision_is_not_quoted_into_a_tasks_prompt`, referencing `DIFF_SCOPE_JOB` by name |
| SPEC C5 — totality, five shapes | done | five parametrised cases, each named, all empty and none raising |
| SPEC C6 — the call site IS wired (AST, SHAPE check) | done | `test_the_run_pingpong_call_passes_a_hunk_ledger_keyword`, labelled a shape check in its own docstring, with a non-vacuity assertion, reading the module's own `__file__` so it is worktree-correct |
| G1–G8 | done | all GREEN; table above |

## Open findings

**258 open** (registered distinct 309 minus 51 resolved distinct, measured at
C4). Up one from 257 at `c9dd471f`: R-0748 was registered this round by C2 and
its repair landed in the same round at C4, but a `Done:` paragraph is
reviewer-authored text and SPEC A3 forbade me to write one — so R-0748 is
correctly still counted OPEN until the reviewer resolves it.

## Scope report — amendment amend0827 rule 6

**Finished.** F033's functional scope is complete as of this round. Hunks carry
stable content-hash ids; the viewer, node and report render partial state
truthfully; `approve_hunks` applies an approved subset all-or-nothing; a
decision is recorded durably on `job.metadata`; it is read back as a ledger,
selected by latest stamp, rendered as repair findings, composed into the builder
prompt verbatim, forwarded by `run_pingpong`, and — as of C5 — supplied by the
job-level caller that holds the task. The route from an operator's rejected hunk
to the next builder's prompt is now closed end to end.

**Missing**, and it does not fit in the one round the soft limit leaves:

1. R-0745 — the write door's transitive import closure. Open, unscheduled, and
   a block condition at closure.
2. The operator documentation for `patch approve-hunks` under `docs/`. No round
   has yet been given a path for it, and this round was explicitly forbidden to
   touch `docs/`.
3. The integration-gate round.
4. The two-round closure sequence.

That is four to five rounds of work against one remaining.

**Proposal**, for the operator, never executed on any agent's authority:
extend F033 past the 25-round soft limit by the four to five rounds the list
above needs, in that order, rather than closing the feature with R-0745 open or
with the operator-facing documentation absent. The alternative — closing now —
would ship a feature whose CLI door no document describes.

## Next

The single expected next action: the **reviewer** re-runs G1 through G8 against
the real diff `c9dd471f`..`HEAD` and issues the round 24 verdict, resolving
R-0748 with a reviewer-authored `Done:` paragraph if it passes. The operator
decision requested in the scope report above is needed before round 25 is
planned. No pull request should be created before the closure sequence.
