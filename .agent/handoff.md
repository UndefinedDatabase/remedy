# Handoff — F257 self-use track, round 8 (closure precondition 6)

## Session

SESSION 3 of feature F257 · round 8 · rounds so far 8

Roster of this session's rounds, this round included: R8. Session 2 ran R4–R7 and
ended at `ba28d224`; this session opens with this round.

## Range

Review of `ba28d224..HEAD` (HEAD = the C4 commit that writes this file).

## Commits

### 03cea660 chore(f257): save the round 8 block verbatim — C0a

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r8.md` | +285/-0 | the block saved verbatim by `shutil.copyfile` from `.remedy-wt/f257-r8-block.md` |

### c0617c11 chore(f257): mirror the round 8 block to last_block — C0b

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +167/-222 | the same bytes mirrored; one blob id with the authored copy |

### 61338424 docs(f257): advance the plan to the self-use run round — C1

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +10/-8 | whole-file replacement by slice `PLANF257R8` |

### 6c9fd816 docs(f257): book the round 7 gate verdict — C2

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +8/-0 | slice `GATEF257R7` appended under constraint 6. No id registered, none resolved |

### 61cdc6fa docs(f257): plan self-use item SU-001 and record the transcript — C3

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/selfuse_f257/SU-001.md` | +22/-0 | the job file the SHIPPED renderer wrote, copied out of the gitignored run directory by `shutil.copyfile` |
| `.agent/selfuse_f257/run.txt` | +69/-0 | the full untruncated run transcript, every path relative to the repository root |

### C4 — this handoff commit

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | the round handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above was taken from `git diff --numstat` per commit.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, REAL exit 0.
- `git push origin feature/f257-self-use-track` → outcome recorded in the session output.
- No pull request was created. Nothing was merged. No force-push, no history
  rewrite, no branch created. No worktree was added or removed this round.

## Verification

One line per gate, with the result actually measured.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk with `os.path.exists` twice:
  before C0a **False**, before C3 **False**. Constraint 0: `gh pr list …` printed
  `[]` at REAL exit 0; `git rev-parse HEAD` printed
  `ba28d2249bd7b2ce0baed73fc2f42b141a5f32de`, which equals `ba28d224`'s full sha;
  `git branch --show-current` printed `feature/f257-self-use-track`.
  `git status --porcelain | wc -l` after each commit: C0a **0**, C0b **0**,
  C1 **0**, C2 **0**, C3 **0**.
- **G2 TRANSPORT — PASS.** Committed blob `03cea660:.agent/authored/f257-r8.md`
  sha256 `36200f7b15600f1f702c2f3add880fd97318b33ed61eea367cd5fba7f4d360e7`,
  **19141 bytes**; the reviewer's own original `.remedy-wt/f257-r8-block.md`
  sha256 `36200f7b15600f1f702c2f3add880fd97318b33ed61eea367cd5fba7f4d360e7`,
  **19141 bytes**; **EQUAL True**. That original was written before this worker
  existed, so the reading covers more than self-consistency; and it covers no
  emission, because this workflow has none — the block was never retyped, only
  copied by `shutil.copyfile`. `git rev-parse c0617c11:.agent/authored/f257-r8.md`
  and `git rev-parse c0617c11:.agent/last_block.md` print ONE blob id,
  `2c252c39ab88b3f9dfb3fb6723490ab8bb78c727`.
- **G3 THE PLAN AT C1 — PASS.** `.agent/plan.md` at C1 equals `PLANF257R8`
  including the trailing newline: **True**, **2107 bytes** on both sides. `wc -l`
  **42**, under 50 **True**. Lines exactly `## Goal`: **1**. Lines exactly
  `## Next Steps`: **1**.
- **G4 THE RECORD APPEND AT C2 — PASS.** `.agent/live_review.md` reconstructed
  from the `ba28d224` blob plus `GATEF257R7` under constraint 6: **True**; pre
  **1402722** bytes, slice **3178** bytes, reconstruction **1405901**, C2 blob
  **1405901**. NEGATIVE CONTROL: the script flipped one byte at absolute offset
  **1404312**, and confirmed by the inequality
  `len(base)+1 <= 1404312 < len(recon)` that the offset lies inside the appended
  text — reconstruction then **False**, as it must be. The pre-round blob is a
  byte PREFIX of the C2 blob: **True** (1402722 of 1405901). The C2 blob ends in
  exactly ONE newline: **True**.
- **G5 THE LEDGER AT C2 — PASS, counted by DISTINCT ID per constraint 7.**
  At `ba28d224` / at C2 — lines matching `^- R-\d+ — `: **297 / 297**, UNMOVED,
  all DISTINCT True / True; lines matching `^Done: R-\d+ — `: **44 / 44** with
  DISTINCT ids among them **42 / 42**, both numbers UNMOVED; `^Landed: R-`:
  **11 / 11**, UNMOVED; `^Gate: F\d+ R\d+ — `: **112 → 113**, a rise of exactly
  one. OPEN SET `len(set(registered) - set(resolved))`: **255 / 255**, UNMOVED —
  this round registers no id and resolves none. `^Gate: F257 R7 — ` at C2: **1**.
- **G6 THE SELF-USE RUN AT C3 — PASS.** Every reading, in the block's order. The
  queue was read only through the SHIPPED loader
  (`default_self_use_queue_path`, `pending_self_use_items`, `next_self_use_item`)
  and the plan made only through
  `self_use_job.plan_next_self_use_item(dest_dir, repo_path=<repository root>)`
  with `dest_dir` = `.remedy-wt/f257-r8-selfuse`, outside the tracked tree.
  - **(a) THE RENDERED BYTES ARE THE CURATED BYTES.** The SU-001 `job_markdown`
    of `scripts/self_use_queue.json` at `ba28d224`, encoded UTF-8: **1235 bytes**,
    sha256 `a26bf66250b9aedb58d9a30837aba8c4ca425ed1a26644ce11d79721ebbdaf51`.
    `.agent/selfuse_f257/SU-001.md` at C3: **1235 bytes**, sha256
    `a26bf66250b9aedb58d9a30837aba8c4ca425ed1a26644ce11d79721ebbdaf51`.
    BYTE-IDENTICAL: **True**, measured both on the rendered file and again on the
    committed blob `61cdc6fa:.agent/selfuse_f257/SU-001.md`.
  - **(b)** `plan.job_file_sha256` =
    `a26bf66250b9aedb58d9a30837aba8c4ca425ed1a26644ce11d79721ebbdaf51`; EQUALS the
    curated digest: **True**. Nothing was templated between the queue and the plan.
  - **(c)** `plan.status` = `'planned'`. `plan.job_title` =
    `'Document the Markdown job-file format'`. `[t.task_id for t in plan.tasks]` =
    `['T001']`. `plan.repo_path` resolves to this repository's root: **True**
    (its path relative to the root is `.`).
  - **(d)** `plan.job_id` = **`124d7421965146bd`**; `plan.created_at` =
    **`2026-08-29T00:39:10.823190+00:00`**. No expected value was stated for
    either, and none is asserted here: both are freshly minted per run.
  - **(e) THE RUN DID NOT CONSUME ITS OWN ITEM.** BEFORE the run:
    `next_self_use_item().id` = `'SU-001'`, `pending_self_use_items()` ids =
    `['SU-001']`. AFTER the run: `next_self_use_item().id` = `'SU-001'`,
    `pending_self_use_items()` ids = `['SU-001']`. `entry.consumed_by` = `''`.
    `git status --porcelain scripts/self_use_queue.json` printed the EMPTY string.
  - **(f) NOTHING WAS PROMOTED.** Occurrences of the promotion module's name in
    the run script `.remedy-wt/f257-r8-c3.py`: **0**. The needle that counts them
    is assembled from two fragments inside that script, precisely so the check
    does not defeat itself by containing what it searches for; the script neither
    imports nor calls that module. `plan.status` = `'planned'`, never `promoted`.
  - **(g)** `git status --porcelain | wc -l` immediately after the run and BEFORE
    C3 staged anything: **0**, with the entry list `[]` — the run wrote only into
    the gitignored `.remedy-wt/`.
  - **(h)** `.agent/selfuse_f257/run.txt`: **3514 bytes**; occurrences of the
    absolute-home path prefix in it: **0**, measured both on disk and on the
    committed blob. Every path in that file is written relative to the
    repository root.
- **G7 THE SUITES AT C3 — PASS.** All four paths confirmed to resolve on disk
  first; the MISSING list is **empty** (`[]`). One pytest process at a time, from
  the repository root, in the PRIMARY checkout, each REAL exit read through
  `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with no pipe to mask it:
  - `python3 -m pytest tests/orchestration/test_self_use_job.py -q --no-header -p no:cacheprovider`
    → `18 passed in 0.22s`, REAL exit **0**.
  - `python3 -m pytest tests/orchestration/test_self_use_queue.py -q --no-header -p no:cacheprovider`
    → `18 passed in 0.21s`, REAL exit **0**.
  - `python3 -m pytest tests/docs/test_docs_consistency.py -q --no-header -p no:cacheprovider`
    → `295 passed in 0.43s`, REAL exit **0**.
  - `python3 -m pytest tests/cli/test_golden_path.py -q --no-header -p no:cacheprovider`
    (canary) → `42 passed in 20.71s`, REAL exit **0**.
- **G8 STRUCTURE — PASS**, over `ba28d224..61cdc6fa`, the range that ends BEFORE
  the handback commit. Range paths (**6**), listed in full:
  `.agent/authored/f257-r8.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/selfuse_f257/SU-001.md`,
  `.agent/selfuse_f257/run.txt`. Changeset-minus-range residue, computed over the
  change set WITHOUT the excluded path — **the excluded path is
  `.agent/handoff.md`**, which C4 writes — is **empty**. Range-minus-changeset
  residue, computed against the FULL change set, is **empty**. Insertions from
  `git diff --numstat` and parent counts: C0a **285**, C0b **167**, C1 **10**,
  C2 **8**, C3 **91** — every one under 500, and each of the five is
  **single-parent**. Delimiter counts over each file's C3 content, lines beginning
  `<<<SLICE ` and `<<<END `: `.agent/plan.md` **0 and 0**;
  `.agent/live_review.md` **0 and 0**; `.agent/selfuse_f257/SU-001.md` **0 and
  0**; `.agent/selfuse_f257/run.txt` **0 and 0** — beside the non-zero CONTROL
  `.agent/authored/f257-r8.md` at **2 and 2**, which shows the counter can see
  delimiters when they are there. `git ls-files .remedy-wt | wc -l` = **0**.
  `git diff --numstat` over the range for `scripts/self_use_queue.json`,
  `docs/roadmap/STATUS.md`, `README.md`,
  `packages/orchestration/self_use_job.py` and
  `docs/system/self-use-track-v1.md` printed the EMPTY string for all five — all
  five **ABSENT**, as the change set requires.

Push: `git push origin feature/f257-self-use-track` — outcome recorded in the
session output; no PR was created and nothing was merged.

## Authored-text proofs

- `PLANF257R8` and `GATEF257R7` were both extracted from the COMMITTED blob
  `git show 03cea660:.agent/authored/f257-r8.md` (constraint 3), never from the
  prompt text, by `.remedy-wt/f257-r8-slices.py`. The delimiter lines were dropped
  as transport (constraint 2) and reach no target file, which G8's delimiter
  counts confirm at 0 in all four targets against a 2/2 control.
- Disk-to-disk: the committed authored file and the reviewer's original
  `.remedy-wt/f257-r8-block.md` are byte-identical, sha256
  `36200f7b15600f1f702c2f3add880fd97318b33ed61eea367cd5fba7f4d360e7`, 19141 bytes
  each — G2. The digest the delegation message stated for that original was
  verified before the file was acted on, and matched.
- `.agent/last_block.md` shares ONE blob id with the authored copy at C0b:
  `2c252c39ab88b3f9dfb3fb6723490ab8bb78c727`.
- No authored slice was corrected, reflowed, retitled or shortened. No `Done:` or
  `Gate:` paragraph of my own was written anywhere; `GATEF257R7` is
  reviewer-authored text applied verbatim, and the round-7 verdict it carries is
  the reviewer's, not mine.

## Deviations & assumptions

1. **THE JOB WAS PLANNED AND NOT RUN, AND THE DOCUMENTATION PAGE SU-001 ASKS FOR
   WAS NOT WRITTEN.** This is the most important line in this handback and it is
   stated without hedging. SU-001 asks for a new page under `docs/` describing the
   Markdown job-file format, registered in `docs/README.md`. **No such page
   exists. Nothing under `docs/` was touched this round at all.** What happened is
   that the curated item was rendered to a job file and parsed into a `JobPlan`
   with status `planned`, and there it stopped. That is the whole of what the
   shipped code offers: `packages/orchestration/self_use_job.py`'s own docstring
   says "REMEDY DELIBERATELY DOES NOT RUN A JOB HERE" and "Remedy deliberately
   does not PROMOTE a job here", so planning to the gate and stopping IS the
   module's complete behaviour. Running the job would additionally drop an
   unrelated documentation page onto a feature branch, which AGENTS.md's scope
   rules forbid. The approval gate the plan now waits at is the OPERATOR'S:
   promotion stays behind the `--approve` barrier in the promotion module, which
   this round neither imported nor called. A reader who finishes this handback
   believing the page was written has been misled, and this paragraph exists so
   that cannot happen.
2. **SU-001 is still PENDING and this round did not mark it consumed.** Both queue
   readings answer `SU-001` before and after the run, `consumed_by` is still the
   empty string, and `scripts/self_use_queue.json` is untouched in the range. The
   `consumed_by` edit belongs to the closure commit — DECISION F257 D2 rules
   exactly this, because an item that could be marked consumed by its own run
   would not be a gate.
3. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, C4 were committed in exactly that order, one logical step each; no commit
   was added, dropped or reordered.
4. **Guard re-expressions (constraint 5), every one reported as required.** This
   session's guard rejects several ordinary shell forms BY FORM, so each was
   re-expressed rather than skipped or weakened:
   - `cp` is rejected outright → both transport copies (C0a/C0b) and the C3
     evidence copy used `shutil.copyfile`.
   - Loops, `$( )` inside a compound, `${arr[0]}` and brace literals containing
     quotes are rejected, and environment-variable assignment is rejected → every
     piece of iteration (slice extraction, G4's reconstruction and negative
     control, G5's two-revision ledger count, the whole C3 run, and G8's
     per-commit walk, delimiter sweep and residue computation) was moved into a
     scratch script under the gitignored `.remedy-wt/`: `f257-r8-c0.py`,
     `f257-r8-g2.py`, `f257-r8-slices.py`, `f257-r8-g3.py`, `f257-r8-g45.py`,
     `f257-r8-c3.py`, `f257-r8-g8.py`. None is tracked — G8 reports
     `git ls-files .remedy-wt` = 0. The scripts were created with the
     file-writing tool rather than typed into a heredoc.
   - Python 3.10 forbids a backslash inside an f-string expression → every regex
     in `f257-r8-g45.py` is hoisted into a named module-level constant
     (`REGISTERED_RE`, `DONE_RE`, `LANDED_RE`, `GATE_RE`, `GATE_F257R7_RE`) and
     never interpolated.
   - The tool does not surface non-zero exits → every gate command was wrapped as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, or read from `subprocess`. The first
     invocation of the `test_self_use_job.py` suite was piped to `tail` and read
     through `${PIPESTATUS[0]}`; because that form is one the guard rejects by
     shape, that suite was **re-run unpiped** and its REAL exit code re-read as 0.
     Only the unpiped reading is reported in G7. No gate result is reported that
     was not actually seen.
5. **Constraint 6 versus the gate formulas raised no disagreement this round.**
   `.agent/live_review.md`'s last byte was already a newline and `GATEF257R7`
   carries its own single terminator, so the bytes appended were one newline then
   the slice — exactly one blank-line separator, exactly one trailing newline. The
   script asserted the pre-append tail rather than assuming it, and G4 confirms
   the reconstruction byte-exactly.
6. **No authored slice looked wrong to me, so constraint 1 was applied with
   nothing to declare beyond applying it.** One reading is worth naming so it is
   not mistaken for a claim of mine: `PLANF257R8`'s item table marks "plan SU-001
   and stop at the approval gate" as `done | this round`, and that line was
   committed at C1, BEFORE the run at C3 had happened. It is the reviewer's
   authored text applied verbatim in the order the block sets, and by the time
   this handback is read it is true. I did not write it and did not adjust it.
7. **`.agent/plan.md` was not current at C0a and C0b.** Those two commits carry
   the round-7 plan, because the block's own order puts the plan advance at C1.
   This is the standing shape of every round in this loop, stated here so the
   reading is not mistaken for drift: the plan is current from C1 onward, and it
   was current before C2, C3 and C4.
8. **Nothing outside the change set was touched.** No file under `packages/`,
   `apps/`, `tests/` or `scripts/` was edited, and `docs/` was not touched at all.
   R-0734 and R-0736 remain registered and deliberately unrepaired on this branch;
   both sit outside F257's surface. G8's five absence readings prove the five
   named paths.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f257-r8.md` | done | `03cea660`, byte-identical to the reviewer's original at 19141 bytes |
| C0b mirror the same bytes to `.agent/last_block.md` | done | `c0617c11`, one blob id with the authored copy |
| C1 advance `.agent/plan.md` | done | `61338424`, whole-file `PLANF257R8` |
| C2 book the F257 R7 verdict | done | `6c9fd816`, `GATEF257R7` appended under constraint 6; no id registered, none resolved |
| C3 run the self-use item and commit the evidence | done | `61cdc6fa`, SU-001 PLANNED to the approval gate; two evidence files, 91 insertions |
| C4 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP `False` at both readings; three constraint-0 readings correct; clean tree after all five commits |
| G2 transport | done | digests EQUAL at 19141 bytes; one blob id at C0b |
| G3 the plan at C1 | done | equal including the trailing newline at 2107 bytes; 42 lines, under 50; 1 and 1 |
| G4 the record append at C2 | done | reconstruction True at 1405901, negative control False at offset 1404312 proved inside the appended text, prefix holds, one trailing newline |
| G5 the ledger at C2 | done | registered UNMOVED at 297 all distinct, `Done:` 44/42 and `Landed:` 11 UNMOVED, `Gate:` 112→113, open set UNMOVED at 255, `^Gate: F257 R7 — ` = 1 |
| G6 the self-use run at C3 | done | rendered bytes = curated bytes at 1235 and one sha256; `job_file_sha256` equal; status `planned`, title and `['T001']` as ordered, `repo_path` = the root; `job_id` and `created_at` reported without an expectation; SU-001 pending before AND after with an empty queue-file status; 0 mentions of the promotion module; clean tree after the run; run.txt 3514 bytes with 0 absolute paths |
| G7 the suites at C3 | done | four paths resolve, missing list empty; 18, 18, 295 and 42 passed, all REAL exit 0, one process at a time |
| G8 structure | done | both residues empty with `.agent/handoff.md` named as the exclusion; five single-parent commits at 285/167/10/8/91 insertions, all under 500; delimiters 0 in four targets against a 2/2 control; `.remedy-wt` untracked at 0; all five named paths ABSENT from the range |

## Open findings

**255 open**, counted by DISTINCT ID per constraint 7 (`len(set(registered) -
set(resolved))`), UNMOVED from `ba28d224`: this round registers no id and
resolves none. Registered lines stand UNMOVED at 297, all distinct.

## Next

Build the evidence bundle with
`job_evidence.create_manual_completion_bundle(review_feature_id="f257")` and the
review zip from a clean tree, recording package, SHA-256 and archived path. The
closure commit follows — `docs/roadmap/STATUS.md`, `README.md`, the
`scripts/self_use_queue.json` `consumed_by` edit that marks SU-001 consumed by
F257, and the final `.agent/` state — then the PR. It is not merged in this
session.
