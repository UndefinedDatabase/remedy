# Handback — F257 Self-use track, round 10 (the closure blocker, repaired)

## Session

SESSION 3 of feature F257 · round 10 · rounds so far 10

Roster of this session's rounds, this round included: R8, R9, R10. Session 2 ran
R4–R7 and ended at `ba28d224`; session 3 opened at R8 and continues with this
round.

## Range

Review of `5cb48adc`..HEAD.

## Values the next round needs and cannot re-derive

- The round 9 package is SUPERSEDED. `remedy-review-20260829-025133-READY_FOR_REVIEW.zip`
  recorded `506bbab5d719974f69593087f8d4fa31f45edfb1` as the accepted HEAD; C3 of
  this round is a CONTENT commit under `tests/`, so the head being closed has
  moved to `ceac0e3a1ebd98cccefe71cfbf6bfb66956829d7` and the package no longer
  covers it. Rebuild at the new head before the closure commit.
- Base of the packaged review subject, still valid:
  `f17b1d0d03e4042df8452b2019b719cbe4704b21` (`git merge-base main HEAD`).
- The repaired suite is state-independent, so the closure commit's
  `consumed_by` edit no longer reddens anything (G6 below).

## Commits

### 911cf534 docs(f257): save the round 10 block verbatim

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r10.md` | +305/-0 | C0a — the round 10 block saved byte for byte |

### 8c50356a chore(f257): mirror the round 10 block to last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +195/-221 | C0b — same bytes as C0a; ONE blob id |

### 2b8523b7 docs(f257): advance the plan to the round 10 repair

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +13/-8 | C1 — PLANF257R10 whole-file replacement |

### 9f5a2639 docs(f257): book the round 9 gate verdict and register R-0737

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +14/-0 | C2 — GATEF257R9 then FINDF257R10, two appends in that order |

### ceac0e3a test(f257): make three self-use tests survive queue exhaustion

| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_self_use_job.py` | +15/-5 | C3 — the R-0737 repair; 18 tests before and 18 after |

### (C4, sha not knowable here) docs(f257): hand back the round 10 repair result

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | whole-file rewrite | C4 — this file. A handoff cannot table the commit that writes it (R-0149 pattern), and its own sha and numstat are unmeasurable at authoring time, so no numeral is invented for either cell. |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f257-r10-redproof 5cb48adc`
  → exit 0.
- `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f257-r10-redproof`
  → exit 0, removed BY EXACT PATH, never by glob. `git worktree list` afterwards
  lists exactly one entry: `/home/decodeux/Repos/remedy  ceac0e3a [feature/f257-self-use-track]`.
- `git push origin feature/f257-self-use-track` after C4 → see the final push line
  below.
- No branch created, no PR created, no merge, no force-push, no history rewrite,
  no checkbox flipped to `[x]`.

## Artifact-build attempts (AGENTS.md — every attempt, status included)

None this round. No evidence bundle and no review zip were attempted; the block
defers the rebuild to the next round because this round moves the head.

## Verification — one line per gate, real transcripts

G1 HYGIENE — PASS. `os.path.exists('.agent/STOP')` → **False** before C0a and
**False** again before C3. `gh pr list …` → `[]`; `git rev-parse HEAD` →
`5cb48adcd382581b8a644b7fff381ad753392692`, which equals `5cb48adc`'s full sha;
`git branch --show-current` → `feature/f257-self-use-track`.
`git status --porcelain | wc -l` → **0** after each of C0a, C0b, C1, C2 and C3.

G2 TRANSPORT — PASS. `git show 911cf534:.agent/authored/f257-r10.md` → **23379
bytes**, sha256 `a46995ebf4938a7abab38756852db6e3af06f1c1dca62eccbf80365348797640`;
the reviewer's own original `.remedy-wt/f257-r10-block.md` → **23379 bytes**, same
sha256; **EQUAL: True**. That original was written before this worker existed, so
the reading covers more than self-consistency; and it covers no emission, because
this workflow has none — the block reached disk as a file the reviewer wrote, not
as text a model re-typed. `git rev-parse 8c50356a:.agent/authored/f257-r10.md` and
`git rev-parse 8c50356a:.agent/last_block.md` both print ONE blob id
`8b559546c7718483839a0bb936471f71dec444c6`.

G3 THE PLAN AT C1 — PASS. `.agent/plan.md` at `2b8523b7` equals PLANF257R10
including the trailing newline: **True**; slice **2559 bytes**, blob **2559
bytes**. `wc -l` **47**, under 50. Lines exactly `## Goal`: **1**. Lines exactly
`## Next Steps`: **1**.

G4 THE RECORD APPENDS AT C2 — PASS. Reconstruction: `5cb48adc` blob (1409456) +
one newline + GATEF257R9 (4226) + one newline + FINDF257R10 (2249) = **1415933**,
each append under constraint 6, applied in that order — equals the C2 blob of
`.agent/live_review.md`, which is also **1415933**: **True**. NEGATIVE CONTROL:
one byte flipped at offset **1409557**, which the script CONFIRMED lies inside the
FIRST appended paragraph (that paragraph spans bytes 1409457..1410490; the 40-byte
context at the flip reads `HE ROUND PASSED AND THE PACKAGE BUILT RE`) — equality
then reads **False**. The pre-round blob is a byte PREFIX of the C2 blob:
**True** (1409456 of 1415933). The C2 blob ends in exactly ONE newline: **True**.
Constraint 6 and the G4 formula did not disagree, so no disagreement is declared.

G5 THE LEDGER AT C2 — PASS, counted under constraint 7 as
`len(set(registered) - set(resolved))`.

| Reading | `5cb48adc` | C2 `9f5a2639` |
|---------|-----------|---------------|
| `^- R-\d+ — ` lines | 297, all DISTINCT True | 298, all DISTINCT True |
| `^Done: R-\d+ — ` lines | 44 | 44 |
| DISTINCT ids among them | 42 | 42 |
| `^Landed: R-` | 11 | 11 |
| `^Gate: F\d+ R\d+ — ` | 114 | 115 |
| OPEN SET | 255 | 256 |

Registered 297 → 298 all distinct; the two `Done:` numbers UNMOVED at 44 and 42;
`Landed:` UNMOVED at 11; `Gate:` 114 → 115; open set 255 → 256 — one id
registered, none resolved, as ordered. `^Gate: F257 R9 — ` at C2: **1**.
`^- R-0737 — ` at C2: **1**.

G6 THE REPAIR PROVED IN BOTH LEDGER STATES — PASS, and the red WAS reproduced.
All four runs ran inside the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/f257-r10-redproof`, created with
`git worktree add --detach`, never in the primary checkout (constraint 8).

IMPORT-PATH PROOF FIRST, so the runs are known to exercise the worktree and not
the primary checkout: in that worktree,
`python3 -B -c "import packages.orchestration.self_use_queue as m; …"` prints
`module file: /home/decodeux/Repos/remedy/.remedy-wt/f257-r10-redproof/packages/orchestration/self_use_queue.py`
and
`queue path : /home/decodeux/Repos/remedy/.remedy-wt/f257-r10-redproof/scripts/self_use_queue.json`.

Command for all four:
`python3 -B -m pytest tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q`

| Run | Commit | Queue state | REAL exit | Counts |
|-----|--------|-------------|-----------|--------|
| (A) | `5cb48adc` | PENDING (`consumed_by` `""`) | **0** | `36 passed in 0.29s` |
| (B) | `5cb48adc` | EXHAUSTED (`consumed_by` `"F257"`) | **1** | `3 failed, 33 passed in 0.31s` |
| (C) | `ceac0e3a` (C3) | PENDING | **0** | `36 passed in 0.29s` |
| (D) | `ceac0e3a` (C3) | EXHAUSTED | **0** | `36 passed in 0.29s` |

(B) IS THE NEGATIVE CONTROL — the defect reproduced. Its three failing node ids,
IN FULL and untruncated, from `-rf`:

    FAILED tests/orchestration/test_self_use_job.py::TestPlanSelfUseItem::test_the_shipped_item_plans_with_its_title_and_tasks
    FAILED tests/orchestration/test_self_use_job.py::TestPlanSelfUseItem::test_the_shipped_item_plans_to_exactly_one_task_with_acceptance
    FAILED tests/orchestration/test_self_use_job.py::TestPlanNextSelfUseItem::test_it_returns_the_shipped_pending_item

Their three distinct failure modes, as measured — this is why the coupling is real
and not one shared assertion:

- `test_the_shipped_item_plans_with_its_title_and_tasks` —
  `AssertionError: the shipped queue has no pending item / assert None is not None`
  at `tests/orchestration/test_self_use_job.py:89`.
- `test_the_shipped_item_plans_to_exactly_one_task_with_acceptance` —
  `AttributeError: 'NoneType' object has no attribute 'id'` raised inside
  `packages/orchestration/self_use_job.py:98`, because `next_self_use_item()`
  answered `None` and the test passed it straight on.
- `test_it_returns_the_shipped_pending_item` —
  `packages.orchestration.self_use_job.SelfUseJobError: no pending self-use item in
  the shipped queue: the track is exhausted and needs curation`, raised at
  `packages/orchestration/self_use_job.py:167` — the shipped module behaving
  exactly as designed.

(D) at C3 passes all 36. The three ids from (B) among the passing ones, read from
`-v` output at C3 with the queue EXHAUSTED:

    tests/orchestration/test_self_use_job.py::TestPlanSelfUseItem::test_the_shipped_item_plans_with_its_title_and_tasks PASSED
    tests/orchestration/test_self_use_job.py::TestPlanSelfUseItem::test_the_shipped_item_plans_to_exactly_one_task_with_acceptance PASSED
    tests/orchestration/test_self_use_job.py::TestPlanNextSelfUseItem::test_it_plans_the_pending_item_or_raises_when_the_queue_is_exhausted PASSED

The third id differs from (B) by NAME only, because C3 step 3 ORDERED that rename;
it is the same test method, in the same class, in the same file, and it is the
third of the three. See deviation 2.

THE ONLY DIFFERENCE BETWEEN (B) AND (D) IS THE COMMIT: the same worktree, the same
queue edit (`items[0].consumed_by` set to `"F257"`, verified read back as
`is_pending False` before each of (B) and (D)), the same pytest invocation, the
same interpreter. Only `git rev-parse HEAD` in the worktree changed, from
`5cb48adc` to `ceac0e3a1ebd98cccefe71cfbf6bfb66956829d7`.

THE QUEUE EDIT NEVER TOUCHED THE PRIMARY CHECKOUT. Measured at the exact moment
after (B), in `/home/decodeux/Repos/remedy`: `git status --porcelain` → exit 0 and
**EMPTY output**, and `git diff -- scripts/self_use_queue.json` → exit 0 and
**EMPTY output**. Measured again after (D): `git status --porcelain` → **EMPTY**.
The worktree was then removed BY ITS EXACT PATH (exit 0) and `git worktree list`
prints one line only:
`/home/decodeux/Repos/remedy  ceac0e3a [feature/f257-self-use-track]`.

G7 THE SUITES AT C3 IN THE PRIMARY CHECKOUT — PASS, one pytest process at a time.
Path resolution confirmed FIRST: the list of paths that do NOT resolve on disk is
**`[]`**, and each of the four resolves `True` individually.

| Command | REAL exit | Result | Expected |
|---------|-----------|--------|----------|
| `python3 -m pytest tests/orchestration/test_self_use_job.py -q` | **0** | `18 passed in 0.23s` | 18 |
| `python3 -m pytest tests/orchestration/test_self_use_queue.py -q` | **0** | `18 passed in 0.23s` | 18 |
| `python3 -m pytest tests/docs/test_docs_consistency.py -q` | **0** | `295 passed in 0.44s` | 295 |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | **0** | `42 passed in 20.75s` | 42 |

Every one exit 0; none was red, so no failure list is carried.

G8 STRUCTURE — PASS, over `5cb48adc..ceac0e3a`, the range that ends BEFORE the
handback commit. Range paths: `.agent/authored/f257-r10.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`tests/orchestration/test_self_use_job.py`. The path EXCLUDED from the
changeset-minus-range computation is **`.agent/handoff.md`**, which C4 writes after
this range ends. changeset-minus-range residue (change set WITHOUT that one path):
**empty, `[]`**. range-minus-changeset residue, computed against the FULL change
set: **empty, `[]`**. Insertions from `git diff --numstat` and parent counts:
C0a `911cf534` **305**, single-parent; C0b `8c50356a` **195**, single-parent;
C1 `2b8523b7` **13**, single-parent; C2 `9f5a2639` **14**, single-parent;
C3 `ceac0e3a` **15**, single-parent — each under 500. Delimiter lines at C3:
`.agent/plan.md` `<<<SLICE ` **0** / `<<<END ` **0**; `.agent/live_review.md`
**0** / **0**; `tests/orchestration/test_self_use_job.py` **0** / **0**; NON-ZERO
CONTROL `.agent/authored/f257-r10.md` **3** / **3**, so the zeros are a reading and
not a silence. `git ls-files .remedy-wt | wc -l` → **0**. `git diff --numstat` over
the range for `scripts/self_use_queue.json`, `docs/roadmap/STATUS.md`, `README.md`
and `packages/orchestration/self_use_job.py`: **all four ABSENT** (empty output for
each) — in particular the queue file, whose edit belongs to the closure commit.
Lint: `python3 -m ruff check tests/orchestration/test_self_use_job.py` → REAL exit
**0**, `All checks passed!`. **Ruff was available, so ruff is the one that ran**;
`py_compile` was not needed.

## The three repaired tests — FULL final text at C3

No assertion was removed. Every assertion the three carried at `5cb48adc` is still
present; two tests changed only WHERE `entry` comes from, and the third gained a
branch for the exhausted state while keeping all four of its assertions on the
pending path. No test was deleted, none was skipped, none was weakened, and no
`xfail` was added. `tests/orchestration/test_self_use_job.py` collects **18** tests
at `5cb48adc` and **18** at C3.

The one-line WHY comment added directly above the changed region:

    # R-0737 — these two classes read the shipped queue's CONTENTS because closure precondition 6 is designed to exhaust its PENDING state.

Test 1:

    def test_the_shipped_item_plans_with_its_title_and_tasks(
        self, tmp_path: Path, isolate_data_root
    ):
        queue = load_self_use_queue()
        assert queue, "the shipped queue is empty"
        entry = queue[0]
        path, plan = plan_self_use_item(entry, tmp_path / "jobs", str(tmp_path))
        assert path.exists()
        assert plan.error == ""
        assert plan.job_title == "Document the Markdown job-file format"
        assert plan.tasks, "a planned self-use job must carry at least one task"

Test 2:

    def test_the_shipped_item_plans_to_exactly_one_task_with_acceptance(
        self, tmp_path: Path, isolate_data_root
    ):
        entry = load_self_use_queue()[0]
        _path, plan = plan_self_use_item(entry, tmp_path / "jobs", str(tmp_path))
        assert len(plan.tasks) == 1
        assert plan.tasks[0].task_id == "T001"
        assert plan.tasks[0].acceptance.strip()

Test 3, renamed from `test_it_returns_the_shipped_pending_item`:

    def test_it_plans_the_pending_item_or_raises_when_the_queue_is_exhausted(
        self, tmp_path: Path, isolate_data_root
    ):
        pending = next_self_use_item()
        if pending is None:
            with pytest.raises(SelfUseJobError):
                plan_next_self_use_item(tmp_path / "jobs", str(tmp_path))
            return
        entry, path, plan = plan_next_self_use_item(tmp_path / "jobs", str(tmp_path))
        assert entry.id == pending.id
        assert entry.is_pending
        assert path.name == f"{entry.id}.md"
        assert plan.error == ""

The import block gained one name, kept in the order the file already used
(`order-by-type`: the class first, then the two functions alphabetically):

    from packages.orchestration.self_use_queue import (
        SelfUseQueueEntry,
        load_self_use_queue,
        next_self_use_item,
    )

## Authored-text proofs

- `PLANF257R10`, `GATEF257R9` and `FINDF257R10` were all extracted from the
  COMMITTED blob `911cf534:.agent/authored/f257-r10.md` by their
  `<<<SLICE`/`<<<END` marker lines, never from the prompt text (constraint 3). No
  delimiter line reached any target file — G8 measures 0/0 in all three targets
  against a 3/3 control.
- Disk-to-disk: the committed `.agent/authored/f257-r10.md` blob is byte-identical
  to the reviewer's own `.remedy-wt/f257-r10-block.md` (G2, 23379 bytes, equal
  sha256), so all three applied slices are byte-identical to the authored source
  by construction, and G3 and G4 confirm each on its target.
- C3 is NOT authored text. It is production test code written by this worker from
  the block's five-item specification; the block describes the change and does not
  paste it. Nothing was applied verbatim there.

## Deviations & assumptions

1. **Guard re-expressions (constraint 5).** No shell loop, `$( )`, `${arr[0]}`,
   `cp`, brace literal containing quotes, or environment-variable assignment was
   used. All multi-step work was routed through scratch scripts under the
   gitignored `.remedy-wt/`: `r10_c0a.py`, `r10_c0b.py`, `r10_slices.py`,
   `r10_c1.py`, `r10_c2.py`, `r10_ledger.py`, `r10_g4.py`, `r10_g6.py`,
   `r10_g7.py`, `r10_g8.py`. The single file copy (C0a) used `shutil.copyfile`; no
   directory copy was needed this round. The two real exit codes captured from a
   shell — the ruff run and the worktree removal — used
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'`; every other exit code came from
   `subprocess.run(...).returncode` directly. No f-string carries a backslash; the
   five ledger regexes are hoisted into named module-level variables in
   `r10_ledger.py`.
2. **G6(D)'s third node id differs from G6(B)'s by NAME.** The block's G6(D)
   asks for "the three ids from (B) among the passing ones", while the block's own
   C3 step 3 ORDERS that the third of those tests be renamed. The two clauses
   cannot both hold literally. What is reported is the same test method, in the
   same class `TestPlanNextSelfUseItem`, in the same file, under its post-rename
   name `test_it_plans_the_pending_item_or_raises_when_the_queue_is_exhausted`;
   the first two ids are byte-identical between (B) and (D). This is declared
   rather than papered over.
3. **The WHY comment is ONE line placed once, above `TestPlanSelfUseItem`.** C3
   step 4 says "Above the two changed classes, put a one-line WHY comment"
   (singular). The two changed classes are contiguous in the file — nothing sits
   between `TestPlanSelfUseItem` and `TestPlanNextSelfUseItem` — so a single
   comment above the first precedes both, and its text names both ("these two
   classes"). It was not duplicated above the second class, which would have been
   a second comment the block did not order.
4. **The module docstring was NOT touched.** C3 step 5 makes the docstring edit
   conditional on the docstring naming a renamed test. It names
   `TestWriteSelfUseJobFile.test_rendered_bytes_equal_the_curated_bytes` and
   `TestPlanNextSelfUseItem.test_exhausted_queue_raises_rather_than_answering_none`
   — measured, neither was renamed — so the condition is false and the docstring
   is left as it was.
5. **The `assert entry is not None` message changed wording, as ordered.** C3
   step 2 requires that assertion to become "an assertion that the shipped queue
   is NOT EMPTY, with a message saying so". It is now
   `assert queue, "the shipped queue is empty"`. This is the one assertion whose
   TEXT changed; it was not removed and it was not weakened — it still fails the
   test when the shipped queue cannot supply an entry, and it now fails for the
   condition the test actually depends on.
6. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, C4 — in that order, no extra commit, none dropped, none reordered. The push
   happens once, after C4, as the block orders.
7. **The comment line is 134 characters.** `line-length` is 120 in
   `pyproject.toml`, but `E501` is in the project's `ruff.lint.ignore` list, so
   ruff passes it; clarity was preferred over splitting a one-line WHY comment
   into two lines, which step 4 forbids.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f257-r10.md` | done | `911cf534` |
| C0b mirror to `.agent/last_block.md` | done | `8c50356a`, one blob id |
| C1 advance `.agent/plan.md` | done | `2b8523b7` |
| C2 book the F257 R9 verdict and register R-0737 | done | `9f5a2639` |
| C3 repair `tests/orchestration/test_self_use_job.py` | done | `ceac0e3a` |
| C4 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP False twice; PR list `[]`; status 0 five times |
| G2 transport | done | EQUAL True, 23379 bytes; one blob id |
| G3 the plan at C1 | done | True, 2559/2559; 47 lines; 1 and 1 |
| G4 the record appends at C2 | done | True, 1415933; control False at 1409557 |
| G5 the ledger at C2 | done | 297→298, Gate 114→115, open set 255→256 |
| G6 the repair in both ledger states | done | red reproduced at (B) exit 1, 3 failed; (D) exit 0, 36 passed |
| G7 the four suites at C3 | done | 18, 18, 295, 42 — all exit 0 |
| G8 structure | done | both residues empty; ruff exit 0 |

Every gate was executed and every reading above is a real one. No gate was red.

## Open findings

**256**, up one from 255 at `5cb48adc` — this round registered R-0737 and resolved
nothing. R-0737's own resolution condition ("green at one commit in BOTH ledger
states") is what G6 measured, but this worker writes no verdict on its own work and
therefore books no `Done:` line; the reviewer decides whether G6 discharges it.

## Next

Rebuild the evidence bundle and the review zip at the repaired head
`ceac0e3a1ebd98cccefe71cfbf6bfb66956829d7` (the round 9 package records the
superseded head `506bbab5` and no longer covers what is being closed). Then the
closure commit, in ONE commit — the `[x]` flip on `docs/roadmap/STATUS.md`, the
README accepted count, its `Next:` clause, the tier-5 Done cell, the README
capability paragraph, the `scripts/self_use_queue.json` `consumed_by` edit and the
final `.agent/` state — and then the pull request, unmerged.
