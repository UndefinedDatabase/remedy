# Handoff — F257 self-use track, round 4

## Session

SESSION 2 of feature F257 · round 4 · rounds so far 4

## Range

Review of `a12ba4ed..HEAD` (HEAD = the C5 commit that writes this file).

## Commits

### 16e2c78f chore(f257): save the round 4 step block — C0a

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r4.md` | +384/-0 | the block saved verbatim by `shutil.copyfile` from `.remedy-wt/f257-r4-block.md` |

### cefbf05d chore(f257): mirror the round 4 block to last_block — C0b

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +237/-170 | the same bytes mirrored from the COMMITTED blob; one blob id with the authored copy |

### 6ddb6a4c docs(f257): advance the plan to the consumption-point round — C1

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +7/-6 | whole-file replacement by slice `PLANF257R4` |

### 4ba886ab docs(f257): book the round 3 verdict and register two findings — C2

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +14/-0 | slices `GATEF257R3` then `FINDF257R4`, each appended under constraint 8 |
| `.agent/prose_slips.md` | +2/-0 | slice `SLIPSF257R3` appended under constraint 8 |

### 60a7c5e3 fix(f257): refuse a self-use job file written outside its destination — C3

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/self_use_job.py` | +38/-5 | S1–S6: containment check on RESOLVED paths, the refusal reason in the WHY comment, and the `SelfUseJobError` line of the Public API block |
| `tests/orchestration/test_self_use_job.py` | +37/-0 | S7: four new tests in their own class, every destination under `tmp_path` |

### 3c84e020 docs(f257): wire the self-use consumption point into the closure protocol — C4

| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS_closure_protocol.md` | +14/-1 | PAIR A adds precondition 6; PAIR B adds `scripts/self_use_queue.json` to the closure commit's path set |

### C5 — this handoff commit

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | the round handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above was taken from `git diff --numstat` per commit and compared
cell by cell against the figures G8 reports; all six commits agree.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, REAL exit 0.
- `git worktree add --detach .remedy-wt/g6-f257r4 60a7c5e3` → added; used for G6 only.
- `git worktree remove --force .remedy-wt/g6-f257r4` → removed BY EXACT PATH; `git worktree list` then shows the primary alone.
- `git push origin feature/f257-self-use-track` → outcome recorded in the session output.
- No pull request was created. Nothing was merged. No force-push, no history rewrite.

## Verification

One line per gate, with the result actually measured.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk with `os.path.exists` twice:
  before C0a `False`, before C3 `False`. Constraint 0: `gh pr list …` printed
  `[]` at REAL exit 0; `git rev-parse HEAD` printed
  `a12ba4ed6df6d0f842e5bb0958fb72cfc611f52a`; `git branch --show-current` printed
  `feature/f257-self-use-track`. `git status --porcelain | wc -l` after each
  commit: C0a 0, C0b 0, C1 0, C2 0, C3 0, C4 0.
- **G2 TRANSPORT — PASS.** Committed blob `16e2c78f:.agent/authored/f257-r4.md`
  sha256 `c0e01bf791c01211881b92d62226c5e0b0231b8046ae114003fdee59fdb23ca0`,
  27597 bytes; reviewer original `.remedy-wt/f257-r4-block.md` sha256
  `c0e01bf791c01211881b92d62226c5e0b0231b8046ae114003fdee59fdb23ca0`, 27597
  bytes; **EQUAL True**. That original was written before this worker existed, so
  the reading covers more than self-consistency; and it covers no emission,
  because this workflow has none — the block was never retyped, only copied by
  `shutil.copyfile`. `git rev-parse cefbf05d:.agent/authored/f257-r4.md` and
  `git rev-parse cefbf05d:.agent/last_block.md` both print the single blob id
  `66898275f916d9de1ed62aef72b324ba814877bd`.
- **G3 THE PLAN AT C1 — PASS.** `.agent/plan.md` at C1 equals `PLANF257R4`
  including the trailing newline: **True**, 1659 bytes on both sides. `wc -l`
  **35**, under 50 True. Lines exactly `## Goal`: **1**. Lines exactly
  `## Next Steps`: **1**.
- **G4 THE RECORD APPENDS AT C2 — PASS.** `.agent/live_review.md` reconstructed
  from the `a12ba4ed` blob plus `GATEF257R3` plus `FINDF257R4`, applied IN THAT
  ORDER each under constraint 8: **True**; base 1381210 bytes, rebuilt 1388216,
  C2 blob 1388216. NEGATIVE CONTROL: byte at absolute offset 1381311 — the script
  confirmed it lies inside the FIRST appended paragraph, which spans
  1381211..1384489, and that it equals the corresponding byte of the
  `GATEF257R3` slice — XORed with 0x01; reconstruction then **False**. The
  pre-round blob is a byte PREFIX of the C2 blob: **True** (1381210 → 1388216).
  The C2 blob ends in exactly ONE newline: **True**. Separately,
  `.agent/prose_slips.md` at C2 reconstructs from its `a12ba4ed` blob plus
  `SLIPSF257R3` under constraint 8: **True** (15914 → 16258 bytes).
- **G5 THE LEDGER AT C2 — PASS, counted by DISTINCT ID per constraint 9.**
  At `a12ba4ed` / at C2 — lines matching `^- R-\d+ — `: **293 / 295**, all
  DISTINCT True / True; lines matching `^Done: R-\d+ — `: **44 / 44** with
  DISTINCT ids among them **42 / 42** (the two numbers differ exactly as
  constraint 9 says), both UNMOVED; `^Landed: R-`: **11 / 11**, UNMOVED;
  `^Gate: F\d+ R\d+ — `: **108 / 109**, a rise of exactly one. OPEN SET
  `len(set(registered) - set(resolved))`: **251 → 253**, exactly the two ids this
  round registers. `^Gate: F257 R3 — ` at C2: **1**. `^- R-0733 — ` at C2: **1**.
  `^- R-0734 — ` at C2: **1**.
- **G6 THE RED-PROOF AT C3 — PASS**, run only inside `.remedy-wt/g6-f257r4`
  (worktree added detached at `60a7c5e3`), never in the primary. Command each
  time:
  `python3 -B -m pytest tests/orchestration/test_self_use_job.py -q -p no:cacheprovider`,
  with `__pycache__` purged before every run.
  - CONTROL FIRST, unmutated: REAL exit **0**, `11 passed in 0.23s`.
  - MUTATION (i), the containment check DELETED and the path built exactly as at
    `a12ba4ed` (`dest_dir.mkdir(...)`, then `path = dest_dir / f"{entry.id}.md"`,
    then `path.write_text(...)`, then `return path`): REAL exit **1**,
    `4 failed, 7 passed in 0.26s`. Reverted before the next.
  - MUTATION (ii), S4 of round 3 broken — `write_self_use_job_file` appends a
    trailing line instead of writing `entry.job_markdown` verbatim: REAL exit
    **1**, `1 failed, 10 passed in 0.24s`. Reverted.
  - CONTROL AGAIN, module restored byte-clean (byte equality against the pristine
    bytes: **True**, sha256
    `56bd9abd69535aea65f1a1fac80e422d05c7a1af22a040898225876af048b9f9`): REAL
    exit **0**, `11 passed in 0.23s`.
  - After `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/g6-f257r4`
    (exact path, never a glob): `git worktree list` shows
    `/home/decodeux/Repos/remedy  60a7c5e3 [feature/f257-self-use-track]` alone,
    and `git status --porcelain | wc -l` in the primary is **0**.
- **G7 THE SUITES AT C4 — PASS, all ten exit 0.** One pytest process at a time,
  from the repository root, in the PRIMARY checkout, each as
  `python3 -B -m pytest <path> -q -p no:cacheprovider`. All ten ordered paths
  were confirmed to resolve on disk FIRST — the missing list is **`[]`** — so no
  suite exited 4 silently.
  - `tests/orchestration/test_self_use_job.py` — REAL exit 0, `11 passed in 0.21s`
  - `tests/orchestration/test_self_use_queue.py` — REAL exit 0, `18 passed in 0.21s`
  - `tests/test_data_paths.py` — REAL exit 0, `23 passed in 0.25s`
  - `tests/test_path_utils.py` — REAL exit 0, `28 passed in 0.19s`
  - `tests/regression/test_named_bugs.py` — REAL exit 0, `64 passed, 6 skipped in 1.25s`
  - `tests/orchestration/test_development_artifact_boundary.py` — REAL exit 0, `18 passed in 1.40s`
  - `tests/orchestration/test_job_promote.py` — REAL exit 0, `85 passed in 8.39s`
  - `tests/orchestration/test_pingpong_cli.py` — REAL exit 0, `172 passed in 2.34s`
  - `tests/docs/test_docs_consistency.py` — REAL exit 0, `295 passed in 0.43s`
  - `tests/cli/test_golden_path.py` — REAL exit 0, `42 passed in 20.63s`
- **G8 STRUCTURE — PASS**, over `a12ba4ed..3c84e020`, the range that ends BEFORE
  the handback commit. Range paths (8): `.agent/authored/f257-r4.md`,
  `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
  `.agent/prose_slips.md`, `docs/roadmap/STATUS_closure_protocol.md`,
  `packages/orchestration/self_use_job.py`,
  `tests/orchestration/test_self_use_job.py`. Changeset-minus-range residue,
  computed over the change set WITHOUT the excluded path — **the excluded path is
  `.agent/handoff.md`**, which C5 writes — is **empty**. Range-minus-changeset
  residue, computed against the FULL change set, is **empty**. Insertions and
  parents: C0a **384**, C0b **237**, C1 **7**, C2 **16**, C3 **75**, C4 **14** —
  each under 500, and each of the six is **single-parent**. Delimiter counts over
  each file's C4 content, lines beginning `<<<SLICE ` and `<<<END `:
  `.agent/plan.md` 0 and 0; `.agent/live_review.md` 0 and 0;
  `.agent/prose_slips.md` 0 and 0; `packages/orchestration/self_use_job.py` 0 and
  0; `tests/orchestration/test_self_use_job.py` 0 and 0;
  `docs/roadmap/STATUS_closure_protocol.md` 0 and 0 — beside the non-zero CONTROL
  `.agent/authored/f257-r4.md` at **8 and 8**, which shows the counter can see
  delimiters when they are there. `git ls-files .remedy-wt | wc -l` = **0**.
  `git diff --numstat a12ba4ed..3c84e020 -- <path>` is EMPTY, i.e. **ABSENT**,
  for all three of `packages/orchestration/self_use_queue.py`,
  `scripts/self_use_queue.json` and `tests/ui_server/test_command_channel.py`.
  Over the C4 blob of `docs/roadmap/STATUS_closure_protocol.md`: lines exactly
  `5. Working tree clean, branch pushed, worker idle.` = **1**; lines beginning
  `6. EXACTLY ONE SELF-USE ITEM` = **1**; occurrences of
  `scripts/self_use_queue.json` = **2**.

Push: `git push origin feature/f257-self-use-track` — outcome recorded in the
session output; no PR was created and nothing was merged.

## Authored-text proofs

- `PLANF257R4`, `GATEF257R3`, `FINDF257R4`, `SLIPSF257R3`, `PAIRAFROM`,
  `PAIRATO`, `PAIRBFROM` and `PAIRBTO` were all extracted from the COMMITTED blob
  `git show 16e2c78f:.agent/authored/f257-r4.md` (constraint 3), never from the
  prompt text, by `.remedy-wt/f257r4_slices.py`; the delimiter lines were dropped
  as transport (constraint 2) and reach no target file, which G8's delimiter
  counts confirm at 0 in all six targets against an 8/8 control.
- Disk-to-disk: the committed authored file and the reviewer's original
  `.remedy-wt/f257-r4-block.md` are byte-identical, sha256
  `c0e01bf7…fdb23ca0`, 27597 bytes each — G2.
- `.agent/last_block.md` shares ONE blob id with the authored copy at C0b:
  `66898275f916d9de1ed62aef72b324ba814877bd`.
- Constraint 10: before replacing, `PAIRAFROM` was counted in
  `docs/roadmap/STATUS_closure_protocol.md` at **exactly 1** occurrence and
  `PAIRBFROM` at **exactly 1**. Each FROM was replaced by its TO and nothing else
  in the file changed — the C4 diff is +14/-1 and touches only those two regions.

## Deviations & assumptions

1. **Guard re-expressions (constraint 6), every one reported as required.** This
   session's guard rejects several ordinary shell forms BY FORM, so each was
   re-expressed rather than skipped or weakened:
   - `cp` is rejected outright → the C0a transport copy used
     `python3 -c "import shutil; shutil.copyfile(...)"`, and C0b was written from
     the COMMITTED blob through `git show` inside Python.
   - Loops, `$( )` inside a compound, `${arr[0]}`, process substitution and
     multi-operation one-liners are rejected → every gate that needed iteration
     (G4's reconstruction and negative control, G5's two-revision ledger count,
     G6's mutate/run/revert cycle with its `__pycache__` purges, G8's per-commit
     walk and delimiter sweep) was moved into a scratch script under the
     gitignored `.remedy-wt/`: `f257r4_slices.py`, `f257r4_g4g5.py`,
     `f257r4_g6.py`, `f257r4_g8.py`. None is tracked — G8 reports
     `git ls-files .remedy-wt` = 0.
   - Brace literals containing quotes are rejected → the scratch scripts were
     created with the file-writing tool rather than typed into a heredoc.
   - All three env-var forms (`VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`)
     are rejected → the data-root isolation the job planner needs is set
     in-process by `monkeypatch.setenv` inside the existing test fixture
     `isolate_data_root`; no new environment assignment was needed this round.
   - `cd X && git ...` is rejected → `git -C <path>` throughout, and `cwd=` on
     `subprocess.run` for every pytest invocation, including the worktree runs.
   - The tool does not surface non-zero exits → every command was wrapped as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or run through `subprocess` and its
     `returncode` printed. No gate result is reported that was not actually seen.
2. **Constraint 8 versus the gate formulas: NO disagreement arose.** G4 phrases
   its reconstruction as "under constraint 8" rather than restating an arithmetic
   of its own, so there was nothing to conflict with. Both appends were made
   exactly as constraint 8 states — the target's last byte was verified to be a
   single newline first, then one newline, then the slice, then one newline — and
   both targets end in exactly one trailing newline afterwards. Recorded only
   because the block asked for a disagreement to be declared if one existed; none
   did.
3. **S7's "list the parent of `dest_dir` before and after" needed a traversal
   depth that lands the escape IN that parent, so the fourth new test uses the id
   `../escaped` rather than `../../escaped`.** With `../../escaped` the refused
   write would target `dest_dir.parent.parent`, which the ordered listing of
   `dest_dir.parent` cannot see, and the assertion would have passed vacuously —
   the "gate the truth, not the shape" failure mode. `../escaped` aims exactly
   one level up, so the directory listed is precisely where the escaped file
   would land. The other three new tests use `../../escaped` and an ABSOLUTE id
   as S7 states, and every destination stays under `tmp_path`. G6's mutation (i)
   confirms the choice is not cosmetic: deleting the check reddens **4** of the
   4 new tests.
4. **The containment check runs BEFORE `dest_dir.mkdir(...)`, which reorders two
   statements S1 did not order.** At `a12ba4ed` the directory was created first;
   creating it on the way to a refusal would itself be a write outside nothing
   useful and would have made S7's before/after listing dirty in the case where
   `dest_dir` does not yet exist. The check therefore precedes the `mkdir`, and
   `Path.resolve()` is non-strict, so it is well defined on a destination that
   does not exist yet. Mutation (i) restores the original ordering exactly, as
   the block asks.
5. **Applied as written where I would have written it differently.** Constraint 1
   binds and nothing was corrected. Two observations, for the record only:
   `PLANF257R4` marks "consume exactly one item per feature close" as `done`
   before C4 exists, which is true of the finished round and was applied verbatim
   at C1; and `FINDF257R4` names the R-0733 fix as "four lines long", where the
   shipped check is one `if` plus a two-line `raise` beside the WHY comment the
   discoverability convention asks for. Neither is a change to any target.
6. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, C4, C5 were committed in exactly that order, one logical step each; no
   commit was added, dropped or reordered. This round registers R-0733 and R-0734
   and resolves neither, and no `Done:` or `Gate:` paragraph of my own was
   written anywhere — `GATEF257R3` and `FINDF257R4` are reviewer-authored text
   applied verbatim.
7. **One extra check beyond the block, non-destructive.**
   `python3 -m ruff check` was run over the two C3 files before committing them
   (`All checks passed!`, REAL exit 0). It is a read-only lint, ordered by no
   gate, reported here so the record is complete.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f257-r4.md` | done | `16e2c78f`, byte-identical to the reviewer's original |
| C0b mirror the same bytes to `.agent/last_block.md` | done | `cefbf05d`, one blob id with the authored copy |
| C1 advance `.agent/plan.md` | done | `6ddb6a4c`, whole-file `PLANF257R4` |
| C2 book the F257 R3 verdict, register R-0733 and R-0734, append the prose slip | done | `4ba886ab`, all three appends under constraint 8 |
| C3 the R-0733 containment fix and its tests | done | `60a7c5e3`, +38/-5 and +37/-0, 11 tests green |
| C4 the closure-protocol wiring | done | `3c84e020`, both pairs applied, each FROM counted at exactly 1 first |
| C5 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP False at both readings; three constraint-0 readings correct; clean tree after all six commits |
| G2 transport | done | digests EQUAL at 27597 bytes; one blob id at C0b |
| G3 the plan at C1 | done | equal including trailing newline at 1659 bytes; 35 lines; 1 and 1 |
| G4 the record appends at C2 | done | reconstruction True, negative control False, prefix holds, one trailing newline; slips file too |
| G5 the ledger at C2 | done | registered 293→295, `Done:` 44/42 and `Landed:` 11 unmoved, `Gate:` 108→109, open set 251→253, the three counts each 1 |
| G6 the red-proof at C3 | done | control 0 at 11 passed; mutation (i) exit 1 at 4 failed, 7 passed; mutation (ii) exit 1 at 1 failed, 10 passed; restored control 0; worktree removed by exact path, primary clean |
| G7 the suites at C4 | done | all ten paths resolved, all ten REAL exit 0 |
| G8 structure | done | both residues empty; six single-parent commits under 500; delimiters 0 in six targets against an 8/8 control; `.remedy-wt` untracked; all three forbidden paths absent; the three protocol counts 1, 1 and 2 |

## Open findings

**253 open**, counted by DISTINCT ID per constraint 9 (`len(set(registered) -
set(resolved))`), risen from 251 at `a12ba4ed` by exactly the two ids this round
registers, R-0733 and R-0734. R-0733 is repaired in C3 but NOT resolved here —
the record carries no `Done:` line for it, because a resolution is the reviewer's
to author.

## Next

Document the queue format and the job-file format where a reader would look, and
register the page in `docs/README.md` — acceptance item 1, the last open item
before the integration gate and the closure package.
