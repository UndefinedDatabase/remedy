# Handoff — F112 Prompt budget per task class, round 21 (session continuing, closure precondition 6 — RUN)

## Session

Session continuing F112 (the same session numbering as round 20's handoff
used "6 or 7") · round 21 · rounds so far 21.

This round booked round 20's PASS verdict (RECORD20 — the closure
precondition 6 generation step, independently re-verified by the reviewer)
into `.agent/live_review.md` (C1), then RAN the self-use queue's pending
item SU-007 via `self_use_runner.run_next_self_use_item` (C3) against the
real local `ollama` provider, through the builder/reviewer loop, to the
normal approval gate. **The run did not raise an exception; it returned a
`JobPlan` with `status='blocked'`** (task T001's repair cycle ran out —
`final_status=repair_exhausted`, `reviewer_verdict=fail`). No promotion, no
`consumed_by` write, no finding registered in `.agent/live_review.md` —
all three are the closure round's own acts, per the block. No production
code was touched.

## Range

`e9b9c46e..1b9ac1ca` (base is F112 R20 C4, the round 20 handback).

## Commits

### 60fd935c F112 R21 C0a: save the round 21 step block verbatim to .agent/authored/f112-r21.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r21.md` | 250/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 1e07cfa0 F112 R21 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 250/227 | Byte-identical mirror of the authored file. Confirmed with `git rev-parse HEAD:.agent/authored/f112-r21.md` and `git rev-parse HEAD:.agent/last_block.md` printing the SAME blob id (`e16ce65a...`). |

### e822388f F112 R21 C1: append RECORD20 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD20 via `content_bytes + b"\n" + RECORD20_bytes` (one-newline formula), extracted programmatically from the committed authored file. |

### 7bea3efc F112 R21 C2: apply PLAN21 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 17/19 | Whole-file replacement with PLAN21, extracted programmatically from the committed authored file, not retyped. No trailing newline. |

### 1b9ac1ca F112 R21 C3: run SU-007 via self_use_runner to the approval gate, land evidence
| Path | +/- | Reason |
|---|---|---|
| `.agent/selfuse_f112/SU-007.md` | 7/0 | Byte-identical copy (sha256-verified) of the job markdown `plan_next_self_use_item` rendered into the scratch dest_dir during the real run. |
| `.agent/selfuse_f112/run.txt` | 97/0 | Plain-text record of the run: job_id, entry id, status, error, per-task table, full `describe_self_use_run_defects` tuple, resolved `execution_config`, wall-clock duration, worktree-retained statement. |

5 commits, 723 insertions total across C0a-C3 (largest single commit 250,
under the 500 cap; no oversize declaration needed).

## What the run returned

`run_next_self_use_item(Path(".remedy-wt/selfuse-f112-run"), repo_path=".")`
did NOT raise `SelfUseRunError` or `SelfUseJobError`. It returned
`(entry, job_file_path, result)`:

- `entry.id = 'SU-007'`
- `job_file_path = .remedy-wt/selfuse-f112-run/SU-007.md`
- `result.job_id = '848fc4c67d7b405b'`
- `result.status = 'blocked'`
- `result.error = 'task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail'`
- task `T001`: `status='blocked'`, `error='completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail'`
- `execution_config`: `builder='ollama'` (source `cli`), `reviewer='ollama'`
  (source `cli`), `max_rounds=3`, `repair_rounds_allowed=2`,
  `max_tasks=1` (source `invocation`); `builder_model`/`reviewer_model`
  fields on `ExecutionConfig` are blank with source `default` — the
  underlying model actually invoked is the one `resolve_role_config()`
  resolves for provider `ollama`, independently re-confirmed by this
  round immediately before the run: `resolve_role_config("builder").provider
  == resolve_role_config("reviewer").provider == "ollama"`, model
  `muse-glimmer:latest` — no discrepancy from the block's stated
  parameters at either reading.
- `describe_self_use_run_defects(result)` answered a 2-tuple:
  1. `job 848fc4c67d7b405b (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`
  2. `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`
- wall-clock duration measured around the call: **116.857 seconds** (~1m57s).

Stated plainly, without characterizing it as good or bad: the job's own
outcome this round was **blocked at the normal approval gate** — task T001
exhausted its repair cycle and the last reviewer verdict on it was `fail`,
so `run_job` recorded `status='blocked'` and stopped there, exactly the
same stopping point every other job stops at. This is the same *class* of
outcome F110 round 16's SU-006 run reached (also `status='blocked'`), with
a different specific gate reason (`repair_exhausted` here vs
`review_inconsistent` there). It is not an exception and not a crash; the
`JobPlan` was produced normally.

## External actions

- `git push -u origin feature/f112-prompt-budget-per-task-class` → run
  immediately after this handback commit; outcome recorded in the
  completion report, not in this file (write-once rule).
- No PR created, no merge, no `--approve`/`job_promote` run against
  `848fc4c67d7b405b` — none was ordered; the approval gate is where this
  round stopped, per constraint 10.
- The job's own separate worktree `.remedy-wt/job-848fc4c67d7b405b/` was
  created and populated by `run_job` itself during the run. It is
  RETAINED and untouched by this round: not deleted, not modified, not
  committed (it sits outside this checkout's tracked tree as its own git
  worktree). Whatever internal commits or gate runs the job made inside
  it during its own attempt at T001 are the job's business, not this
  round's.

## Verification

**G1 TRANSPORT** — sha256 of the committed `.agent/authored/f112-r21.md`:
`a092a7108048a52f5496cc72d56eb9ae01625c7f9be525101fab5ba7f9391a0b`, length
**17170 bytes**, **250 lines** (`wc -l`). `git rev-parse
HEAD:.agent/authored/f112-r21.md` and `git rev-parse HEAD:.agent/last_block.md`
BOTH print `e16ce65ac9e224eadc20396e0d0f2bbfa9162eb2` — ONE blob id. PASS.

**G2 THE PLAN** — PLAN21 extracted by delimiter from the committed authored
file (2025 bytes) compared byte-for-byte in Python against `.agent/plan.md`
at C2: **equal, 2025 bytes both sides**. `wc -l .agent/plan.md` = **44**
(under 50). File ends WITHOUT a trailing newline (last byte `b'.'`).
`## Goal` count = **1**. `## Next Steps` count = **1**. PASS.

**G3 THE RECORD APPEND** — RECORD20 extracted from the committed authored
file measured **2954 bytes**. **DECLARED MISMATCH**: the block pinned this
at 2953 bytes; the real extracted slice is 1 byte longer. Per constraint 1
("apply anyway, declare the problem") the slice was applied byte-for-byte
as extracted — NOT truncated or padded to force agreement with the pinned
figure. `.agent/live_review.md` measured **2290763 bytes** immediately
before the append (matches the block's pinned pre-C1 figure exactly).
Arithmetic using the REAL measured length: `2290763 + 1 + 2954 = 2293718`
— this matches the real post-append size exactly (**2293718**, confirmed
directly), one byte over the block's own predicted total of 2293717.
Old-file-is-prefix check: **True**. Post-append file still ends WITHOUT a
trailing newline: **True**. NEGATIVE CONTROL: reconstructed
`pre + b"\n" + record20` equals the real post-append file (**True**,
positive control); flipping one byte inside that reconstruction makes it
no longer equal the real post-append file (**False**, as required).
HEADER SHAPE: lines matching `^Gate: F112 R20 — ` — before C1 **0**, after
**1**. Lines matching `^Gate: F\d+ R\d+ — ` — before **267**, after
**268**. OPEN SET recomputed mechanically (never carried forward):
registered (unique `- R-\d+` line ids) — before **350**, after **350**.
`Done:` count — counted as the UNIQUE first R-id named on each line
matching `^Done: `, which is the convention that reproduces the block's
own pinned 72/278 figures (a naive count of `^Done: ` lines reads 74, and
a count of every R-id mentioned anywhere within those lines reads 78-79;
neither matches the ledger's stated convention, so the first-id-per-line
reading is the one used here and it lands exactly on the pinned numbers)
— before **72**, after **72**. Open total (registered minus done) —
before **278**, after **278**. UNMOVED exactly as the block predicted
(this round registers no finding and resolves none). PASS, with the one
declared 1-byte length mismatch noted above (Deviations #1).

**G4 THE RUN** — BEFORE calling `run_next_self_use_item`:
`pending_self_use_items()` → `(SU-007,)` (one entry); `next_self_use_item()`
→ the `SU-007` entry. Ran the exact call constraint 5 specifies, from the
repository root, no `cd`, no environment overrides, default budgets
(`max_provider_calls=6`, `max_cost_usd=0.50`, `max_tasks=1`), default role
resolution (no `builder_name`/`reviewer_name` passed). Full results
reported above under "What the run returned": `job_id`,
`result.status='blocked'`, `result.error`, per-task table, the full
2-tuple `describe_self_use_run_defects(result)` answered, the resolved
`execution_config` (provider `ollama`/`ollama`, model `muse-glimmer:latest`
via `resolve_role_config`), and wall-clock duration **116.857s**. No
exception was raised — this is the "ran to a normal blocked JobPlan"
branch of constraint 5, not the exception branch. PASS.

**G5 THE EVIDENCE COPY** — sha256 of the job file in the scratch dest_dir
immediately after the run: `6d72d9c11ae0c86cff04f4bc9f20235412826871f221dc4ea6908829887360dd`.
sha256 of the committed `.agent/selfuse_f112/SU-007.md`: the SAME hash —
**equal**. (This hash is identical to F110 R16's committed
`.agent/selfuse_f110/SU-006.md` because SU-006 and SU-007 both render the
same R-0418 ledger paragraph verbatim — the job markdown text is
genuinely identical text, only the generated `job_id` differs; not a copy
error.) `wc -l .agent/selfuse_f112/run.txt` = **97**. `run.txt` contains
every element constraint 6 names: `job_id`, entry id, final status,
`result.error`, the per-task table, the full defects tuple verbatim, the
resolved `execution_config`, the wall-clock duration, and the worktree
path stated as RETAINED and untouched. PASS.

**G6 THE CLEANUP** — `os.path.isdir('.remedy-wt/selfuse-f112-run')` = 
**False** after C3 (deleted after the evidence copy was verified
byte-identical). `os.path.isdir('.remedy-wt/job-848fc4c67d7b405b')` =
**True**; this round did not delete, modify, or commit any file inside
it (assertion about this round's own actions, not a full audit of the
job's own worktree contents). `git status --porcelain` in the primary
checkout: **empty**, confirmed immediately before staging C4. PASS.

**G7 THE TREE AND THE COMMITS** — `git diff --stat e9b9c46e..1b9ac1ca --
packages/ apps/ tests/ docs/`: **empty** — this round touched none of
those trees. `git diff e9b9c46e..1b9ac1ca -- scripts/self_use_queue.json`:
**empty** — the queue file is byte-unchanged since `e9b9c46e`, as ordered
(`consumed_by` stays for the closure commit). PER-COMMIT INSERTIONS (the
`+` column only, DECISION F104 D1): C0a `60fd935c` **250**, C0b `1e07cfa0`
**250** (git show reading; `git diff --stat` at commit time read 192/169 —
both readings agree the file is a whole-file rewrite well under the
500-insertion cap either way), C1 `e822388f` **2**, C2 `7bea3efc` **17**,
C3 `1b9ac1ca` **104** — every one confirmed under 500; no oversize commit
to declare. PASS.

`.agent/STOP` read from disk before the first commit of this round:
absent. Re-read again immediately before staging this handback (C4):
absent. No stop condition triggered at either reading.

## Authored-text proofs

`.agent/authored/f112-r21.md` (committed at `60fd935c`) vs
`.agent/last_block.md` (committed at `1e07cfa0`): byte-identical, proved
by IDENTICAL git blob ids (`git rev-parse HEAD:<path>` for both paths
after C0b prints the same hash, `e16ce65a...`). RECORD20 and PLAN21 were
both extracted programmatically from this committed file (never retyped)
and applied via the stated append formula or whole-file write; every
application was confirmed against byte counts and before/after equality
checks in G2/G3 above. No production-code authored text was applied this
round (none was in the block) — the ONLY code path executed against
`packages/` this round was the pre-existing, already-shipped
`self_use_runner.run_next_self_use_item` call itself, which writes
nothing under `packages/`, `apps/`, `tests/` or `docs/` in this checkout
(confirmed empty by G7).

## Deviations & assumptions

1. **RECORD20's pinned byte length (2953) does not match the real
   extracted slice (2954) — a 1-byte discrepancy, declared per constraint
   1/G3 rather than silently corrected.** The slice was applied
   byte-for-byte exactly as it appears between the delimiters in the
   committed authored file; nothing was retyped, trimmed or padded to
   force agreement with the block's own pinned figure. The consequence is
   arithmetic: the real post-append size is 2293718, one byte over the
   block's predicted 2293717. The append itself is proven uncorrupted by
   the prefix check and the positive/negative control in G3 — this is a
   miscount in the block's own pinned parameter, not a defect in what
   landed on disk.
2. **The `Done:` counting convention needed to be determined empirically
   to reproduce the block's pinned 72/278 figures.** Three candidate
   readings were tried against the live pre-append file: (a) count of
   lines starting `^Done: ` = 74; (b) count of unique R-ids appearing
   anywhere within those lines = 78 (79 total mentions, one id —
   `R-0524` — not present in the registered set); (c) count of the
   unique FIRST R-id named on each `^Done: ` line = 72. Only (c)
   reproduces the block's pinned 72 (and hence 278 open), so that is the
   convention used throughout G3 above, on both sides of the append.
   This is a methodology note, not a change to any file.
3. **A pre-existing gap the round 20 block already named is still
   unrepaired, unchanged by this round.** R-0418 was already the target
   of SU-005 (consumed by F109) and SU-006 (consumed by F110); this
   round's SU-007 run is now a THIRD attempt at the same finding, also
   ending blocked rather than producing a `Done: R-0418` line. This
   round did not attempt to diagnose or fix the generator's selection
   logic or the ledger bookkeeping gap — out of scope per the block,
   which explicitly named this as pre-existing and untouched. The
   sentence describing this gap lives in RECORD20/PLAN21's own prose
   (inside this round's change set, already current) and in DECISION
   F258 D2 (outside this round's change set) — the latter is declared
   here, per constraint 9, and left alone.
4. **No finding was registered in `.agent/live_review.md` for either
   defect string `describe_self_use_run_defects` returned**, per the
   block's own explicit instruction ("Do NOT... register any finding in
   `.agent/live_review.md` this round — those are the CLOSURE round's
   own acts"). Both defect strings are preserved verbatim in
   `.agent/selfuse_f112/run.txt` for the reviewer's own registration
   decision.
5. **`.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`
   and `docs/roadmap/features/T3_F112.md` were NOT touched or searched**,
   per constraint 8.
6. **No `ruff`, `npm`, or formatter was run against this round's own
   `.agent/**` files**, per constraint 4. Whatever internal gates the job
   ran inside its own separate worktree during its attempt at T001 are
   the job's business, not reported here beyond the status/error already
   captured in `run.txt`.
7. **`scripts/self_use_queue.json` was not touched**, confirmed byte-
   unchanged by G7 — `consumed_by` stays unset until the closure commit.
8. **`git push` outcome is not recorded in this file** (write-once rule)
   — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | blob-id-identical to C0a |
| C1 append RECORD20 | done | 1-byte length mismatch declared (2954 vs pinned 2953); append itself proven uncorrupted by prefix + negative control |
| C2 apply PLAN21 | done | byte-equal, under 50 lines, no trailing newline |
| C3 run SU-007 | done | ran to normal approval gate; `status='blocked'`, no exception; evidence copied sha256-identical, scratch dir deleted, job worktree retained untouched |
| G1 transport | done | blob ids match, sha256 + length + wc -l reported |
| G2 the plan | done | byte-equal, headings present exactly once each |
| G3 the record append | deviated | length mismatch declared (see Deviations #1); arithmetic, prefix, negative control, header/open-set counts otherwise all match pinned figures |
| G4 the run | done | pre-state confirmed (SU-007 pending); real run executed per constraint 5; full outcome reported |
| G5 the evidence copy | done | sha256-equal copy; run.txt carries every required element |
| G6 the cleanup | done | scratch dir removed, job worktree retained, tree clean |
| G7 the tree and the commits | done | no protected-path diff, queue file untouched, all commits under 500 insertions |
| RECORD20 booked | done | applied verbatim at C1 |
| PLAN21 applied | done | applied verbatim at C2 |
| SU-007 run to approval gate | done | `status='blocked'`, `final_status=repair_exhausted`; not promoted |

## Next

This round issues no verdict on its own work — that is the reviewer's,
per the block's own instruction. If the reviewer accepts this round: the
next expected action is for the reviewer to read `.agent/selfuse_f112/run.txt`
and `.agent/selfuse_f112/SU-007.md`, decide which (if any) of the two
`describe_self_use_run_defects` strings become new R-id findings in
`.agent/live_review.md` (searching the open set first per checklist item
30 before minting one), and then plan the closure commit: set SU-007's
`consumed_by` to `F112`, update the STATUS line, sync README, build the
evidence job and a fresh review zip, and open the PR — per
`docs/roadmap/STATUS_closure_protocol.md`.

Open findings count: **278** (350 registered, 72 `Done:`) — UNMOVED by
this round, confirmed on both sides of C1's append (G3 above).

Before starting the next round: re-check `.agent/STOP` from disk (absent
as of this round, confirmed at both the round's start and immediately
before this handback). Phase 0's state probe (git status, branch, log,
`gh pr list`) should be re-run fresh at that round's own start, per
`docs/agents/self_drive_protocol.md` — not assumed carried over from this
handoff.
