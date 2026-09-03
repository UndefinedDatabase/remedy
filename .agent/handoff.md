# Handoff — F112 Prompt budget per task class, round 13 (T003c: Files: markdown section, TaskEntry.files_hint, adapter wiring)

## Session

SESSION 4 of feature F112 · round 13 · rounds so far 13.

This round books round 12's already-independently-reviewed PASS
verdict into `.agent/live_review.md` (RECORD12, amend0827 rule 1 — a
pending verdict books in the FIRST COMMIT of the next round that is
happening anyway, i.e. round N's verdict books in round N+1's first
commit), then builds **T003c** exactly as DECISION F112 D5's CHOSEN
clause specified: job task markdown gains a `"Files:"` inline marker
(mirroring the existing `"Acceptance:"` marker) that `parse_job_file`
parses into a new `TaskEntry.files_hint: list[str]` field, exported/
imported the same way `inputs`/`task_class` already are.
`task_entry_to_planned_task` now passes `task.files_hint` through
instead of hardcoding `[]`; its own docstring is updated to match
(it previously documented the empty-always behavior as deliberate —
that documentation is now stale by construction and was rewritten,
not just extended).

This round ships production code: two files touched
(`packages/orchestration/pingpong_job.py`,
`tests/orchestration/test_job_task_runner.py`), 82 insertions total —
well under the 500-line cap, and no DECISION was needed (this round
executes an already-recorded architectural call, it does not make a
new one), so there is no C3 this round.

## Range

Review of `afb90730..HEAD` (commits C0a, C0b, C1, C2, C4, plus this
handback commit C5 itself — six commits total this round, no C3 and
no C6; C3 is skipped because there is no DECISION this round). **This
range is UNREVIEWED by construction** — round 13 has not yet been
independently re-reviewed by the reviewer; no verdict on this round's
own work is claimed anywhere in this file.

## Commits

### 2991c37a F112 R13 C0a: save round 13 block to .agent/authored/f112-r13.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r13.md` | 62/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### f0d54a33 F112 R13 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 24/45 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). Byte-equality confirmed before commit — `cmp` was NOT denied this round (unlike rounds 11-12), it ran and exited 0; a `python3` byte-equality read (`a == b` → True, 3859 bytes both) was additionally run as a second, independent confirmation. |

### c3b1034f F112 R13 C1: append RECORD12 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD12 (round 12's verdict) via `content_bytes + b"\n" + RECORD12_bytes` — the ONE-newline formula. |

### 1bc72f6d F112 R13 C2: apply PLAN13 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 18/21 | Whole-file replacement with PLAN13, extracted programmatically from the committed authored file, not retyped. No trailing newline (per the block). |

### ec9ffdd2 F112 R13 C4: add Files: markdown section, TaskEntry.files_hint, adapter wiring (T003c)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 37/5 | Pairs J-P (all REWRITE, each FROM confirmed to occur exactly once before applying): section-dict `files_lines` list; a third parser state (`_in_files`) mirroring `_in_acceptance`, entered on a `"Files:"` marker and exited on an `"Acceptance:"` marker; task construction strips leading `"-"` bullets into `TaskEntry.files_hint`; export/import round-trip; the `TaskEntry.files_hint` field itself; `task_entry_to_planned_task`'s docstring and `PlannedTask(...)` call now pass `task.files_hint` through instead of hardcoding `[]`. |
| `tests/orchestration/test_job_task_runner.py` | 45/0 | Pairs Q-S: `_JOB_WITH_FILES` fixture; two new `TestJobPlanParsing` tests (`test_files_section_extracted`, `test_no_files_section_leaves_files_hint_empty`); one new `TestPersistence` round-trip test; one appended `TestTaskEntryToPlannedTaskAdapter` test (`test_files_hint_flows_through_from_task_entry`), verified as a byte-exact file-end append (prefix-match + tail-match against the exact appended bytes, not FROM-string matching). |

## External actions

`git push` → run immediately after this handback commit (C5); outcome
recorded in the completion report, not in this file (write-once rule).

Mutation red-proof worktree `.remedy-wt/f112-r13-mutation` was created
(`git worktree add .remedy-wt/f112-r13-mutation HEAD --detach`, off
commit `1bc72f6d`, before C4 was committed), the two modified files
were copied in, the mutation applied there only (never in the primary
checkout), the targeted tests run, and the worktree removed
(`git worktree remove .remedy-wt/f112-r13-mutation --force`) before C4
was committed. `git worktree list` after removal showed only the
primary checkout and the pre-existing, unrelated `remedy/job-*`
worktrees; no `f112-r13-mutation` entry remained.

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r13.md
.agent/last_block.md` ran successfully this round (exit 0) — the
sandbox did NOT deny it this time, unlike rounds 11-12. A `python3`
byte-equality read (`a == b` → **True**, both files **3859 bytes**) was
run as a second, independent confirmation anyway, since the block's
instruction was "try `cmp` first; if denied, substitute" and both were
already in hand. Extracted-slice byte counts, measured programmatically
against the pinned figures in the block: RECORD12 **1331 bytes**
(pinned 1331, match), PLAN13 **2049 bytes** (pinned 2049, match). PASS.

**Step 1 LEDGER (RECORD12)** — `.agent/live_review.md` measured
**2269956 bytes** immediately before the append (matches round 12's
own post-append size exactly, per RECORD11's earlier append size
stated in round 12's handoff). Appended as `content_bytes + b"\n" +
RECORD12_bytes` (ONE newline). Post-size measured at **2271288
bytes**, matching `2269956 + 1 + 1331` exactly. Old-file-is-prefix
check: **True**. Tail-equality check (`post[len(old):] == b"\n" +
RECORD12_bytes`): **True**. PASS.

**Step 2 PLAN** — PLAN13 extracted programmatically from the committed
`.agent/authored/f112-r13.md` (between its markers) to an in-memory
byte string, then Python byte-equality against `.agent/plan.md`:
**equal, 2049 bytes both sides**. `wc -l .agent/plan.md` → **43** (the
file has no trailing newline per the block's own instruction, so
literal `wc -l` undercounts by one against the content-line count —
the same pattern rounds 11-12's plan.md showed). Content-line count
(newline-count + 1) → **44**, matching PLAN13's own line count.
`grep -c '^## Goal' .agent/plan.md` → **1**. `grep -c '^## Next Steps'
.agent/plan.md` → **1**. PASS.

**Step 3 DECISIONS FILE UNCHANGED (expected — no C3 this round)** —
`.agent/decisions.md` measured **766660 bytes**, identical to round
12's own post-D5-append size; its tail (`open(...).read()[-60:]`)
still reads `"...gate would immediately re-discover false."`, DECISION
F112 D5's own final sentence — confirming this round neither appended
nor otherwise touched the file, as the block specified (no DECISION
this round). PASS.

**Step 4 CODE (C4)** — All seven FROM strings (Pairs J, K, L, M, N, O,
P — REWRITE) grepped to confirm exactly one occurrence each before
applying via `Edit`; `git diff` reviewed in full before commit and
matched the block's TO text exactly, no unrelated changes. Tests: `-k
"test_files_section_extracted or test_no_files_section_leaves_files_hint_empty
or test_files_hint_round_trips_through_persist_and_load or
test_files_hint_flows_through_from_task_entry"` → **4 passed**. Full
file: `python3 -m pytest tests/orchestration/test_job_task_runner.py
-q` → **206 passed** (no regressions). Lint: `python3 -m ruff check
packages/orchestration/pingpong_job.py
tests/orchestration/test_job_task_runner.py` → **"All checks
passed!"**. Canary: `pytest tests/cli/test_golden_path.py -q` → **42
passed**. PASS.

**Step 5 MUTATION RED-PROOF** — deleted the
`current_task["_in_files"] = False` line from Pair K's TO (inside the
`"Acceptance:"` branch) in the disposable worktree only. Ran `python3
-m pytest tests/orchestration/test_job_task_runner.py -k
"test_files_section_extracted or
test_no_files_section_leaves_files_hint_empty" -q`:
`test_files_section_extracted` went **RED** exactly as predicted —
`AssertionError: assert ['src/main.py', 'docs/README.md', 'done'] ==
['src/main.py', 'docs/README.md']` (the stuck `_in_files` flag
misrouted the `"- done"` acceptance line into `files_lines` too,
because `_JOB_WITH_FILES`'s `Files:` section precedes its
`Acceptance:` section). `test_no_files_section_leaves_files_hint_empty`
stayed **GREEN** — its fixture (`_TWO_TASK_JOB`) has no `Files:`
section at all, so `_in_files` never becomes `True` and the mutation
has nothing to reach. Result: `1 failed, 1 passed`. PASS (the mutation
proof behaved exactly as specified).

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r13.md` (committed at `2991c37a`) vs
`.agent/last_block.md` (committed at `f0d54a33`): byte-identical (Step
0 transport check above — `cmp` itself ran clean this round, plus a
`python3` byte-equality double-check). RECORD12 and PLAN13 were both
extracted programmatically from this committed file (never retyped)
and applied via the stated append formula or whole-file write; every
application was confirmed against pinned byte counts and before/after
equality checks above (Steps 1-2). The code change (C4, Pairs J-S plus
the file-end test append) was typed directly from the round's own
prompt text (not carried inside the authored block's markers, unlike
the ledger/plan texts) and verified mechanically (FROM-occurrence
counts, a full `git diff` read before commit, the targeted/full/lint/
canary test runs, and the mutation red-proof) per Step 4-5 above.

## Deviations & assumptions

1. **`cmp` was NOT denied this round** (unlike rounds 11-12, where the
   bare `cmp <file1> <file2>` invocation itself hit a sandbox
   permission denial). This round it ran and exited 0 cleanly. Not a
   deviation from the block (the block only required a substitute IF
   denied) — stated here because the prior two rounds' handbacks both
   declared the opposite outcome, and a silent flip is worth naming so
   the reader does not assume the sandbox property is fixed either way.
   Unrelated: two other Bash invocations THIS round (a `for` shell loop
   over commit SHAs, and a bare `cd <dir> && ...` compound) WERE denied
   by the sandbox guard — consistent with the documented
   loops/`cd`-compounding restriction, not the `cmp` property; worked
   around by running one `git show` per commit and by using `git -C
   <dir>` / absolute paths instead of `cd`.
2. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — the round is a same-DECISION
   implementation slice (T003c), not a defect record. Item 30's "grep
   the DEFECT before minting an id" checklist obligation therefore does
   not apply this round; stated here for completeness rather than
   silently omitted.
3. **This round has five real commits (C0a, C0b, C1, C2, C4) plus this
   handback as C5** — no C3 (no DECISION this round, per the block's
   explicit instruction not to invent one to fill the gap), and no
   split of C4 into separate production-code commits (the block itself
   states this round's code "lands in one file pair", unlike some
   prior rounds with a separate "code change 2"). Stated here per item
   30's "an extra commit, a dropped one, or a reordering is a deviation
   even when correct" instruction — this is the block's own instructed
   shape, not a departure from it.
4. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Next

**T003b2b2** (per PLAN13's Next Steps, now unblocked by T003c):
`fit_task_context_to_class_cap` + `run_pingpong` wiring at the
dispatch site, using a task's real `files_hint` as
`compiled_context_paths`, plus the `cannot_fit` → decision-escalation
chain. **Residual risk PLAN13's own Risks section names**: a task with
no `"Files:"` section still cannot engage the capped path at all —
`run_pingpong`'s `use_compiled_context` gate requires BOTH
`compiled_context_paths` and `compiled_context_candidates` non-empty,
so an empty `files_hint` (the honest default for any job task that
declares no files) still falls through to the uncapped
`build_repo_context` path. This is not a regression introduced this
round — it is the same gate DECISION F112 D5 already found — but
T003b2b2's own investigation should confirm whether that residual gap
needs its own follow-up decision or is an accepted edge case, rather
than assuming either answer before that investigation happens.

**RECORD13 (this round's own verdict) is NOT YET in the ledger** —
round 13 has not been independently re-reviewed by the reviewer yet,
so no verdict exists to book. Per amend0827-process-diet rule 1, it
books in the FIRST COMMIT of the next round that is happening anyway —
that is round 14's own C1. Before starting T003b2b2: Phase 1 rule 1 —
re-check `.agent/STOP` from disk (not present as of this round).
