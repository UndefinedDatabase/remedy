# Handoff — F260 One world · round 20 · closure part 1

## Session

SESSION 7 of feature F260 · round 20 · rounds so far 20

`.agent/STOP` did NOT exist at the base commit `a3b89f3c` (`os.path.exists` →
False), was re-checked after C4 and before this handback, and still does not
exist.

Context self-assessment (amend0905-throughput): context is comfortable — this
round is five small commits plus one real 96-second job execution, and the only
reading that needed care was the self-use record's job.json path, so nothing here
argues for ending the session.

**ALL EIGHT GATES ARE GREEN AT THEIR REAL EXIT CODES.** The consolidation took
the §3 checklist from 36 items to 35 with gaps exactly `[19, 32]`; the self-use
track was NOT exhausted — `generate_and_append_if_empty()` appended `SU-011` and
the run executed to the normal approval gate, where it BLOCKED and its own reader
returned TWO defect strings, reproduced verbatim below. NOTHING in this round
touched `docs/roadmap/STATUS.md` or `README.md`.

## Range

Review of `a3b89f3c0a3476a6850c87f591d400e7fc70ed28`..`HEAD`.

FIVE commits plus this handback. ALL FIVE are single-parent. They are EXACTLY the
bundle's ordered sequence C0a → C0b → C1 → C2 → C3 → C4, with nothing added,
dropped or reordered. Largest insertion count 346
(`.agent/authored/f260-r20.md`, a single `.agent/**` state write); nothing
approached the 500-insertion cap.

## Commits

`+/-` taken from `git log --numstat` / `git diff --numstat`, never re-derived by
eye.

### cb379af7 — f260 r20: save the round 20 block verbatim as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r20.md | +346 / -0 | C0a — `shutil.copyfile` from `.remedy-wt/f260-r20-block.md`, proved by `filecmp.cmp(shallow=False)` = True and sha256 equal to the delegation digest BEFORE staging |

### a9534863 — f260 r20: mirror the round 20 block into the last block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +285 / -175 | C0b — same source file, same `shutil.copyfile` route, same two proofs |

### f0e17dcb — f260 r20: point the plan at closure part 1
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 / -21 | C1 — whole-file replacement by the PLAN slice plus exactly one trailing newline; 1666 bytes, 36 lines, under the 50-line cap, carrying `## Goal` and `## Next Steps` |

### 7bda50f9 — f260 r20: book round 19 integration gate verdict and one reviewer prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — GATE_R19 appended by the recipe derived from this file's own measured terminal byte (exactly one newline); 969325 → 974830 bytes |
| .agent/prose_slips.md | +2 / -0 | C2 — SLIP25 appended by the same recipe from this file's own measured terminal byte; 123846 → 125380 bytes |

### 3c10561b — f260 r20: consolidate the pre-emission checklist from 36 items to 35
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +24 / -17 | C3 — the four consolidation pairs CONS1..CONS4, each applied with `str.replace(FROM, TO, 1)` after asserting FROM occurs exactly once; 92039 → 92539 bytes |

### 35144f8e — f260 r20: generate and run self-use item SU-011 for closure precondition 6
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8 / -0 | C4 — the entry `generate_and_append_if_empty()` appended; `consumed_by` is the EMPTY STRING and was NOT set this round (constraint 5) |
| .agent/selfuse_f260/SU-011.md | +7 / -0 | C4 — the generated job markdown, byte-identical to the file the runner rendered |
| .agent/selfuse_f260/run.txt | +118 / -0 | C4 — commands, JobPlan id and status, the defect strings, the budgets in force, and the raw live transcript |

## External actions

- `git push -u origin feature/f260-one-world` — the only external action.
- NO pull request was created, NOTHING was merged, there was no force-push, and
  no commit was made on `main`.
- ONE real job execution ran against a real budget: `run_next_self_use_item`,
  provider `ollama` for both roles, 96.499 s wall. It was allowed to run to its
  own completion.
- I created NO git worktree of my own. `run_job` created and RETAINED its own,
  `.remedy-wt/job-101fad068c0741f4` on branch `remedy/job-101fad068c0741f4`,
  exactly as every prior self-use run has left its own.

## Verification — one line per gate, REAL exit codes

| Gate | Exit | Evidence |
|---|---|---|
| G1 TRANSPORT | 0 | `.remedy-wt/f260-r20-block.md` (the delegation's source file), `.agent/authored/f260-r20.md` and `.agent/last_block.md` are all **26833 bytes** and all sha256 `e83dbaad265b6fe1a130f2c9b6e692d35ff3c87ae495d891f6b90273721a06c6`, equal to the digest the delegation names. Both writes were `shutil.copyfile`; `filecmp.cmp(shallow=False)` True for source-vs-authored and source-vs-mirror. Measured BEFORE staging C0a |
| G2 THE RECORD (a) | 0 | `.agent/live_review.md`: `post == pre + b"\n" + GATE_R19 + b"\n"` **True**; `post[:len(pre)] == pre` **True**; pre **969325** bytes → post **974830** bytes, delta **5505** = slice 5503 + 2. Pre terminal byte was exactly ONE newline, asserted before the write |
| G2 THE RECORD (b) | 0 | Structural, independent of (a): the WHOLE file split on a blank line, **441** units before → **442** after; N = **1** paragraph counted by the script from the slice; the last 1 unit equals the slice's 1 paragraph in order **True**. See deviation 1 — the first splitter I wrote read False for a trailing-newline reason of its own |
| G2 THE RECORD (c) | 0 | Negative control IN MEMORY on a `bytes` object: byte at offset **969366**, inside the FIRST appended paragraph, `b'T'` → `b't'` (XOR 0x20) → reader (a) REJECTS **True**, reader (b) REJECTS **True**; restored → (a) ACCEPTS **True**, (b) ACCEPTS **True**, restored image == disk image **True** |
| G2 THE SLIPS | 0 | `.agent/prose_slips.md`: `post == pre + b"\n" + SLIP25 + b"\n"` **True**; pre **123846** bytes / **155** units → post **125380** bytes / **156** units, delta **1534** = slice 1532 + 2. Pre terminal byte was exactly ONE newline, asserted before the write |
| G3 THE PLAN | 0 | `.agent/plan.md` **1666 bytes**, == PLAN slice (1665 B) + exactly one trailing newline **True**, terminal byte is exactly one newline **True**; **36 lines**, under the 50-line cap **True**; carries `## Goal` **True** and `## Next Steps` **True** |
| G4 CONS1 | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 CONS2 | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 CONS3 | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 CONS4 | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 RECONSTRUCTION | 0 | `docs/agents/planner_reviewer_prompt.md` rebuilt INDEPENDENTLY from its pre-edit bytes (`git show HEAD:<path>` at C2) with ONLY those four pairs applied, in a second script: equals the disk image **True**. Byte count before **92039**, after **92539**; the file still ends with exactly one newline **True** |
| G5 THE LIST | 0 | Items counted mechanically as lines matching `^  \d+\. \*\*` between the line beginning `  1. **Size.**` (line 244) and the line beginning `  Why this is on disk and not a habit` (line 996). Numbers: `[1..18, 20..31, 33..37]`. Count **35** — required 35 **True**. Sorted gaps in `range(1, 38)`: **`[19, 32]`** — required `[19, 32]` **True** |
| G5 PROVENANCE | 0 | `item 19` occurs **3** times, exactly the three the reviewer's simulation predicted, all provenance and none live: L232 `  Consolidated again at F260's closure on 2026-09-06: item 19 was merged into item`; L241 ``  references across the record and its archive and the prose slips, and `item 19` ``; L807 `      commit writing that text. THE SLICE HALF, formerly item 19 and finding R-0515:`. Lines matching `^  19\. \*\*` anywhere in the file: **0** — the item itself is gone |
| G6 THE SELF-USE ITEM | 0 | Full transcript in its own section below. `next_self_use_item()` BEFORE = **None**; `generate_and_append_if_empty()` appended **SU-011**; queue entries **10 → 11**; empty-`consumed_by` count **0 → 1**; runner returned SU-011, JobPlan `101fad068c0741f4`, status **blocked**; `describe_self_use_run_defects` returned a **2-tuple**, NOT empty |
| G7 tests/docs | 0 | `python3 -m pytest tests/docs/ -q -p no:randomly` → **303 passed in 0.49s**; `^FAILED` lines **0**, `^ERROR` lines **0** |
| G7 test_self_use_generator | 0 | `python3 -m pytest tests/orchestration/test_self_use_generator.py -q -p no:randomly` → **20 passed in 0.25s**; `^FAILED` **0**, `^ERROR` **0** |
| G7 test_golden_path | 0 | `python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly` → **42 passed in 21.08s**; `^FAILED` **0**, `^ERROR` **0** |
| G7 integrity check | 0 | `python3 -m apps.cli.grouped integrity check --json` → returncode **0**, `"passed": true`, `"fail_count": 0`, `check_count` present, failing checks **[]** |
| G8 TREE | 0 | `git status --porcelain` **EMPTY**; `git ls-files .remedy-wt` **EMPTY**; `git worktree list` = **13 rows** — the primary plus **12** `remedy/job-*` rows, being the 11 pre-existing ones and the one this round's own self-use run retained. `git branch --list "tmp/*"` EMPTY |
| G8 STRUCTURE | 0 | C0a `cb379af7` 1 parent, **+346**; C0b `a9534863` 1 parent, **+285**; C1 `f0e17dcb` 1 parent, **+20**; C2 `7bda50f9` 1 parent, **+4**; C3 `3c10561b` 1 parent, **+24**; C4 `35144f8e` 1 parent, **+133**. Insertions only — the `+` column of `git diff --numstat`, never insertions plus deletions. Every count under 500 |
| G8 LINT HALF | n/a | `git diff --name-only a3b89f3c..C4` lists **9** files and **0** of them end `.py`. The lint half is NOT APPLICABLE; no target was invented |

## The COMPLETE self-use transcript (G6)

Order as the block requires it.

1. **`next_self_use_item()` BEFORE the generator** → `None`. The queue held **10**
   entries (`SU-001`..`SU-010`), every one with a non-empty `consumed_by`; entries
   with an empty `consumed_by`: **0**. Queue sha256 before:
   `d245816f1730e18463c047a8dab43e0d249b18ef9d5de9e8523086df67d3ee5c`.
2. **`generate_and_append_if_empty()` appended one entry**:
   - id: `SU-011`
   - title: `Address ledger finding R-0419`
   - provenance: `generated (self-use-generator tier 1, ledger scan, R-0419)`
   - `consumed_by`: `''` — the EMPTY STRING, and it was NOT set this round
     (constraint 5; precondition 6 wants that edit in the closure commit).
   Queue entries **10 → 11**; entries with an empty `consumed_by` **0 → 1**
   (`['SU-011']`). Queue sha256 after:
   `2ab2db3c101d1703edb0ea706c2c2f46e46f167baa176e115ebbca3b32c459fd`.
   `next_self_use_item()` then answered `SU-011`, so the track is NOT exhausted
   and `self-use NONE (queue exhausted)` is NOT the reading here.
3. **The run.**
   `run_next_self_use_item(Path('.remedy-wt/selfuse-f260-run'), repo_path='.')`,
   with `max_provider_calls`, `max_cost_usd` and `max_tasks` left at the
   function's own defaults. No `builder_name`/`reviewer_name`/provider/queue_path
   override was passed.
   - returned entry id: `SU-011`
   - job file path: `.remedy-wt/selfuse-f260-run/SU-011.md` (2009 bytes, sha256
     `29fa81063d19edf8b9daee627682709ccd1f9d9b86a0b77aa4acdb71dc4691ad`, equal to
     the `job_file_sha256` the persisted plan records)
   - JobPlan id: `101fad068c0741f4`
   - JobPlan status: **`blocked`**
   - plan error: `task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`
   - budgets in force: `max_provider_calls=6`, `max_cost_usd=0.5`,
     `max_total_tokens=None`, `max_wall_clock_minutes=None`, `deadline=None`,
     `max_tasks=1`; `budget_actuals` is `None`
   - providers: builder `ollama` (source `cli`), reviewer `ollama` (source `cli`),
     both models blank with source `default`
   - one task: `T001 "Task 1"` — `final_status=repair_exhausted`,
     `reviewer_verdict=fail`, `status=blocked`, `test_passed=None`,
     `repair_rounds_used=2 of 2`
   - wall clock **96.499 s** (start epoch 1788690955.444, end 1788691051.942)
   - the job's own retained worktree: `.remedy-wt/job-101fad068c0741f4` on branch
     `remedy/job-101fad068c0741f4`, base and head `3c10561b`, cleanup status
     `retained`, `result.diff` **0 bytes** — nothing was applied anywhere.
4. **`describe_self_use_run_defects(plan)` returned a tuple of length 2, NOT an
   empty tuple.** Both strings VERBATIM, COMPLETE and IN ORDER:

```
job 101fad068c0741f4 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail
T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail
```

   Python repr, untruncated:
   `('job 101fad068c0741f4 (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail', 'T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail')`

   NO R-id was minted and NO `Done:`/`Landed:` paragraph was authored for them —
   constraint 4. The reviewer authors the findings; precondition 6 requires that
   registration before the close.
5. **`.agent/selfuse_f260/` listing**: `SU-011.md` **2009 bytes**, `run.txt`
   **10778 bytes**. `SU-011.md` is byte-identical to the rendered job file
   (`filecmp.cmp(shallow=False)` True).

## Authored-text proofs

- **Transport is a COPY chain, never a retype.** `.remedy-wt/f260-r20-block.md`
  (the delegation's source file on disk), `.agent/authored/f260-r20.md` and
  `.agent/last_block.md` all hash to
  `e83dbaad265b6fe1a130f2c9b6e692d35ff3c87ae495d891f6b90273721a06c6` at 26833
  bytes. Both writes went through `shutil.copyfile` and each was proved with
  `filecmp.cmp(shallow=False)` = True before staging. The digest was verified
  against the delegation's stated value BEFORE the block was executed at all.
- **Every slice was extracted from the COMMITTED authored copy** after C0a, never
  from the delegation message and never retyped. The extractor matches lines
  EXACTLY equal to `<<<BEGIN name>>>` / `<<<END name>>>` by POSITION and asserts
  exactly one of each, which matters here because `<<<END PLAN>>>` is immediately
  followed by `<<<BEGIN GATE_R19>>>` with no blank line between them.
- **Slice sizes**: CONS1_FROM 999 B / 12 lines, CONS1_TO 84 B / 1 line;
  CONS2_FROM 161 B / 2 lines, CONS2_TO 1141 B / 14 lines; CONS3_FROM 643 B /
  8 lines, CONS3_TO 1078 B / 14 lines; CONS4_FROM 87 B / 1 line, CONS4_TO 87 B /
  1 line; PLAN 1665 B / 36 lines; GATE_R19 5503 B / 1 line / 1 paragraph;
  SLIP25 1532 B / 1 line / 1 paragraph.
- **ZERO marker lines reached any written file**: `.agent/plan.md`,
  `.agent/live_review.md`, `.agent/prose_slips.md`,
  `docs/agents/planner_reviewer_prompt.md`, `.agent/selfuse_f260/run.txt` and
  `.agent/selfuse_f260/SU-011.md` each contain **0** lines beginning
  `<<<BEGIN ` or `<<<END `.
- **Each append recipe was derived from its OWN target's measured terminal byte**,
  with the `assert` executed BEFORE the write, as constraint 2 orders. The
  block's two measurements reproduced EXACTLY: `.agent/live_review.md` 969325 B
  and `.agent/prose_slips.md` 123846 B, each with exactly ONE terminal newline.
- **Blank-line unit definition**, stated so the reviewer can reproduce it: the
  WHOLE file image split on the regex `\n[ \t]*\n`, empty units dropped, each
  surviving unit stripped of leading and trailing newlines. Under that definition
  `.agent/live_review.md` reads **441 → 442** and `.agent/prose_slips.md` reads
  **155 → 156**.
- **Constraint 4 upheld — no `Done:` or `Landed:` paragraph was authored and no
  R-id was minted.** The appended region of `.agent/live_review.md` contains ZERO
  lines beginning `Done:` or `Landed:`. Whole-file line-anchored census after C2:
  `^Gate: ` **29** (28 before), `^Gate: R19 — ` exactly **1**, registrations
  `^- R-dddd` **301** over **301** distinct ids, `^Done: ` **5** lines over **3**
  distinct ids (`R-0721`, `R-0725`, `R-0814`).
- **Constraint 5 upheld — `consumed_by` was NOT set.** The appended queue entry
  carries `"consumed_by": ""`, and the only queue diff is the appended entry
  (+8 / -0); no existing entry was touched.

## Deviations & assumptions

**1 — MY FIRST G2 (b) SPLITTER READ FALSE, FOR A REASON IN THE SPLITTER, NOT IN
THE FILE.** The first version split the image on a blank line but did not
normalise each unit's surrounding newlines, so the file's LAST unit carried the
file's own terminal newline while the slice's single paragraph did not; the
comparison read `False`. Reader (a), which is byte-exact, read `True` on the same
image, which is what identified the fault as the reader's. I changed the READER,
never the file and never the slice: units are now stripped of leading and
trailing newlines. The corrected reader was then re-run against the on-disk image
with `pre` re-read from `git show HEAD:.agent/live_review.md` — not from memory —
and reads **True**, and the negative control still REJECTS the one-byte mutation
in both readers. Nothing was adjusted to make a reading come out as ordered.

**2 — CONS2_TO CONTAINS A PHRASE I BELIEVE IS WRONG, AND I APPLIED IT BYTE FOR
BYTE ANYWAY.** The slice reads "This item absorbed former item 32-neighbour ITEM
19 at F260's closure on 2026-09-06". Item 19 was not a neighbour of item 32:
item 32 is the number F259's pass retired when it merged 32 into 16, and item 19
sat between items 18 and 20. Constraint 1 says apply as written and declare, so
the text on disk is the slice's exact bytes and this is the declaration. The
reviewer may want a follow-up pair; I did not author one.

**3 — F259's PRECEDENT RECORD NAMES A JOB PATH THIS REPOSITORY NO LONGER USES.**
`.agent/selfuse_f259/run.txt` cites `.data/task_jobs/1cbb6972bf7c4ffc/job.json`.
No such directory exists here: `packages.orchestration.data_paths.job_record_path`
resolves this round's plan to `.data/jobs/101fad068c0741f4/job.json`, which does
exist and whose `job_file_sha256` matches the rendered job file. My first draft of
`run.txt` inherited the stale path, printed `exists: False`, and I repaired it by
calling the product's own resolver instead of guessing a path — the record on
disk was rewritten before C4 was staged. Reported because it means the F259 record
carries a path that no longer resolves; repairing that file was outside this
round's change set, so I did not touch it.

**4 — THE SELF-USE RUN BLOCKED. IT IS REPORTED, NOT HIDDEN, AND IT DID NOT
RAISE.** `run_next_self_use_item` returned normally; the `JobPlan` came back with
status `blocked` after both repair rounds were used and the reviewer verdict was
`fail`. Per the runner's own docstring that is an ordinary outcome of the normal
approval gate, not an exception path — `SelfUseRunError` is reserved for planning
that blocked before any task ran, and it was not raised. So C4 WAS committed, as
the block orders for a completed run. The two defect strings are above, verbatim
and complete. This is the same outcome shape as F259's SU-010 run.

**5 — THE JOB RETAINED ITS OWN WORKTREE; I CREATED NONE.** `run_job` created
`.remedy-wt/job-101fad068c0741f4` on branch `remedy/job-101fad068c0741f4` with
`cleanup_status=retained`, exactly as the eleven pre-existing `remedy/job-*`
worktrees were left by prior runs. I removed nothing by glob and created no
worktree of my own, so there was nothing of mine to remove by exact path.
`git worktree list` is **13 rows**: primary + 12 `remedy/job-*`.

**6 — THE RUN WROTE RUNTIME STATE OUTSIDE THE CHANGE SET, ALL OF IT IGNORED.**
`.data/jobs/101fad068c0741f4/`, `.data/runs/101fad068c0741f4/` and
`.remedy-wt/selfuse-f260-run/` were written by the job itself.
`git check-ignore -v` resolves them to `.gitignore:211 .data/` and
`.gitignore:235 .remedy-wt/`; `git status --porcelain` is EMPTY, so no path
outside the block's change set was COMMITTED.

**7 — SANDBOX SUBSTITUTIONS, AS THE BLOCK PRESCRIBES.** `cmp` was replaced by
`filecmp.cmp(shallow=False)` plus sha256; the `remedy` binary by
`python3 -m apps.cli.grouped`; every exit code was read from
`subprocess.run(...).returncode`; no environment assignment was written on a
command line. Helper scripts live under the gitignored `.remedy-wt/f260r20/` and
NONE was `git add`ed — `git ls-files .remedy-wt` is EMPTY.

**8 — CONSTRAINT 8 UPHELD.** This handback's own commit is tabled nowhere and its
numbers are reported nowhere. No pull request was created, nothing was merged,
there was no force-push, and no commit was made on `main`.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a `.agent/authored/f260-r20.md` | done | |
| C0b `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` | done | |
| C2 `.agent/live_review.md` + `.agent/prose_slips.md` | done | one commit, that file order |
| C3 `docs/agents/planner_reviewer_prompt.md` | done | all four pairs |
| C4 self-use item | done | the run BLOCKED but completed and did not raise — deviation 4 |
| C5 `.agent/handoff.md` | done | this file; its own numbers are reported nowhere, per constraint 8 |
| G1 TRANSPORT | done | exit 0 |
| G2 THE RECORD | deviated | exit 0 on all four readings AS REPORTED, but reader (b) needed its own splitter corrected first — deviation 1 |
| G3 THE PLAN | done | exit 0 |
| G4 THE CONSOLIDATION | done | exit 0; four numbers per pair plus the independent reconstruction |
| G5 THE LIST | done | exit 0; count 35, gaps `[19, 32]`, `item 19` provenance 3, live `^  19\. \*\*` 0 |
| G6 THE SELF-USE ITEM | done | exit 0; the runner did not raise; two defect strings reported verbatim |
| G7 THE SUITES | done | exit 0 on all four, run serially in the primary checkout after C4 |
| G8 TREE AND STRUCTURE | done | exit 0; lint half NOT APPLICABLE, 0 `.py` files in the range |

## Open findings

**298 OPEN BY DISTINCT ID**, unchanged by this round, which is correct: this
round registers nothing and resolves nothing. Census over `.agent/live_review.md`
after C2 — registrations **301** over 301 distinct ids, `^Done: ` **5** lines
over **3** distinct ids, 301 − 3 = **298**.

TWO DEFECT STRINGS from the self-use run are AWAITING THE REVIEWER'S
REGISTRATION. They are reproduced verbatim in the G6 section above and in
`.agent/selfuse_f260/run.txt`. Closure precondition 6 requires each to be
registered as a normal R-id finding — or shown to be evidence for an already-open
one — BEFORE the close, and the closure paragraph must name every finding raised
and whether it was repaired. A worker-authored finding would itself be a finding,
so I authored none.

## Next

Awaiting the reviewer's independent re-run and verdict on round 20. Per the plan:

1. Closure part 2 — register the two self-use defect strings FIRST (or attach
   them to an open id), then the evidence job, the review zip, and the ledger
   rotation by `scripts/rotate_live_review.py`, which re-baselines the byte
   arithmetic of every later block.
2. Closure part 3 — the STATUS accepted flip, the README sync, `consumed_by` set
   to `F260` on `SU-011`, the handback, and the pull request, left UNMERGED as the
   operator's review window.

Two items may want a ruling before part 2: the CONS2_TO wording of deviation 2,
and the stale job path in `.agent/selfuse_f259/run.txt` of deviation 3. Neither
blocks the closure and both were outside this round's change set.
